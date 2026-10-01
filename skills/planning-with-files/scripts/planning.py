#!/usr/bin/env python3
"""Local file planning: explicit task selection, read-only context and evidence.

Python 3.10+, standard library. No session-store reads, subprocesses or network.
Only explicit init, bind/unbind and configure-hooks commands write within real HOME.
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
import tempfile


LIMIT = 4 * 1024 * 1024
SLUG = re.compile(r"[A-Za-z0-9_][A-Za-z0-9._-]*\Z")
PHASE = re.compile(r"^###\s+(?:Phase\s+\d+|阶段\s*\d+)(?:\b|[：:]).*", re.I)
STATUS = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(?:Status|状态):(?:\*\*)?\s*(\S+)\s*$", re.I)
VALUES = {"pending", "in_progress", "complete", "blocked", "unverified"}
EVENTS = ("SessionStart", "UserPromptSubmit")
REGISTRY_LIMIT = 8192


class PlanningError(ValueError):
    pass


def real_home() -> Path:
    # CODEX_HOME and a spoofed HOME must not redefine the write boundary.
    if os.name == "posix":
        import pwd
        return Path(pwd.getpwuid(os.getuid()).pw_dir).resolve()
    return Path.home().resolve()


def expanded(value: str, base: Path | None = None) -> Path:
    if "\0" in value:
        raise PlanningError("A path must not contain a null byte")
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


def codex_home() -> Path:
    return expanded(os.environ.get("CODEX_HOME", "").strip() or str(real_home() / ".codex"))


def decode_json(raw: bytes) -> object:
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise PlanningError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique_object)


def atomic_write(target: Path, content: bytes) -> None:
    within(target.resolve(), real_home(), "Write target")
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    within(target.resolve(), real_home(), "Write target")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".pwf-", dir=target.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def session_id(value: object) -> str:
    if not isinstance(value, str) or not value or len(value) > 256:
        raise PlanningError("Session ID must be a non-empty string of at most 256 characters")
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in value):
        raise PlanningError("Session ID must not contain whitespace or control characters")
    return value


def current_session(args: argparse.Namespace) -> str:
    if args.session is not None:
        return session_id(args.session)
    session = os.environ.get("CODEX_SESSION_ID", "")
    thread = os.environ.get("CODEX_THREAD_ID", "")
    if session and thread and session != thread:
        raise PlanningError("CODEX_SESSION_ID and CODEX_THREAD_ID differ; use --session with the target hook session_id")
    if not (session or thread):
        raise PlanningError("No current session ID; use --session with the target hook session_id")
    return session_id(session or thread)


def registry_root(args: argparse.Namespace) -> Path:
    if args.registry == "":
        raise PlanningError("--registry must not be empty")
    root = expanded(args.registry) if args.registry else codex_home() / "planning-with-files" / "bindings"
    return within(root.resolve(), real_home(), "Binding registry")


def binding_file(args: argparse.Namespace, selected_session: str) -> Path:
    root = registry_root(args)
    target = root / (hashlib.sha256(selected_session.encode("utf-8")).hexdigest() + ".json")
    if target.is_symlink():
        raise PlanningError("A session binding file must not be a symlink")
    return within(target.resolve(), root, "Session binding")


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
        if args.record == "" or args.task == "":
            raise PlanningError("An explicit record/task must not be empty")
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


def bind(args: argparse.Namespace, project: Path) -> dict:
    record_value, task = selector(args)
    if record_value is None and task is None:
        raise PlanningError("bind requires --record/--task or PWF_RECORD/PLAN_ID; no inferred task binding")
    record = resolve_record(args, project)
    selected_session = current_session(args)
    target = binding_file(args, selected_session)
    metadata = {"version": 1, "session_id": selected_session, "project": str(project), "record": str(record)}
    content = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if len(content) > REGISTRY_LIMIT:
        raise PlanningError("Binding metadata is too large")
    if target.exists() and not target.is_file():
        raise PlanningError("Session binding is not a regular file")
    if target.exists() and target.stat().st_size > REGISTRY_LIMIT:
        raise PlanningError("Existing binding metadata is too large")
    changed = not target.exists() or target.read_bytes() != content
    if changed:
        atomic_write(target, content)
    return {"session_id": selected_session, "project": str(project), "record": str(record),
            "binding_file": str(target), "changed": changed}


def unbind(args: argparse.Namespace) -> dict:
    selected_session = current_session(args)
    target = binding_file(args, selected_session)
    if target.exists() and not target.is_file():
        raise PlanningError("Session binding is not a regular file")
    removed = target.exists()
    target.unlink(missing_ok=True)
    return {"session_id": selected_session, "binding_file": str(target), "removed": removed}


def bound_record(args: argparse.Namespace, selected_session: str, event_cwd: Path) -> tuple[Path, Path] | None:
    target = binding_file(args, selected_session)
    if not target.exists():
        return None
    if not target.is_file():
        raise PlanningError("Session binding is not a regular file")
    with target.open("rb") as stream:
        raw = stream.read(REGISTRY_LIMIT + 1)
    if len(raw) > REGISTRY_LIMIT:
        raise PlanningError("Binding metadata is too large")
    metadata = decode_json(raw)
    if not isinstance(metadata, dict) or type(metadata.get("version")) is not int or metadata["version"] != 1:
        raise PlanningError("Unknown binding metadata format")
    if metadata.get("session_id") != selected_session:
        raise PlanningError("Binding session ID does not match its registry file")
    if set(metadata) != {"version", "session_id", "project", "record"}:
        raise PlanningError("Binding metadata needs only version, session_id, project and record")
    project_value = metadata.get("project")
    if not isinstance(project_value, str) or not Path(project_value).is_absolute():
        raise PlanningError("Binding project must be absolute")
    # Metadata paths are canonical literals, not environment-variable templates.
    project = Path(project_value).resolve()
    if not project.is_dir():
        raise PlanningError("Binding project no longer exists")
    if str(project) != project_value:
        raise PlanningError("Binding project is no longer its recorded canonical path")
    if not event_cwd.is_relative_to(project):
        return None
    if args.project is not None or os.environ.get("PWF_PLAN_ROOT", "").strip():
        if project_path(args.project) != project:
            return None
    record = metadata.get("record")
    if not isinstance(record, str) or not Path(record).is_absolute():
        raise PlanningError("Binding record must be absolute")
    resolved = safe_file(Path(record), project)
    if str(resolved) != record:
        raise PlanningError("Binding record is no longer its recorded canonical path")
    return project, resolved


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
    class Parser(argparse.ArgumentParser):
        def error(self, message):
            # A malformed optional hook invocation must also remain non-blocking.
            if len(sys.argv) > 1 and sys.argv[1] == "hook":
                raise PlanningError(message)
            super().error(message)
    parser = Parser(description=__doc__)
    parser.add_argument("command", choices=["paths", "list", "select", "init", "status", "print", "bind", "unbind",
                                            "hook", "hooks-template", "configure-hooks"])
    parser.add_argument("--project", help="Project root; default PWF_PLAN_ROOT or cwd")
    selectors = parser.add_mutually_exclusive_group()
    selectors.add_argument("--record", help="Existing record, absolute or project-relative")
    selectors.add_argument("--task", help="Named task under .planning/<id>/task_plan.md")
    parser.add_argument("--title", help="Title for a newly initialized task")
    parser.add_argument("--evidence", help="Optional project-relative or absolute evidence JSON")
    parser.add_argument("--max-chars", type=int, default=16000, help="Context character budget (default 16000)")
    parser.add_argument("--python", help="Absolute trusted Python executable for a hook template")
    parser.add_argument("--session", help="Explicit target hook session_id for bind/unbind; default verified current ID environment")
    parser.add_argument("--registry", help="Binding registry directory within real HOME; default CODEX_HOME/planning-with-files/bindings")
    parser.add_argument("--hooks-file", help="Explicit hooks.json file within real HOME for configure-hooks; default CODEX_HOME/hooks.json")
    return parser


def hook(args: argparse.Namespace) -> int:
    raw = sys.stdin.buffer.read(65537)
    if len(raw) > 65536:
        raise PlanningError("Hook payload exceeds 65536 bytes")
    payload = decode_json(raw)
    if not isinstance(payload, dict):
        raise PlanningError("Hook payload must be an object")
    event, cwd = payload.get("hook_event_name"), payload.get("cwd")
    if event not in EVENTS:
        return 0
    if not isinstance(cwd, str) or not Path(cwd).is_absolute():
        raise PlanningError("Hook cwd must be an absolute path")
    event_cwd = Path(cwd).resolve()
    if not event_cwd.is_dir():
        raise PlanningError("Hook cwd must be an existing directory")
    if selector(args) != (None, None):
        # Explicit command/environment selectors retain their original behavior.
        project_arg = args.project if args.project or os.environ.get("PWF_PLAN_ROOT", "").strip() else cwd
        project = project_path(project_arg)
        if not event_cwd.is_relative_to(project):
            return 0
        record = resolve_record(args, project)
    else:
        # No shared active pointer, disk-singleton fallback, or inherited ID guess.
        selected = bound_record(args, session_id(payload.get("session_id")), event_cwd)
        if selected is None:
            return 0
        project, record = selected
    output = {"hookSpecificOutput": {"hookEventName": event,
                                    "additionalContext": context(args, project, record)}}
    print(json.dumps(output, ensure_ascii=False))
    return 0


def hooks_template(args: argparse.Namespace) -> dict:
    if args.record is not None or args.task is not None:
        selector(args)
    if args.task is not None and not SLUG.fullmatch(args.task):
        raise PlanningError("Task ID must be a single safe identifier")
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
    if args.registry is not None:
        parts += ["--registry", str(registry_root(args))]
    command = shlex.join(parts)
    entry = {"hooks": [{"type": "command", "command": command, "timeout": 5,
                        "additionalContextLimit": 0}]}
    return {"hooks": {event: [entry] for event in EVENTS}}


def validate_hooks_config(config: object) -> dict:
    if not isinstance(config, dict) or not isinstance(config.get("hooks", {}), dict):
        raise PlanningError("hooks.json must be an object with an object-valued hooks field")
    for event, groups in config.get("hooks", {}).items():
        if not isinstance(groups, list):
            raise PlanningError(f"Unknown hooks format for {event}: expected matcher-group list")
        for group in groups:
            if not isinstance(group, dict) or set(group) - {"matcher", "hooks"}:
                raise PlanningError(f"Unknown matcher-group format for {event}")
            if "matcher" in group and not isinstance(group["matcher"], str):
                raise PlanningError(f"Hook matcher for {event} must be a string")
            if not isinstance(group.get("hooks"), list):
                raise PlanningError(f"Hook group for {event} needs a hooks list")
            for handler in group["hooks"]:
                if not isinstance(handler, dict) or not isinstance(handler.get("type"), str) or not handler["type"]:
                    raise PlanningError(f"Unknown handler format for {event}")
                if handler["type"] == "command" and (not isinstance(handler.get("command"), str) or not handler["command"]):
                    raise PlanningError(f"Command handler for {event} needs a command string")
    return config


def own_hook_command(handler: dict, interpreter: Path, script: Path, script_hash: str) -> bool:
    """Recognize only this helper's generated invocation, never arbitrary shell text."""
    if handler.get("type") != "command" or set(handler) - {"type", "command", "timeout", "additionalContextLimit"}:
        return False
    try:
        parts = shlex.split(handler["command"])
        if len(parts) < 4 or parts[1] != "-I" or parts[3] != "hook":
            return False
        if not Path(parts[0]).is_absolute() or Path(parts[0]).resolve() != interpreter:
            return False
        if not Path(parts[2]).is_absolute():
            return False
        candidate = within(Path(parts[2]).resolve(), real_home(), "Prior hook helper")
        if candidate != script:
            if not candidate.is_file() or candidate.stat().st_size > LIMIT or sha256(candidate) != script_hash:
                return False
        options = parts[4:]
        seen = set()
        if len(options) % 2:
            return False
        for flag, value in zip(options[::2], options[1::2]):
            if flag in seen or flag not in {"--max-chars", "--project", "--task", "--record", "--registry"} or not value:
                return False
            if flag == "--max-chars" and not 512 <= int(value) <= 65536:
                return False
            if flag in {"--project", "--registry"} and not Path(value).is_absolute():
                return False
            if flag == "--task" and not SLUG.fullmatch(value):
                return False
            seen.add(flag)
        return not {"--task", "--record"}.issubset(seen)
    except (PlanningError, OSError, ValueError):
        return False


