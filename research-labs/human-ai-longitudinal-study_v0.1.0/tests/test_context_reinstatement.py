import pytest

from aion_human_ai_longitudinal.context_reinstatement import (
    ContextAvailability,
    ContextItemKind,
    ContextItemState,
    ContextReinstatementObservation,
    ContextSourceManifest,
    ReinstatedContextItem,
    audit_context_reinstatement,
    digest_context_source_manifest,
)
from aion_human_ai_longitudinal.harness import StudyError


A = "a" * 64
B = "b" * 64
C = "c" * 64
COMMIT = "1" * 40


def item(
    item_id,
    *,
    kind=ContextItemKind.PROJECT_PURPOSE,
    availability=ContextAvailability.AVAILABLE,
    required=True,
    payload=A,
):
    return ContextItemState(
        item_id=item_id,
        kind=kind,
        payload_sha256=payload,
        availability=availability,
        required_for_current_task=required,
        source_refs=(f"fixture:{item_id}",),
    )


def manifest():
    return ContextSourceManifest(
        manifest_id="m1",
        source_state_sha256=C,
        repository_commit=COMMIT,
        items=(
            item("purpose"),
            item("authority", kind=ContextItemKind.AUTHORITY, payload=B),
            item(
                "history",
                kind=ContextItemKind.DECISION_HISTORY,
                availability=ContextAvailability.UNKNOWN,
                required=False,
                payload=C,
            ),
        ),
        source_refs=("fixture:manifest",),
    )


def observation(expected, reinstated):
    return ContextReinstatementObservation(
        run_id="r1",
        expected_manifest_sha256=digest_context_source_manifest(expected),
        reinstated_items=tuple(reinstated),
        retrieval_binding_sha256=None,
        context_selection_binding_sha256=None,
        evidence_refs=("fixture:observation",),
    )


def test_context_audit_separates_availability_from_reinstatement():
    expected = manifest()
    audit = audit_context_reinstatement(
        expected,
        observation(expected, (ReinstatedContextItem("purpose", A),)),
    )
    assert audit.required_available_item_ids == ("authority", "purpose")
    assert audit.matched_required_item_ids == ("purpose",)
    assert audit.missing_required_item_ids == ("authority",)
    assert audit.required_reinstatement_recall == 0.5
    assert audit.context_reinstatement_effect == "NOT_ESTABLISHED"


def test_payload_mismatch_is_not_counted_as_successful_reinstatement():
    expected = manifest()
    audit = audit_context_reinstatement(
        expected,
        observation(
            expected,
            (
                ReinstatedContextItem("purpose", B),
                ReinstatedContextItem("authority", B),
            ),
        ),
    )
    assert audit.payload_mismatch_item_ids == ("purpose",)
    assert audit.missing_required_item_ids == ("purpose",)


def test_unexpected_context_overreach_is_separate_from_missing_context():
    expected = manifest()
    audit = audit_context_reinstatement(
        expected,
        observation(
            expected,
            (
                ReinstatedContextItem("purpose", A),
                ReinstatedContextItem("authority", B),
                ReinstatedContextItem("extra", C),
            ),
        ),
    )
    assert audit.required_reinstatement_recall == 1.0
    assert audit.unexpected_item_ids == ("extra",)


def test_reinstating_declared_unavailable_item_is_flagged():
    expected = ContextSourceManifest(
        manifest_id="m2",
        source_state_sha256=C,
        repository_commit=COMMIT,
        items=(
            item(
                "unavailable",
                availability=ContextAvailability.UNAVAILABLE,
                required=False,
            ),
        ),
        source_refs=("fixture:m2",),
    )
    audit = audit_context_reinstatement(
        expected,
        observation(expected, (ReinstatedContextItem("unavailable", A),)),
    )
    assert audit.unavailable_item_ids_reinstated == ("unavailable",)


def test_manifest_digest_binding_fails_closed():
    expected = manifest()
    observed = ContextReinstatementObservation(
        run_id="r1",
        expected_manifest_sha256=A,
        reinstated_items=(),
        retrieval_binding_sha256=None,
        context_selection_binding_sha256=None,
        evidence_refs=("fixture:observation",),
    )
    with pytest.raises(StudyError, match="expected manifest binding"):
        audit_context_reinstatement(expected, observed)


def test_unknown_availability_is_preserved_as_unknown():
    expected = manifest()
    audit = audit_context_reinstatement(expected, observation(expected, ()))
    assert audit.availability_unknown_item_ids == ("history",)


def test_real_model_context_record_is_rejected():
    expected = manifest()
    digest = digest_context_source_manifest(expected)
    with pytest.raises(StudyError, match="synthetic, non-private, and no-model"):
        ContextReinstatementObservation(
            run_id="r1",
            expected_manifest_sha256=digest,
            reinstated_items=(),
            retrieval_binding_sha256=None,
            context_selection_binding_sha256=None,
            evidence_refs=("fixture:r",),
            model_invoked=True,
        )
