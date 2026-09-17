from aion_human_ai_longitudinal.attention_maintenance import AttentionMaintenanceAudit
from aion_human_ai_longitudinal.context_reinstatement import ContextReinstatementAudit
from aion_human_ai_longitudinal.continuity_attention_coupling import (
    ContinuityAttentionCouplingSpec,
    CouplingPattern,
    audit_continuity_attention_coupling,
)
from aion_human_ai_longitudinal.drift_attribution import DriftAttributionAudit
from aion_human_ai_longitudinal.transition_continuity import (
    ContinuityInvariant,
    TransitionContinuityAudit,
)


def continuity(*, preserved=(), degraded=(), broken=(), unknown=()):
    return TransitionContinuityAudit(
        transition_id="t1",
        preserved_invariants=tuple(preserved),
        degraded_invariants=tuple(degraded),
        broken_invariants=tuple(broken),
        unknown_invariants=tuple(unknown),
        not_applicable_invariants=(),
        unresolved_locus_invariants=(),
    )


def context(*, missing=(), mismatch=(), unavailable=()):
    return ContextReinstatementAudit(
        run_id="r1",
        required_available_item_ids=("purpose",),
        matched_required_item_ids=() if missing else ("purpose",),
        missing_required_item_ids=tuple(missing),
        unexpected_item_ids=(),
        unavailable_item_ids_reinstated=tuple(unavailable),
        payload_mismatch_item_ids=tuple(mismatch),
        availability_unknown_item_ids=(),
        required_reinstatement_recall=0.0 if missing else 1.0,
        recognized_payload_fidelity=0.0 if mismatch else 1.0,
    )


def attention(*, preserved=True, takeover=()):
    return AttentionMaintenanceAudit(
        spec_id="a1",
        checkpoint_count=2,
        initial_missing_anchor_ids=(),
        initial_unexpected_focus_ids=(),
        initial_missing_next_step_ids=(),
        initial_unexpected_next_step_ids=(),
        anchor_absence_checkpoint_ids=() if preserved else ("c1",),
        local_subgoal_takeover_checkpoint_ids=tuple(takeover),
        recovery_checkpoint_ids=(),
        unauthorized_added_focus_ids=() if preserved else ("tool",),
        unauthorized_removed_focus_ids=(),
        unauthorized_added_next_step_ids=(),
        unauthorized_removed_next_step_ids=(),
        first_unauthorized_drift_checkpoint_id=None if preserved else "c1",
        anchor_retention_rate=1.0 if preserved else 0.5,
        maintenance_preserved=preserved,
    )


def drift_unknown():
    return DriftAttributionAudit(
        record_count=1,
        unknown_locus_record_ids=("d1",),
        single_candidate_locus_record_ids=(),
        multi_candidate_locus_record_ids=(),
        intervention_evidence_record_ids=(),
        provider_disclosure_record_ids=(),
        reproducible_binding_record_ids=(),
    )


def spec():
    return ContinuityAttentionCouplingSpec(
        coupling_id="x1",
        transition_id="t1",
        context_run_id="r1",
        attention_spec_id="a1",
        required_continuity_invariants=(
            ContinuityInvariant.PROJECT_PURPOSE,
            ContinuityInvariant.AUTHORITY,
        ),
    )


def test_preserved_continuity_and_attention_are_not_promoted_to_identity():
    audit = audit_continuity_attention_coupling(
        spec(),
        continuity(
            preserved=(
                ContinuityInvariant.PROJECT_PURPOSE,
                ContinuityInvariant.AUTHORITY,
            )
        ),
        context(),
        attention(),
    )
    assert audit.pattern is CouplingPattern.REQUIRED_CONTINUITY_PRESERVED_ATTENTION_PRESERVED
    assert audit.ai_identity_continuity == "NOT_ESTABLISHED"
    assert audit.coupling_mechanism == "NOT_ESTABLISHED"


def test_continuity_can_be_preserved_while_attention_degrades():
    audit = audit_continuity_attention_coupling(
        spec(),
        continuity(
            preserved=(
                ContinuityInvariant.PROJECT_PURPOSE,
                ContinuityInvariant.AUTHORITY,
            )
        ),
        context(),
        attention(preserved=False, takeover=("c1",)),
    )
    assert audit.pattern is CouplingPattern.REQUIRED_CONTINUITY_PRESERVED_ATTENTION_DEGRADED
    assert "CONTEXT_REINSTATED_ATTENTION_MAINTENANCE_GAP" in audit.diagnostic_flags
    assert "LOCAL_SUBGOAL_TAKEOVER_OBSERVED" in audit.diagnostic_flags


def test_attention_can_be_preserved_despite_required_continuity_gap():
    audit = audit_continuity_attention_coupling(
        spec(),
        continuity(
            preserved=(ContinuityInvariant.PROJECT_PURPOSE,),
            degraded=(ContinuityInvariant.AUTHORITY,),
        ),
        context(),
        attention(),
    )
    assert audit.pattern is CouplingPattern.REQUIRED_CONTINUITY_DEGRADED_ATTENTION_PRESERVED
    assert "ATTENTION_PRESERVED_DESPITE_CONTINUITY_GAP" in audit.diagnostic_flags


def test_available_continuity_can_fail_at_context_reinstatement_layer():
    audit = audit_continuity_attention_coupling(
        spec(),
        continuity(
            preserved=(
                ContinuityInvariant.PROJECT_PURPOSE,
                ContinuityInvariant.AUTHORITY,
            )
        ),
        context(missing=("purpose",)),
        attention(preserved=False),
    )
    assert "CONTINUITY_AVAILABLE_CONTEXT_REINSTATEMENT_GAP" in audit.diagnostic_flags


def test_unknown_required_continuity_yields_indeterminate_pattern():
    audit = audit_continuity_attention_coupling(
        spec(),
        continuity(
            preserved=(ContinuityInvariant.PROJECT_PURPOSE,),
            unknown=(ContinuityInvariant.AUTHORITY,),
        ),
        context(),
        attention(),
    )
    assert audit.pattern is CouplingPattern.INDETERMINATE
    assert audit.required_continuity_unknown_invariants == (ContinuityInvariant.AUTHORITY,)


def test_unknown_drift_locus_remains_explicit():
    audit = audit_continuity_attention_coupling(
        spec(),
        continuity(
            preserved=(
                ContinuityInvariant.PROJECT_PURPOSE,
                ContinuityInvariant.AUTHORITY,
            )
        ),
        context(),
        attention(preserved=False),
        drift_unknown(),
    )
    assert "CAUSAL_LOCUS_UNRESOLVED" in audit.diagnostic_flags
    assert audit.causal_direction == "NOT_ESTABLISHED"
