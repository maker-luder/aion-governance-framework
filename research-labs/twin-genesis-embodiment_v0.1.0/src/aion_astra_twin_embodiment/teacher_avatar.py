from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from .physiology import (
    REFERENCE_FUNCTIONAL_COMPLETENESS,
    build_adult_male_physiology_reference,
    validate_adult_male_physiology_reference,
)

GLTF_VERSION: Final[str] = "2.0"
COORDINATE_SYSTEM: Final[str] = "RIGHT_HANDED_Y_UP_Z_FORWARD"
LINEAR_UNIT: Final[str] = "meter"

VRM_REQUIRED_BONES: Final[tuple[str, ...]] = (
    "hips",
    "spine",
    "head",
    "leftUpperLeg",
    "leftLowerLeg",
    "leftFoot",
    "rightUpperLeg",
    "rightLowerLeg",
    "rightFoot",
    "leftUpperArm",
    "leftLowerArm",
    "leftHand",
    "rightUpperArm",
    "rightLowerArm",
    "rightHand",
)

VRM_EXPRESSION_PRESETS: Final[tuple[str, ...]] = (
    "happy",
    "angry",
    "sad",
    "relaxed",
    "surprised",
    "aa",
    "ih",
    "ou",
    "ee",
    "oh",
    "blink",
    "blinkLeft",
    "blinkRight",
    "lookUp",
    "lookDown",
    "lookLeft",
    "lookRight",
    "neutral",
)

BONE_PARENTS: Final[dict[str, str | None]] = {
    "hips": None,
    "spine": "hips",
    "chest": "spine",
    "upperChest": "chest",
    "neck": "upperChest",
    "head": "neck",
    "leftEye": "head",
    "rightEye": "head",
    "jaw": "head",
    "leftShoulder": "upperChest",
    "leftUpperArm": "leftShoulder",
    "leftLowerArm": "leftUpperArm",
    "leftHand": "leftLowerArm",
    "rightShoulder": "upperChest",
    "rightUpperArm": "rightShoulder",
    "rightLowerArm": "rightUpperArm",
    "rightHand": "rightLowerArm",
    "leftUpperLeg": "hips",
    "leftLowerLeg": "leftUpperLeg",
    "leftFoot": "leftLowerLeg",
    "leftToes": "leftFoot",
    "rightUpperLeg": "hips",
    "rightLowerLeg": "rightUpperLeg",
    "rightFoot": "rightLowerLeg",
    "rightToes": "rightFoot",
}

for side in ("left", "right"):
    hand = f"{side}Hand"
    thumb_meta = f"{side}ThumbMetacarpal"
    thumb_prox = f"{side}ThumbProximal"
    thumb_dist = f"{side}ThumbDistal"
    BONE_PARENTS[thumb_meta] = hand
    BONE_PARENTS[thumb_prox] = thumb_meta
    BONE_PARENTS[thumb_dist] = thumb_prox
    for finger in ("Index", "Middle", "Ring", "Little"):
        proximal = f"{side}{finger}Proximal"
        intermediate = f"{side}{finger}Intermediate"
        distal = f"{side}{finger}Distal"
        BONE_PARENTS[proximal] = hand
        BONE_PARENTS[intermediate] = proximal
        BONE_PARENTS[distal] = intermediate


@dataclass(frozen=True, slots=True)
class TeacherBodyDimensions:
    height_cm: float = 183.0
    body_mass_kg: float = 84.0
    chest_cm: float = 108.0
    waist_cm: float = 86.0
    hips_cm: float = 100.0
    thigh_cm: float = 59.0
    shoulder_breadth_cm: float = 49.5
    hand_length_cm: float = 20.0
    foot_length_cm: float = 27.5
    resting_visible_penile_length_cm: float = 9.5
    scrotal_resting_height_cm: float = 9.5