def configure_hooks(args: argparse.Namespace) -> dict:
    if args.hooks_file == "":
        raise PlanningError("--hooks-file must not be empty")
    target = expanded(args.hooks_file) if args.hooks_file else (codex_home() / "hooks.json").resolve()
    target = within(target, real_home(), "User hooks configuration")
    before = None
    if target.exists():
        if not target.is_file() or target.stat().st_size > LIMIT:
            raise PlanningError("Existing hooks.json must be a regular file of at most 4 MiB")
        before = target.read_bytes()
    original = validate_hooks_config(decode_json(before) if before is not None else {})
    # Use this invocation's final helper path and explicitly selected options.
    fragment = hooks_template(args)
    command = fragment["hooks"][EVENTS[0]][0]["hooks"][0]["command"]
    interpreter = expanded(shlex.split(command)[0])
    script = within(Path(__file__).resolve(), real_home(), "Hook helper")
    script_hash = sha256(script)
    merged = dict(original)
    events = dict(original.get("hooks", {}))
    for event in EVENTS:
        kept = []
        for group in events.get(event, []):
            # Source-specific or otherwise matched user definitions keep their scope.
            if group.get("matcher", "") not in {"", "*"}:
                kept.append(group)
                continue
            handlers = [handler for handler in group["hooks"]
                        if not own_hook_command(handler, interpreter, script, script_hash)]
            if len(handlers) == len(group["hooks"]):
                kept.append(group)
            elif handlers:
                kept.append({**group, "hooks": handlers})
        events[event] = kept + fragment["hooks"][event]
    merged["hooks"] = events
    changed = original != merged
    backup = None
    if changed:
        within(target.resolve(), real_home(), "User hooks configuration")
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if before is not None:
            # Preserve the exact previous bytes; normal client trust remains separate.
            with tempfile.NamedTemporaryFile(prefix=target.name + ".pwf-backup-", suffix=".json",
                                             dir=target.parent, delete=False) as stream:
                backup = str(Path(stream.name).resolve())
                stream.write(before)
        if (target.read_bytes() if target.exists() else None) != before:
            raise PlanningError("hooks.json changed during configuration; no configuration overwritten")
        atomic_write(target, (json.dumps(merged, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"hooks_file": str(target), "changed": changed, "backup": backup,
            "events": list(EVENTS), "command": command, "trust": "Review through the client's normal Hooks UI or /hooks"}


def main() -> int:
    is_hook = len(sys.argv) > 1 and sys.argv[1] == "hook"
    try:
        args = build_parser().parse_args()
        if not 512 <= args.max_chars <= 65536:
            raise PlanningError("max-chars must be between 512 and 65536")
        if args.session is not None and args.command not in {"bind", "unbind"}:
            raise PlanningError("--session is only for bind/unbind; hook session_id comes from stdin")
        if args.hooks_file is not None and args.command != "configure-hooks":
            raise PlanningError("--hooks-file is only for configure-hooks")
        if args.command == "paths":
            print(json.dumps({"real_home": str(real_home()), "codex_home": str(codex_home()),
                              "codex_home_within_write_boundary": codex_home().is_relative_to(real_home()),
                              "default_binding_registry": str((codex_home() / "planning-with-files" / "bindings").resolve()),
                              "default_hooks_file": str((codex_home() / "hooks.json").resolve()),
                              "writes": "explicit init, bind/unbind and configure-hooks only"}, ensure_ascii=False))
            return 0
        if args.command == "hook":
            return hook(args)
        if args.command == "hooks-template":
            print(json.dumps(hooks_template(args), ensure_ascii=False, indent=2))
            return 0
        if args.command == "configure-hooks":
            print(json.dumps(configure_hooks(args), ensure_ascii=False, indent=2))
            return 0
        if args.command == "unbind":
            print(json.dumps(unbind(args), ensure_ascii=False, indent=2))
            return 0
        project = project_path(args.project)
        if args.command == "init":
            output = initialize(args, project)
        elif args.command == "bind":
            output = bind(args, project)
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
    except (ValueError, OSError, RecursionError) as exc:
        # Optional context injection must not block normal work on bad/missing state.
        if is_hook:
            return 0
        print(f"planning-with-files: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
