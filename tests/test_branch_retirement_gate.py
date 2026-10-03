"""Regression for Teacher review 5971958839: HOLD must have no delete side effect."""
from scripts import validate_branch_topology as gate


def test_closed_event_without_preservation_or_authority_never_deletes(monkeypatch, capsys):
    requests = []

    def api(url, token, method="GET"):
        requests.append((method, url))
        if "/branches/" in url:
            return {"commit": {"sha": "a" * 40}}, {}
        if url.endswith("/git/refs/heads/work/example"):
            return None, {}
        if "/branches?" in url:
            return [{"name": name} for name in (
                "main", "research/ccts-human-ai-learning-lane",
                "research/embodiment-lane", "research/legacy-uncertainty-hold",
            )], {}
        if "/pulls?" in url:
            return [], {}
        raise AssertionError(url)

    monkeypatch.setattr(gate, "_request_json", api)
    monkeypatch.setenv("GITHUB_TOKEN", "test-only")
    result = gate.main(["--delete-closed-pr-head", "work/example", "--expected-head", "a" * 40])
    assert result == 10
    assert '"status": "HOLD"' in capsys.readouterr().out
    assert not [call for call in requests if call[0] == "DELETE"]

import json
from pathlib import Path

import pytest


def preserved_evidence():
    return {
        "pr_disposition": "CLOSED_UNMERGED",
        "history_value_known": True,
        "all_commits_reachable": False,
        "unique_history_present": True,
        "preservation_ref": "refs/tags/archive/branch-heads/pr-264/" + "a" * 40,
        "preservation_exact_sha": "a" * 40,
        "preservation_exact_sha_verified": True,
        "reconstruction_ref": "bundle:sha256:" + "c" * 64,
        "reconstruction_verified": True,
        "verification_ref": "verification:sha256:" + "d" * 64,
    }


def policy():
    return gate.load_policy(Path(gate.DEFAULT_POLICY))


@pytest.mark.parametrize("field,value", [
    ("pr_disposition", "OPEN"),
    ("pr_disposition", "UNKNOWN"),
    ("history_value_known", False),
    ("history_value_known", "true"),
    ("unique_history_present", None),
    ("preservation_ref", ""),
    ("preservation_exact_sha", "b" * 40),
    ("preservation_exact_sha_verified", False),
    ("reconstruction_ref", ""),
    ("reconstruction_verified", False),
    ("verification_ref", ""),
    ("all_commits_reachable", "true"),
])
def test_missing_or_false_retirement_evidence_is_hold(field, value):
    evidence = preserved_evidence()
    evidence[field] = value
    result = gate.assess_retirement_evidence(policy(), "work/example", "a" * 40, "a" * 40, evidence)
    assert result["status"] == "HOLD"
    assert result["preservation_readiness"] != "READY"
    assert result["deletion_authority"] == "NONE"
    assert result["mutation_performed"] is False


@pytest.mark.parametrize("source", [
    "prompt", "recommendation", "agent_self_report", "ui_state", "handoff",
    "workflow_event", "historical_verification", "ci_success", "merge_receipt",
    "stale_human_approval", "fresh_human_approval",
])
def test_no_self_declared_source_can_promote_delete_authority(source):
    evidence = preserved_evidence()
    evidence["deletion_authority_ref"] = source
    evidence["branch_delete_authority"] = "GRANTED"
    result = gate.assess_retirement_evidence(policy(), "work/example", "a" * 40, "a" * 40, evidence)
    assert result["status"] == "HOLD"
    assert result["deletion_authority"] == "NONE"
    assert result["mutation_performed"] is False


@pytest.mark.parametrize("disposition", ["MERGED", "CLOSED_UNMERGED"])
def test_complete_preservation_is_readiness_not_delete_authority(disposition):
    evidence = preserved_evidence()
    evidence["pr_disposition"] = disposition
    result = gate.assess_retirement_evidence(policy(), "work/example", "a" * 40, "a" * 40, evidence)
    assert result["preservation_readiness"] == "READY"
    assert result["status"] == "HOLD"
    assert result["deletion_authority"] == "NONE"
    assert result["mutation_performed"] is False


@pytest.mark.parametrize("branch,live", [("main", "a" * 40), ("work/example", "b" * 40)])
def test_durable_or_moved_head_holds_even_with_complete_preservation(branch, live):
    result = gate.assess_retirement_evidence(policy(), branch, "a" * 40, live, preserved_evidence())
    assert result["status"] == "HOLD"
    assert result["preservation_readiness"] == "HOLD"


@pytest.mark.parametrize("payload", [None, [], {}, {"state": "closed", "merged": "false"}])
def test_malformed_pr_live_read_holds_without_mutation(monkeypatch, capsys, payload):
    calls = []
    def api(url, token, method="GET"):
        calls.append(method)
        return payload, {}
    monkeypatch.setattr(gate, "_request_json", api)
    assert gate.main(["--assess-closed-pr", "264", "--expected-head", "a" * 40,
                      "--branch", "work/example"]) == 10
    assert json.loads(capsys.readouterr().out)["status"] == "HOLD"
    assert set(calls) <= {"GET"}


