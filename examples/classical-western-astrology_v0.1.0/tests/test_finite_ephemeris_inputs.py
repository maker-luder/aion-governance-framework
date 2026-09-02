from dataclasses import replace

import pytest

from aion_astra_classical_astrology.engine import build_chart, normalize_longitude
from aion_astra_classical_astrology.errors import ValidationError
from aion_astra_classical_astrology.fixtures import synthetic_reference_input
from aion_astra_classical_astrology.profiles import hellenistic_medieval_profile


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), True, False])
def test_invalid_speeds_rejected(value):
    s = synthetic_reference_input()
    bad = replace(s, positions=(replace(s.positions[0], speed_longitude=value),) + s.positions[1:])
    with pytest.raises(ValidationError, match="finite"):
        build_chart(bad, hellenistic_medieval_profile(), chart_id="INVALID_SPEED")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), True, False])
def test_invalid_longitudes_rejected(value):
    with pytest.raises(ValidationError):
        normalize_longitude(value)
