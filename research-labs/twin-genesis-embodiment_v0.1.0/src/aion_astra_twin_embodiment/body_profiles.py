from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

ALLOWED_SOURCE_CLASSES = frozenset({"DESIGN", "ANATOMICAL_REFERENCE"})

REQUIRED_BOUNDARIES = {
    "adult_status": True,
    "erotic_intent": "NONE",
    "identity_transfer": "NO",
    "rendering_3d": "DEFERRED",
    "runtime_binding": "NOT_IMPLEMENTED",
    "sexual_function_status": "NOT_IMPLEMENTED",
    "body_sensation": "NOT_ESTABLISHED",
    "subjectivity_effect": "NONE",
    "canonical_effect": "NONE",
}

REQUIRED_EXTERNAL_ANATOMY = frozenset(
    {
        "penis",
        "glans",
        "prepuce_or_foreskin",
        "scrotum",
        "testes_volume_representation",
        "pubic_attachment",
        "inguinal_transition",
        "perineum",
        "anal_region",
    }
)


class BodyProfileValidationError(ValueError):
    """Raised when a machine-readable body-profile candidate violates a boundary."""


@dataclass(frozen=True, slots=True)
class DimensionSpec:
    unit: str
    minimum: float
    maximum: float
    canonical: float | None
    source_class: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "DimensionSpec":
        return cls(
            unit=str(value["unit"]),
            minimum=float(value["minimum"]),
            maximum=float(value["maximum"]),
            canonical=None if value.get("canonical") is None else float(value["canonical"]),
            source_class=str(value["source_class"]),
        )


@dataclass(frozen=True, slots=True)
class BodyProfileCandidate:
    schema_version: str
    profile_id: str
    agent_id: str
    body_character: tuple[str, ...]
    measurements: Mapping[str, DimensionSpec]
    external_anatomy: tuple[str, ...]
    engineering_requirements: tuple[str, ...]
    boundaries: Mapping[str, Any]
    provenance: Mapping[str, Any]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "BodyProfileCandidate":
        measurements = {
            name: DimensionSpec.from_mapping(spec)
            for name, spec in dict(value["measurements"]).items()
        }
        return cls(
            schema_version=str(value["schema_version"]),
            profile_id=str(value["profile_id"]),
            agent_id=str(value["agent_id"]),
            body_character=tuple(str(item) for item in value["body_character"]),
            measurements=measurements,
            external_anatomy=tuple(str(item) for item in value["external_anatomy"]),
            engineering_requirements=tuple(
                str(item) for item in value["engineering_requirements"]
            ),
            boundaries=dict(value["boundaries"]),
            provenance=dict(value["provenance"]),
        )


@dataclass(frozen=True, slots=True)
class PoseDeformationTestCandidate:
    schema_version: str
    test_id: str
    agent_id: str
    status: str
    pose_features: tuple[str, ...]
    pass_conditions: tuple[str, ...]
    boundaries: Mapping[str, Any]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "PoseDeformationTestCandidate":
        return cls(
            schema_version=str(value["schema_version"]),
            test_id=str(value["test_id"]),
            agent_id=str(value["agent_id"]),
            status=str(value["status"]),
            pose_features=tuple(str(item) for item in value["pose_features"]),
            pass_conditions=tuple(str(item) for item in value["pass_conditions"]),
            boundaries=dict(value["boundaries"]),
        )


