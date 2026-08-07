from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from astra_engineering_workbench.audit import AppendOnlyAudit

from aion_astra_runtime import BoundedExecutionEngine, RunStatus, TaskSpec
from aion_astra_runtime.cli import main as cli_main
from aion_astra_runtime.errors import PlannerFailure, PolicyDenied
from aion_astra_runtime.models import Action, NetworkPolicy
from aion_astra_runtime.planner import OllamaJsonPlanner
from aion_astra_runtime.policy import deny_privileged_operation, relative_path, validate_endpoint, validate_task_paths


def runtime_context(agent_id: str = "AION") -> dict[str, str]:
    return {
        "agent_id": agent_id,
        "runtime_instance_id": f"{agent_id}-I-001",
        "memory_stream_id": f"{agent_id}-MEM-001",
        "event_lineage_id": f"{agent_id}-EVENT-001",
        "canonical_state_reference": f"{agent_id}-CANONICAL",
        "genesis_root_id": "ROOT-001",
    }


def task(task_id: str = "RUNTIME-E2E-001") -> TaskSpec:
    return TaskSpec.from_dict(
        {
            "task_id": task_id,
            "objective": "Inventory and summarize the approved local input",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["input.txt"],
            "output_path": "runtime_output/summary.md",
            "owner_approved": True,
            "approved_by": "RESEARCH_OWNER",
            "runtime_context": runtime_context(),
            "max_steps": 8,
            "network_policy": "OFFLINE",
            "canonical_effect": "NONE",
        }
    )


class RuntimeEndToEndTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.baseline = root / "baseline"
        self.sessions = root / "sessions"
        self.baseline.mkdir()
        self.sessions.mkdir()
        (self.baseline / "input.txt").write_text("runtime test\nSecond line\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_complete_candidate_loop_preserves_baseline_and_context(self) -> None:
        before = (self.baseline / "input.txt").read_bytes()
        result = BoundedExecutionEngine().run(task(), baseline_root=self.baseline, sessions_root=self.sessions)
        self.assertEqual(result.status, RunStatus.PASS_PENDING_OWNER_REVIEW)
        self.assertEqual(result.runtime_context.agent_id, "AION")
        self.assertTrue(result.baseline_unchanged)
        self.assertTrue(result.audit_chain_valid)
        self.assertEqual((self.baseline / "input.txt").read_bytes(), before)
        candidate = Path(result.candidate_root) / result.output_relative_path
        self.assertTrue(candidate.is_file())
        self.assertIn("canonical_effect: `NONE`", candidate.read_text(encoding="utf-8"))
        self.assertTrue(AppendOnlyAudit(Path(result.audit_path)).verify())
        record = json.loads((Path(result.output_root) / "RUN_RESULT.json").read_text(encoding="utf-8"))
        self.assertEqual(record["runtime_context"]["runtime_instance_id"], "AION-I-001")
        events = AppendOnlyAudit(Path(result.audit_path)).events()
        self.assertTrue(all(event["details"]["agent_id"] == "AION" for event in events))

    def test_kill_switch_holds_before_first_action(self) -> None:
        kill = Path(self.temp.name) / "KILL"
        kill.write_text("stop", encoding="utf-8")
        result = BoundedExecutionEngine().run(task("RUNTIME-KILL-001"), baseline_root=self.baseline, sessions_root=self.sessions, kill_switch=kill)
        self.assertEqual(result.status, RunStatus.HOLD)
        self.assertIn("kill switch", result.failure_reason or "")

    def test_step_budget_exhaustion_holds(self) -> None:
        class RepeatingPlanner:
            def next_action(self, _task: TaskSpec, _observations: tuple[object, ...]) -> Action:
                return Action("list_files")

        result = BoundedExecutionEngine(RepeatingPlanner()).run(task("RUNTIME-BUDGET-001"), baseline_root=self.baseline, sessions_root=self.sessions)
        self.assertEqual(result.status, RunStatus.HOLD)
        self.assertIn("step budget", result.failure_reason or "")

    def test_cli_executes_installed_contract(self) -> None:
        task_path = Path(self.temp.name) / "task.json"
        task_path.write_text(json.dumps({
            "task_id": "RUNTIME-CLI-001",
            "objective": "Inventory and summarize",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["input.txt"],
            "output_path": "out/summary.md",
            "owner_approved": True,
            "approved_by": "RESEARCH_OWNER",
            "runtime_context": runtime_context("ASTRA"),
            "max_steps": 8,
            "network_policy": "OFFLINE",
            "canonical_effect": "NONE",
        }), encoding="utf-8")
        self.assertEqual(cli_main(["run", "--task", str(task_path), "--baseline", str(self.baseline), "--sessions", str(self.sessions)]), 0)


class PolicyTests(unittest.TestCase):
    def test_runtime_context_is_mandatory(self) -> None:
        raw = {
            "task_id": "NO-CONTEXT",
            "objective": "x",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["a.txt"],
            "output_path": "out.txt",
            "owner_approved": True,
            "approved_by": "OWNER",
        }
        with self.assertRaises(PolicyDenied):
            TaskSpec.from_dict(raw)

    def test_owner_approval_is_mandatory(self) -> None:
        raw = {
            "task_id": "NO-APPROVAL",
            "objective": "x",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["a.txt"],
            "output_path": "out.txt",
            "owner_approved": False,
            "approved_by": "",
            "runtime_context": runtime_context(),
        }
        with self.assertRaises(PolicyDenied):
            TaskSpec.from_dict(raw)

    def test_path_traversal_is_rejected(self) -> None:
        with self.assertRaises(PolicyDenied):
            relative_path("../outside.txt")

    def test_external_network_is_rejected(self) -> None:
        with self.assertRaises(PolicyDenied):
            validate_endpoint("https://example.invalid", NetworkPolicy.LOOPBACK_ONLY)

    def test_offline_and_credentialed_endpoints_are_rejected(self) -> None:
        with self.assertRaises(PolicyDenied):
            validate_endpoint("http://127.0.0.1:11434", NetworkPolicy.OFFLINE)
        with self.assertRaises(PolicyDenied):
            validate_endpoint("http://user:pass@127.0.0.1:11434", NetworkPolicy.LOOPBACK_ONLY)
        validate_endpoint("http://localhost:11434", NetworkPolicy.LOOPBACK_ONLY)

    def test_privileged_operations_are_rejected(self) -> None:
        for operation in ("canonical_write", "identity_mutation", "memory_write", "deployment", "privilege_escalation"):
            with self.assertRaises(PolicyDenied):
                deny_privileged_operation(operation)

    def test_task_validation_rejects_scope_expansion(self) -> None:
        base = {
            "task_id": "VALIDATION",
            "objective": "x",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["a.txt"],
            "output_path": "out.txt",
            "owner_approved": True,
            "approved_by": "OWNER",
            "runtime_context": runtime_context(),
            "max_steps": 8,
        }
        for key, value in (("profile", "GENERAL"), ("canonical_effect", "WRITE"), ("max_steps", 2)):
            raw = dict(base)
            raw[key] = value
            with self.assertRaises(PolicyDenied):
                TaskSpec.from_dict(raw)
        same = TaskSpec.from_dict({**base, "output_path": "a.txt"})
        with self.assertRaises(PolicyDenied):
            validate_task_paths(same)


class PlannerTests(unittest.TestCase):
    @staticmethod
    def planner_task() -> TaskSpec:
        return TaskSpec.from_dict({
            "task_id": "MODEL-PLANNER",
            "objective": "choose a tool",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["a.txt"],
            "output_path": "out.txt",
            "owner_approved": True,
            "approved_by": "OWNER",
            "runtime_context": runtime_context(),
            "max_steps": 8,
            "network_policy": "LOOPBACK_ONLY",
        })

    def test_localhost_planner_valid_decision(self) -> None:
        fake = SimpleNamespace(generate=lambda *_args, **_kwargs: SimpleNamespace(text='{"tool":"list_files","arguments":{}}'))
        with patch("aion_astra_runtime.planner.OllamaRuntime", return_value=fake):
            action = OllamaJsonPlanner("local-model").next_action(self.planner_task(), ())
        self.assertEqual(action.tool, "list_files")

    def test_localhost_planner_rejects_bad_responses(self) -> None:
        for text in ("not-json", '{"tool":"external","arguments":{}}', '{"tool":"read_text","arguments":{"path":1}}'):
            fake = SimpleNamespace(generate=lambda *_args, _text=text, **_kwargs: SimpleNamespace(text=_text))
            with patch("aion_astra_runtime.planner.OllamaRuntime", return_value=fake):
                with self.assertRaises(PlannerFailure):
                    OllamaJsonPlanner("local-model").next_action(self.planner_task(), ())


if __name__ == "__main__":
    unittest.main()
