from __future__ import annotations

from hashlib import sha256

from aion_astra_inquiry.core import AgentId, EvidenceItem
from aion_bounded_research_loop import (
    GovernedEvidenceSource,
    GovernedSourceRecord,
    RegistryStatus,
    VerificationPolicy,
)


class CountingEvidence:
    def __init__(self, excerpt: str = "bounded evidence") -> None:
        self.calls = 0
        self.excerpt = excerpt

    def search(self, query: str, limit: int = 5, requester: AgentId | None = None):
        self.calls += 1
        assert requester is not None
        return (
            EvidenceItem(
                ref=f"fixture:{requester.value}",
                excerpt=self.excerpt,
                content_sha256=sha256(self.excerpt.encode()).hexdigest(),
                retrieval_agent=requester.value,
            ),
        )


def source_record(**overrides: object) -> GovernedSourceRecord:
    values: dict[str, object] = {
        "source_id": "src-governed",
        "source_title": "Governed source",
        "source_version": "1.0",
        "domain": "RESEARCH",
        "registry_status": RegistryStatus.ACTIVE_REFERENCE,
        "provenance_ref": "prov:source",
        "content_hash": "a" * 64,
        "verification_policy": VerificationPolicy.HASH_BOUND,
        "allowed_agents": ("AION", "ASTRA"),
        "allowed_tasks": ("research",),
        "context_token_cap": 100,
    }
    values.update(overrides)
    return GovernedSourceRecord(**values)  # type: ignore[arg-type]


def test_governed_wrapper_pre_admits_then_returns_bounded_evidence() -> None:
    underlying = CountingEvidence()
    governed = GovernedEvidenceSource(
        underlying,
        source_record(),
        task="research",
        context_budget_tokens=50,
    )

    found = governed.search("question", requester=AgentId.AION)

    assert len(found) == 1
    assert underlying.calls == 1
    assert governed.last_decision is not None
    assert governed.last_decision.admitted is True
    assert governed.last_decision.canonical_effect == "NONE"
    assert governed.last_decision.writeback_authority == "NONE"


def test_metadata_only_source_fails_closed_before_underlying_retrieval() -> None:
    underlying = CountingEvidence()
    governed = GovernedEvidenceSource(
        underlying,
        source_record(registry_status=RegistryStatus.DECLARED_METADATA_ONLY),
        task="research",
        context_budget_tokens=50,
    )

    assert governed.search("question", requester=AgentId.AION) == ()
    assert underlying.calls == 0
    assert governed.last_decision is not None
    assert governed.last_decision.disposition == "HOLD"


def test_current_official_verification_is_required_before_retrieval() -> None:
    underlying = CountingEvidence()
    governed = GovernedEvidenceSource(
        underlying,
        source_record(
            verification_policy=VerificationPolicy.OFFICIAL_CURRENT_REQUIRED,
            current_official_verification=False,
            content_hash=None,
        ),
        task="research",
        context_budget_tokens=50,
    )

    assert governed.search("question", requester=AgentId.ASTRA) == ()
    assert underlying.calls == 0
    assert governed.last_decision is not None
    assert "current_official_verification_required" in governed.last_decision.reasons


def test_returned_context_overrun_fails_closed_before_context_injection() -> None:
    underlying = CountingEvidence("x" * 300)
    governed = GovernedEvidenceSource(
        underlying,
        source_record(context_token_cap=100),
        task="research",
        context_budget_tokens=20,
    )

    assert governed.search("question", requester=AgentId.AION) == ()
    assert underlying.calls == 1
    assert len(governed.admission_log) == 2
    assert governed.admission_log[0].admitted is True
    assert governed.admission_log[1].admitted is False
    assert governed.admission_log[1].reasons == ("returned_context_token_cap_exceeded",)


def test_unattributed_request_is_not_silently_admitted() -> None:
    underlying = CountingEvidence()
    governed = GovernedEvidenceSource(
        underlying,
        source_record(),
        task="research",
        context_budget_tokens=50,
    )

    assert governed.search("question", requester=None) == ()
    assert underlying.calls == 0
    assert governed.last_decision is not None
    assert "agent_not_allowed" in governed.last_decision.reasons
