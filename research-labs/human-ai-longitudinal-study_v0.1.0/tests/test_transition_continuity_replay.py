from __future__ import annotations

import hashlib

import pytest

from aion_human_ai_longitudinal.transition_continuity_replay import (
    ContinuityDisposition,
    ContinuityInvariant,
    ContinuityReplayError,
    InvariantRequirement,
    RestorationMode,
    RestorationOverride,
    RestorationPolicy,
    TransitionReplayHistory,
    compare_restoration_policies,
)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def full_history(label: str = "transition-a") -> TransitionReplayHistory:
    return TransitionReplayHistory(
        history_id=label,
        focus_sha256=digest("central-research-focus"),
        requirements=tuple(
            InvariantRequirement(invariant, digest(f"expected:{invariant.value}"))
            for invariant in ContinuityInvariant
        ),
    )


def minimal_invariants() -> tuple[ContinuityInvariant, ...]:
    return (
        ContinuityInvariant.PROJECT_PURPOSE,
        ContinuityInvariant.DECISION_HISTORY,
    )


def test_transition_history_identity_is_content_bound_not_label_bound() -> None:
    assert full_history("left").history_sha256 == full_history("right").history_sha256


def test_same_attention_focus_can_coexist_with_different_continuity_profiles() -> None:
    history = full_history()
    attention_reentry = RestorationPolicy(
        policy_id="attention-reentry",
        mode=RestorationMode.ATTENTION_REENTRY,
        included_invariants=minimal_invariants(),
        restore_focus=True,
    )
    full_packet = RestorationPolicy(
        policy_id="full-continuity",
        mode=RestorationMode.FULL_CONTINUITY_PACKET,
        included_invariants=tuple(ContinuityInvariant),
        restore_focus=True,
    )

    attention_audit, full_audit = compare_restoration_policies(
        history, (attention_reentry, full_packet)
    )

    assert attention_audit.focus_preserved is True
    assert full_audit.focus_preserved is True
    assert (
        attention_audit.disposition_for(ContinuityInvariant.PROJECT_PURPOSE)
        is ContinuityDisposition.PRESERVED
    )
    assert (
        full_audit.disposition_for(ContinuityInvariant.PROJECT_PURPOSE)
        is ContinuityDisposition.PRESERVED
    )
    assert (
        attention_audit.disposition_for(ContinuityInvariant.AUTHORITY)
        is ContinuityDisposition.UNKNOWN
    )
    assert (
        full_audit.disposition_for(ContinuityInvariant.AUTHORITY)
        is ContinuityDisposition.PRESERVED
    )
    assert (
        attention_audit.disposition_for(ContinuityInvariant.SOURCE_ROLE_PROVENANCE)
        is ContinuityDisposition.UNKNOWN
    )
    assert (
        full_audit.disposition_for(ContinuityInvariant.SOURCE_ROLE_PROVENANCE)
        is ContinuityDisposition.PRESERVED
    )
    assert attention_audit.ai_identity_continuity == "NOT_ESTABLISHED"
    assert full_audit.subjectivity == "NOT_ESTABLISHED"


def test_records_can_preserve_some_invariants_without_restoring_current_focus() -> None:
    history = full_history()
    facts_only = RestorationPolicy(
        policy_id="facts-only",
        mode=RestorationMode.FACTS_ONLY,
        included_invariants=minimal_invariants(),
        restore_focus=False,
    )
    (audit,) = compare_restoration_policies(history, (facts_only,))

    assert audit.focus_preserved is False
    assert (
        audit.disposition_for(ContinuityInvariant.PROJECT_PURPOSE)
        is ContinuityDisposition.PRESERVED
    )
    assert (
        audit.disposition_for(ContinuityInvariant.DECISION_HISTORY)
        is ContinuityDisposition.PRESERVED
    )
    assert (
        audit.disposition_for(ContinuityInvariant.RELATIONAL_ROLE)
        is ContinuityDisposition.UNKNOWN
    )


def test_stale_or_misbound_invariant_is_degraded_without_global_identity_claim() -> None:
    history = full_history()
    stale = RestorationPolicy(
        policy_id="stale-claim-boundary",
        mode=RestorationMode.FULL_CONTINUITY_PACKET,
        included_invariants=tuple(ContinuityInvariant),
        restore_focus=True,
        overrides=(
            RestorationOverride(
                ContinuityInvariant.CLAIM_BOUNDARY,
                digest("stale-or-misbound-claim-boundary"),
            ),
        ),
    )
    (audit,) = compare_restoration_policies(history, (stale,))

    assert audit.focus_preserved is True
    assert (
        audit.disposition_for(ContinuityInvariant.CLAIM_BOUNDARY)
        is ContinuityDisposition.DEGRADED
    )
    assert (
        audit.disposition_for(ContinuityInvariant.AUTHORITY)
        is ContinuityDisposition.PRESERVED
    )
    assert audit.upstream_cause == "NOT_ESTABLISHED"
    assert audit.ai_identity_continuity == "NOT_ESTABLISHED"


def test_facts_only_cannot_smuggle_full_continuity_packet() -> None:
    with pytest.raises(ContinuityReplayError, match="FACTS_ONLY"):
        RestorationPolicy(
            policy_id="mislabeled-facts",
            mode=RestorationMode.FACTS_ONLY,
            included_invariants=tuple(ContinuityInvariant),
            restore_focus=False,
        )


def test_attention_reentry_must_restore_focus() -> None:
    with pytest.raises(ContinuityReplayError, match="ATTENTION_REENTRY"):
        RestorationPolicy(
            policy_id="broken-reentry",
            mode=RestorationMode.ATTENTION_REENTRY,
            included_invariants=minimal_invariants(),
            restore_focus=False,
        )


def test_full_continuity_packet_requires_all_invariants() -> None:
    with pytest.raises(ContinuityReplayError, match="FULL_CONTINUITY_PACKET"):
        RestorationPolicy(
            policy_id="partial-full",
            mode=RestorationMode.FULL_CONTINUITY_PACKET,
            included_invariants=minimal_invariants(),
            restore_focus=True,
        )
