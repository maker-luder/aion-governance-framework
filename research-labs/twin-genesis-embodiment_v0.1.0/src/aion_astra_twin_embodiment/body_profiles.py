from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

ALLOWED_SOURCE_CLASSES = frozenset({"DESIGN", "ANATOMICAL_REFERENCE"})

REQUIRED_BOUNDARIES = {
    "adult_form_reference": True,
    "erotic_intent": "NONE",
    "identity_transfer": "NO",
    "biological_tissue": "NO",
    "biological_reproduction": "NOT_APPLICABLE",
    "rendering_3d": "DEFERRED",
    "runtime_binding": "NOT_IMPLEMENTED",
    "sexual_function_status": "NOT_IMPLEMENTED",
    "body_sensation": "NOT_ESTABLISHED",
    "subjectivity_effect": "NONE",
    "canonical_effect": "NONE",
}

REQUIRED_ROBOTIC_LAYERS = frozenset(
    {
        "INTERNAL_STRUCTURAL_FRAME",
        "ACTUATOR_INTERFACE_LAYER",
        "COMPLIANT_VOLUME_LAYER",
        "SYNTHETIC_SKIN_SHELL",
    }
)

REQUIRED_REPRESENTATION_LAYERS = frozenset(
    {
        "MORPHOLOGY_LAYER",
        "VISUAL_GEOMETRY_LAYER",
        "STRUCTURAL_MODEL_LAYER",
        "KINEMATIC_MODEL_LAYER",
        "DYNAMIC_MODEL_LAYER",
        "COLLISION_MODEL_LAYER",
        "ACTUATION_INTERFACE_LAYER",
        "SENSOR_INTERFACE_LAYER",
        "COMPLIANT_BODY_LAYER",
        "SYNTHETIC_SKIN_LAYER",
    }
)

REQUIRED_FULL_BODY_COMPONENTS = frozenset(
    {
        "HEAD",
        "NECK",
        "TORSO",
        "PELVIS",
        "LEFT_ARM",
        "RIGHT_ARM",
        "LEFT_HAND",
        "RIGHT_HAND",
        "LEFT_LEG",
        "RIGHT_LEG",
        "LEFT_FOOT",
        "RIGHT_FOOT",
        "EXTERNAL_MALE_FORM_SURFACE",
    }
)

REQUIRED_EXTERNAL_MALE_FORM_MODULES = frozenset(
    {
        "penile_form",
        "glans_form",
        "prepuce_form",
        "scrotal_form",
        "testicular_volume_form",
        "pubic_mount",
        "inguinal_transition",
        "perineal_panel",
        "anal_region_surface",
    }
)

REQUIRED_MODEL_STATUS = {
    "physical_robot": "NOT_IMPLEMENTED",
    "digital_twin": "NOT_ESTABLISHED",
    "robot_description": "NOT_IMPLEMENTED",
    "visual_asset": "NOT_IMPLEMENTED",
    "kinematic_model": "NOT_IMPLEMENTED",
    "dynamic_model": "NOT_IMPLEMENTED",
    "collision_model": "NOT_IMPLEMENTED",
    "actuation_interface": "NOT_IMPLEMENTED",
    "sensor_interface": "NOT_IMPLEMENTED",
}


