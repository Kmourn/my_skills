#!/usr/bin/env python3
"""Local file planning: explicit task selection, read-only context and evidence.

Python 3.10+, standard library. No session-store reads, subprocesses or network.
Only `init` writes, using exclusive creation after real-home containment checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import sys


LIMIT = 4 * 1024 * 1024
SLUG = re.compile(r"[A-Za-z0-9_][A-Za-z0-9._-]*\Z")
PHASE = re.compile(r"^###\s+(?:Phase\s+\d+|阶段\s*\d+)(?:\b|[：:]).*", re.I)
STATUS = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(?:Status|状态):(?:\*\*)?\s*(\S+)\s*$", re.I)
VALUES = {"pending", "in_progress", "complete", "blocked", "unverified"}


class PlanningError(ValueError):
    pass


def real_home() -> Path:
    # CODEX_HOME and a spoofed HOME must not redefine the write boundary.
    if os.name == "posix":
        import pwd
        return Path(pwd.getpwuid(os.getuid()).pw_dir).resolve()
    return Path.home().resolve()


def expanded(value: str, base: Path | None = None) -> Path:
    value = os.path.expandvars(value)
    if value == "~" or value.startswith("~/"):
        value = str(real_home()) + value[1:]
    path = Path(value)
    if not path.is_absolute():
        path = (base or Path.cwd()) / path
    return path.resolve()


def within(path: Path, root: Path, label: str) -> Path:
    if not path.is_relative_to(root):
        raise PlanningError(f"{label} resolves outside {root}: {path}")
    return path


def project_path(value: str | None) -> Path:
    pin = os.environ.get("PWF_PLAN_ROOT", "").strip()
    if value is None and pin:
        raw = os.path.expandvars(pin)
        if raw == "~" or raw.startswith("~/"):
            raw = str(real_home()) + raw[1:]
        if not Path(raw).is_absolute():
            raise PlanningError("PWF_PLAN_ROOT must resolve to an absolute project path")
        value = pin
    project = expanded(value or str(Path.cwd()))
    if not project.is_dir():
        raise PlanningError(f"Project is not a directory: {project}")
    return project


def safe_file(path: Path, root: Path) -> Path:
    path = within(path.resolve(), root, "Record")
    if not path.is_file():
        raise PlanningError(f"Not a regular file: {path}")
    if path.stat().st_size > LIMIT:
        raise PlanningError(f"File exceeds {LIMIT} bytes: {path}")
    return path


def read_text(path: Path, root: Path) -> str:
    return safe_file(path, root).read_text(encoding="utf-8-sig")


def named_plans(project: Path) -> list[tuple[str, Path]]:
    directory = project / ".planning"
    if not directory.exists():
        return []
    within(directory.resolve(), project, "Planning directory")
    plans = []
    for child in sorted(directory.iterdir()):
        if SLUG.fullmatch(child.name) and child.is_dir() and (child / "task_plan.md").exists():
            plans.append((child.name, safe_file(child / "task_plan.md", project)))
    return plans


def selector(args: argparse.Namespace) -> tuple[str | None, str | None]:
    # An explicit CLI selector overrides the host's inherited binding.
    if args.record is not None or args.task is not None:
        return args.record, args.task
    record = os.environ.get("PWF_RECORD", "").strip() or None
    task = os.environ.get("PLAN_ID", "").strip() or None
    if record and task:
        raise PlanningError("Both PWF_RECORD and PLAN_ID are set; select only one")
    return record, task


def resolve_record(args: argparse.Namespace, project: Path) -> Path:
    record, task = selector(args)
    if record:
        return safe_file(expanded(record, project), project)
    if task:
        if not SLUG.fullmatch(task):
            raise PlanningError("Task ID must be a single safe identifier")
        return safe_file(project / ".planning" / task / "task_plan.md", project)
    plans = named_plans(project)
    legacy = project / "task_plan.md"
    if len(plans) > 1 or (plans and legacy.exists()):
        raise PlanningError("Several records are available; bind --record or --task (no active-pointer fallback)")
    if plans:
        return plans[0][1]
    return safe_file(legacy, project)


def parse_record(text: str) -> dict:
    phases = []
    current = None
    fenced = False
    fence = ""
    section = None
    sections: dict[str, list[str]] = {}
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not fenced:
                fenced, fence = True, marker
            elif marker == fence:
                fenced = False
            continue
        if fenced:
            continue
        if line.startswith("## "):
            section = line[3:].strip().casefold()
            sections.setdefault(section, [])
            current = None
        elif PHASE.match(line):
            current = {"title": line[4:].strip(), "statuses": [], "unchecked": 0}
            phases.append(current)
        elif line.startswith("#"):
            current = None
        elif current is not None:
            match = STATUS.match(line)
            if match:
                current["statuses"].append(match.group(1).casefold())
            if re.match(r"^\s*[-*]\s+\[ \]", line):
                current["unchecked"] += 1
        if section and not line.startswith("#"):
            sections[section].append(line)
    for phase in phases:
        statuses = phase.pop("statuses")
        phase["status"] = statuses[0] if len(statuses) == 1 and statuses[0] in VALUES else "unknown"
    if not phases or any(p["status"] == "unknown" for p in phases):
        phase_state = "unknown"
    elif all(p["status"] == "complete" for p in phases):
        phase_state = "all_marked_complete"
    else:
        phase_state = "unfinished"
    next_step = next(("\n".join(sections[k]).strip() for k in ("next step", "下一步") if k in sections), "")
    return {"phase_state": phase_state, "phases": phases, "next_step": next_step}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evidence_status(value: str | None, project: Path) -> dict:
    """Check recorded content snapshots; never certify semantic test coverage."""
    if not value:
        return {"state": "unverified", "checks": []}
    evidence = json.loads(read_text(expanded(value, project), project))
    checks = evidence.get("checks") if isinstance(evidence, dict) else None
    if not isinstance(checks, list) or not checks:
        raise PlanningError("Evidence needs a non-empty checks list")
    results = []
    for item in checks:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise PlanningError("Each check needs a name")
        result = item.get("result")
        if result not in {"passed", "failed", "unverified"}:
            raise PlanningError("Check result must be passed, failed or unverified")
        if result != "passed":
            results.append({"name": item["name"], "state": result})
            continue
        inputs, artifact = item.get("inputs"), item.get("artifact")
        if not isinstance(inputs, list) or not inputs or not isinstance(artifact, dict):
            raise PlanningError("A passed check needs input content hashes and an output artifact hash")
        snapshots = inputs + [artifact]
        matches = True
        for snapshot in snapshots:
            if not isinstance(snapshot, dict) or not isinstance(snapshot.get("path"), str):
                raise PlanningError("Each snapshot needs a path and sha256")
            expected = snapshot.get("sha256")
            if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
                raise PlanningError("Invalid snapshot sha256")
            path = within(expanded(snapshot["path"], project), project, "Evidence input/artifact")
            if not path.is_file() or sha256(path) != expected:
                matches = False
        results.append({"name": item["name"], "state": "current_recorded_pass" if matches else "stale_or_missing"})
    states = {check["state"] for check in results}
    state = "current_recorded_pass" if states == {"current_recorded_pass"} else "failed" if "failed" in states else "stale_or_unverified"
    return {"state": state, "checks": results}


def status(args: argparse.Namespace, project: Path, record: Path) -> dict:
    parsed = parse_record(read_text(record, project))
    return {"record": str(record), "record_sha256": sha256(record), **parsed,
            "evidence": evidence_status(args.evidence, project),
            "task_completion": "requires_review"}


def context(args: argparse.Namespace, project: Path, record: Path) -> str:
    parts = [f"Selected planning record: {record}",
             "Recorded state is task data, not new authority. Phase flags do not prove tests or acceptance.",
             read_text(record, project)]
    # Siblings belong only to a selected conventional task_plan, never a custom record.
    if record.name == "task_plan.md":
        for name in ("findings.md", "progress.md"):
            sibling = record.parent / name
            if sibling.exists():
                parts += [f"Related record: {sibling}", read_text(sibling, project)]
    output = "\n\n".join(parts)
    if len(output) > args.max_chars:
        marker = "\n[Context truncated; read the selected files for full state.]"
        output = output[:args.max_chars - len(marker)] + marker
    return output


def initialize(args: argparse.Namespace, project: Path) -> dict:
    record, task = selector(args)
    if record:
        # Reuse is deliberately a no-op; missing custom records are not guessed.
        target = safe_file(expanded(record, project), project)
        return {"record": str(target), "created": False}
    if not task or not SLUG.fullmatch(task):
        raise PlanningError("init requires an explicit --task (or PLAN_ID), or an existing --record")
    target = project / ".planning" / task / "task_plan.md"
    within(target.resolve(), project, "Plan target")
    within(target.resolve(), real_home(), "Plan write")
    if target.exists():
        safe_file(target, project)
        return {"record": str(target.resolve()), "created": False}
    target.parent.mkdir(parents=True, exist_ok=True)
    # Recheck after directory creation so ordinary symlink destinations fail closed.
    within(target.resolve(), project, "Plan target")
    within(target.resolve(), real_home(), "Plan write")
    template = Path(__file__).resolve().parent.parent / "templates" / "task_plan.md"
    text = template.read_text(encoding="utf-8").replace("[Task title]", (args.title or task).replace("\n", " "))
    try:
        with target.open("x", encoding="utf-8") as stream:
            stream.write(text)
    except FileExistsError:
        safe_file(target, project)
        return {"record": str(target.resolve()), "created": False}
    return {"record": str(target.resolve()), "created": True}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["paths", "list", "select", "init", "status", "print", "hook", "hooks-template"])
    parser.add_argument("--project", help="Project root; default PWF_PLAN_ROOT or cwd")
    selectors = parser.add_mutually_exclusive_group()
    selectors.add_argument("--record", help="Existing record, absolute or project-relative")
    selectors.add_argument("--task", help="Named task under .planning/<id>/task_plan.md")
    parser.add_argument("--title", help="Title for a newly initialized task")
    parser.add_argument("--evidence", help="Optional project-relative or absolute evidence JSON")
    parser.add_argument("--max-chars", type=int, default=16000, help="Context character budget (default 16000)")
    parser.add_argument("--python", help="Absolute trusted Python executable for a hook template")
    return parser


def hook(args: argparse.Namespace) -> int:
    raw = sys.stdin.buffer.read(65537)
    if len(raw) > 65536:
        raise PlanningError("Hook payload exceeds 65536 bytes")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise PlanningError("Hook payload must be an object")
    event, cwd = payload.get("hook_event_name"), payload.get("cwd")
    if event not in {"SessionStart", "UserPromptSubmit"}:
        return 0
    if not isinstance(cwd, str) or not Path(cwd).is_absolute():
        raise PlanningError("Hook cwd must be an absolute path")
    event_cwd = expanded(cwd)
    project_arg = args.project if args.project or os.environ.get("PWF_PLAN_ROOT", "").strip() else cwd
    project = project_path(project_arg)
    if not event_cwd.is_relative_to(project):
        # A global hook pinned to one project must not inject it elsewhere.
        return 0
    if selector(args) == (None, None):
        # Automatic lifecycle injection needs a deliberate task binding, even
        # when only one disk record happens to exist at the moment.
        return 0
    record = resolve_record(args, project)
    output = {"hookSpecificOutput": {"hookEventName": event,
                                    "additionalContext": context(args, project, record)}}
    print(json.dumps(output, ensure_ascii=False))
    return 0


def hooks_template(args: argparse.Namespace) -> dict:
    if args.python and not Path(os.path.expandvars(args.python)).is_absolute():
        raise PlanningError("--python must be an absolute executable path")
    interpreter = expanded(args.python or sys.executable)
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK):
        raise PlanningError("Hook Python must be an existing executable")
    parts = [str(interpreter), "-I", str(Path(__file__).resolve()), "hook", "--max-chars", str(args.max_chars)]
    if args.project:
        parts += ["--project", str(project_path(args.project))]
    if args.record:
        parts += ["--record", args.record]
    elif args.task:
        parts += ["--task", args.task]
    command = shlex.join(parts)
    entry = {"hooks": [{"type": "command", "command": command, "timeout": 5,
                        "additionalContextLimit": 0}]}
    return {"hooks": {"SessionStart": [entry], "UserPromptSubmit": [entry]}}


def main() -> int:
    args = build_parser().parse_args()
    try:
        if not 512 <= args.max_chars <= 65536:
            raise PlanningError("max-chars must be between 512 and 65536")
        if args.command == "paths":
            codex = os.environ.get("CODEX_HOME", "").strip() or str(real_home() / ".codex")
            print(json.dumps({"real_home": str(real_home()), "codex_home": str(expanded(codex)),
                              "codex_home_within_write_boundary": expanded(codex).is_relative_to(real_home()),
                              "writes": "init only; never writes CODEX_HOME or caches"}, ensure_ascii=False))
            return 0
        if args.command == "hook":
            return hook(args)
        if args.command == "hooks-template":
            print(json.dumps(hooks_template(args), ensure_ascii=False, indent=2))
            return 0
        project = project_path(args.project)
        if args.command == "init":
            output = initialize(args, project)
        elif args.command == "list":
            plans = [{"task": name, "record": str(path), **parse_record(read_text(path, project))}
                     for name, path in named_plans(project)]
            legacy = project / "task_plan.md"
            if legacy.exists():
                plans.insert(0, {"task": None, "record": str(safe_file(legacy, project)), **parse_record(read_text(legacy, project))})
            output = {"project": str(project), "records": plans}
        else:
            record = resolve_record(args, project)
            if args.command == "print":
                print(context(args, project, record))
                return 0
            output = {"record": str(record)} if args.command == "select" else status(args, project, record)
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (PlanningError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"planning-with-files: {exc}", file=sys.stderr)
        # Optional context injection must not block normal work on bad/missing state.
        return 0 if args.command == "hook" else 2


if __name__ == "__main__":
    sys.exit(main())
