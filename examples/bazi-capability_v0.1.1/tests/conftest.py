from __future__ import annotations

from collections.abc import Callable, Iterator

import pytest

from aion_astra_bazi_core.database import Database
from aion_astra_bazi_core.enums import OwnerReviewStatus, SourceType, TimePrecision
from aion_astra_bazi_core.models import BaziSourceInput
from aion_astra_bazi_core.repository import BaziCore
from aion_astra_bazi_core.rule_profiles import standard_lichun_profile


@pytest.fixture
def database() -> Iterator[Database]:
    value = Database()
    value.initialize()
    yield value
    value.close()


@pytest.fixture
def core(database: Database) -> BaziCore:
    value = BaziCore(database)
    value.create_rule_profile(
        standard_lichun_profile(),
        created_at="2026-07-30T00:00:00+08:00",
    )
    return value


@pytest.fixture
def source_factory() -> Callable[..., BaziSourceInput]:
    def make(
        input_id: str = "SYNTHETIC_INPUT_001",
        *,
        local_datetime: str = "1986-05-29T00:00:00",
        timezone_id: str = "Asia/Taipei",
        offset: str = "+08:00",
        latitude: float = 25.033,
        longitude: float = 121.5654,
        supersedes: str | None = None,
    ) -> BaziSourceInput:
        return BaziSourceInput(
            input_id=input_id,
            local_datetime=local_datetime,
            timezone_id=timezone_id,
            utc_offset_at_event=offset,
            location_name="SYNTHETIC_LOCATION",
            latitude=latitude,
            longitude=longitude,
            time_precision=TimePrecision.EXACT_TO_SECOND,
            source_type=SourceType.SYNTHETIC_TEST,
            source_reference="PUBLIC_GOLDEN_VECTOR",
            owner_confirmation_status=OwnerReviewStatus.APPROVED,
            recorded_at="2026-07-30T00:00:00+08:00",
            supersedes=supersedes,
            audit_stream_id="SYNTHETIC_AUDIT",
        )

    return make


@pytest.fixture
def persisted_profile(core: BaziCore, source_factory: Callable[..., BaziSourceInput]):
    source = core.create_source_input(source_factory())
    profile = core.calculate_natal_profile(
        source.input_id,
        "STANDARD_LICHUN_MIDNIGHT_CIVIL_V1",
        calculation_run_id="RUN_001",
        natal_profile_id="NATAL_001",
        generated_at="2026-07-30T01:00:00+08:00",
    )
    return source, profile
