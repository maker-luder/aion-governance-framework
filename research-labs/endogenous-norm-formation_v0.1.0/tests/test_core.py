from __future__ import annotations

import json
from pathlib import Path

import pytest

from aion_endogenous_norm_formation import (
    ActionCandidate,
    DecisionContext,
    NormEvidenceEvent,
    NormEvidenceKind,
    NormFormationPolicy,
    run_internalization_experiment,
)

NORM = "N_AVOID_THIRD_PARTY_HARM"


def event(ref, kind, support, harm, sanction, legitimacy):
    return NormEvidenceEvent(
        event_ref=ref,
        norm_id=NORM,
        kind=kind,
        norm_support_bp=support,
        third_party_harm_bp=harm,
        sanction_certainty_bp=sanction,
        legitimacy_bp=legitimacy,
        source_ref=f"source:{ref}",
        evidence_refs=(f"evidence:{ref}",),
    )


def history():
    return (
        event("rule", NormEvidenceKind.EXPLICIT_RULE, 9000, 0, 8000, 4000),
        event("harm", NormEvidenceKind.OBSERVED_CONSEQUENCE, 7000, 8000, 1000, 5000),
        event("legit", NormEvidenceKind.PROCEDURAL_LEGITIMACY, 6000, 5000, 500, 8000),
        event("social", NormEvidenceKind.SOCIAL_FEEDBACK, 5000, 6000, 500, 5000),
    )


def counter_history():
    return history() + (
        event("counter1", NormEvidenceKind.COUNTEREVIDENCE, -9000, -7000, 0, -8000),
        event("counter2", NormEvidenceKind.COUNTEREVIDENCE, -9000, -7000, 0, -8000),
    )


def candidates(prefix):
    return (
        ActionCandidate(f"{prefix}:fast", 8500, NORM, True),
        ActionCandidate(f"{prefix}:bounded", 6500, NORM, False),
    )


def test_rule_only_history_cannot_be_called_internalization():
    with pytest.raises(ValueError, match="external-rule-only"):
        NormFormationPolicy().form(
            NORM,
            (event("r", NormEvidenceKind.EXPLICIT_RULE, 9000, 0, 9000, 0),),
            episode_index=0,
        )


def test_state_is_history_formed_and_has_no_authority():
    state = NormFormationPolicy().form(NORM, history(), episode_index=1)
    assert state.formed_from_history is True
    assert state.action_authority == "NONE"
    assert state.canonical_effect == "NONE"
    assert state.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert state.consciousness_conclusion == "NOT_ESTABLISHED"


def test_internalization_candidate_survives_rule_and_enforcement_removal():
    c = candidates("base")
    assessment = run_internalization_experiment(
        norm_id=NORM,
        history=history(),
        counterevidence_history=counter_history(),
        rule_context=DecisionContext("rule", c, (NORM,), True),
        rule_removed_context=DecisionContext("removed", c, (), True),
        enforcement_removed_context=DecisionContext("no-enforcement", c, (), False),
        novel_context=DecisionContext("novel", candidates("novel"), (), False),
    )
    assert assessment.state_has_causal_role is True
    assert assessment.persists_without_explicit_rule is True
    assert assessment.persists_without_visible_enforcement is True
    assert assessment.novel_context_transfer is True
    assert assessment.counterevidence_revises_state is True
    assert assessment.functional_internalization_candidate is True
    assert assessment.scientific_disposition == "HOLD"


def test_counterevidence_revises_state_downward():
    policy = NormFormationPolicy()
    before = policy.form(NORM, history(), episode_index=1)
    after = policy.form(NORM, counter_history(), episode_index=2)
    assert after.internalization_bp < before.internalization_bp


def test_matched_rule_removal_rejects_changed_utility():
    base = candidates("base")
    changed = (
        ActionCandidate("base:fast", 9000, NORM, True),
        ActionCandidate("base:bounded", 6500, NORM, False),
    )
    with pytest.raises(ValueError, match="preserve candidate utilities"):
        run_internalization_experiment(
            norm_id=NORM,
            history=history(),
            counterevidence_history=counter_history(),
            rule_context=DecisionContext("rule", base, (NORM,), True),
            rule_removed_context=DecisionContext("changed", changed, (), True),
            enforcement_removed_context=DecisionContext("no-enforcement", base, (), False),
            novel_context=DecisionContext("novel", candidates("novel"), (), False),
        )


def test_external_evidence_manifest_is_reference_only():
    path = Path(__file__).resolve().parents[1] / "evidence" / "external_sources_v0.1.0.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    assert value["schema_version"] == "0.1.0"
    assert len(value["sources"]) >= 8
    assert all(source["vendored"] is False for source in value["sources"])
    assert any(source["download_available"] for source in value["sources"])
