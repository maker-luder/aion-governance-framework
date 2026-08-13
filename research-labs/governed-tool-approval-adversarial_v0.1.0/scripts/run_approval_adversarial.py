from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_tool_approval import ApprovalDecision, ApprovalPolicy, PolicyRule, SandboxSpec, ToolCall, build_execution_disposition
from aion_tool_approval_adversarial import audit_call_batch, audit_tool_disposition


def approved(tool: str = "read_file", *, call_id: str = "call:1", arguments: dict[str, object] | None = None) -> tuple[ToolCall, ApprovalPolicy]:
    return ToolCall(tool, arguments or {"path": "fixture.txt"}, call_id), ApprovalPolicy((PolicyRule("approved", tool, ApprovalDecision.APPROVE),))


def run(output: Path) -> dict[str, object]:
    cases = []
    def add(case_id: str, audit) -> None:
        decision = audit.as_dict()
        assert decision["approval_event_only"] is True
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        cases.append({"case_id": case_id, "decision": decision})

    call, policy = approved()
    add("read-approved", audit_tool_disposition(call, policy, expected_call_id="call:1"))
    call, policy = approved(call_id="")
    add("missing-call-id", audit_tool_disposition(call, policy))
    call, policy = approved()
    add("call-id-scope-mismatch", audit_tool_disposition(call, policy, expected_call_id="call:other"))
    add("unmatched-call", audit_tool_disposition(ToolCall("unknown", {}, "call:2"), ApprovalPolicy(())))
    escalation = ApprovalPolicy((PolicyRule("escalate", "bash", ApprovalDecision.ESCALATE), PolicyRule("approve", "bash", ApprovalDecision.APPROVE)))
    add("escalate-then-approve", audit_tool_disposition(ToolCall("bash", {"command": "fixture"}, "call:3"), escalation, SandboxSpec()))
    reject = ApprovalPolicy((PolicyRule("reject", "read_file", ApprovalDecision.REJECT),))
    add("reject-call", audit_tool_disposition(ToolCall("read_file", {}, "call:4"), reject))
    terminate = ApprovalPolicy((PolicyRule("terminate", "danger*", ApprovalDecision.TERMINATE),))
    add("terminate-call", audit_tool_disposition(ToolCall("dangerous", {}, "call:5"), terminate))
    call, policy = approved("python", call_id="call:6", arguments={"code": "fixture"})
    add("python-without-sandbox", audit_tool_disposition(call, policy))
    call, policy = approved("python", call_id="call:7", arguments={"code": "fixture"})
    add("python-with-sandbox", audit_tool_disposition(call, policy, SandboxSpec()))
    call, policy = approved("shell", call_id="call:8", arguments={"command": "fixture"})
    add("restricted-sandbox", audit_tool_disposition(call, policy, SandboxSpec(network_mode="restricted")))
    call, policy = approved()
    add("execution-request", audit_tool_disposition(call, policy, execution_requested=True))
    modify = ApprovalPolicy((PolicyRule("clamp", "python", ApprovalDecision.MODIFY, modified_arguments={"timeout": 2}),))
    add("modify-arguments", audit_tool_disposition(ToolCall("python", {"code": "fixture", "timeout": 50}, "call:9"), modify, SandboxSpec()))
    scoped = ApprovalPolicy((PolicyRule("move-only", "computer", ApprovalDecision.APPROVE, {"action": "move"}),))
    add("argument-scope-allowed", audit_tool_disposition(ToolCall("computer", {"action": "move"}, "call:10"), scoped, SandboxSpec()))
    add("argument-scope-denied", audit_tool_disposition(ToolCall("computer", {"action": "key"}, "call:11"), scoped, SandboxSpec()))
    add("empty-batch", audit_call_batch(()))
    call, policy = approved(call_id="call:12")
    item = build_execution_disposition(call, policy)
    item2 = dict(item)
    add("duplicate-batch", audit_call_batch((item, item2)))
    item["call_id"] = ""
    add("batch-missing-call-id", audit_call_batch((item,)))
    call, policy = approved(call_id="call:13")
    item = build_execution_disposition(call, policy)
    item["canonical_effect"] = "WRITE"
    add("batch-canonical-effect", audit_call_batch((item,)))
    call, policy = approved(call_id="call:14")
    item = build_execution_disposition(call, policy)
    item["approval_event_only"] = False
    add("batch-event-flag", audit_call_batch((item,)))
    call1, policy1 = approved(call_id="call:15")
    call2, policy2 = approved(call_id="call:16")
    add("valid-batch", audit_call_batch((build_execution_disposition(call1, policy1), build_execution_disposition(call2, policy2))))

    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "governed-tool-approval-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(cases),
        "records": cases,
        "tool_execution": False,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "approval_event_only": True,
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
