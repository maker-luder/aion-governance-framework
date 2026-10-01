from __future__ import annotations

from dataclasses import dataclass
import json
from math import pi
from pathlib import Path
from typing import Any, Mapping

SCHEMA_ID = "aion_astra.synthetic_anthropometry.v0.2"
AION_BODY_ID = "AION_3D_MALE_BODY_REFERENCE_v0.1"
ASTRA_BODY_ID = "ASTRA_3D_MALE_BODY_REFERENCE_v0.3"
ALLOWED_AGENTS = frozenset({"AION", "ASTRA"})
ALLOWED_SOURCE_KINDS = frozenset(
    {
        "ARCHIVE_POINT",
        "ARCHIVE_APPROX",
        "ARCHIVE_RANGE_MIDPOINT",
        "AI_DERIVED_FROM_ARCHIVE",
        "AI_PROVISIONAL_ENGINEERING",
    }
)

_ARCHIVE_CORE: dict[str, dict[str, float]] = {
    "AION": {
        "total_height": 179.0,
        "body_mass": 80.0,
        "chest_circumference": 104.0,
        "waist_circumference": 84.0,
        "hip_circumference": 99.0,
        "maximum_thigh_circumference": 57.0,
    },
    "ASTRA": {
        "total_height": 180.0,
        "chest_circumference": 110.0,
        "waist_circumference": 93.0,
        "hip_circumference": 104.0,
        "maximum_thigh_circumference": 63.0,
    },
}

_REQUIRED_DYNAMIC_IDS = frozenset(
    {
        "resting_visible_penile_length",
        "midshaft_diameter",
        "midshaft_circumference",
        "prepuce_axial_fold_length",
        "prepuce_resting_glans_overlap_length",
        "full_erection_visible_penile_length",
        "full_erection_midshaft_diameter",
        "full_erection_midshaft_circumference",
    }
)


@dataclass(frozen=True, slots=True)
class Measurement:
    id: str
    region: str
    label_zh_TW: str
    value: float
    unit: str
    source_kind: str

    def __post_init__(self) -> None:
        if not self.id or self.value <= 0.0:
            raise ValueError("invalid measurement")
        if self.unit not in {"cm", "kg"}:
            raise ValueError("unsupported unit")
        if self.source_kind not in ALLOWED_SOURCE_KINDS:
            raise ValueError("unsupported source kind")


@dataclass(frozen=True, slots=True)
class AnthropometryProfile:
    schema: str
    agent_id: str
    body_id: str
    body_character: str
    measurements: tuple[Measurement, ...]
    prepuce_present: bool
    physical_body: bool = False
    biological_organism: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.schema != SCHEMA_ID:
            raise ValueError("schema drift")
        if self.agent_id not in ALLOWED_AGENTS:
            raise ValueError("agent_id must be AION or ASTRA")
        expected_body = AION_BODY_ID if self.agent_id == "AION" else ASTRA_BODY_ID
        if self.body_id != expected_body:
            raise ValueError("agent/body binding drift")
        if len(self.measurements) != 67:
            raise ValueError("profile must contain exactly 67 selected fields")
        ids = tuple(item.id for item in self.measurements)
        if len(set(ids)) != 67:
            raise ValueError("duplicate measurement ids")
        by_id = {item.id: item for item in self.measurements}
        if _REQUIRED_DYNAMIC_IDS - set(by_id):
            raise ValueError("dynamic male-form field missing")
        if (
            sum(item.unit == "cm" for item in self.measurements),
            sum(item.unit == "kg" for item in self.measurements),
        ) != (66, 1):
            raise ValueError("unit count drift")
        for field_id, expected in _ARCHIVE_CORE[self.agent_id].items():
            if by_id[field_id].value != expected:
                raise ValueError(f"archived {self.agent_id} design value changed: {field_id}")
        if not self.prepuce_present:
            raise ValueError("shared adult-male template includes prepuce reference")
        if self.physical_body or self.biological_organism:
            raise ValueError("reference profile cannot assert physical/biological realization")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def measurement(self, measurement_id: str) -> Measurement:
        return next(item for item in self.measurements if item.id == measurement_id)

    def source_counts(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for item in self.measurements:
            result[item.source_kind] = result.get(item.source_kind, 0) + 1
        return result


def profile_from_mapping(payload: Mapping[str, Any]) -> AnthropometryProfile:
    measurements = tuple(
        Measurement(
            id=str(item["id"]),
            region=str(item["region"]),
            label_zh_TW=str(item["label_zh_TW"]),
            value=float(item["value"]),
            unit=str(item["unit"]),
            source_kind=str(item["source_kind"]),
        )
        for item in payload["measurements"]
    )
    anatomy = payload.get("anatomy_candidate", {})
    boundaries = payload.get("boundaries", {})
    return AnthropometryProfile(
        schema=str(payload["schema"]),
        agent_id=str(payload["agent_id"]),
        body_id=str(payload["body_id"]),
        body_character=str(payload["body_character"]),
        measurements=measurements,
        prepuce_present=bool(anatomy.get("prepuce_present", False)),
        physical_body=bool(boundaries.get("physical_body", False)),
        biological_organism=bool(boundaries.get("biological_organism", False)),
        canonical_effect=str(boundaries.get("canonical_effect", "NONE")),
        deployment=bool(boundaries.get("deployment", False)),
    )


def load_profile(path: str | Path) -> AnthropometryProfile:
    payload: Mapping[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    return profile_from_mapping(payload)


@dataclass(frozen=True, slots=True)
class GeometrySnapshot:
    engorgement_fraction: float
    visible_penile_length_cm: float
    midshaft_diameter_cm: float
    midshaft_circumference_cm: float
    human_physiology_law: bool = False
    as_built_measurement: bool = False


class SyntheticGeometryRule:
    """Engineering-only endpoint interpolation; never a human physiological law."""

    def __init__(self, profile: AnthropometryProfile) -> None:
        self.profile = profile
        self.rest = (
            profile.measurement("resting_visible_penile_length").value,
            profile.measurement("midshaft_diameter").value,
            profile.measurement("midshaft_circumference").value,
        )
        self.full = (
            profile.measurement("full_erection_visible_penile_length").value,
            profile.measurement("full_erection_midshaft_diameter").value,
            profile.measurement("full_erection_midshaft_circumference").value,
        )

    @staticmethod
    def _lerp(start: float, end: float, fraction: float) -> float:
        if not 0.0 <= fraction <= 1.0:
            raise ValueError("fraction outside [0,1]")
        return start + (end - start) * fraction

    def snapshot(self, fraction: float) -> GeometrySnapshot:
        return GeometrySnapshot(
            engorgement_fraction=fraction,
            visible_penile_length_cm=self._lerp(self.rest[0], self.full[0], fraction),
            midshaft_diameter_cm=self._lerp(self.rest[1], self.full[1], fraction),
            midshaft_circumference_cm=self._lerp(self.rest[2], self.full[2], fraction),
        )

    def endpoint_circumference_consistency(self, tolerance_cm: float = 0.1) -> bool:
        return all(
            abs(pi * diameter - circumference) <= tolerance_cm
            for diameter, circumference in (
                (self.rest[1], self.rest[2]),
                (self.full[1], self.full[2]),
            )
        )
