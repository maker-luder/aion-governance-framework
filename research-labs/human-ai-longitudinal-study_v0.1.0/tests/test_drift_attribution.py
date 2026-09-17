import pytest

from aion_human_ai_longitudinal.drift_attribution import (
    DriftAttributionRecord,
    DriftKind,
    audit_drift_attribution,
)
from aion_human_ai_longitudinal.harness import StudyError
from aion_human_ai_longitudinal.transition_continuity import TransitionChangeLocus


def record(**overrides):
    values = {
        "drift_id": "d1",
        "source_checkpoint_id": "c0",
        "target_checkpoint_id": "c1",
        "kind": DriftKind.LOCAL_SUBGOAL_TAKEOVER,
        "candidate_loci": (TransitionChangeLocus.UNKNOWN,),
        "evidence_refs": ("fixture:d1",),
    }
    values.update(overrides)
    return DriftAttributionRecord(**values)


def test_unknown_locus_is_retained_without_causal_promotion():
    audit = audit_drift_attribution((record(),))
    assert audit.unknown_locus_record_ids == ("d1",)
    assert audit.causal_identification == "NOT_ESTABLISHED"
    assert audit.model_capability_ordering == "NOT_ESTABLISHED"


def test_multiple_candidate_loci_are_not_collapsed():
    audit = audit_drift_attribution(
        (
            record(
                candidate_loci=(
                    TransitionChangeLocus.CONTEXT_SELECTION,
                    TransitionChangeLocus.HARNESS,
                ),
            ),
        )
    )
    assert audit.multi_candidate_locus_record_ids == ("d1",)


def test_unknown_cannot_be_mixed_with_named_loci():
    with pytest.raises(StudyError, match="UNKNOWN locus must be the sole"):
        record(
            candidate_loci=(
                TransitionChangeLocus.UNKNOWN,
                TransitionChangeLocus.MODEL,
            )
        )


def test_structural_record_cannot_claim_causal_identification():
    with pytest.raises(StudyError, match="cannot claim causal identification"):
        record(claims_causal_identification=True)


def test_evidence_route_flags_remain_descriptive_only():
    audit = audit_drift_attribution(
        (
            record(
                candidate_loci=(TransitionChangeLocus.SYSTEM_POLICY,),
                direct_intervention_evidence=True,
                provider_disclosure_evidence=True,
                reproducible_binding_evidence=True,
            ),
        )
    )
    assert audit.single_candidate_locus_record_ids == ("d1",)
    assert audit.intervention_evidence_record_ids == ("d1",)
    assert audit.provider_disclosure_record_ids == ("d1",)
    assert audit.reproducible_binding_record_ids == ("d1",)
    assert audit.causal_identification == "NOT_ESTABLISHED"


def test_drift_ids_must_be_unique():
    with pytest.raises(StudyError, match="drift_id values must be unique"):
        audit_drift_attribution((record(), record()))
