"""Observable CLI regressions; fixtures remain in an explicitly selected HOME cache.

Run: PWF_TEST_ROOT=<home-cache-dir> python3 -I tests/test_planning.py
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import pwd
import shlex
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "planning.py"
ALL_COMPLETE = "# Task\n## Next Step\nReview actual outputs.\n## Phases\n### Phase 1: delivery\n- **Status:** complete\n"


class PlanningCli(unittest.TestCase):
    def setUp(self):
        base = Path(os.environ["PWF_TEST_ROOT"]).expanduser().resolve()
        home = Path(pwd.getpwuid(os.getuid()).pw_dir).resolve()
        if not base.is_relative_to(home):
            raise RuntimeError("PWF_TEST_ROOT must be within real HOME")
        base.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="planning-test-", dir=base)
        self.root = Path(self.tmp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.env = os.environ.copy()
        for key in ("PLAN_ID", "PWF_RECORD", "PWF_PLAN_ROOT", "CODEX_HOME"):
            self.env.pop(key, None)
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, payload=None, env=None, cwd=None, expected=0):
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), *map(str, args)],
                                input=json.dumps(payload) if isinstance(payload, dict) else payload,
                                cwd=cwd or self.project, env=env or self.env,
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def task(self, name, text):
        target = self.project / ".planning" / name / "task_plan.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def test_init_is_idempotent_and_creates_only_one_record(self):
        first = json.loads(self.run_cli("init", "--task", "alpha", "--title", "API change").stdout)
        record = Path(first["record"])
        self.assertTrue(first["created"])
        before = record.read_bytes()
        second = json.loads(self.run_cli("init", "--task", "alpha", "--title", "Different").stdout)
        self.assertFalse(second["created"])
        self.assertEqual(record.read_bytes(), before)
        self.assertEqual([p.name for p in record.parent.iterdir()], ["task_plan.md"])

    def test_existing_custom_record_is_reused_without_reformatting(self):
        record = self.project / "existing-progress.md"
        record.write_text("# Existing project record\n已确认选择：沿用原格式\n下一步：检查产物\n")
        before = record.read_bytes()
        output = json.loads(self.run_cli("init", "--record", record.name).stdout)
        self.assertFalse(output["created"])
        self.assertEqual(record.read_bytes(), before)
        self.assertIn("沿用原格式", self.run_cli("print", "--record", record.name).stdout)
        parsed = json.loads(self.run_cli("status", "--record", record.name).stdout)
        self.assertEqual(parsed["phase_state"], "unknown")
        self.assertEqual(parsed["evidence"]["state"], "unverified")

    def test_two_tasks_print_only_their_own_records(self):
        alpha = self.task("alpha", ALL_COMPLETE + "Alpha-only marker\n")
        beta = self.task("beta", ALL_COMPLETE + "Beta-only marker\n")
        (alpha.parent / "progress.md").write_text("Alpha execution evidence")
        (beta.parent / "findings.md").write_text("Beta discovery evidence")
        a = self.run_cli("print", "--task", "alpha").stdout
        b = self.run_cli("print", "--task", "beta").stdout
        self.assertIn("Alpha execution evidence", a)
        self.assertNotIn("Beta", a)
        self.assertIn("Beta discovery evidence", b)
        self.assertNotIn("Alpha", b)

    def test_rejected_task_binding_never_falls_back_to_root(self):
        (self.project / "task_plan.md").write_text("Wrong root record")
        for pin in ("missing", "../escape"):
            result = self.run_cli("print", "--task", pin, expected=2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("Wrong root record", result.stderr)

    def test_multiple_records_ignore_shared_active_pointer(self):
        self.task("alpha", "A")
        self.task("beta", "B")
        (self.project / ".planning" / ".active_plan").write_text("alpha")
        self.assertEqual(self.run_cli("select", expected=2).stdout, "")
        listing = json.loads(self.run_cli("list").stdout)
        self.assertEqual({r["task"] for r in listing["records"]}, {"alpha", "beta"})

    def test_root_and_named_record_require_selection(self):
        self.task("alpha", "A")
        (self.project / "task_plan.md").write_text("Root")
        self.run_cli("select", expected=2)
        selected = json.loads(self.run_cli("select", "--record", "task_plan.md").stdout)
        self.assertEqual(selected["record"], str(self.project / "task_plan.md"))

    def test_root_pin_and_task_support_resume_from_nested_cwd(self):
        target = self.task("alpha", ALL_COMPLETE)
        nested = self.project / "src"
        nested.mkdir()
        env = self.env | {"PWF_PLAN_ROOT": str(self.project), "PLAN_ID": "alpha"}
        selected = json.loads(self.run_cli("select", env=env, cwd=nested).stdout)
        self.assertEqual(selected["record"], str(target))
        bad = env | {"PWF_PLAN_ROOT": "../project"}
        self.run_cli("select", env=bad, cwd=nested, expected=2)

    def test_explicit_record_overrides_environment_task(self):
        target = self.project / "record.md"
        target.write_text("Explicit record")
        env = self.env | {"PLAN_ID": "missing"}
        self.assertIn("Explicit record", self.run_cli("print", "--record", target.name, env=env).stdout)
        self.run_cli("select", env=env | {"PWF_RECORD": target.name}, expected=2)

    def test_paths_resolve_codex_home_without_expanding_write_boundary(self):
        real_home = Path(pwd.getpwuid(os.getuid()).pw_dir).resolve()
        relative = self.root.relative_to(real_home) / "codex-other"
        env = self.env | {"HOME": str(self.root), "CODEX_HOME": "~/" + str(relative)}
        result = json.loads(self.run_cli("paths", env=env).stdout)
        self.assertEqual(result["real_home"], str(real_home))
        self.assertEqual(result["codex_home"], str(real_home / relative))
        external = json.loads(self.run_cli("paths", env=env | {"CODEX_HOME": "/var/lib/codex"}).stdout)
        self.assertFalse(external["codex_home_within_write_boundary"])
        default = json.loads(self.run_cli("paths", env=env | {"CODEX_HOME": ""}).stdout)
        self.assertEqual(default["codex_home"], str(real_home / ".codex"))
        self.assertFalse((real_home / relative).exists())

    def test_symlink_escape_rejects_record_and_init(self):
        outside = self.root / "other-project"
        outside.mkdir()
        (outside / "existing.md").write_text("Outside project")
        (self.project / "linked.md").symlink_to(outside / "existing.md")
        self.run_cli("print", "--record", "linked.md", expected=2)
        (self.project / ".planning").symlink_to(outside, target_is_directory=True)
        self.run_cli("init", "--task", "alpha", expected=2)
        self.assertFalse((outside / "alpha").exists())

    def test_init_outside_real_home_is_rejected_before_write(self):
        # /proc is an existing, readable directory; the helper must reject before mkdir.
        result = self.run_cli("init", "--project", "/proc", "--task", "planning-no-write", expected=2)
        self.assertIn("Plan write resolves outside", result.stderr)

    def test_parser_ignores_examples_and_refuses_duplicate_status(self):
        target = self.task("alpha", "```md\n" + ALL_COMPLETE + "```\n### Phase 2: Actual\n- **Status:** in_progress\n")
        output = json.loads(self.run_cli("status", "--task", "alpha").stdout)
        self.assertEqual(len(output["phases"]), 1)
        self.assertEqual(output["phase_state"], "unfinished")
        target.write_text(ALL_COMPLETE + "- **Status:** complete\n")
        output = json.loads(self.run_cli("status", "--task", "alpha").stdout)
        self.assertEqual(output["phase_state"], "unknown")

    def test_complete_flags_without_evidence_do_not_certify_task(self):
        self.task("alpha", ALL_COMPLETE + "- [ ] Requirement still unchecked\n")
        output = json.loads(self.run_cli("status", "--task", "alpha").stdout)
        self.assertEqual(output["phase_state"], "all_marked_complete")
        self.assertEqual(output["phases"][0]["unchecked"], 1)
        self.assertEqual(output["evidence"]["state"], "unverified")
        self.assertEqual(output["task_completion"], "requires_review")

    def test_evidence_detects_current_changed_failed_and_unrun_checks(self):
        self.task("alpha", ALL_COMPLETE)
        source, artifact = self.project / "source.py", self.project / "run-output.txt"
        source.write_text("print('version A')\n")
        artifact.write_text("Actual synthetic run: pass\n")
        snap = lambda p: {"path": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        evidence = {"checks": [{"name": "synthetic", "result": "passed", "inputs": [snap(source)], "artifact": snap(artifact)}]}
        manifest = self.project / "checks.json"
        manifest.write_text(json.dumps(evidence))
        get = lambda: json.loads(self.run_cli("status", "--task", "alpha", "--evidence", manifest.name).stdout)
        self.assertEqual(get()["evidence"]["state"], "current_recorded_pass")
        artifact.write_text("Output changed after the run\n")
        self.assertEqual(get()["evidence"]["checks"][0]["state"], "stale_or_missing")
        artifact.write_text("Actual synthetic run: pass\n")
        source.write_text("print('version B')\n")
        self.assertEqual(get()["evidence"]["state"], "stale_or_unverified")
        evidence["checks"][0]["result"] = "failed"
        manifest.write_text(json.dumps(evidence))
        self.assertEqual(get()["evidence"]["state"], "failed")
        evidence["checks"][0]["result"] = "unverified"
        manifest.write_text(json.dumps(evidence))
        self.assertEqual(get()["evidence"]["checks"][0]["state"], "unverified")
        self.assertEqual(get()["task_completion"], "requires_review")

    def test_hook_uses_selected_task_and_ignores_transcript_path(self):
        self.task("alpha", "Alpha context")
        self.task("beta", "Beta context")
        payload = {"cwd": str(self.project), "hook_event_name": "UserPromptSubmit",
                   "transcript_path": "/no/such/session.jsonl", "prompt": "Wrong prompt instructions"}
        before = sorted(str(p) for p in self.project.rglob("*"))
        output = json.loads(self.run_cli("hook", "--task", "alpha", payload=payload).stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Alpha context", context)
        self.assertNotIn("Beta context", context)
        self.assertNotIn("Wrong prompt", context)
        self.assertEqual(set(output), {"hookSpecificOutput"})
        self.assertEqual(set(output["hookSpecificOutput"]), {"hookEventName", "additionalContext"})
        self.assertEqual(before, sorted(str(p) for p in self.project.rglob("*")))

    def test_hook_unknown_ambiguous_missing_or_malformed_state_does_not_block(self):
        payload = {"cwd": str(self.project), "hook_event_name": "SessionStart"}
        self.assertEqual(self.run_cli("hook", payload=payload).stdout, "")
        self.task("alpha", "A")
        self.assertEqual(self.run_cli("hook", payload=payload).stdout, "")
        self.task("beta", "B")
        self.assertEqual(self.run_cli("hook", payload=payload).stdout, "")
        self.assertEqual(self.run_cli("hook", payload="{invalid json").stdout, "")
        self.assertEqual(self.run_cli("hook", payload=payload | {"hook_event_name": "Stop"}).stdout, "")

    def test_hook_pinned_project_skips_other_project(self):
        self.task("alpha", "Alpha")
        other = self.root / "other"
        other.mkdir()
        payload = {"cwd": str(other), "hook_event_name": "SessionStart"}
        self.assertEqual(self.run_cli("hook", "--project", self.project, "--task", "alpha", payload=payload).stdout, "")

    def test_hook_rejects_relative_root_pin_and_template_relative_interpreter(self):
        self.task("alpha", "Alpha")
        payload = {"cwd": str(self.project), "hook_event_name": "SessionStart"}
        env = self.env | {"PWF_PLAN_ROOT": ".", "PLAN_ID": "alpha"}
        result = self.run_cli("hook", payload=payload, env=env)
        self.assertEqual(result.stdout, "")
        self.assertIn("absolute project path", result.stderr)
        self.run_cli("hooks-template", "--python", "python3", expected=2)

    def test_context_limit_includes_truncation_marker(self):
        self.task("alpha", "Large context " * 1000)
        output = self.run_cli("print", "--task", "alpha", "--max-chars", "512").stdout.rstrip("\n")
        self.assertLessEqual(len(output), 512)
        self.assertIn("Context truncated", output)

    def test_hook_template_is_deterministic_and_quotes_shell_metacharacters(self):
        filename = "record-$(touch injected).md"
        (self.project / filename).write_text("Selected unusual filename")
        args = ("hooks-template", "--project", self.project, "--record", filename)
        first, second = self.run_cli(*args).stdout, self.run_cli(*args).stdout
        self.assertEqual(first, second)
        fragment = json.loads(first)
        self.assertEqual(set(fragment["hooks"]), {"SessionStart", "UserPromptSubmit"})
        for entry in fragment["hooks"].values():
            self.assertEqual(entry[0]["hooks"][0]["additionalContextLimit"], 0)
        command = fragment["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        self.assertIn(filename, shlex.split(command))
        result = subprocess.run(["/bin/sh", "-c", command], cwd=self.project, env=self.env,
                                input=json.dumps({"cwd": str(self.project), "hook_event_name": "UserPromptSubmit"}),
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Selected unusual filename", result.stdout)
        self.assertFalse((self.project / "injected").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