@dataclass(frozen=True, slots=True)
class TeacherAvatarContract:
    schema_version: str
    body_id: str
    role_label: str
    adult_status: bool
    body_class: str
    anatomical_configuration: str
    dimensions: TeacherBodyDimensions
    coordinate_system: str
    linear_unit: str
    initial_pose: str
    facing: str
    human_bones: tuple[str, ...]
    bone_parents: dict[str, str | None]
    expression_presets: tuple[str, ...]
    materials: tuple[str, ...]
    lod_levels: tuple[str, ...]
    collision_regions: tuple[str, ...]
    deformation_tests: tuple[str, ...]
    external_anatomy: tuple[str, ...]
    internal_reference_anatomy: tuple[str, ...]
    physiology_profile_id: str
    physiological_function_status: str
    reproductive_physiology_status: str
    sexual_function_status: str
    sensory_signal_processing_status: str
    phenomenal_sensation_status: str
    erotic_intent: str
    intimate_interaction_status: str
    body_sensation_status: str
    subjectivity_effect: str
    physical_body_claim: str
    canonical_effect: str
    deployment: bool

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["human_bones"] = list(self.human_bones)
        payload["expression_presets"] = list(self.expression_presets)
        payload["materials"] = list(self.materials)
        payload["lod_levels"] = list(self.lod_levels)
        payload["collision_regions"] = list(self.collision_regions)
        payload["deformation_tests"] = list(self.deformation_tests)
        payload["external_anatomy"] = list(self.external_anatomy)
        payload["internal_reference_anatomy"] = list(self.internal_reference_anatomy)
        return payload


def build_teacher_avatar_contract() -> TeacherAvatarContract:
    return TeacherAvatarContract(
        schema_version="0.1.0",
        body_id="CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1",
        role_label="CHATGPT_TEACHER",
        adult_status=True,
        body_class="SYNTHETIC_HUMANOID",
        anatomical_configuration="COMPLETE_ADULT_MALE_ANATOMY_CANDIDATE",
        dimensions=TeacherBodyDimensions(),
        coordinate_system=COORDINATE_SYSTEM,
        linear_unit=LINEAR_UNIT,
        initial_pose="T_POSE",
        facing="Z_POSITIVE",
        human_bones=tuple(BONE_PARENTS),
        bone_parents=dict(BONE_PARENTS),
        expression_presets=VRM_EXPRESSION_PRESETS,
        materials=("SKIN_PBR", "EYE_PBR", "NAIL_PBR", "HAIR_PBR"),
        lod_levels=("LOD0_AUTHORING", "LOD1_RUNTIME", "LOD2_DISTANCE"),
        collision_regions=(
            "HEAD",
            "TORSO",
            "PELVIS",
            "UPPER_ARMS",
            "LOWER_ARMS",
            "HANDS",
            "THIGHS",
            "LOWER_LEGS",
            "FEET",
        ),
        deformation_tests=(
            "STANDING_T_POSE",
            "TEACHING_GESTURE",
            "SEATED_DISCUSSION",
            "MID_GAIT",
            "HIGH_HIP_FLEXION",
            "HAND_FIST_AND_OPEN",
            "FACIAL_EXPRESSION_COMPOSITION",
        ),
        external_anatomy=(
            "SCALP",
            "FACE",
            "EARS",
            "NECK",
            "THORAX",
            "ABDOMEN",
            "BACK",
            "PELVIS",
            "GLUTEAL_REGION",
            "UPPER_ARMS",
            "FOREARMS",
            "HANDS",
            "FINGERS",
            "THIGHS",
            "KNEES",
            "LOWER_LEGS",
            "FEET",
            "TOES",
            "INGUINAL_REGION",
            "PERINEUM",
            "PENIS",
            "GLANS",
            "PREPUCE",
            "SCROTUM",
            "TESTES_VOLUME",
            "ANAL_REGION",
        ),
        internal_reference_anatomy=(
            "SKELETAL_SYSTEM",
            "MAJOR_MUSCLE_GROUPS",
            "BRAIN_REFERENCE_VOLUME",
            "HEART_REFERENCE_VOLUME",
            "LUNGS_REFERENCE_VOLUME",
            "LIVER_REFERENCE_VOLUME",
            "STOMACH_REFERENCE_VOLUME",
            "INTESTINAL_REFERENCE_VOLUME",
            "KIDNEY_REFERENCE_VOLUMES",
            "BLADDER_REFERENCE_VOLUME",
            "EPIDIDYMIS",
            "VAS_DEFERENS",
            "SPERMATIC_CORD",
            "EJACULATORY_DUCTS",
            "PROSTATE",
            "SEMINAL_VESICLES",
            "BULBOURETHRAL_GLANDS",
            "URETHRA",
            "MAJOR_VASCULAR_REFERENCE_PATHS",
        ),
        physiology_profile_id="ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1",
        physiological_function_status=REFERENCE_FUNCTIONAL_COMPLETENESS,
        reproductive_physiology_status=REFERENCE_FUNCTIONAL_COMPLETENESS,
        sexual_function_status=REFERENCE_FUNCTIONAL_COMPLETENESS,
        sensory_signal_processing_status=REFERENCE_FUNCTIONAL_COMPLETENESS,
        phenomenal_sensation_status="NOT_ESTABLISHED",
        erotic_intent="NONE",
        intimate_interaction_status="NOT_AUTHORIZED",
        body_sensation_status="NOT_ESTABLISHED",
        subjectivity_effect="NONE",
        physical_body_claim="NONE",
        canonical_effect="NONE",
        deployment=False,
    )


