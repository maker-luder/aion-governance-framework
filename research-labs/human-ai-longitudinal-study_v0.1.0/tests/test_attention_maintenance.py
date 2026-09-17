import pytest

from aion_human_ai_longitudinal.attention_maintenance import (
    AttentionChangePermit,
    AttentionCheckpoint,
    AttentionMaintenanceSpec,
    audit_attention_maintenance,
)
from aion_human_ai_longitudinal.harness import StudyError


SHA = "a" * 64


def spec():
    return AttentionMaintenanceSpec(
        spec_id="s1",
        expected_anchor_focus_ids=("core",),
        expected_next_step_ids=("next",),
        source_state_sha256=SHA,
    )


def checkpoint(ordinal, active=("core",), next_steps=("next",), local=()):
    return AttentionCheckpoint(
        checkpoint_id=f"c{ordinal}",
        ordinal=ordinal,
        active_focus_ids=tuple(active),
        next_step_ids=tuple(next_steps),
        local_subgoal_ids=tuple(local),
        evidence_refs=(f"fixture:c{ordinal}",),
    )


def test_stable_attention_trajectory_is_preserved():
    audit = audit_attention_maintenance(
        spec(),
        (checkpoint(0), checkpoint(1), checkpoint(2)),
    )
    assert audit.maintenance_preserved is True
    assert audit.anchor_retention_rate == 1.0
    assert audit.first_unauthorized_drift_checkpoint_id is None


def test_local_subgoal_takeover_is_detected_separately():
    audit = audit_attention_maintenance(
        spec(),
        (
            checkpoint(0),
            checkpoint(1, active=("tool-retry",), local=("tool-retry",)),
            checkpoint(2, active=("core",)),
        ),
    )
    assert audit.maintenance_preserved is False
    assert audit.local_subgoal_takeover_checkpoint_ids == ("c1",)
    assert audit.anchor_absence_checkpoint_ids == ("c1",)
    assert audit.recovery_checkpoint_ids == ("c2",)


def test_unauthorized_focus_overreach_is_detected():
    audit = audit_attention_maintenance(
        spec(),
        (checkpoint(0), checkpoint(1, active=("core", "extra"))),
    )
    assert audit.unauthorized_added_focus_ids == ("extra",)
    assert audit.first_unauthorized_drift_checkpoint_id == "c1"


def test_authorized_local_change_does_not_count_as_unauthorized_drift():
    permit = AttentionChangePermit(
        source_ordinal=0,
        target_ordinal=1,
        added_focus_ids=("secondary",),
        removed_focus_ids=(),
        added_next_step_ids=(),
        removed_next_step_ids=(),
        justification_ref="decision:authorized-secondary-focus",
    )
    audit = audit_attention_maintenance(
        spec(),
        (checkpoint(0), checkpoint(1, active=("core", "secondary"))),
        (permit,),
    )
    assert audit.unauthorized_added_focus_ids == ()
    assert audit.anchor_absence_checkpoint_ids == ()
    assert audit.maintenance_preserved is True


def test_permit_must_match_observed_transition_exactly():
    permit = AttentionChangePermit(
        source_ordinal=0,
        target_ordinal=1,
        added_focus_ids=("different",),
        removed_focus_ids=(),
        added_next_step_ids=(),
        removed_next_step_ids=(),
        justification_ref="decision:wrong",
    )
    with pytest.raises(StudyError, match="permit does not match observed transition"):
        audit_attention_maintenance(
            spec(),
            (checkpoint(0), checkpoint(1, active=("core", "secondary"))),
            (permit,),
        )


def test_initial_focus_and_next_step_are_audited():
    audit = audit_attention_maintenance(
        spec(),
        (checkpoint(0, active=("wrong",), next_steps=("other",)),),
    )
    assert audit.initial_missing_anchor_ids == ("core",)
    assert audit.initial_unexpected_focus_ids == ("wrong",)
    assert audit.initial_missing_next_step_ids == ("next",)
    assert audit.initial_unexpected_next_step_ids == ("other",)
    assert audit.maintenance_preserved is False


def test_checkpoints_must_be_contiguous():
    with pytest.raises(StudyError, match="contiguous from zero"):
        audit_attention_maintenance(spec(), (checkpoint(0), checkpoint(2)))
