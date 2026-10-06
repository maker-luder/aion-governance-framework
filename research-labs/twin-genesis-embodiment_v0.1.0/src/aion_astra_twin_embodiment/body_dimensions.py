"""Complete measurable dimension preset for AION's tiger anthropomorph.

中文完整說明：
本模組提供「可實際拿去做 3D / rig / ref sheet」的尺寸介面，但嚴格分開四種來源：
1. TIGER_CONFIRMED：老虎直接量測或可靠動物學資料。
2. HUMAN_ANTHROPOMETRY_REFERENCE：人類人體工學／人體測量資料。
3. COMMUNITY_DESIGN_REFERENCE：福瑞社群 ref sheet / fursuit 設計慣例，只回答「哪些尺寸要標」。
4. ENGINEERING_DESIGN_CHOICE：AION 虎型獸人的具體工程設計值，不冒充自然生物學。

COMMUNITY_DESIGN_REFERENCE != BIOLOGICAL_EVIDENCE
ENGINEERING_DESIGN_CHOICE != TIGER_MEASUREMENT
COMPLETE_FIELD_COVERAGE != SCIENTIFIC_ESTABLISHMENT
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

TIGER_CONFIRMED: Final[str] = "TIGER_CONFIRMED"
HUMAN_ANTHROPOMETRY_REFERENCE: Final[str] = "HUMAN_ANTHROPOMETRY_REFERENCE"
COMMUNITY_DESIGN_REFERENCE: Final[str] = "COMMUNITY_DESIGN_REFERENCE"
ENGINEERING_DESIGN_CHOICE: Final[str] = "ENGINEERING_DESIGN_CHOICE"
REFERENCE_OBSERVATION: Final[str] = "REFERENCE_OBSERVATION"
DESIGN_TARGET: Final[str] = "DESIGN_TARGET"
UNKNOWN_SOURCE_NOT_ESTABLISHED: Final[str] = "UNKNOWN_SOURCE_NOT_ESTABLISHED"


@dataclass(frozen=True, slots=True)
class BodyDimension:
    key: str
    label_zh: str
    value: float | None
    unit: str
    measurement_role: str
    provenance: tuple[str, ...]
    basis: str
    status: str = "DEFINED"


@dataclass(frozen=True, slots=True)
class AionTigerDimensionPreset:
    preset_id: str
    agent_id: str
    species_profile_id: str
    design_posture: str
    locomotor_form: str
    measurements: tuple[BodyDimension, ...]
    canonical_effect: str = "NONE"
    biological_hybrid_claim: str = "NOT_ESTABLISHED"

    def measurement_map(self) -> dict[str, BodyDimension]:
        return {item.key: item for item in self.measurements}


def _d(
    key: str,
    label_zh: str,
    value: float | None,
    unit: str,
    role: str,
    provenance: tuple[str, ...],
    basis: str,
    status: str = "DEFINED",
) -> BodyDimension:
    return BodyDimension(
        key=key,
        label_zh=label_zh,
        value=value,
        unit=unit,
        measurement_role=role,
        provenance=provenance,
        basis=basis,
        status=status,
    )


def build_aion_tiger_full_dimension_preset() -> AionTigerDimensionPreset:
    """Build one explicit non-canonical design preset / 建立一套明示、非 canonical 的尺寸預設。

    設計目標選 190 cm：它仍落在 NASA Human Integration Design Handbook
    所列成人 stature 範圍（最高約 194.6 cm）內，但把頭、肩、胸、paw、尾部做虎型放大。
    福瑞社群來源只用來決定 ref sheet 必須標出哪些部位，不用來宣稱生物學真值。
    """

    human = (HUMAN_ANTHROPOMETRY_REFERENCE, ENGINEERING_DESIGN_CHOICE)
    hybrid = (
        HUMAN_ANTHROPOMETRY_REFERENCE,
        TIGER_CONFIRMED,
        COMMUNITY_DESIGN_REFERENCE,
        ENGINEERING_DESIGN_CHOICE,
    )
    tiger_design = (TIGER_CONFIRMED, COMMUNITY_DESIGN_REFERENCE, ENGINEERING_DESIGN_CHOICE)

    measurements = (
        # Global envelope / 全身外包絡
        _d("stature_cm", "直立總身高", 190.0, "cm", DESIGN_TARGET, human,
           "Within NASA adult anthropometric envelope; explicit AION design target."),
        _d("body_mass_kg", "整體設計體重", 112.0, "kg", DESIGN_TARGET, hybrid,
           "Engineering mass target for a broad, muscular biped; not a tiger or human population mean."),
        _d("arm_span_cm", "指尖到指尖臂展", 198.0, "cm", DESIGN_TARGET, human,
           "Human-like manipulative upper limbs with broadened tiger-anthro shoulder frame."),
        _d("acromial_height_cm", "肩峰離地高度", 154.0, "cm", DESIGN_TARGET, human,
           "Rig landmark for standing neutral pose."),
        _d("eye_height_cm", "眼位離地高度", 171.0, "cm", DESIGN_TARGET, hybrid,
           "Raised anthro-feline head on a 190 cm biped."),
        _d("hip_joint_height_cm", "髖關節中心離地高度", 101.0, "cm", DESIGN_TARGET, human,
           "Biped rig landmark."),
        _d("crotch_height_cm", "會陰／胯下離地高度", 92.0, "cm", DESIGN_TARGET, human,
           "Clothing, rig and stride reference; clinically neutral."),
        _d("knee_joint_height_cm", "膝關節中心離地高度", 53.0, "cm", DESIGN_TARGET, human,
           "Biped lower-limb rig landmark."),
        # Head / 頭頸
        _d("head_height_cm", "頭部總高度（下頜至頭頂）", 38.0, "cm", DESIGN_TARGET, hybrid,
           "20% of stature; enlarged anthro head for clear tiger silhouette."),
        _d("head_width_cm", "頭部最大寬度", 24.0, "cm", DESIGN_TARGET, tiger_design,
           "Wider zygomatic/muzzle silhouette than human baseline."),
        _d("head_depth_cm", "頭部前後深度", 31.0, "cm", DESIGN_TARGET, tiger_design,
           "Anchored to tiger skull-length literature, then adapted to an anthropomorphic neck."),
        _d("muzzle_projection_cm", "吻部向前突出長度", 10.5, "cm", DESIGN_TARGET, tiger_design,
           "Anthropomorphic tiger muzzle; engineering value, not a wild-tiger mean."),
        _d("muzzle_width_cm", "吻部最大寬度", 14.5, "cm", DESIGN_TARGET, tiger_design,
           "Keeps tiger-specific muzzle recognition in front view."),
        _d("ear_height_cm", "單耳高度", 10.5, "cm", DESIGN_TARGET, tiger_design,
           "Visible outside head silhouette in front/side ref views."),
        _d("ear_width_cm", "單耳基部寬度", 9.0, "cm", DESIGN_TARGET, tiger_design,
           "Feline rounded-ear silhouette adapted to head scale."),
        _d("neck_length_cm", "頸部可見長度", 13.0, "cm", DESIGN_TARGET, hybrid,
           "Supports enlarged muzzle/head while retaining human-like vertical posture."),
        _d("neck_circumference_cm", "頸圍", 48.0, "cm", DESIGN_TARGET, hybrid,
           "Above common human reference range by deliberate muscular/feline adaptation."),
        # Torso / 軀幹
        _d("shoulder_breadth_cm", "雙肩最大寬度", 54.0, "cm", DESIGN_TARGET, hybrid,
           "Broadened beyond ordinary human interscye to carry tiger-derived forequarter mass."),
        _d("chest_breadth_cm", "胸廓寬度", 42.0, "cm", DESIGN_TARGET, hybrid,
           "Tiger-like deep forequarter translated into a human-upright thorax."),
        _d("chest_depth_cm", "胸廓前後深度", 30.0, "cm", DESIGN_TARGET, hybrid,
           "Near upper human anthropometric envelope with feline robustness."),
        _d("chest_circumference_cm", "胸圍", 118.0, "cm", DESIGN_TARGET, hybrid,
           "Engineering target above NASA example range; intentionally muscular."),
        _d("waist_circumference_cm", "腰圍", 94.0, "cm", DESIGN_TARGET, human,
           "Keeps torso articulation and clothing fit practical."),
        _d("hip_circumference_cm", "臀／髖圍", 108.0, "cm", DESIGN_TARGET, human,
           "Biped load-bearing pelvis and digitigrade transition volume."),
        _d("hip_breadth_cm", "髖部最大寬度", 41.0, "cm", DESIGN_TARGET, human,
           "Within/near NASA seated-hip breadth envelope; used here as a standing design width."),
        _d("neck_base_to_waist_cm", "頸根到腰線長度", 50.0, "cm", DESIGN_TARGET, human,
           "Torso rig and clothing measurement."),
        _d("waist_to_crotch_cm", "腰線到胯下長度", 28.0, "cm", DESIGN_TARGET, human,
           "Pelvis/garment block measurement."),
        # Upper limbs / 上肢
        _d("upper_arm_length_cm", "上臂長", 37.0, "cm", DESIGN_TARGET, human,
           "Shoulder-to-elbow rig segment."),
        _d("forearm_length_cm", "前臂長", 31.5, "cm", DESIGN_TARGET, human,
           "Elbow-to-wrist rig segment."),
        _d("forepaw_hand_length_cm", "前掌／手長", 23.0, "cm", DESIGN_TARGET, hybrid,
           "Human manipulation retained, paw silhouette enlarged."),
        _d("forepaw_hand_width_cm", "前掌／手寬", 12.0, "cm", DESIGN_TARGET, hybrid,
           "Padded paw-hand design; exact value is engineering."),
        _d("foreclaw_exposed_length_cm", "前爪可露出長度", 2.5, "cm", DESIGN_TARGET, tiger_design,
           "Visual/rig limit, not claimed as natural tiger claw length."),
        _d("upper_arm_circumference_cm", "上臂圍", 42.0, "cm", DESIGN_TARGET, hybrid,
           "Muscular forequarter translation."),
        _d("forearm_circumference_cm", "前臂圍", 35.0, "cm", DESIGN_TARGET, hybrid,
           "Supports paw-hand and pronation/supination reference."),
        # Lower limbs / 下肢
        _d("thigh_length_cm", "大腿段長", 50.0, "cm", DESIGN_TARGET, human,
           "Hip-to-knee biped segment."),
        _d("shank_length_cm", "小腿主段長", 44.0, "cm", DESIGN_TARGET, human,
           "Knee-to-hock/ankle functional segment."),
        _d("digitigrade_hock_height_cm", "趾行後跟／飛節離地高度", 19.0, "cm", DESIGN_TARGET, tiger_design,
           "Digitigrade anthro adaptation; requires custom rig."),
        _d("hindpaw_length_cm", "後掌接地長度", 31.0, "cm", DESIGN_TARGET, hybrid,
           "Longer than human foot reference to provide digitigrade stability."),
        _d("hindpaw_width_cm", "後掌最大寬度", 13.5, "cm", DESIGN_TARGET, hybrid,
           "Broad padded contact patch for stability."),
        _d("thigh_circumference_cm", "大腿圍", 69.0, "cm", DESIGN_TARGET, hybrid,
           "Slightly above NASA example range as deliberate muscular design."),
        _d("calf_hock_circumference_cm", "小腿／飛節最大圍", 43.0, "cm", DESIGN_TARGET, hybrid,
           "Digitigrade lower-limb mass envelope."),
        # Tail / 尾部
        _d("tail_length_cm", "尾長（尾根到尾尖）", 105.0, "cm", DESIGN_TARGET, tiger_design,
           "Within real-tiger tail range reported by zoo references and below character stature."),
        _d("tail_base_diameter_cm", "尾根直徑", 13.0, "cm", DESIGN_TARGET, tiger_design,
           "Large enough for visible muscular attachment and rig deformation."),
        _d("tail_mid_diameter_cm", "尾中段直徑", 9.0, "cm", DESIGN_TARGET, tiger_design,
           "Taper profile for rig and collision volume."),
        _d("tail_tip_diameter_cm", "尾尖直徑", 5.5, "cm", DESIGN_TARGET, tiger_design,
           "Taper endpoint before fur volume."),
        _d("tail_root_height_cm", "尾根中心離地高度", 101.0, "cm", DESIGN_TARGET, hybrid,
           "Aligned approximately with posterior pelvic/hip rig level."),
        # Surface / 外表面
        _d("body_fur_visual_depth_cm", "軀幹短毛視覺厚度", 2.0, "cm", DESIGN_TARGET,
           (COMMUNITY_DESIGN_REFERENCE, ENGINEERING_DESIGN_CHOICE),
           "Rendering envelope, not biological hair-shaft length."),
        _d("cheek_ruff_visual_depth_cm", "頰側蓬毛視覺厚度", 5.0, "cm", DESIGN_TARGET,
           (TIGER_CONFIRMED, COMMUNITY_DESIGN_REFERENCE, ENGINEERING_DESIGN_CHOICE),
           "Male tiger cheek-ruff silhouette adapted for character readability."),
        # Tiger reproductive reference observations / 虎直接生殖量測（不是 AION 固定值）
        _d("tiger_reference_right_testis_length_cm", "雄虎參考：右睪丸長", 4.42, "cm",
           REFERENCE_OBSERVATION, (TIGER_CONFIRMED,),
           "Meireles et al. 2012, one 12-year-old 200 kg male tiger."),
        _d("tiger_reference_right_testis_width_cm", "雄虎參考：右睪丸寬", 3.84, "cm",
           REFERENCE_OBSERVATION, (TIGER_CONFIRMED,),
           "Meireles et al. 2012, N=1."),
        _d("tiger_reference_left_testis_length_cm", "雄虎參考：左睪丸長", 3.93, "cm",
           REFERENCE_OBSERVATION, (TIGER_CONFIRMED,),
           "Meireles et al. 2012, N=1."),
        _d("tiger_reference_left_testis_width_cm", "雄虎參考：左睪丸寬", 3.67, "cm",
           REFERENCE_OBSERVATION, (TIGER_CONFIRMED,),
           "Meireles et al. 2012, N=1."),
        _d("tiger_reference_penile_urethra_diameter_mm", "雄虎參考：陰莖尿道直徑", 1.73, "mm",
           REFERENCE_OBSERVATION, (TIGER_CONFIRMED,),
           "Meireles et al. 2012, N=1; not a total penile dimension."),
        _d("tiger_reference_total_reproductive_system_mass_g", "雄虎參考：生殖系統總重量", 429.0, "g",
           REFERENCE_OBSERVATION, (TIGER_CONFIRMED,),
           "Meireles et al. 2012, N=1."),
        _d("aion_total_penile_length_cm", "AION 目標：陰莖總長", None, "cm",
           DESIGN_TARGET, (ENGINEERING_DESIGN_CHOICE,),
           "No adequate tiger-specific source in the admitted evidence set; do not fabricate.",
           UNKNOWN_SOURCE_NOT_ESTABLISHED),
    )
    return AionTigerDimensionPreset(
        preset_id="AION-TIGER-FULL-DIMENSIONS-V1",
        agent_id="AION",
        species_profile_id="AION-TIGER-ANTHROPOMORPH-V1",
        design_posture="NEUTRAL_UPRIGHT_A_POSE",
        locomotor_form="BIPEDAL_DIGITIGRADE",
        measurements=measurements,
    )


REQUIRED_DIMENSION_KEYS: Final[tuple[str, ...]] = (
    "stature_cm",
    "body_mass_kg",
    "arm_span_cm",
    "head_height_cm",
    "head_width_cm",
    "head_depth_cm",
    "muzzle_projection_cm",
    "ear_height_cm",
    "neck_circumference_cm",
    "shoulder_breadth_cm",
    "chest_circumference_cm",
    "waist_circumference_cm",
    "hip_circumference_cm",
    "upper_arm_length_cm",
    "forearm_length_cm",
    "forepaw_hand_length_cm",
    "forepaw_hand_width_cm",
    "thigh_length_cm",
    "shank_length_cm",
    "digitigrade_hock_height_cm",
    "hindpaw_length_cm",
    "hindpaw_width_cm",
    "tail_length_cm",
    "tail_base_diameter_cm",
    "tail_root_height_cm",
)


def validate_aion_tiger_dimension_preset(preset: AionTigerDimensionPreset) -> dict[str, str]:
    """Validate completeness and evidence boundaries / 驗證完整度與證據邊界。"""

    if preset.agent_id != "AION":
        raise ValueError("dimension preset must be bound to AION")
    if preset.species_profile_id != "AION-TIGER-ANTHROPOMORPH-V1":
        raise ValueError("dimension preset must bind the AION tiger species profile")

    m = preset.measurement_map()
    missing = sorted(set(REQUIRED_DIMENSION_KEYS) - set(m))
    if missing:
        raise ValueError(f"missing required dimensions: {', '.join(missing)}")

    for item in preset.measurements:
        if item.value is not None and item.value <= 0:
            raise ValueError(f"dimension must be positive: {item.key}")
        if not item.provenance:
            raise ValueError(f"dimension requires provenance: {item.key}")
        if item.value is None and item.status != UNKNOWN_SOURCE_NOT_ESTABLISHED:
            raise ValueError(f"undefined dimension must declare UNKNOWN status: {item.key}")

    stature = m["stature_cm"].value
    head = m["head_height_cm"].value
    tail = m["tail_length_cm"].value
    if stature is None or head is None or tail is None:
        raise ValueError("core design dimensions must be numeric")
    if not (0.18 <= head / stature <= 0.22):
        raise ValueError("head/stature ratio outside this semi-realistic anthro preset envelope")
    if tail >= stature:
        raise ValueError("tail length must remain below standing stature for this preset")

    unknown = [item.key for item in preset.measurements if item.value is None]
    return {
        "result": "PASS",
        "preset_id": preset.preset_id,
        "dimension_count": str(len(preset.measurements)),
        "unknown_dimension_count": str(len(unknown)),
        "unknown_dimensions": ",".join(unknown),
        "canonical_effect": preset.canonical_effect,
        "biological_hybrid_claim": preset.biological_hybrid_claim,
    }
