"""AION tiger anthropomorphic full-dimension preset V2.

V2 is additive and backward-compatible with V1. It upgrades every V1 row with
category, measurement method, source refs, evidence strength, and value semantics.

DIRECT_TIGER_OBSERVATION != AION_DESIGN_TARGET
COMMUNITY_PRACTITIONER != BIOLOGICAL_EVIDENCE
FORENSIC_DRY_SPECIMEN_CONSTRAINT != LIVE_NORMAL_RANGE
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .body_dimensions import (
    COMMUNITY_DESIGN_REFERENCE,
    DESIGN_TARGET,
    ENGINEERING_DESIGN_CHOICE,
    HUMAN_ANTHROPOMETRY_REFERENCE,
    REFERENCE_OBSERVATION,
    TIGER_CONFIRMED,
    UNKNOWN_SOURCE_NOT_ESTABLISHED,
    BodyDimension,
    build_aion_tiger_full_dimension_preset,
)
from .dimension_sources import source_map

REFERENCE_CONSTRAINT: Final[str] = "REFERENCE_CONSTRAINT"
DIRECT_SINGLE_SPECIMEN: Final[str] = "DIRECT_SINGLE_SPECIMEN"
DIRECT_MULTI_SPECIMEN: Final[str] = "DIRECT_MULTI_SPECIMEN"
INSTITUTIONAL_SPECIES_RANGE: Final[str] = "INSTITUTIONAL_SPECIES_RANGE"
HUMAN_ANTHROPOMETRY: Final[str] = "HUMAN_ANTHROPOMETRY"
COMMUNITY_PRACTITIONER: Final[str] = "COMMUNITY_PRACTITIONER"
ENGINEERING_SYNTHESIS: Final[str] = "ENGINEERING_SYNTHESIS"
FORENSIC_CONSTRAINT: Final[str] = "FORENSIC_CONSTRAINT"
GAP_NOT_ESTABLISHED: Final[str] = "GAP_NOT_ESTABLISHED"

TARGET_VALUE: Final[str] = "TARGET_VALUE"
OBSERVED_VALUE: Final[str] = "OBSERVED_VALUE"
APPROX_UPPER_BOUND: Final[str] = "APPROX_UPPER_BOUND"
EXCLUSION_IF_GREATER_THAN: Final[str] = "EXCLUSION_IF_GREATER_THAN"
UNDEFINED: Final[str] = "UNDEFINED"


@dataclass(frozen=True, slots=True)
class BodyDimensionV2:
    key: str
    label_zh: str
    category: str
    value: float | None
    unit: str
    measurement_role: str
    provenance: tuple[str, ...]
    basis: str
    measurement_method_zh: str
    source_refs: tuple[str, ...]
    evidence_strength: str
    value_semantics: str
    status: str = "DEFINED"


@dataclass(frozen=True, slots=True)
class AionTigerDimensionPresetV2:
    preset_id: str
    agent_id: str
    species_profile_id: str
    design_posture: str
    locomotor_form: str
    measurements: tuple[BodyDimensionV2, ...]
    canonical_effect: str = "NONE"
    biological_hybrid_claim: str = "NOT_ESTABLISHED"

    def measurement_map(self) -> dict[str, BodyDimensionV2]:
        return {item.key: item for item in self.measurements}


def _category_for_key(key: str) -> str:
    if "reference_" in key or key.startswith("tiger_"):
        return "TIGER_REFERENCE"
    if any(token in key for token in ("head", "muzzle", "ear", "eye", "pupil", "nose", "mandible", "chin", "brow", "crown")):
        return "HEAD_NECK"
    if any(token in key for token in ("arm", "forepaw", "hand", "wrist", "finger", "thumb", "palm")):
        return "UPPER_LIMB"
    if any(token in key for token in ("thigh", "shank", "hock", "hindpaw", "knee", "ankle", "foot", "inseam", "outseam")):
        return "LOWER_LIMB"
    if "tail" in key:
        return "TAIL"
    if any(token in key for token in ("fur", "ruff")):
        return "SURFACE"
    if any(token in key for token in ("chest", "waist", "hip", "torso", "back", "shoulder", "crotch", "neck_base")):
        return "TORSO"
    return "GLOBAL"


def _method_for_v1(item: BodyDimension) -> str:
    if item.key.startswith("tiger_reference_"):
        return "依原始研究定義讀取標本量測；不得把 reference observation 反推為 AION 目標值。"
    if item.value is None:
        return "目前不量化；保留欄位並等待可辯護來源或明確工程決策。"
    if item.unit in {"kg", "g"}:
        return "使用校準秤重設備；工程目標與來源標本重量必須分開記錄。"
    if "circumference" in item.key:
        return "中立站姿，以軟尺水平繞量最大或指定 landmark 周徑，不壓縮表面輪廓。"
    if "diameter" in item.key:
        return "沿指定截面量測直徑；若為來源觀察則遵守原研究定義。"
    if "height" in item.key:
        return "中立直立 A-pose，由地面垂直量至指定 anatomical/rig landmark。"
    if "width" in item.key or "breadth" in item.key:
        return "正面中立 A-pose，沿左右最外或指定 landmark 的水平距離量測。"
    if "depth" in item.key or "projection" in item.key:
        return "側面中立姿勢，沿前後方向量指定 landmark 間距。"
    if "length" in item.key or "span" in item.key:
        return "依欄位兩端 landmark 量直線或表面路徑；rig segment 預設 joint-center to joint-center。"
    return "依欄位 anatomical/rig landmark 以公制量測並記錄姿勢。"


def _sources_for_v1(item: BodyDimension) -> tuple[str, ...]:
    if item.key.startswith("tiger_reference_"):
        return ("MEIRELES_2012_REPRODUCTIVE",)
    refs: list[str] = []
    if HUMAN_ANTHROPOMETRY_REFERENCE in item.provenance:
        refs.append("NASA_HIDH")
    if TIGER_CONFIRMED in item.provenance:
        if "tail" in item.key:
            refs.append("TAIPEI_ZOO_TIGER")
        elif any(token in item.key for token in ("head", "muzzle", "ear", "ruff")):
            refs.append("MAZAK_2010_CRANIOMETRY")
        else:
            refs.append("DUNN_2022_FORELIMB")
    if COMMUNITY_DESIGN_REFERENCE in item.provenance:
        refs.append("FURNFURRY_MEASURE")
    if item.key == "aion_total_penile_length_cm":
        refs.extend(("MEIRELES_2012_REPRODUCTIVE", "USFWS_YATES_2005_TIGER_GENITAL_ID"))
    return tuple(dict.fromkeys(refs))


def _evidence_for_v1(item: BodyDimension) -> str:
    if item.value is None:
        return GAP_NOT_ESTABLISHED
    if item.measurement_role == REFERENCE_OBSERVATION:
        return DIRECT_SINGLE_SPECIMEN
    if COMMUNITY_DESIGN_REFERENCE in item.provenance and ENGINEERING_DESIGN_CHOICE in item.provenance:
        return ENGINEERING_SYNTHESIS
    if ENGINEERING_DESIGN_CHOICE in item.provenance:
        return ENGINEERING_SYNTHESIS
    if HUMAN_ANTHROPOMETRY_REFERENCE in item.provenance:
        return HUMAN_ANTHROPOMETRY
    return ENGINEERING_SYNTHESIS


def _upgrade_v1(item: BodyDimension) -> BodyDimensionV2:
    if item.value is None:
        semantics = UNDEFINED
    elif item.measurement_role == REFERENCE_OBSERVATION:
        semantics = OBSERVED_VALUE
    else:
        semantics = TARGET_VALUE
    return BodyDimensionV2(
        key=item.key,
        label_zh=item.label_zh,
        category=_category_for_key(item.key),
        value=item.value,
        unit=item.unit,
        measurement_role=item.measurement_role,
        provenance=item.provenance,
        basis=item.basis,
        measurement_method_zh=_method_for_v1(item),
        source_refs=_sources_for_v1(item),
        evidence_strength=_evidence_for_v1(item),
        value_semantics=semantics,
        status=item.status,
    )


def _d(
    key: str,
    label_zh: str,
    category: str,
    value: float | None,
    unit: str,
    role: str,
    provenance: tuple[str, ...],
    basis: str,
    method: str,
    source_refs: tuple[str, ...],
    evidence_strength: str,
    value_semantics: str = TARGET_VALUE,
    status: str = "DEFINED",
) -> BodyDimensionV2:
    return BodyDimensionV2(
        key=key,
        label_zh=label_zh,
        category=category,
        value=value,
        unit=unit,
        measurement_role=role,
        provenance=provenance,
        basis=basis,
        measurement_method_zh=method,
        source_refs=source_refs,
        evidence_strength=evidence_strength,
        value_semantics=value_semantics,
        status=status,
    )


def build_aion_tiger_full_dimension_preset_v2() -> AionTigerDimensionPresetV2:
    v1 = build_aion_tiger_full_dimension_preset()
    upgraded = tuple(_upgrade_v1(item) for item in v1.measurements)

    human_design = (HUMAN_ANTHROPOMETRY_REFERENCE, ENGINEERING_DESIGN_CHOICE)
    community_design = (COMMUNITY_DESIGN_REFERENCE, ENGINEERING_DESIGN_CHOICE)
    hybrid_design = (
        HUMAN_ANTHROPOMETRY_REFERENCE,
        TIGER_CONFIRMED,
        COMMUNITY_DESIGN_REFERENCE,
        ENGINEERING_DESIGN_CHOICE,
    )
    tiger_ref = (TIGER_CONFIRMED,)

    added = (
        _d("neck_base_height_cm", "頸根離地高度", "GLOBAL", 160.0, "cm", DESIGN_TARGET, human_design,
           "補足 ref sheet 與 rig 的上軀幹 landmark。", "由地面垂直量至 C7/頸根視覺 landmark。",
           ("NASA_HIDH", "SPIRITPANDA_DTD"), ENGINEERING_SYNTHESIS),
        _d("standing_vertical_reach_cm", "站立單手上舉最高可及高度", "GLOBAL", 246.0, "cm", DESIGN_TARGET, human_design,
           "提供場景 clearance 與 animation reach envelope。", "自然站姿，單臂完全上舉，量地面至前掌最高點。",
           ("NASA_HIDH",), ENGINEERING_SYNTHESIS),
        _d("functional_forward_reach_cm", "肩部中立前伸可及距離", "GLOBAL", 79.0, "cm", DESIGN_TARGET, human_design,
           "操作空間的工程目標。", "肩峰保持軀幹中立，手臂前伸，量肩垂直平面至前掌最遠點。",
           ("NASA_HIDH",), ENGINEERING_SYNTHESIS),
        _d("seated_height_cm", "坐姿頭頂高度", "GLOBAL", 101.0, "cm", DESIGN_TARGET, human_design,
           "補足座椅、車艙與場景 clearance。", "坐骨接觸水平座面，軀幹直立，量座面至頭頂最高點。",
           ("NASA_HIDH",), ENGINEERING_SYNTHESIS),

        _d("head_brow_circumference_cm", "眉弓水平頭圍", "HEAD_NECK", 76.0, "cm", DESIGN_TARGET, hybrid_design,
           "把虎型頭殼／毛量轉成可製作的 head fitting envelope。", "軟尺水平繞過眉弓與後腦最大點，不壓縮毛量。",
           ("FRECKLED_CAT_MEASUREMENTS", "SPIRITPANDA_DTD", "MAZAK_2010_CRANIOMETRY"), ENGINEERING_SYNTHESIS),
        _d("head_chin_back_circumference_cm", "下巴—後腦環圍", "HEAD_NECK", 84.0, "cm", DESIGN_TARGET, community_design,
           "fursuit head 常用的第二環圍，避免只用水平頭圍。", "軟尺由下巴下緣繞過後腦再回下巴。",
           ("SPIRITPANDA_DTD",), COMMUNITY_PRACTITIONER),
        _d("head_crown_chin_circumference_cm", "頭頂—下巴垂直環圍", "HEAD_NECK", 88.0, "cm", DESIGN_TARGET, community_design,
           "補足頭部上下包絡與下頜空間。", "軟尺由頭頂中線經耳前／臉側到下巴再回頭頂。",
           ("SPIRITPANDA_DTD",), COMMUNITY_PRACTITIONER),
        _d("interpupillary_distance_cm", "瞳孔中心距", "HEAD_NECK", 8.2, "cm", DESIGN_TARGET, hybrid_design,
           "眼位、視線、mask/fursuit 視野與 3D rig 需要。", "正面直視，以左右瞳孔中心的水平距離量測。",
           ("FOK_MEASUREMENTS", "FRECKLED_CAT_MEASUREMENTS"), ENGINEERING_SYNTHESIS),
        _d("eye_opening_width_cm", "單眼可視開口寬", "HEAD_NECK", 5.6, "cm", DESIGN_TARGET, community_design,
           "角色外形與實際視線 aperture 分開定義。", "正面量單眼可視開口內緣至外緣最大水平距離。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("eye_opening_height_cm", "單眼可視開口高", "HEAD_NECK", 3.8, "cm", DESIGN_TARGET, community_design,
           "建立眼部 mesh/rig 開口。", "正面量單眼可視開口上下緣最大垂直距離。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("nose_tip_to_pupil_height_cm", "鼻尖到瞳孔中心垂直距離", "HEAD_NECK", 10.0, "cm", DESIGN_TARGET, community_design,
           "對應 maker 的 eye-height 定位欄位。", "正面自然頭位，量鼻尖水平線至瞳孔中心水平線。",
           ("FOK_MEASUREMENTS",), COMMUNITY_PRACTITIONER),
        _d("chin_to_nose_tip_cm", "下巴最低點到鼻尖", "HEAD_NECK", 11.5, "cm", DESIGN_TARGET, community_design,
           "補足吻部與下頜前視比例。", "正面／側面頭位一致，量下巴最低點至鼻尖 landmark。",
           ("FOK_MEASUREMENTS",), ENGINEERING_SYNTHESIS),
        _d("chin_to_pupil_cm", "下巴最低點到瞳孔中心", "HEAD_NECK", 19.5, "cm", DESIGN_TARGET, community_design,
           "maker fitting 與 eye alignment 欄位。", "正面量下巴最低點至雙眼瞳孔中心線。",
           ("FRECKLED_CAT_MEASUREMENTS",), ENGINEERING_SYNTHESIS),
        _d("nose_leather_width_cm", "鼻鏡最大寬", "HEAD_NECK", 8.5, "cm", DESIGN_TARGET, hybrid_design,
           "虎型鼻鏡的 engineering target。", "正面量鼻鏡左右最寬點，不含周邊毛。",
           ("MAZAK_2010_CRANIOMETRY",), ENGINEERING_SYNTHESIS),
        _d("nose_leather_height_cm", "鼻鏡最大高", "HEAD_NECK", 5.2, "cm", DESIGN_TARGET, hybrid_design,
           "虎型鼻部 mesh target。", "正面量鼻鏡上下最大距離，不含吻毛。",
           ("MAZAK_2010_CRANIOMETRY",), ENGINEERING_SYNTHESIS),
        _d("mandible_breadth_cm", "下頜後段最大寬", "HEAD_NECK", 20.0, "cm", DESIGN_TARGET, hybrid_design,
           "顱顏 robust morphology 的工程值。", "正面量左右下頜角最外點。",
           ("MAZAK_2010_CRANIOMETRY",), ENGINEERING_SYNTHESIS),
        _d("ear_root_spacing_cm", "雙耳根內側間距", "HEAD_NECK", 11.0, "cm", DESIGN_TARGET, hybrid_design,
           "避免耳朵只定大小未定 attachment。", "正面量左右耳根內側最近 landmark。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("ear_root_length_cm", "單耳根附著長", "HEAD_NECK", 7.5, "cm", DESIGN_TARGET, hybrid_design,
           "耳部 rig 與變形帶寬。", "沿頭皮曲面量單耳前後附著邊界。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("muzzle_circumference_cm", "吻部環圍", "HEAD_NECK", 38.0, "cm", DESIGN_TARGET, hybrid_design,
           "補足只有長寬、沒有 3D volume 的缺口。", "閉口中立，軟尺繞過吻部最大周徑，不壓毛。",
           ("MAZAK_2010_CRANIOMETRY",), ENGINEERING_SYNTHESIS),

        _d("back_width_armpit_to_armpit_cm", "背寬（腋下到腋下）", "TORSO", 47.0, "cm", DESIGN_TARGET, human_design,
           "fursuit maker 常用背寬欄位。", "背面 A-pose，水平量左右後腋襞 landmark。",
           ("FRECKLED_CAT_MEASUREMENTS",), ENGINEERING_SYNTHESIS),
        _d("torso_shoulder_to_crotch_cm", "肩頸點到胯下軀幹長", "TORSO", 76.0, "cm", DESIGN_TARGET, human_design,
           "DTD／bodysuit 核心長度。", "由肩頸交界沿軀幹表面至胯下最低點。",
           ("SPIRITPANDA_DTD", "FURNFURRY_MEASURE"), ENGINEERING_SYNTHESIS),
        _d("armpit_to_waist_cm", "腋下到腰線", "TORSO", 29.0, "cm", DESIGN_TARGET, human_design,
           "補足上軀幹 pattern segment。", "側面由腋下最低點垂直量至自然腰線。",
           ("FOK_MEASUREMENTS",), ENGINEERING_SYNTHESIS),
        _d("shoulder_to_waist_front_cm", "肩頸點到前腰線", "TORSO", 52.0, "cm", DESIGN_TARGET, human_design,
           "前身 pattern block。", "由肩頸交界經胸前自然表面至前腰線。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("shoulder_to_waist_back_cm", "肩頸點到後腰線", "TORSO", 54.0, "cm", DESIGN_TARGET, human_design,
           "後身 pattern block。", "由肩頸交界經背部自然表面至後腰線。",
           ("KEMONO_LINE_DTD",), ENGINEERING_SYNTHESIS),
        _d("neck_base_to_tail_root_surface_cm", "頸根到尾根表面距離", "TORSO", 67.0, "cm", DESIGN_TARGET, hybrid_design,
           "把 tail placement 從單一高度改成 body-surface landmark。", "由後頸根沿脊柱中線表面量至尾根中心。",
           ("FOK_MEASUREMENTS", "KEMONO_LINE_DTD"), ENGINEERING_SYNTHESIS),
        _d("waist_height_cm", "自然腰線離地高度", "TORSO", 116.0, "cm", DESIGN_TARGET, human_design,
           "服裝、pattern 與尾部定位共同基準。", "自然站姿，由地面垂直量至側腰自然凹點水平線。",
           ("NASA_HIDH",), ENGINEERING_SYNTHESIS),
        _d("abdomen_circumference_cm", "腹部最大圍", "TORSO", 101.0, "cm", DESIGN_TARGET, human_design,
           "胸腰之間補一個 volume control。", "自然呼氣，軟尺水平繞腹部最大點。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),

        _d("sleeve_neck_to_wrist_extended_cm", "頸根到腕（手臂伸展）", "UPPER_LIMB", 81.0, "cm", DESIGN_TARGET, human_design,
           "maker pattern 長度。", "手臂側向伸展，沿肩線／外臂量頸根至腕橫紋。",
           ("FOK_MEASUREMENTS",), ENGINEERING_SYNTHESIS),
        _d("sleeve_neck_to_wrist_relaxed_cm", "頸根到腕（手臂放鬆）", "UPPER_LIMB", 79.0, "cm", DESIGN_TARGET, human_design,
           "比較伸展與自然姿勢的 pattern 餘量。", "手臂自然下垂，沿肩外側至腕橫紋。",
           ("FOK_MEASUREMENTS",), ENGINEERING_SYNTHESIS),
        _d("inside_arm_length_cm", "腋下到腕內臂長", "UPPER_LIMB", 52.0, "cm", DESIGN_TARGET, human_design,
           "補足內臂 seam 長度。", "A-pose，由腋下最低點沿內臂至腕橫紋。",
           ("SPIRITPANDA_DTD", "FOK_MEASUREMENTS"), ENGINEERING_SYNTHESIS),
        _d("wrist_circumference_cm", "腕圍", "UPPER_LIMB", 21.0, "cm", DESIGN_TARGET, human_design,
           "paw cuff 與手臂套接口。", "軟尺繞腕骨突起近端，不過度收緊。",
           ("SPIRITPANDA_DTD", "FURNFURRY_MEASURE"), ENGINEERING_SYNTHESIS),
        _d("hand_paw_circumference_cm", "前掌／手最大環圍", "UPPER_LIMB", 30.0, "cm", DESIGN_TARGET, hybrid_design,
           "僅長寬不足以製作 paw volume。", "手掌自然伸展，繞掌骨頭最大處，不含拇指。",
           ("SPIRITPANDA_DTD", "FRECKLED_CAT_MEASUREMENTS"), ENGINEERING_SYNTHESIS),
        _d("middle_digit_length_cm", "中指／中央主趾長", "UPPER_LIMB", 10.5, "cm", DESIGN_TARGET, hybrid_design,
           "保留類人操作但外觀 paw 化。", "由掌指關節折線至中央指尖。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("thumb_digit_length_cm", "拇指長", "UPPER_LIMB", 7.5, "cm", DESIGN_TARGET, human_design,
           "精細操作與手套／paw pattern。", "由第一掌指關節至拇指尖。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("forepaw_central_pad_length_cm", "前掌中央肉球長", "UPPER_LIMB", 9.5, "cm", DESIGN_TARGET, hybrid_design,
           "視覺與接觸面 mesh target。", "掌面正投影量中央 pad 前後最大長。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("forepaw_central_pad_width_cm", "前掌中央肉球寬", "UPPER_LIMB", 9.0, "cm", DESIGN_TARGET, hybrid_design,
           "視覺與接觸面 mesh target。", "掌面正投影量中央 pad 左右最大寬。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),

        _d("inseam_crotch_to_floor_cm", "內側腿長（胯下到地面）", "LOWER_LIMB", 92.0, "cm", DESIGN_TARGET, human_design,
           "DTD／bodysuit 核心欄位。", "自然站姿，沿內腿由胯下最低點量至地面。",
           ("SPIRITPANDA_DTD", "FURNFURRY_MEASURE"), ENGINEERING_SYNTHESIS),
        _d("outseam_waist_to_floor_cm", "外側腿長（腰線到地面）", "LOWER_LIMB", 112.0, "cm", DESIGN_TARGET, human_design,
           "外側 seam 與 digitigrade padding 定位。", "由自然腰線側點沿外腿至地面。",
           ("SPIRITPANDA_DTD", "FOK_MEASUREMENTS"), ENGINEERING_SYNTHESIS),
        _d("hip_to_knee_cm", "髖側點到膝中心", "LOWER_LIMB", 52.0, "cm", DESIGN_TARGET, human_design,
           "digitigrade maker 要求的上腿 segment。", "由髖側 landmark 沿外腿至膝關節中心。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("knee_to_anatomical_ankle_cm", "膝中心到生理解剖踝", "LOWER_LIMB", 44.0, "cm", DESIGN_TARGET, human_design,
           "把人類承重腿與外觀飛節分開。", "量膝關節中心至內外踝中心線。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("upper_thigh_circumference_cm", "大腿上段圍", "LOWER_LIMB", 69.0, "cm", DESIGN_TARGET, hybrid_design,
           "digitigrade padding 基準。", "軟尺水平量臀褶下方最大大腿圍。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("lower_thigh_circumference_cm", "大腿下段圍", "LOWER_LIMB", 53.0, "cm", DESIGN_TARGET, hybrid_design,
           "避免整條腿只有一個圍度。", "膝上約一掌寬位置水平量周徑。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("knee_circumference_cm", "膝圍", "LOWER_LIMB", 44.0, "cm", DESIGN_TARGET, human_design,
           "膝部活動餘量與 mesh cross-section。", "站姿膝伸直但不鎖死，繞髕骨中心量。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("anatomical_ankle_circumference_cm", "生理解剖踝圍", "LOWER_LIMB", 27.0, "cm", DESIGN_TARGET, human_design,
           "內部承重腳與外觀 digitigrade paw 分離。", "繞內外踝最窄安全截面量周徑。",
           ("FOK_MEASUREMENTS", "FURNFURRY_MEASURE"), ENGINEERING_SYNTHESIS),
        _d("internal_human_foot_length_cm", "內部承重人形足長", "LOWER_LIMB", 28.0, "cm", DESIGN_TARGET, human_design,
           "區分內部承重足與 31 cm 外觀後掌。", "站立負重，由後跟最末端至最長趾尖。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("internal_human_foot_width_cm", "內部承重人形足寬", "LOWER_LIMB", 10.8, "cm", DESIGN_TARGET, human_design,
           "feetpaw 內部鞋楦／承重空間。", "站立負重，量前足最寬處。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("hindpaw_central_pad_length_cm", "後掌中央肉球長", "LOWER_LIMB", 14.0, "cm", DESIGN_TARGET, hybrid_design,
           "後掌接觸 patch 設計。", "足底正投影量中央 pad 前後最大長。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("hindpaw_central_pad_width_cm", "後掌中央肉球寬", "LOWER_LIMB", 11.0, "cm", DESIGN_TARGET, hybrid_design,
           "後掌接觸 patch 設計。", "足底正投影量中央 pad 左右最大寬。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("digitigrade_padding_max_depth_cm", "趾行小腿墊最大外凸深度", "LOWER_LIMB", 12.0, "cm", DESIGN_TARGET, community_design,
           "把 digitigrade silhouette 與真實腿骨分開建模。", "側面由內部小腿表面基準至外觀 padding 最外點。",
           ("FURNFURRY_MEASURE", "KEMONO_LINE_DTD"), ENGINEERING_SYNTHESIS),

        _d("tail_base_circumference_cm", "尾根圍", "TAIL", 40.8, "cm", DESIGN_TARGET, hybrid_design,
           "由 V1 13 cm 尾根直徑導出的 mesh cross-section target。", "尾根垂直於尾軸的截面周徑量測。",
           ("TAIPEI_ZOO_TIGER", "FURNFURRY_MEASURE"), ENGINEERING_SYNTHESIS),
        _d("tail_mid_circumference_cm", "尾中段圍", "TAIL", 28.3, "cm", DESIGN_TARGET, hybrid_design,
           "由 V1 9 cm 中段直徑建立 collision/mesh 參考。", "尾長 50% 位置、垂直尾軸量周徑。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("tail_tip_circumference_cm", "尾尖近端圍", "TAIL", 17.3, "cm", DESIGN_TARGET, hybrid_design,
           "由 V1 5.5 cm 尾尖直徑建立 taper target。", "尾長約 90% 位置、垂直尾軸量周徑。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("tail_rig_segment_length_cm", "尾部單節 rig 建議長度", "TAIL", 8.75, "cm", DESIGN_TARGET, community_design,
           "105 cm 尾巴以約 12 節建立可控曲線的工程選擇。", "沿中立尾軸將總長等分；不是生物椎骨長。",
           ("KEMONO_LINE_DTD",), ENGINEERING_SYNTHESIS),

        _d("chest_ruff_visual_depth_cm", "胸前鬃毛視覺厚度", "SURFACE", 6.0, "cm", DESIGN_TARGET, hybrid_design,
           "雄虎 robust silhouette 的表面層；不當作毛幹生物長度。", "由皮膚基準面到渲染外輪廓的法線距離。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("forearm_fur_visual_depth_cm", "前臂毛層視覺厚度", "SURFACE", 2.5, "cm", DESIGN_TARGET, community_design,
           "讓肢體 mesh 與毛層 envelope 分離。", "由皮膚／base mesh 法線量到外觀 fur shell。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),
        _d("tail_fur_visual_depth_cm", "尾部毛層視覺厚度", "SURFACE", 2.5, "cm", DESIGN_TARGET, hybrid_design,
           "尾部 collision core 與 fur shell 分層。", "由尾 core mesh 法線量到渲染外輪廓。",
           ("FURNFURRY_MEASURE",), ENGINEERING_SYNTHESIS),

        _d("tiger_reference_scapula_max_length_right_cm", "虎參考：右肩胛最大長", "TIGER_REFERENCE", 26.5, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，成年 Royal Bengal Tiger N=1。", "原研究：dorsal border 至 glenoid cavity 最大長。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_scapula_max_length_left_cm", "虎參考：左肩胛最大長", "TIGER_REFERENCE", 26.5, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "依原研究定義量測。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_scapula_max_width_right_cm", "虎參考：右肩胛最大寬", "TIGER_REFERENCE", 20.0, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "原研究：cranial border 至 caudal angle 最大寬。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_scapula_max_width_left_cm", "虎參考：左肩胛最大寬", "TIGER_REFERENCE", 17.2, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "依原研究定義量測。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_glenoid_length_right_cm", "虎參考：右肩胛盂長", "TIGER_REFERENCE", 5.2, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "原研究 glenoid cavity length。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_glenoid_width_right_cm", "虎參考：右肩胛盂寬", "TIGER_REFERENCE", 3.7, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "原研究 glenoid cavity width。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_humerus_length_right_cm", "虎參考：右肱骨總長", "TIGER_REFERENCE", 28.0, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "依原研究乾骨 total length。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_humerus_length_left_cm", "虎參考：左肱骨總長", "TIGER_REFERENCE", 27.9, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "依原研究乾骨 total length。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_humerus_midshaft_circ_right_cm", "虎參考：右肱骨中段圍", "TIGER_REFERENCE", 10.5, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "依原研究 humeral shaft middle circumference。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_humerus_head_circ_right_cm", "虎參考：右肱骨頭圍", "TIGER_REFERENCE", 19.4, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "依原研究 circumference of head。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_ulna_length_right_cm", "虎參考：右尺骨總長", "TIGER_REFERENCE", 28.0, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "依原研究乾骨 total length。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_ulna_length_left_cm", "虎參考：左尺骨總長", "TIGER_REFERENCE", 27.0, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Uddin et al. 2022，N=1。", "依原研究乾骨 total length。",
           ("UDDIN_2022_FORELIMB",), DIRECT_SINGLE_SPECIMEN, OBSERVED_VALUE),

        _d("tiger_reference_tibia_upper_shaft_circ_mean_cm", "虎參考：脛骨上段幹平均圍", "TIGER_REFERENCE", 16.72, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Tomar et al. 2026，五隻成年虎，mean ±0.29 cm。", "依原研究上段 shaft circumference。",
           ("TOMAR_2026_TIBIA_FIBULA",), DIRECT_MULTI_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_tibia_midshaft_circ_mean_cm", "虎參考：脛骨中段幹平均圍", "TIGER_REFERENCE", 10.06, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Tomar et al. 2026，五隻成年虎，mean ±0.17 cm。", "依原研究中段 shaft circumference。",
           ("TOMAR_2026_TIBIA_FIBULA",), DIRECT_MULTI_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_tibia_lower_shaft_circ_mean_cm", "虎參考：脛骨下段幹平均圍", "TIGER_REFERENCE", 10.18, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Tomar et al. 2026，五隻成年虎，mean ±0.18 cm。", "依原研究下段 shaft circumference。",
           ("TOMAR_2026_TIBIA_FIBULA",), DIRECT_MULTI_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_fibula_length_mean_cm", "虎參考：腓骨平均長", "TIGER_REFERENCE", 29.26, "cm", REFERENCE_OBSERVATION, tiger_ref,
           "Tomar et al. 2026，五隻成年虎，mean ±0.28 cm。", "依原研究 fibula length。",
           ("TOMAR_2026_TIBIA_FIBULA",), DIRECT_MULTI_SPECIMEN, OBSERVED_VALUE),
        _d("tiger_reference_fibula_mass_mean_g", "虎參考：腓骨平均重量", "TIGER_REFERENCE", 28.52, "g", REFERENCE_OBSERVATION, tiger_ref,
           "Tomar et al. 2026，五隻成年虎，mean ±0.46 g。", "依原研究乾骨重量。",
           ("TOMAR_2026_TIBIA_FIBULA",), DIRECT_MULTI_SPECIMEN, OBSERVED_VALUE),

        _d("tiger_forensic_dried_glans_tip_upper_bound_cm", "虎鑑識：約略乾燥龜頭尖端上限", "TIGER_REFERENCE", 5.0, "cm", REFERENCE_CONSTRAINT, tiger_ref,
           "USFWS 2005 鑑識圖說指出 genuine dried tiger glans tip < 約 2 in (~5 cm)；非活體常模。",
           "只作乾燥標本鑑識約束，不拿來設定 AION。",
           ("USFWS_YATES_2005_TIGER_GENITAL_ID",), FORENSIC_CONSTRAINT, APPROX_UPPER_BOUND),
        _d("tiger_forensic_dried_tip_to_scrotum_exclusion_cm", "虎鑑識：乾燥標本 tip-to-scrotum 排除閾值", "TIGER_REFERENCE", 20.32, "cm", REFERENCE_CONSTRAINT, tiger_ref,
           "USFWS 2005：若乾燥標本 tip-to-scrotum > 8 in，不能判為虎；非活體尺寸。",
           "只作 species-exclusion rule，不反推活體尺寸或 AION 目標。",
           ("USFWS_YATES_2005_TIGER_GENITAL_ID",), FORENSIC_CONSTRAINT, EXCLUSION_IF_GREATER_THAN),
    )

    measurements = upgraded + added
    patched: list[BodyDimensionV2] = []
    for item in measurements:
        if item.key != "aion_total_penile_length_cm":
            patched.append(item)
            continue
        patched.append(BodyDimensionV2(
            key=item.key,
            label_zh=item.label_zh,
            category="REPRODUCTIVE_DESIGN_GAP",
            value=None,
            unit="cm",
            measurement_role=DESIGN_TARGET,
            provenance=(ENGINEERING_DESIGN_CHOICE,),
            basis=(
                "擴大檢索找到雄虎生殖解剖、baculum 形態與乾燥標本鑑識約束，"
                "但仍沒有足以合理轉譯成 AION 活體『陰莖總長』的直接虎資料；禁止編造。"
            ),
            measurement_method_zh="欄位保留但不填值；待直接虎資料或明確非生物學工程決策。",
            source_refs=("MEIRELES_2012_REPRODUCTIVE", "USFWS_YATES_2005_TIGER_GENITAL_ID"),
            evidence_strength=GAP_NOT_ESTABLISHED,
            value_semantics=UNDEFINED,
            status=UNKNOWN_SOURCE_NOT_ESTABLISHED,
        ))

    return AionTigerDimensionPresetV2(
        preset_id="AION-TIGER-FULL-DIMENSIONS-V2",
        agent_id="AION",
        species_profile_id="AION-TIGER-ANTHROPOMORPH-V1",
        design_posture="NEUTRAL_UPRIGHT_A_POSE",
        locomotor_form="BIPEDAL_DIGITIGRADE",
        measurements=tuple(patched),
    )


REQUIRED_V2_KEYS: Final[tuple[str, ...]] = (
    "stature_cm",
    "body_mass_kg",
    "head_brow_circumference_cm",
    "interpupillary_distance_cm",
    "back_width_armpit_to_armpit_cm",
    "torso_shoulder_to_crotch_cm",
    "neck_base_to_tail_root_surface_cm",
    "inside_arm_length_cm",
    "wrist_circumference_cm",
    "hand_paw_circumference_cm",
    "inseam_crotch_to_floor_cm",
    "outseam_waist_to_floor_cm",
    "hip_to_knee_cm",
    "knee_circumference_cm",
    "anatomical_ankle_circumference_cm",
    "internal_human_foot_length_cm",
    "hindpaw_length_cm",
    "tail_length_cm",
    "tiger_reference_humerus_length_right_cm",
    "tiger_reference_fibula_length_mean_cm",
    "tiger_forensic_dried_tip_to_scrotum_exclusion_cm",
    "aion_total_penile_length_cm",
)


def validate_aion_tiger_dimension_preset_v2(preset: AionTigerDimensionPresetV2) -> dict[str, str]:
    if preset.agent_id != "AION":
        raise ValueError("V2 dimension preset must be bound to AION")
    if preset.species_profile_id != "AION-TIGER-ANTHROPOMORPH-V1":
        raise ValueError("V2 dimension preset must bind AION tiger profile")

    keys = [item.key for item in preset.measurements]
    if len(keys) != len(set(keys)):
        raise ValueError("dimension keys must be unique")
    missing = sorted(set(REQUIRED_V2_KEYS) - set(keys))
    if missing:
        raise ValueError(f"missing V2 dimensions: {', '.join(missing)}")

    source_backed_roles = {REFERENCE_OBSERVATION, REFERENCE_CONSTRAINT}
    known_sources = source_map()
    for item in preset.measurements:
        if item.value is not None and item.value <= 0:
            raise ValueError(f"dimension must be positive: {item.key}")
        if not item.measurement_method_zh:
            raise ValueError(f"measurement method required: {item.key}")
        if item.measurement_role in source_backed_roles and not item.source_refs:
            raise ValueError(f"reference row requires source_refs: {item.key}")
        unknown_refs = sorted(set(item.source_refs) - set(known_sources))
        if unknown_refs:
            raise ValueError(f"unknown source refs for {item.key}: {unknown_refs}")
        if item.value is None and item.status != UNKNOWN_SOURCE_NOT_ESTABLISHED:
            raise ValueError(f"undefined row must be UNKNOWN_SOURCE_NOT_ESTABLISHED: {item.key}")

    m = preset.measurement_map()
    hindpaw = m["hindpaw_length_cm"].value
    internal_foot = m["internal_human_foot_length_cm"].value
    inseam = m["inseam_crotch_to_floor_cm"].value
    outseam = m["outseam_waist_to_floor_cm"].value
    if hindpaw is None or internal_foot is None or hindpaw < internal_foot:
        raise ValueError("external digitigrade hindpaw must cover the internal load-bearing foot")
    if inseam is None or outseam is None or outseam <= inseam:
        raise ValueError("outseam must exceed inseam for this preset")

    unknown = [item.key for item in preset.measurements if item.value is None]
    direct_reference_count = sum(
        item.evidence_strength in {DIRECT_SINGLE_SPECIMEN, DIRECT_MULTI_SPECIMEN}
        for item in preset.measurements
    )
    practitioner_field_count = sum(
        any(ref in {
            "SPIRITPANDA_DTD",
            "FOK_MEASUREMENTS",
            "FRECKLED_CAT_MEASUREMENTS",
            "FURNFURRY_MEASURE",
            "KEMONO_LINE_DTD",
        } for ref in item.source_refs)
        for item in preset.measurements
        if item.measurement_role == DESIGN_TARGET
    )
    return {
        "result": "PASS",
        "preset_id": preset.preset_id,
        "dimension_count": str(len(preset.measurements)),
        "direct_reference_count": str(direct_reference_count),
        "practitioner_field_count": str(practitioner_field_count),
        "unknown_dimension_count": str(len(unknown)),
        "unknown_dimensions": ",".join(unknown),
        "canonical_effect": preset.canonical_effect,
        "biological_hybrid_claim": preset.biological_hybrid_claim,
    }
