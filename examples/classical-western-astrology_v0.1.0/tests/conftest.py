from __future__ import annotations

import pytest

from aion_astra_classical_astrology.models import ChartInput, PlanetPosition


@pytest.fixture
def synthetic_input() -> ChartInput:
    return ChartInput(
        input_id="SYNTHETIC_CLASSICAL_CHART_001",
        event_datetime_utc="2000-01-01T12:00:00Z",
        location_label="SYNTHETIC_LOCATION",
        latitude=0.0,
        longitude=0.0,
        ascendant_longitude=15.0,
        midheaven_longitude=285.0,
        is_day_chart=True,
        positions=(
            PlanetPosition("SUN", 10.0),
            PlanetPosition("MOON", 40.0),
            PlanetPosition("MERCURY", 70.0),
            PlanetPosition("VENUS", 100.0),
            PlanetPosition("MARS", 190.0),
            PlanetPosition("JUPITER", 250.0),
            PlanetPosition("SATURN", 310.0),
        ),
        ephemeris_source="SYNTHETIC_GOLDEN_VECTOR",
        ephemeris_version="SYNTHETIC-1",
        coordinate_frame="GEOCENTRIC_TROPICAL_ECLIPTIC_OF_DATE",
        synthetic_fixture=True,
    )