@pytest.mark.parametrize("exception", [
    OSError("permission denied"), gate.BranchTopologyError("API lookup failed"),
    json.JSONDecodeError("bad payload", "", 0),
])
def test_api_failure_holds_without_mutation(monkeypatch, capsys, exception):
    calls = []
    def api(url, token, method="GET"):
        calls.append(method)
        raise exception
    monkeypatch.setattr(gate, "_request_json", api)
    assert gate.main(["--assess-closed-pr", "264", "--expected-head", "a" * 40,
                      "--branch", "work/example"]) == 10
    assert json.loads(capsys.readouterr().out)["status"] == "HOLD"
    assert set(calls) <= {"GET"}


@pytest.mark.parametrize("merged", [False, True])
def test_live_assessment_classifies_disposition_and_verifies_archive_read_only(monkeypatch, capsys, merged):
    calls = []
    repo = "maker-luder/aion-governance-framework"
    def api(url, token, method="GET"):
        calls.append((method, url))
        if url.endswith("/pulls/264"):
            return {"number": 264, "state": "closed", "merged": merged,
                    "head": {"ref": "work/example", "sha": "a" * 40, "repo": {"full_name": repo}}}, {}
        if "/branches/" in url:
            return {"commit": {"sha": "a" * 40}}, {}
        if "/git/ref/tags/" in url:
            return {"ref": "refs/tags/archive/branch-heads/pr-264/" + "a" * 40,
                    "object": {"type": "commit", "sha": "a" * 40}}, {}
        if "/compare/" in url:
            return {"status": "identical", "behind_by": 0,
                    "base_commit": {"sha": "a" * 40},
                    "merge_base_commit": {"sha": "a" * 40}}, {}
        raise AssertionError(url)
    monkeypatch.setattr(gate, "_request_json", api)
    assert gate.main(["--assess-closed-pr", "264", "--expected-head", "a" * 40,
                      "--branch", "work/example"]) == 10
    result = json.loads(capsys.readouterr().out)
    assert result["evidence"]["pr_disposition"] == ("MERGED" if merged else "CLOSED_UNMERGED")
    assert result["evidence"]["preservation_exact_sha_verified"] is True
    assert result["evidence"]["all_commits_reachable"] is True
    assert result["deletion_authority"] == "NONE"
    assert result["status"] == "HOLD"
    assert all(method == "GET" for method, _ in calls)


def test_http_transport_rejects_delete_even_if_called_directly(monkeypatch):
    calls = []
    monkeypatch.setattr(gate, "urlopen", lambda *a, **k: calls.append(a))
    with pytest.raises(gate.BranchTopologyError, match="read-only"):
        gate._request_json("https://api.github.com/repos/o/r/git/refs/heads/work/x", "test", "DELETE")
    assert calls == []

@pytest.mark.parametrize("archive", [
    None, {}, {"ref": "wrong", "object": {"type": "commit", "sha": "a" * 40}},
    {"ref": "refs/tags/archive/branch-heads/pr-264/" + "a" * 40,
     "object": {"type": "commit", "sha": "b" * 40}},
    {"ref": "refs/tags/archive/branch-heads/pr-264/" + "a" * 40,
     "object": {"type": "tag", "sha": "a" * 40}},
])
def test_archive_missing_collision_or_wrong_sha_holds_before_any_write(monkeypatch, capsys, archive):
    calls = []
    repo = "maker-luder/aion-governance-framework"
    def api(url, token, method="GET"):
        calls.append((method, url))
        if url.endswith("/pulls/264"):
            return {"number": 264, "state": "closed", "merged": False,
                    "head": {"ref": "work/example", "sha": "a" * 40, "repo": {"full_name": repo}}}, {}
        if "/branches/" in url:
            return {"commit": {"sha": "a" * 40}}, {}
        if "/compare/" in url:
            return {"status": "identical", "behind_by": 0,
                    "base_commit": {"sha": "a" * 40},
                    "merge_base_commit": {"sha": "a" * 40}}, {}
        if "/git/ref/tags/" in url:
            return archive, {}
        raise AssertionError(url)
    monkeypatch.setattr(gate, "_request_json", api)
    assert gate.main(["--assess-closed-pr", "264", "--branch", "work/example",
                      "--expected-head", "a" * 40]) == 10
    assert json.loads(capsys.readouterr().out)["status"] == "HOLD"
    assert all(method == "GET" for method, _ in calls)


def test_moved_live_branch_stops_assessment_before_archive_or_deletion(monkeypatch, capsys):
    calls = []
    repo = "maker-luder/aion-governance-framework"
    def api(url, token, method="GET"):
        calls.append((method, url))
        if url.endswith("/pulls/264"):
            return {"number": 264, "state": "closed", "merged": False,
                    "head": {"ref": "work/example", "sha": "a" * 40, "repo": {"full_name": repo}}}, {}
        if "/branches/" in url:
            return {"commit": {"sha": "b" * 40}}, {}
        raise AssertionError(url)
    monkeypatch.setattr(gate, "_request_json", api)
    assert gate.main(["--assess-closed-pr", "264", "--branch", "work/example",
                      "--expected-head", "a" * 40]) == 10
    assert "moved" in json.loads(capsys.readouterr().out)["error"]
    assert len(calls) == 2
    assert all(method == "GET" for method, _ in calls)



