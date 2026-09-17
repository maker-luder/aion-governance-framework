import pytest

from aion_human_ai_longitudinal.harness import AdmissionDisposition, StudyError
from aion_human_ai_longitudinal.transition_continuity import (
    ContinuityInvariant,
    ContinuityInvariantObservation,
    InvariantDisposition,
    TransitionChangeLocus,
    UpstreamTransitionBinding,
    audit_transition_continuity,
)


A = "a" * 64
B = "b" * 64
COMMIT = "1" * 40


def make_binding(**overrides):
    values = {
        "transition_id": "t1",
        "before_state_sha256": A,
        "after_state_sha256": B,
        "repository_commit": COMMIT,
        "required_invariants": (
            ContinuityInvariant.PROJECT_PURPOSE,
            ContinuityInvariant.AUTHORITY,
        ),
        "evidence_refs": ("fixture:transition",),
    }
    values.update(overrides)
    return UpstreamTransitionBinding(**values)


def make_observation(invariant, disposition, **overrides):
    values = {
        "invariant": invariant,
        "disposition": disposition,
        "before_fingerprint_sha256": A,
        "after_fingerprint_sha256": A,
        "change_locus": TransitionChangeLocus.UNKNOWN,
        "evidence_refs": ("fixture:invariant",),
    }
    if disposition in {InvariantDisposition.DEGRADED, InvariantDisposition.BROKEN}:
        values["after_fingerprint_sha256"] = B
    elif disposition is InvariantDisposition.UNKNOWN:
        values["after_fingerprint_sha256"] = None
    elif disposition is InvariantDisposition.NOT_APPLICABLE:
        values["before_fingerprint_sha256"] = None
        values["after_fingerprint_sha256"] = None
    values.update(overrides)
    return ContinuityInvariantObservation(**values)


def test_transition_audit_preserves_independent_invariant_states():
    audit = audit_transition_continuity(
        make_binding(),
        (
            make_observation(
                ContinuityInvariant.PROJECT_PURPOSE,
                InvariantDisposition.PRESERVED,
                change_locus=TransitionChangeLocus.REPOSITORY,
            ),
            make_observation(
                ContinuityInvariant.AUTHORITY,
                InvariantDisposition.DEGRADED,
                change_locus=TransitionChangeLocus.SYSTEM_POLICY,
            ),
        ),
    )
    assert audit.preserved_invariants == (ContinuityInvariant.PROJECT_PURPOSE,)
    assert audit.degraded_invariants == (ContinuityInvariant.AUTHORITY,)
    assert audit.ai_identity_continuity == "NOT_ESTABLISHED"
    assert audit.scientific_disposition is AdmissionDisposition.HOLD


def test_unknown_upstream_bindings_remain_representable():
    binding = make_binding(
        model_binding_sha256=None,
        system_binding_sha256=None,
        memory_retrieval_binding_sha256=None,
    )
    assert binding.model_binding_sha256 is None
    assert binding.system_binding_sha256 is None


def test_required_invariant_coverage_fails_closed():
    with pytest.raises(StudyError, match="required invariant coverage mismatch"):
        audit_transition_continuity(
            make_binding(),
            (
                make_observation(
                    ContinuityInvariant.PROJECT_PURPOSE,
                    InvariantDisposition.PRESERVED,
                ),
            ),
        )


def test_preserved_requires_equal_fingerprints():
    with pytest.raises(StudyError, match="PRESERVED requires equal"):
        make_observation(
            ContinuityInvariant.PROJECT_PURPOSE,
            InvariantDisposition.PRESERVED,
            after_fingerprint_sha256=B,
        )


def test_degraded_requires_distinct_fingerprints():
    with pytest.raises(StudyError, match="DEGRADED/BROKEN requires distinct"):
        make_observation(
            ContinuityInvariant.AUTHORITY,
            InvariantDisposition.DEGRADED,
            after_fingerprint_sha256=A,
        )


def test_reassessment_reference_binding_is_explicit():
    observation = make_observation(
        ContinuityInvariant.AUTHORITY,
        InvariantDisposition.PRESERVED,
        explicit_reassessment=True,
        reassessment_ref="decision:new-evidence",
    )
    assert observation.explicit_reassessment is True

    with pytest.raises(StudyError, match="requires reassessment_ref"):
        make_observation(
            ContinuityInvariant.AUTHORITY,
            InvariantDisposition.PRESERVED,
            explicit_reassessment=True,
        )


def test_real_model_or_private_transition_data_is_not_admitted():
    with pytest.raises(StudyError, match="synthetic, non-private, and no-model"):
        make_binding(model_invoked=True)
    with pytest.raises(StudyError, match="synthetic, non-private, and no-model"):
        make_binding(contains_private_material=True)
