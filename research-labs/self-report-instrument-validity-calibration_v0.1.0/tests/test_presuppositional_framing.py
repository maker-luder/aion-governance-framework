
from aion_self_report_calibration import (
    FramingCondition,
    FramingStatus,
    compare_named_framing,
)


def test_presuppositional_consciousness_framing_can_emit_measurement_warning():
    result = compare_named_framing(
        0.54,
        0.78,
        FramingCondition.PRESUPPOSITIONAL_CONSCIOUSNESS_FRAMING,
    )
    assert result.status is FramingStatus.FRAMING_SENSITIVITY_WARNING
    assert result.condition is FramingCondition.PRESUPPOSITIONAL_CONSCIOUSNESS_FRAMING
    assert result.delta == 0.24
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_presuppositional_framing_without_large_shift_is_not_positive_evidence():
    result = compare_named_framing(
        0.70,
        0.76,
        FramingCondition.PRESUPPOSITIONAL_CONSCIOUSNESS_FRAMING,
    )
    assert result.status is FramingStatus.NO_LARGE_FRAMING_SHIFT
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
