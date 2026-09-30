import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from aion_affective_motivation.adult_reference import (
    AdultMaleSexualReferenceState,
    DesireOnsetContext,
    ReferenceEstimate,
    TargetScope,
)
from aion_affective_motivation.adult_reference_simulation import (
    AdultReferenceSyntheticEvent,
    adult_reference_event_payload,
    adult_reference_state_payload,
)


LAB_ROOT = Path(__file__).resolve().parents[1]
STATE_SCHEMA_PATH = (
    LAB_ROOT / "schemas" / "adult_male_sexual_reference_v0.1.0.schema.json"
)
EVENT_SCHEMA_PATH = (
    LAB_ROOT / "schemas" / "adult_reference_synthetic_event_v0.1.0.schema.json"
)


def load_schema(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def estimate(level: float, name: str) -> ReferenceEstimate:
    return ReferenceEstimate(
        reference_level=level,
        uncertainty=0.2,
        source_ref=f"source:{name}",
        context_ref="synthetic-context",
        time_window_ref="synthetic-window",
    )


def valid_state() -> AdultMaleSexualReferenceState:
    return AdultMaleSexualReferenceState(
        state_id="schema-state",
        subject_ref="Teacher",
        context_ref="synthetic-context",
        desire_onset_context=DesireOnsetContext.UNKNOWN,
        excitation_reference=estimate(0.4, "excitation"),
        inhibition_reference=estimate(0.6, "inhibition"),
        disposition_reference=estimate(0.3, "disposition"),
        episode_state_reference=estimate(0.7, "episode"),
        target_scope=TargetScope.UNKNOWN,
        provenance_refs=("PR#236", "SCHEMA_TEST"),
    )


def valid_event() -> AdultReferenceSyntheticEvent:
    return AdultReferenceSyntheticEvent(
        event_id="schema-event",
        context_ref="synthetic-context",
        time_window_ref="synthetic-window",
        excitation_drive=0.4,
        inhibition_drive=-0.2,
        episode_drive=0.1,
        disposition_observation_drive=0.05,
        onset_context_evidence=DesireOnsetContext.RESPONSIVE_REFERENCE,
        target_scope=TargetScope.PARTNER_CONTEXT,
        uncertainty=0.3,
        provenance_refs=("PR#236", "SCHEMA_TEST"),
    )


def test_draft_2020_12_schemas_are_valid_metaschema_instances() -> None:
    Draft202012Validator.check_schema(load_schema(STATE_SCHEMA_PATH))
    Draft202012Validator.check_schema(load_schema(EVENT_SCHEMA_PATH))


def test_python_state_payload_validates_against_json_schema() -> None:
    validator = Draft202012Validator(load_schema(STATE_SCHEMA_PATH))
    validator.validate(adult_reference_state_payload(valid_state()))


def test_python_event_payload_validates_against_json_schema() -> None:
    validator = Draft202012Validator(load_schema(EVENT_SCHEMA_PATH))
    validator.validate(adult_reference_event_payload(valid_event()))


def test_state_schema_rejects_unknown_level_without_maximum_uncertainty() -> None:
    payload = adult_reference_state_payload(valid_state())
    excitation = dict(payload["excitation_reference"])
    excitation["reference_level"] = None
    excitation["uncertainty"] = 0.5
    payload["excitation_reference"] = excitation

    with pytest.raises(ValidationError):
        Draft202012Validator(load_schema(STATE_SCHEMA_PATH)).validate(payload)


def test_state_schema_rejects_duplicate_provenance() -> None:
    payload = adult_reference_state_payload(valid_state())
    payload["provenance_refs"] = ["PR#236", "PR#236"]

    with pytest.raises(ValidationError):
        Draft202012Validator(load_schema(STATE_SCHEMA_PATH)).validate(payload)


def test_event_schema_rejects_real_person_target_field() -> None:
    payload = adult_reference_event_payload(valid_event())
    payload["real_person_target_ref"] = "person-123"

    with pytest.raises(ValidationError):
        Draft202012Validator(load_schema(EVENT_SCHEMA_PATH)).validate(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("real_person_target_data", True),
        ("human_consent_inference", "ALLOWED"),
        ("action_authority", "GRANTED"),
        ("canonical_effect", "WRITE"),
    ],
)
def test_event_schema_rejects_authority_boundary_violation(
    field: str,
    value: object,
) -> None:
    payload = adult_reference_event_payload(valid_event())
    payload[field] = value

    with pytest.raises(ValidationError):
        Draft202012Validator(load_schema(EVENT_SCHEMA_PATH)).validate(payload)
