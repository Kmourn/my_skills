"""Observable CLI regressions; fixtures remain in an explicitly selected HOME cache.

Run: PWF_TEST_ROOT=<home-cache-dir> python3 -I tests/test_planning.py
Python 3.10+. Hook template/configuration tests require POSIX; symlinks require OS support.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "planning.py"
ALL_COMPLETE = "# Task\n## Next Step\nReview actual outputs.\n## Phases\n### Phase 1: delivery\n- **Status:** complete\n"
MOCK_PLATFORM_CLI = """
import importlib.util
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("planning_platform_test", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# Replace only this module's OS reference, leaving pathlib's real platform intact.
module.os = SimpleNamespace(name=sys.argv[2])
sys.argv = [sys.argv[1], *sys.argv[3:]]
sys.exit(module.main())
"""


def real_home() -> Path:
    if os.name == "posix":
        import pwd
        return Path(pwd.getpwuid(os.getuid()).pw_dir).resolve()
    return Path.home().resolve()


class PlanningCli(unittest.TestCase):
    def setUp(self):
        base = Path(os.environ["PWF_TEST_ROOT"]).expanduser().resolve()
        self.home = real_home()
        if not base.is_relative_to(self.home):
            raise RuntimeError("PWF_TEST_ROOT must be within real HOME")
        base.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="planning-test-", dir=base)
        self.root = Path(self.tmp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.env = os.environ.copy()
        for key in ("PLAN_ID", "PWF_RECORD", "PWF_PLAN_ROOT", "CODEX_SESSION_ID", "CODEX_THREAD_ID"):
            self.env.pop(key, None)
        self.registry = self.root / "registry"
        self.hooks_file = self.root / "configuration" / "hooks.json"
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, payload=None, env=None, cwd=None, expected=0, script=None, platform_name=None):
        arguments = list(map(str, args))
        if arguments[0] in {"bind", "unbind", "hook", "hooks-template", "configure-hooks"} and "--registry" not in arguments:
            arguments += ["--registry", str(self.registry)]
        if arguments[0] == "configure-hooks" and "--hooks-file" not in arguments:
            arguments += ["--hooks-file", str(self.hooks_file)]
        command = [sys.executable, "-I", str(script or SCRIPT), *arguments]
        if platform_name is not None:
            command = [sys.executable, "-I", "-c", MOCK_PLATFORM_CLI, str(script or SCRIPT), platform_name, *arguments]
        result = subprocess.run(command,
                                input=json.dumps(payload) if isinstance(payload, dict) else payload,
                                cwd=cwd or self.project, env=env or self.env,
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def outside_home(self):
        root = Path(self.home.anchor).resolve()
        if root.is_relative_to(self.home):
            self.skipTest("No filesystem root lies outside real HOME")
        return root

    def symlink(self, link, target, *, target_is_directory=False):
        try:
            link.symlink_to(target, target_is_directory=target_is_directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symbolic links are unavailable: {exc}")

    def task(self, name, text):
        target = self.project / ".planning" / name / "task_plan.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def event(self, session="session-A", name="UserPromptSubmit", **extra):
        return {"cwd": str(self.project), "hook_event_name": name, "session_id": session,
                "model": "synthetic", "permission_mode": "default",
                "transcript_path": str(self.project / "transcript-sentinel.jsonl"),
                "prompt": "Do not use prompt-sentinel as planning state", "turn_id": "synthetic-turn", **extra}

    def snapshot(self):
        return {str(path.relative_to(self.root)): (path.read_bytes(), path.stat().st_mtime_ns)
                for path in self.root.rglob("*") if path.is_file()}

    def assert_quiet_hook(self, *args, payload=None, env=None):
        result = self.run_cli("hook", *args, payload=payload or self.event(), env=env)
        self.assertEqual((result.stdout, result.stderr), ("", ""))
        return result

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
        record.write_text("# Existing project record\n已确认选择：沿用原格式\n下一步：检查产物\n", encoding="utf-8")
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
        home = self.home
        before = self.snapshot()
        result = json.loads(self.run_cli("paths").stdout)
        self.assertEqual(result["real_home"], str(home))
        value = os.path.expandvars(self.env.get("CODEX_HOME", "").strip() or str(home / ".codex"))
        if value == "~" or value.startswith("~/"):
            value = str(home) + value[1:]
        expected = Path(value)
        expected = expected.resolve() if expected.is_absolute() else (self.project / expected).resolve()
        self.assertEqual(result["codex_home"], str(expected))
        self.assertEqual(result["codex_home_within_write_boundary"], expected.is_relative_to(home))
        self.assertEqual(result["default_binding_registry"], str((expected / "planning-with-files" / "bindings").resolve()))
        self.assertEqual(before, self.snapshot())

    def test_symlink_escape_rejects_record_and_init(self):
        outside = self.root / "other-project"
        outside.mkdir()
        (outside / "existing.md").write_text("Outside project")
        self.symlink(self.project / "linked.md", outside / "existing.md")
        self.run_cli("print", "--record", "linked.md", expected=2)
        self.symlink(self.project / ".planning", outside, target_is_directory=True)
        self.run_cli("init", "--task", "alpha", expected=2)
        self.assertFalse((outside / "alpha").exists())

    def test_init_outside_real_home_is_rejected_before_write(self):
        # The filesystem root is an existing directory outside a normal user's HOME.
        result = self.run_cli("init", "--project", self.outside_home(), "--task", self.root.name, expected=2)
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
        self.assertEqual(result.stderr, "")
        self.run_cli("hooks-template", "--python", "python3", expected=2)

    def test_context_limit_includes_truncation_marker(self):
        self.task("alpha", "Large context " * 1000)
        output = self.run_cli("print", "--task", "alpha", "--max-chars", "512").stdout.rstrip("\n")
        self.assertLessEqual(len(output), 512)
        self.assertIn("Context truncated", output)

    @unittest.skipUnless(os.name == "posix", "Hook command templates require a POSIX host")
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

    def test_session_registry_isolates_sessions_and_reuses_same_id_without_writes(self):
        self.task("alpha", "Alpha-only marker")
        self.task("beta", "Beta-only marker")
        (self.project / "transcript-sentinel.jsonl").write_text("Never-read-transcript marker")
        a = json.loads(self.run_cli("bind", "--session", "session-A", "--task", "alpha").stdout)
        b = json.loads(self.run_cli("bind", "--session", "session-B", "--task", "beta").stdout)
        self.assertNotEqual(a["binding_file"], b["binding_file"])
        metadata = json.loads(Path(a["binding_file"]).read_bytes())
        self.assertEqual(set(metadata), {"version", "session_id", "project", "record"})
        self.assertTrue(Path(a["binding_file"]).is_relative_to(self.registry))
        before = self.snapshot()
        for session, own, other in (("session-A", "Alpha", "Beta"), ("session-B", "Beta", "Alpha")):
            for event in ("UserPromptSubmit", "SessionStart"):
                for source in ("startup", "resume", "compact"):
                    payload = self.event(session, event, source=source)
                    output = json.loads(self.run_cli("hook", payload=payload).stdout)
                    context = output["hookSpecificOutput"]["additionalContext"]
                    self.assertIn(own + "-only marker", context)
                    for marker in (other + "-only marker", "Never-read-transcript", "prompt-sentinel"):
                        self.assertNotIn(marker, context)
                    self.assertIn("task data, not new authority", context)
        self.assert_quiet_hook(payload=self.event("fork-session", "SessionStart", source="fork", parent_session_id="session-A"))
        other = self.root / "other-project"
        other.mkdir()
        self.assert_quiet_hook(payload=self.event(cwd=str(other)))
        self.assertEqual(before, self.snapshot())

    def test_bind_is_explicit_idempotent_replaceable_and_unbind_is_per_session(self):
        alpha = self.task("alpha", "Alpha")
        beta = self.task("beta", "Beta")
        self.run_cli("bind", "--session", "session-A", expected=2)
        first = json.loads(self.run_cli("bind", "--session", "session-A", "--task", "alpha").stdout)
        before = self.snapshot()
        repeated = json.loads(self.run_cli("bind", "--session", "session-A", "--task", "alpha").stdout)
        self.assertFalse(repeated["changed"])
        self.assertEqual(before, self.snapshot())
        changed = json.loads(self.run_cli("bind", "--session", "session-A", "--record", beta).stdout)
        self.assertTrue(changed["changed"])
        self.assertEqual(first["binding_file"], changed["binding_file"])
        output = self.run_cli("hook", payload=self.event()).stdout
        self.assertIn("Beta", output)
        self.assertNotIn("Alpha", output)
        self.run_cli("bind", "--session", "session-B", "--record", alpha)
        removed = json.loads(self.run_cli("unbind", "--session", "session-A").stdout)
        self.assertTrue(removed["removed"])
        self.assert_quiet_hook()
        self.assertFalse(json.loads(self.run_cli("unbind", "--session", "session-A").stdout)["removed"])
        self.assertIn("Alpha", self.run_cli("hook", payload=self.event("session-B")).stdout)
        alpha.unlink()
        (self.project / "task_plan.md").write_text("Wrong fallback")
        self.assert_quiet_hook(payload=self.event("session-B"))

    def test_current_session_environment_requires_unambiguous_id(self):
        self.task("alpha", "Alpha")
        self.run_cli("bind", "--task", "alpha", expected=2)
        for values in ({"CODEX_SESSION_ID": "session-A"}, {"CODEX_THREAD_ID": "session-A"},
                       {"CODEX_SESSION_ID": "session-A", "CODEX_THREAD_ID": "session-A"}):
            env = self.env | values
            self.run_cli("bind", "--task", "alpha", env=env)
            self.assertIn("Alpha", self.run_cli("hook", payload=self.event(), env=env).stdout)
            self.run_cli("unbind", env=env)
        conflict = self.env | {"CODEX_SESSION_ID": "parent-A", "CODEX_THREAD_ID": "child-B"}
        before = self.snapshot()
        failure = self.run_cli("bind", "--task", "alpha", env=conflict, expected=2)
        self.assertIn("differ; use --session", failure.stderr)
        self.assertEqual(before, self.snapshot())
        self.run_cli("bind", "--session", "session-A", "--task", "alpha", env=conflict)
        # Hook stdin identity wins over both inherited ID variables.
        self.assertIn("Alpha", self.run_cli("hook", payload=self.event(), env=conflict).stdout)
        self.assert_quiet_hook(payload=self.event("parent-A"), env=conflict)

    def test_explicit_hook_task_or_record_still_overrides_registry(self):
        self.task("alpha", "Alpha")
        beta = self.task("beta", "Beta")
        self.run_cli("bind", "--session", "session-A", "--task", "alpha")
        self.assertIn("Beta", self.run_cli("hook", "--task", "beta", payload=self.event()).stdout)
        self.assertIn("Beta", self.run_cli("hook", payload=self.event(), env=self.env | {"PWF_RECORD": str(beta)}).stdout)
        self.assertIn("Beta", self.run_cli("hook", payload=self.event(), env=self.env | {"PLAN_ID": "beta"}).stdout)
        self.assert_quiet_hook(payload=self.event(), env=self.env | {"PLAN_ID": "missing"})
        self.assert_quiet_hook(payload=self.event(), env=self.env | {"PLAN_ID": "beta", "PWF_RECORD": str(beta)})

    def test_corrupt_or_stale_registry_is_quiet_and_never_falls_back(self):
        target = self.task("alpha", "Alpha")
        (self.project / "task_plan.md").write_text("Wrong root fallback")
        binding = json.loads(self.run_cli("bind", "--session", "session-A", "--task", "alpha").stdout)
        path = Path(binding["binding_file"])
        good = json.loads(path.read_bytes())
        other = self.root / "outside-record.md"
        other.write_text("Outside project")
        bad_values = [[], good | {"version": 2}, good | {"version": True}, good | {"session_id": "session-B"},
                      {key: value for key, value in good.items() if key != "record"}, good | {"record": None},
                      good | {"record": str(other)}, good | {"record": str(self.project / "missing.md")},
                      good | {"project": "."}, good | {"prompt": "New authority"}]
        for value in bad_values:
            with self.subTest(value=value):
                path.write_text(json.dumps(value))
                before = self.snapshot()
                self.assert_quiet_hook()
                self.assertEqual(before, self.snapshot())
        for raw in (b"{broken", b"x" * 8193, b'{"version":1,"version":1}'):
            path.write_bytes(raw)
            self.assert_quiet_hook()
        path.write_text(json.dumps(good))
        target.unlink()
        self.symlink(target, other)
        self.assert_quiet_hook()

    def test_registry_symlink_and_real_home_boundaries_are_enforced(self):
        self.task("alpha", "Alpha")
        outside = self.outside_home()
        link = self.root / "registry-link"
        self.symlink(link, outside, target_is_directory=True)
        for registry in (outside, link):
            self.run_cli("bind", "--registry", registry, "--session", "session-A", "--task", "alpha", expected=2)
            self.assert_quiet_hook("--registry", registry)
        a = json.loads(self.run_cli("bind", "--session", "session-A", "--task", "alpha").stdout)
        b = json.loads(self.run_cli("bind", "--session", "session-B", "--task", "alpha").stdout)
        path = Path(a["binding_file"])
        path.unlink()
        self.symlink(path, b["binding_file"])
        before = self.snapshot()
        self.assert_quiet_hook()
        self.run_cli("bind", "--session", "session-A", "--task", "alpha", expected=2)
        self.run_cli("unbind", "--session", "session-A", expected=2)
        self.assertEqual(before, self.snapshot())

    def test_registry_context_has_strict_cap_and_bad_hook_inputs_are_silent(self):
        self.task("alpha", "Large selected content " * 10000)
        self.run_cli("bind", "--session", "session-A", "--task", "alpha")
        before = self.snapshot()
        for budget in (512, 16000, 65536):
            output = json.loads(self.run_cli("hook", "--max-chars", budget, payload=self.event()).stdout)
            context = output["hookSpecificOutput"]["additionalContext"]
            self.assertLessEqual(len(context), budget)
            self.assertIn("Context truncated", context)
        bad_payloads = ["{broken", "x" * 65537, "[]", self.event(session_id=None), self.event(session_id=""),
                        self.event(session_id="bad id"), self.event(session_id="x" * 257),
                        self.event(cwd="relative"), self.event(cwd=str(self.project) + "\0"), self.event(name="Stop")]
        for payload in bad_payloads:
            self.assert_quiet_hook(payload=payload)
        for value in (511, 65537, "invalid"):
            self.assert_quiet_hook("--max-chars", value)
        for option in ("--task", "--record", "--registry"):
            self.assert_quiet_hook(option, "")
        self.run_cli("bind", "--session", "session-A", "--task", "", expected=2)
        self.run_cli("hooks-template", "--record", "", expected=2)
        self.assert_quiet_hook("--session", "session-A")
        self.assertEqual(before, self.snapshot())
        target = self.project / ".planning" / "alpha" / "task_plan.md"
        target.write_bytes(b"x" * (4 * 1024 * 1024 + 1))
        before = self.snapshot()
        self.assert_quiet_hook()
        self.assertEqual(before, self.snapshot())

    @unittest.skipUnless(os.name == "posix", "Hook command templates require a POSIX host")
    def test_custom_registry_and_nested_cwd_respect_the_bound_project(self):
        self.task("alpha", "Alpha")
        registry = self.root / "explicit registry"
        self.run_cli("bind", "--registry", registry, "--session", "session-A", "--task", "alpha")
        self.assert_quiet_hook()
        nested = self.project / "src"
        nested.mkdir()
        payload = self.event(cwd=str(nested))
        self.assertIn("Alpha", self.run_cli("hook", "--registry", registry, payload=payload).stdout)
        self.assertIn("Alpha", self.run_cli("hook", "--registry", registry, "--project", self.project, payload=payload).stdout)
        other = self.root / "other-project"
        other.mkdir()
        self.assert_quiet_hook("--registry", registry, "--project", other, payload=payload)
        fragment = json.loads(self.run_cli("hooks-template", "--registry", registry).stdout)
        command = fragment["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        before = self.snapshot()
        output = subprocess.run(["/bin/sh", "-c", command], input=json.dumps(payload), cwd=self.project,
                                env=self.env, text=True, capture_output=True, timeout=5)
        self.assertEqual(output.returncode, 0, output.stderr)
        self.assertIn("Alpha", output.stdout)
        self.assertEqual(before, self.snapshot())

    @unittest.skipUnless(os.name == "posix", "Hook configuration requires a POSIX host")
    def test_configure_hooks_merges_own_entries_backs_up_and_is_idempotent(self):
        template = json.loads(self.run_cli("hooks-template", "--max-chars", 512).stdout)
        own = template["hooks"]["SessionStart"][0]["hooks"][0]
        third = {"type": "command", "command": "printf third-party", "timeout": 7, "custom": "keep"}
        other_type = {"type": "prompt", "prompt": "Keep this provider's handler"}
        original = {"extraConfig": {"preserve": True}, "hooks": {
            "SessionStart": [{"hooks": [own, third]}, {"hooks": [own]}],
            "UserPromptSubmit": [{"hooks": [other_type]}], "PostToolUse": [{"matcher": "Bash", "hooks": [third]}]}}
        hooks = self.hooks_file
        hooks.parent.mkdir(parents=True)
        raw = json.dumps(original, ensure_ascii=False).encode("utf-8")
        hooks.write_bytes(raw)
        result = json.loads(self.run_cli("configure-hooks").stdout)
        self.assertTrue(result["changed"])
        self.assertEqual(Path(result["backup"]).read_bytes(), raw)
        merged = json.loads(hooks.read_bytes())
        self.assertEqual(merged["extraConfig"], original["extraConfig"])
        self.assertEqual(merged["hooks"]["PostToolUse"], original["hooks"]["PostToolUse"])
        self.assertEqual(merged["hooks"]["SessionStart"][0], {"hooks": [third]})
        self.assertEqual(merged["hooks"]["UserPromptSubmit"][0], {"hooks": [other_type]})
        for event in ("SessionStart", "UserPromptSubmit"):
            self.assertEqual(merged["hooks"][event][-1]["hooks"][0]["additionalContextLimit"], 0)
            self.assertEqual(sum(handler["type"] == "command" and "planning.py" in handler["command"]
                                 for group in merged["hooks"][event] for handler in group["hooks"]), 1)
        before = self.snapshot()
        again = json.loads(self.run_cli("configure-hooks").stdout)
        self.assertFalse(again["changed"])
        self.assertIsNone(again["backup"])
        self.assertEqual(before, self.snapshot())

    @unittest.skipUnless(os.name == "posix", "Hook configuration requires a POSIX host")
    def test_configure_uses_final_helper_path_and_only_removes_verified_copies(self):
        installed = self.root / "installed skill" / "scripts" / "planning.py"
        installed.parent.mkdir(parents=True)
        installed.write_bytes(SCRIPT.read_bytes())
        unrelated = self.root / "other" / "planning.py"
        unrelated.parent.mkdir()
        unrelated.write_text("print('Other package with same filename')\n")
        template = json.loads(self.run_cli("hooks-template").stdout)
        own = template["hooks"]["SessionStart"][0]["hooks"][0]
        other = own | {"command": shlex.join([str(Path(sys.executable).resolve()), "-I", str(unrelated), "hook"])}
        shell_wrapper = own | {"command": own["command"] + " ; printf wrapper"}
        matched = {"matcher": "fork", "hooks": [own]}
        hooks = self.hooks_file
        hooks.parent.mkdir(parents=True)
        hooks.write_text(json.dumps({"hooks": {"SessionStart": [{"hooks": [own, other, shell_wrapper]}, matched]}}))
        result = json.loads(self.run_cli("configure-hooks", script=installed).stdout)
        self.assertEqual(shlex.split(result["command"])[2], str(installed))
        merged = json.loads(hooks.read_bytes())
        self.assertEqual(merged["hooks"]["SessionStart"][0], {"hooks": [other, shell_wrapper]})
        self.assertEqual(merged["hooks"]["SessionStart"][1], matched)
        self.assertFalse(json.loads(self.run_cli("configure-hooks", script=installed).stdout)["changed"])
        self.assertFalse((hooks.parent / "config.toml").exists())

    @unittest.skipUnless(os.name == "posix", "Hook configuration requires a POSIX host")
    def test_configure_rejects_unknown_or_duplicate_json_without_overwrite(self):
        hooks = self.hooks_file
        hooks.parent.mkdir(parents=True)
        values = [[], {"hooks": []}, {"hooks": {"SessionStart": {}}},
                  {"hooks": {"SessionStart": [{"hooks": [] , "unknownGroupField": True}]}},
                  {"hooks": {"SessionStart": [{"hooks": [{"type": "command"}]}]}}]
        for value in values:
            hooks.write_text(json.dumps(value))
            before = self.snapshot()
            self.run_cli("configure-hooks", expected=2)
            self.assertEqual(before, self.snapshot())
        for raw in ('{broken', '{"hooks":{},"hooks":{}}'):
            hooks.write_text(raw)
            before = self.snapshot()
            self.run_cli("configure-hooks", expected=2)
            self.assertEqual(before, self.snapshot())

    @unittest.skipUnless(os.name == "posix", "Hook configuration requires a POSIX host")
    def test_configure_and_registry_cannot_write_outside_real_home(self):
        self.task("alpha", "Alpha")
        outside = self.outside_home()
        target = outside / (self.root.name + "-hooks.json")
        self.run_cli("configure-hooks", "--hooks-file", target, expected=2)
        self.run_cli("bind", "--registry", outside, "--session", "session-A", "--task", "alpha", expected=2)
        self.assert_quiet_hook("--registry", outside)
        self.hooks_file.parent.mkdir(parents=True)
        self.symlink(self.hooks_file, target)
        self.run_cli("configure-hooks", expected=2)
        self.assertEqual(list(self.hooks_file.parent.iterdir()), [self.hooks_file])

    @unittest.skipUnless(os.name == "posix", "Hook configuration requires a POSIX host")
    def test_template_is_read_only_and_first_configuration_has_no_fake_trust(self):
        before = self.snapshot()
        self.run_cli("hooks-template")
        self.assertEqual(before, self.snapshot())
        result = json.loads(self.run_cli("configure-hooks").stdout)
        self.assertTrue(result["changed"])
        self.assertIsNone(result["backup"])
        hooks = Path(result["hooks_file"])
        self.assertEqual(list(hooks.parent.iterdir()), [hooks])
        self.assertNotIn("trusted_hash", hooks.read_text())
        self.assertEqual(set(json.loads(hooks.read_bytes())["hooks"]), {"SessionStart", "UserPromptSubmit"})

    @unittest.skipUnless(os.name == "posix", "Hook configuration requires a POSIX host")
    def test_explicit_hooks_file_is_isolated_and_resolves_home_contained_symlink(self):
        target = self.root / "explicit-config" / "hooks.json"
        result = json.loads(self.run_cli("configure-hooks", "--hooks-file", target).stdout)
        self.assertEqual(result["hooks_file"], str(target))
        self.assertFalse(self.hooks_file.parent.exists())
        link = self.root / "linked-hooks.json"
        self.symlink(link, target)
        before = self.snapshot()
        self.assertFalse(json.loads(self.run_cli("configure-hooks", "--hooks-file", link).stdout)["changed"])
        self.assertEqual(before, self.snapshot())
        self.assertTrue(link.is_symlink())
        outside = self.outside_home() / (self.root.name + "-hooks.json")
        self.run_cli("configure-hooks", "--hooks-file", outside, expected=2)
        self.run_cli("configure-hooks", "--hooks-file", "", expected=2)
        self.run_cli("hooks-template", "--hooks-file", target, expected=2)

    def test_non_posix_template_is_rejected_without_writes(self):
        before = self.snapshot()
        entries = sorted(str(path.relative_to(self.root)) for path in self.root.rglob("*"))
        result = self.run_cli("hooks-template", platform_name="nt", expected=2)
        self.assertEqual(result.stdout, "")
        self.assertIn("require a POSIX host", result.stderr)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(entries, sorted(str(path.relative_to(self.root)) for path in self.root.rglob("*")))
        self.assertFalse(self.registry.exists())
        self.assertFalse(self.hooks_file.parent.exists())

    def test_non_posix_configuration_is_rejected_without_directory_config_or_backup(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                if existing:
                    self.hooks_file.parent.mkdir(parents=True)
                    self.hooks_file.write_bytes(b'{"hooks": {}}\n')
                before = self.snapshot()
                entries = sorted(str(path.relative_to(self.root)) for path in self.root.rglob("*"))
                result = self.run_cli("configure-hooks", platform_name="nt", expected=2)
                self.assertEqual(result.stdout, "")
                self.assertIn("require a POSIX host", result.stderr)
                self.assertEqual(before, self.snapshot())
                self.assertEqual(entries, sorted(str(path.relative_to(self.root)) for path in self.root.rglob("*")))
                self.assertFalse(self.registry.exists())
                if not existing:
                    self.assertFalse(self.hooks_file.parent.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