class BodyProfileValidationError(ValueError):
    """Raised when a machine-readable robotic body-profile candidate violates a boundary."""


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
    profile_status: str
    agent_id: str
    embodiment_platform: str
    body_scope: str
    morphology_class: str
    model_class: str
    substrate: str
    anatomy_reference_mode: str
    body_character: tuple[str, ...]
    full_body_components: tuple[str, ...]
    robotic_layers: tuple[str, ...]
    representation_layers: tuple[str, ...]
    robotic_systems: Mapping[str, str]
    model_status: Mapping[str, str]
    future_interchange_targets: Mapping[str, tuple[str, ...]]
    measurements: Mapping[str, DimensionSpec]
    external_male_form_modules: tuple[str, ...]
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
            profile_status=str(value["profile_status"]),
            agent_id=str(value["agent_id"]),
            embodiment_platform=str(value["embodiment_platform"]),
            body_scope=str(value["body_scope"]),
            morphology_class=str(value["morphology_class"]),
            model_class=str(value["model_class"]),
            substrate=str(value["substrate"]),
            anatomy_reference_mode=str(value["anatomy_reference_mode"]),
            body_character=tuple(str(item) for item in value["body_character"]),
            full_body_components=tuple(str(item) for item in value["full_body_components"]),
            robotic_layers=tuple(str(item) for item in value["robotic_layers"]),
            representation_layers=tuple(
                str(item) for item in value["representation_layers"]
            ),
            robotic_systems={
                str(name): str(status)
                for name, status in dict(value["robotic_systems"]).items()
            },
            model_status={
                str(name): str(status)
                for name, status in dict(value["model_status"]).items()
            },
            future_interchange_targets={
                str(name): tuple(str(item) for item in values)
                for name, values in dict(value["future_interchange_targets"]).items()
            },
            measurements=measurements,
            external_male_form_modules=tuple(
                str(item) for item in value["external_male_form_modules"]
            ),
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

    if profile.schema_version != "0.3.0":
        failures.append("Unsupported robotic body-profile schema_version")
    if profile.profile_status != "IMPLEMENTED_SPEC_CANDIDATE":
        failures.append("profile_status must be IMPLEMENTED_SPEC_CANDIDATE")
    if profile.agent_id not in {"AION", "ASTRA"}:
        failures.append("agent_id must be AION or ASTRA")
    if not profile.profile_id.startswith(f"{profile.agent_id}_"):
        failures.append("profile_id must be bound to agent_id")
    if profile.embodiment_platform != "HUMANOID_ROBOT":
        failures.append("embodiment_platform must be HUMANOID_ROBOT")
    if profile.body_scope != "FULL_BODY":
        failures.append("body_scope must be FULL_BODY")
    if profile.morphology_class != "HUMANLIKE_MALE_FORM":
        failures.append("morphology_class must be HUMANLIKE_MALE_FORM")
    if profile.model_class != "ROBOTIC_EMBODIMENT_DIGITAL_MODEL":
        failures.append(
            "model_class must be ROBOTIC_EMBODIMENT_DIGITAL_MODEL"
        )
    if profile.substrate != "SYNTHETIC_NONBIOLOGICAL":
        failures.append("substrate must be SYNTHETIC_NONBIOLOGICAL")
    if profile.anatomy_reference_mode != "HUMAN_ANATOMY_TO_ROBOTIC_MORPHOLOGY":
        failures.append(
            "anatomy_reference_mode must be HUMAN_ANATOMY_TO_ROBOTIC_MORPHOLOGY"
        )
    if not profile.body_character:
        failures.append("body_character must not be empty")
    if not profile.measurements:
        failures.append("measurements must not be empty")
    if not profile.engineering_requirements:
        failures.append("engineering_requirements must not be empty")

    missing_components = REQUIRED_FULL_BODY_COMPONENTS.difference(
        profile.full_body_components
    )
    if missing_components:
        failures.append(
            "Full-body component set is incomplete: "
            + ", ".join(sorted(missing_components))
        )

    missing_layers = REQUIRED_ROBOTIC_LAYERS.difference(profile.robotic_layers)
    if missing_layers:
        failures.append(
            "Robotic body layer stack is incomplete: "
            + ", ".join(sorted(missing_layers))
        )

    missing_representation_layers = REQUIRED_REPRESENTATION_LAYERS.difference(
        profile.representation_layers
    )
    if missing_representation_layers:
        failures.append(
            "Digital robotic representation stack is incomplete: "
            + ", ".join(sorted(missing_representation_layers))
        )

    missing_modules = REQUIRED_EXTERNAL_MALE_FORM_MODULES.difference(
        profile.external_male_form_modules
    )
    if missing_modules:
        failures.append(
            "Complete robotic male-form external module set is incomplete: "
            + ", ".join(sorted(missing_modules))
        )

    required_robotic_systems = {
        "actuation": "NOT_IMPLEMENTED",
        "sensing": "NOT_IMPLEMENTED",
        "power_distribution": "NOT_IMPLEMENTED",
        "thermal_management": "NOT_IMPLEMENTED",
        "service_access": "FUTURE_DESIGN_REQUIRED",
    }
    for name, expected in required_robotic_systems.items():
        if profile.robotic_systems.get(name) != expected:
            failures.append(f"Robotic system {name} must be {expected!r}")

    for name, expected in REQUIRED_MODEL_STATUS.items():
        if profile.model_status.get(name) != expected:
            failures.append(f"Model status {name} must be {expected!r}")

    required_robot_targets = {"URDF", "SDF"}
    actual_robot_targets = set(
        profile.future_interchange_targets.get("robot_description", ())
    )
    if not required_robot_targets.issubset(actual_robot_targets):
        failures.append("Future robot-description targets must include URDF and SDF")

    required_visual_targets = {"GLB", "USD"}
    actual_visual_targets = set(
        profile.future_interchange_targets.get("visual_asset", ())
    )
    if not required_visual_targets.issubset(actual_visual_targets):
        failures.append("Future visual-asset targets must include GLB and USD")

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
    if profile.provenance.get("reference_role") != "MORPHOLOGY_AND_POSE_ONLY":
        failures.append("Reference role must remain morphology / pose only")
    if profile.provenance.get("terminology_standardization_claim") != "NONE":
        failures.append("Repository-local terminology must not be misrepresented as a standard")

    if failures:
        raise BodyProfileValidationError("; ".join(sorted(set(failures))))

    serializable = {
        "schema_version": profile.schema_version,
        "profile_id": profile.profile_id,
        "profile_status": profile.profile_status,
        "agent_id": profile.agent_id,
        "embodiment_platform": profile.embodiment_platform,
        "body_scope": profile.body_scope,
        "morphology_class": profile.morphology_class,
        "model_class": profile.model_class,
        "substrate": profile.substrate,
        "anatomy_reference_mode": profile.anatomy_reference_mode,
        "body_character": list(profile.body_character),
        "full_body_components": list(profile.full_body_components),
        "robotic_layers": list(profile.robotic_layers),
        "representation_layers": list(profile.representation_layers),
        "robotic_systems": dict(profile.robotic_systems),
        "model_status": dict(profile.model_status),
        "future_interchange_targets": {
            name: list(values)
            for name, values in profile.future_interchange_targets.items()
        },
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
        "external_male_form_modules": list(profile.external_male_form_modules),
        "engineering_requirements": list(profile.engineering_requirements),
        "boundaries": dict(profile.boundaries),
        "provenance": dict(profile.provenance),
    }

    return {
        "result": "PASS",
        "profile_hash": deterministic_hash(serializable),
        "embodiment_platform": "HUMANOID_ROBOT",
        "body_scope": "FULL_BODY",
        "morphology_class": "HUMANLIKE_MALE_FORM",
        "model_class": "ROBOTIC_EMBODIMENT_DIGITAL_MODEL",
        "digital_twin_status": "NOT_ESTABLISHED",
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
        "embodiment_platform": "HUMANOID_ROBOT",
        "body_scope": "FULL_BODY",
        "model_class": "ROBOTIC_EMBODIMENT_DIGITAL_MODEL",
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
        "embodiment_platform": "HUMANOID_ROBOT",
        "body_scope": "FULL_BODY",
        "model_class": "ROBOTIC_EMBODIMENT_DIGITAL_MODEL",
        "biological_tissue": "NO",
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