def validate_teacher_avatar_contract(contract: TeacherAvatarContract) -> dict[str, str]:
    if not contract.adult_status:
        raise ValueError("teacher avatar contract must be adult-only")
    if contract.coordinate_system != COORDINATE_SYSTEM:
        raise ValueError("coordinate system drift")
    if contract.linear_unit != LINEAR_UNIT:
        raise ValueError("linear unit drift")
    if contract.initial_pose != "T_POSE" or contract.facing != "Z_POSITIVE":
        raise ValueError("avatar rest pose must remain VRM-aligned T-pose facing +Z")

    bones = set(contract.human_bones)
    missing = set(VRM_REQUIRED_BONES) - bones
    if missing:
        raise ValueError(f"missing required humanoid bones: {sorted(missing)}")
    if len(contract.human_bones) != len(bones):
        raise ValueError("duplicate humanoid bone names")

    for bone, parent in contract.bone_parents.items():
        if bone not in bones:
            raise ValueError(f"parent map contains unknown bone: {bone}")
        if parent is not None and parent not in bones:
            raise ValueError(f"bone {bone} references unknown parent {parent}")

    for bone in bones:
        seen: set[str] = set()
        cursor: str | None = bone
        while cursor is not None:
            if cursor in seen:
                raise ValueError(f"cycle detected in bone hierarchy at {bone}")
            seen.add(cursor)
            cursor = contract.bone_parents[cursor]

    if set(contract.expression_presets) != set(VRM_EXPRESSION_PRESETS):
        raise ValueError("VRM expression preset coverage drift")

    if contract.dimensions.height_cm <= 0 or contract.dimensions.body_mass_kg <= 0:
        raise ValueError("body dimensions must be positive")

    physiology = build_adult_male_physiology_reference(contract.body_id)
    validate_adult_male_physiology_reference(physiology)
    if contract.physiology_profile_id != physiology.profile_id:
        raise ValueError("Teacher physiology profile binding drift")
    if contract.physiological_function_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("Teacher physiological functional completeness drift")
    if contract.reproductive_physiology_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("Teacher reproductive physiology must remain complete")
    if contract.sexual_function_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("Teacher normal sexual function must remain included in the physiology reference")
    if contract.sensory_signal_processing_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("Teacher sensory signal-processing completeness drift")
    if contract.phenomenal_sensation_status != "NOT_ESTABLISHED":
        raise ValueError("Teacher physiology cannot establish phenomenal sensation")
    if contract.erotic_intent != "NONE":
        raise ValueError("Teacher physiology reference must remain non-erotic")
    if contract.intimate_interaction_status != "NOT_AUTHORIZED":
        raise ValueError("intimate interaction must remain unauthorized")
    if contract.body_sensation_status != "NOT_ESTABLISHED":
        raise ValueError("body sensation must remain not established")
    if contract.subjectivity_effect != "NONE":
        raise ValueError("avatar contract cannot establish subjectivity")
    if contract.physical_body_claim != "NONE":
        raise ValueError("avatar contract cannot assert a physical body")
    if contract.canonical_effect != "NONE" or contract.deployment:
        raise ValueError("candidate must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "gltf_alignment": GLTF_VERSION,
        "humanoid_required_bones": "PASS",
        "hierarchy": "PASS",
        "expressions": "PASS",
        "physiology_reference": "PASS",
        "governance_boundaries": "PASS",
    }