def deterministic_hash(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_body_profile(path: str | Path) -> BodyProfileCandidate:
    return BodyProfileCandidate.from_mapping(load_json(path))


def load_pose_test(path: str | Path) -> PoseDeformationTestCandidate:
    return PoseDeformationTestCandidate.from_mapping(load_json(path))


def validate_body_profile(profile: BodyProfileCandidate) -> dict[str, str]:
    failures: list[str] = []

    if profile.schema_version != "0.1.0":
        failures.append("Unsupported body-profile schema_version")
    if profile.agent_id not in {"AION", "ASTRA"}:
        failures.append("agent_id must be AION or ASTRA")
    if not profile.profile_id.startswith(f"{profile.agent_id}_"):
        failures.append("profile_id must be bound to agent_id")
    if not profile.body_character:
        failures.append("body_character must not be empty")
    if not profile.measurements:
        failures.append("measurements must not be empty")
    if not profile.engineering_requirements:
        failures.append("engineering_requirements must not be empty")

    missing_anatomy = REQUIRED_EXTERNAL_ANATOMY.difference(profile.external_anatomy)
    if missing_anatomy:
        failures.append(
            "Complete adult male external anatomy is incomplete: "
            + ", ".join(sorted(missing_anatomy))
        )

    for name, expected in REQUIRED_BOUNDARIES.items():
        if profile.boundaries.get(name) != expected:
            failures.append(f"Boundary {name} must be {expected!r}")

    for name, dimension in profile.measurements.items():
        if dimension.unit not in {"cm", "kg"}:
            failures.append(f"{name}: unsupported unit")
        if dimension.minimum <= 0 or dimension.maximum <= 0:
            failures.append(f"{name}: dimensions must be positive")
        if dimension.minimum > dimension.maximum:
            failures.append(f"{name}: minimum must not exceed maximum")
        if dimension.canonical is not None and not (
            dimension.minimum <= dimension.canonical <= dimension.maximum
        ):
            failures.append(f"{name}: canonical must be inside the declared range")
        if dimension.source_class not in ALLOWED_SOURCE_CLASSES:
            failures.append(f"{name}: unsupported source_class")

    if profile.provenance.get("reference_image_binary_imported") is not False:
        failures.append("Reference image binaries must not be imported")
    if profile.provenance.get("person_identity_reconstruction") != "NO":
        failures.append("Person identity reconstruction must remain NO")
    if profile.provenance.get("source_person_exact_measurement_claim") != "NO":
        failures.append("Source-person exact measurement claims must remain NO")

    if failures:
        raise BodyProfileValidationError("; ".join(sorted(set(failures))))

    serializable = {
        "schema_version": profile.schema_version,
        "profile_id": profile.profile_id,
        "agent_id": profile.agent_id,
        "body_character": list(profile.body_character),
        "measurements": {
            name: {
                "unit": spec.unit,
                "minimum": spec.minimum,
                "maximum": spec.maximum,
                "canonical": spec.canonical,
                "source_class": spec.source_class,
            }
            for name, spec in sorted(profile.measurements.items())
        },
        "external_anatomy": list(profile.external_anatomy),
        "engineering_requirements": list(profile.engineering_requirements),
        "boundaries": dict(profile.boundaries),
        "provenance": dict(profile.provenance),
    }

    return {
        "result": "PASS",
        "profile_hash": deterministic_hash(serializable),
        "canonical_effect": "NONE",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
    }


def validate_profile_pair(
    aion: BodyProfileCandidate,
    astra: BodyProfileCandidate,
) -> dict[str, str]:
    aion_result = validate_body_profile(aion)
    astra_result = validate_body_profile(astra)
    failures: list[str] = []

    if aion.agent_id != "AION" or astra.agent_id != "ASTRA":
        failures.append("Profile pair must be ordered AION then ASTRA")
    if aion.profile_id == astra.profile_id:
        failures.append("AION and Astra must have distinct body profile IDs")
    if aion.body_character == astra.body_character:
        failures.append("AION and Astra body-character candidates must remain distinct")

    if failures:
        raise BodyProfileValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "pair_hash": deterministic_hash(
            {
                "aion_profile_id": aion.profile_id,
                "astra_profile_id": astra.profile_id,
                "aion_hash": aion_result["profile_hash"],
                "astra_hash": astra_result["profile_hash"],
            }
        ),
        "canonical_effect": "NONE",
    }


def validate_pose_test(test: PoseDeformationTestCandidate) -> dict[str, str]:
    failures: list[str] = []

    if test.schema_version != "0.1.0":
        failures.append("Unsupported pose-test schema_version")
    if test.agent_id not in {"AION", "ASTRA"}:
        failures.append("Pose test agent_id must be AION or ASTRA")
    if test.status != "DOCUMENTED_ONLY":
        failures.append("Pose test must remain DOCUMENTED_ONLY")
    if not test.pose_features:
        failures.append("Pose test must declare pose_features")
    if not test.pass_conditions:
        failures.append("Pose test must declare pass_conditions")

    required_boundaries = {
        "rendering_3d": "DEFERRED",
        "runtime_binding": "NOT_IMPLEMENTED",
        "body_sensation": "NOT_ESTABLISHED",
        "subjectivity_effect": "NONE",
        "canonical_effect": "NONE",
    }
    for name, expected in required_boundaries.items():
        if test.boundaries.get(name) != expected:
            failures.append(f"Pose-test boundary {name} must be {expected!r}")

    if failures:
        raise BodyProfileValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "test_id": test.test_id,
        "canonical_effect": "NONE",
    }
