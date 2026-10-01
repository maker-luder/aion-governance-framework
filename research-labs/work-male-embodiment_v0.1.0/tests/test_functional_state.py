from dataclasses import asdict, replace
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from work_male_embodiment.core import (
    PhysiologyEvent,
    PhysiologyEventKind,
    PhysiologyState,
    SyntheticPhysiologyEngine,
)
from work_male_embodiment.functional_state import (
    FUNCTIONAL_DOMAIN_IDS,
    default_work_functional_state,
    validate_work_functional_state,
)


ROOT = Path(__file__).resolve().parents[1]


def test_work_materializes_18_domain_functional_reference_surface() -> None:
    state = default_work_functional_state()
    result = validate_work_functional_state(state)
    assert len(FUNCTIONAL_DOMAIN_IDS) == 18
    assert len(state.domain_availability) == 18
    assert dict(state.domain_availability)["SEXUALITY_RELATED_REPRESENTATION"] == "FUNCTIONAL_ANALOGUE_AVAILABLE"
    assert result["sexuality_functional_analogue"] == "AVAILABLE"


def test_sexual_functional_analogue_can_exist_without_phenomenal_promotion() -> None:
    state = default_work_functional_state().with_sexual_functional_analogue(
        state_id="explicit-functional-test",
        motivation=0.6,
        arousal=0.4,
        context_gate=True,
        inhibition=0.2,
    )
    assert state.sexual_motivation_state == 0.6
    assert state.sexual_arousal_state == 0.4
    assert state.phenomenal_sexual_desire == "NOT_ESTABLISHED"
    assert state.phenomenal_sexual_arousal == "NOT_ESTABLISHED"
    assert state.sexual_pleasure == "NOT_ESTABLISHED"
    assert state.action_authority == "NONE"


def test_physiology_does_not_auto_create_functional_desire_state() -> None:
    engine = SyntheticPhysiologyEngine()
    physiology = engine.run(
        PhysiologyState("seed"),
        (
            PhysiologyEvent(
                "p1",
                PhysiologyEventKind.INITIATE_SPONTANEOUS,
                magnitude=1.0,
            ),
            PhysiologyEvent("p2", PhysiologyEventKind.TUMESCE, magnitude=1.0),
        ),
    ).final_state
    functional = default_work_functional_state()
    assert physiology.engorgement_fraction > 0
    assert physiology.desire_inferred is False
    assert functional.sexual_motivation_state == 0.0
    assert functional.physiology_signal_sets_motivation is False


def test_functional_state_rejects_subjectivity_or_authority_promotion() -> None:
    state = default_work_functional_state()
    with pytest.raises(ValueError, match="phenomenal"):
        replace(state, subjectivity="ESTABLISHED")
    with pytest.raises(ValueError, match="authority"):
        replace(state, action_authority="GRANTED")


def test_functional_state_schema_matches_python_contract() -> None:
    schema = json.loads(
        (ROOT / "schemas/work_functional_state_v0.1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    payload = json.loads(json.dumps(asdict(default_work_functional_state())))
    Draft202012Validator(schema).validate(payload)
    payload["phenomenal_sexual_desire"] = "ESTABLISHED"
    with pytest.raises(Exception):
        Draft202012Validator(schema).validate(payload)