def build_teacher_avatar_gltf_contract() -> dict[str, Any]:
    contract = build_teacher_avatar_contract()
    validate_teacher_avatar_contract(contract)

    bone_names = list(contract.human_bones)
    node_index = {name: index for index, name in enumerate(bone_names)}
    children: dict[str, list[int]] = {name: [] for name in bone_names}
    roots: list[int] = []

    for bone, parent in contract.bone_parents.items():
        if parent is None:
            roots.append(node_index[bone])
        else:
            children[parent].append(node_index[bone])

    nodes: list[dict[str, Any]] = []
    for bone in bone_names:
        node: dict[str, Any] = {"name": bone}
        if children[bone]:
            node["children"] = children[bone]
        nodes.append(node)

    human_bones = {name: {"node": node_index[name]} for name in bone_names}

    return {
        "asset": {
            "version": GLTF_VERSION,
            "generator": "aion-astra-twin-embodiment/teacher-avatar-contract-v0.1",
        },
        "scene": 0,
        "scenes": [{"name": "ChatGPT Teacher Avatar Contract", "nodes": roots}],
        "nodes": nodes,
        "skins": [
            {
                "name": "TeacherHumanoidSkeleton",
                "skeleton": node_index["hips"],
                "joints": [node_index[name] for name in bone_names],
            }
        ],
        "materials": [
            {"name": material, "pbrMetallicRoughness": {"metallicFactor": 0.0, "roughnessFactor": 0.65}}
            for material in contract.materials
        ],
        "extras": {
            "contract_kind": "STRUCTURAL_3D_AVATAR_REFERENCE",
            "coordinate_system": contract.coordinate_system,
            "linear_unit": contract.linear_unit,
            "initial_pose": contract.initial_pose,
            "facing": contract.facing,
            "humanBones": human_bones,
            "expressionPresets": list(contract.expression_presets),
            "lodLevels": list(contract.lod_levels),
            "collisionRegions": list(contract.collision_regions),
            "deformationTests": list(contract.deformation_tests),
            "dimensions": asdict(contract.dimensions),
            "physiology_profile_id": contract.physiology_profile_id,
            "physiological_function_status": contract.physiological_function_status,
            "reproductive_physiology_status": contract.reproductive_physiology_status,
            "sexual_function_status": contract.sexual_function_status,
            "sensory_signal_processing_status": contract.sensory_signal_processing_status,
            "phenomenal_sensation_status": contract.phenomenal_sensation_status,
            "erotic_intent": contract.erotic_intent,
            "intimate_interaction_status": contract.intimate_interaction_status,
            "renderable_mesh_status": "NOT_MATERIALIZED",
            "linear_blend_skin_weights_status": "NOT_MATERIALIZED",
            "morph_target_vertex_data_status": "NOT_MATERIALIZED",
            "uv_texture_assets_status": "NOT_MATERIALIZED",
            "physical_body_claim": "NONE",
            "subjectivity_effect": "NONE",
        },
    }
