import pytest

from iqc_capa import CapaError, CapaLedger, Issue, IssueState


def issue():
    return Issue("issue.001", "Example finding", "medium", "qa-owner", ("qa.test.001",))


def test_evidence_linked_lifecycle_and_chain():
    ledger = CapaLedger()
    ledger.open_issue(issue())
    ledger.transition("issue.001", IssueState.INVESTIGATING, actor="qa", occurred_at="2026-08-13T00:00:00Z")
    ledger.transition("issue.001", IssueState.CORRECTIVE_ACTION, actor="owner", occurred_at="2026-08-13T00:01:00Z", evidence_refs=("repair.commit.001",))
    ledger.transition("issue.001", IssueState.VERIFIED, actor="teacher", occurred_at="2026-08-13T00:02:00Z", evidence_refs=("qa.run.001",))
    ledger.transition("issue.001", IssueState.CLOSED, actor="owner", occurred_at="2026-08-13T00:03:00Z", evidence_refs=("review.signoff.001",))
    assert ledger.get("issue.001").state is IssueState.CLOSED
    assert ledger.validate_chain() == ()
    assert ledger.snapshot()["canonical_effect"] == "NONE"


def test_verification_and_closure_require_evidence():
    ledger = CapaLedger()
    ledger.open_issue(issue())
    ledger.transition("issue.001", IssueState.INVESTIGATING, actor="qa", occurred_at="2026-08-13T00:00:00Z")
    ledger.transition("issue.001", IssueState.CORRECTIVE_ACTION, actor="owner", occurred_at="2026-08-13T00:01:00Z")
    with pytest.raises(CapaError, match="evidence is required"):
        ledger.transition("issue.001", IssueState.VERIFIED, actor="teacher", occurred_at="2026-08-13T00:02:00Z")


def test_invalid_transition_and_secret_path_fail_closed():
    ledger = CapaLedger()
    ledger.open_issue(issue())
    with pytest.raises(CapaError, match="invalid transition"):
        ledger.transition("issue.001", IssueState.CLOSED, actor="qa", occurred_at="2026-08-13T00:00:00Z", evidence_refs=("qa.001",))
    with pytest.raises(CapaError, match="secret-like"):
        ledger.transition("issue.001", IssueState.INVESTIGATING, actor="qa", occurred_at="2026-08-13T00:00:00Z", evidence_refs=("api_key.txt",))


def test_issue_boundary_and_duplicate_fail_closed():
    ledger = CapaLedger()
    with pytest.raises(CapaError, match="governance"):
        ledger.open_issue(Issue("bad", "bad", "high", "qa", canonical_effect="WRITE"))
    ledger.open_issue(issue())
    with pytest.raises(CapaError, match="unique"):
        ledger.open_issue(issue())
