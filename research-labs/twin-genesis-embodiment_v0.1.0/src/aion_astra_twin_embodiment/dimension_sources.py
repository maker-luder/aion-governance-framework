"""Source manifest for AION tiger anthropomorphic dimension research.

來源清單不代表所有來源具有同一證據力。
PRIMARY_TIGER_RESEARCH 可支持虎的直接觀察；COMMUNITY_PRACTITIONER
只支持量測欄位與製作流程；HUMAN_ANTHROPOMETRY 只支持人形基線。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class DimensionSource:
    source_id: str
    source_class: str
    title: str
    locator: str
    supports: tuple[str, ...]
    does_not_support: tuple[str, ...]
    evidence_note_zh: str


SOURCES: Final[tuple[DimensionSource, ...]] = (
    DimensionSource(
        "MEIRELES_2012_REPRODUCTIVE",
        "PRIMARY_TIGER_RESEARCH",
        "Morphological evaluation of the male reproductive system of tiger (Panthera tigris)",
        "doi:10.5216/cab.v13i4.14346",
        ("male_tiger_reproductive_anatomy", "testis_dimensions", "penile_urethra"),
        ("species_wide_normal_range", "anthropomorphic_target_dimensions"),
        "成年雄虎 N=1 解剖／組織學直接資料；可確認結構與該標本量測，不可當族群常模。",
    ),
    DimensionSource(
        "MAZAK_2010_CRANIOMETRY",
        "PRIMARY_TIGER_RESEARCH",
        "Craniometric variation in the tiger (Panthera tigris)",
        "doi:10.1016/j.mambio.2008.06.003",
        ("tiger_skull_measurement_system", "cranial_variation", "sexual_dimorphism"),
        ("single_fixed_tiger_skull", "anthropomorphic_head_validation"),
        "273 個野外來源虎顱骨的形態計量；顯示地理、性別與異速生長差異。",
    ),
    DimensionSource(
        "UDDIN_2022_FORELIMB",
        "PRIMARY_TIGER_RESEARCH",
        "Gross morphometric studies on scapula, humerus, radius, and ulna of the Royal Bengal Tiger",
        "https://exa.ai/library/publication/qvlth0zwvnc",
        ("tiger_scapula", "tiger_humerus", "tiger_radius", "tiger_ulna"),
        ("bipedal_segment_targets", "population_normal_range"),
        "成年孟加拉虎 N=1 乾骨直接量測；可作骨骼 reference observation。",
    ),
    DimensionSource(
        "TOMAR_2019_FEMUR",
        "PRIMARY_TIGER_RESEARCH",
        "Gross Anatomy of Femur in Royal Bengal Tiger (Panthera tigris)",
        "https://epubs.icar.org.in/index.php/IJVA/article/view/90509",
        ("tiger_femur_gross_anatomy", "five_adult_specimens"),
        ("numeric_femur_values_not_recovered", "anthropomorphic_femur_target"),
        "五具成年虎骨架；本輪可取得摘要與形態結論，但未取得可靠數字表，故不填造數值。",
    ),
    DimensionSource(
        "TOMAR_2026_TIBIA_FIBULA",
        "PRIMARY_TIGER_RESEARCH",
        "Morphological and Morphometrical Studies on the Tibia and Fibula of Tiger (Panthera tigris)",
        "https://epubs.icar.org.in/index.php/IJVA/article/view/180535",
        ("tiger_tibia_circumference", "tiger_fibula_length", "tiger_fibula_mass"),
        ("anthropomorphic_lower_leg_target",),
        "五隻成年虎直接量測；可作脛／腓骨 reference observation。",
    ),
    DimensionSource(
        "DUNN_2022_FORELIMB",
        "PRIMARY_TIGER_RESEARCH",
        "Muscular anatomy of the forelimb of tiger (Panthera tigris)",
        "doi:10.1111/joa.13636",
        ("tiger_forelimb_musculature", "pronation_supination_reference"),
        ("human_like_hand_validation", "bipedal_load_validation"),
        "虎前肢肌肉配置可用於工程轉譯，但不是人形上肢力學驗證。",
    ),
    DimensionSource(
        "DOUBE_2009_FELID_LIMB",
        "COMPARATIVE_FELID_RESEARCH",
        "Three-Dimensional Geometric Analysis of Felid Limb Bone Allometry",
        "doi:10.1371/journal.pone.0004742",
        ("felid_limb_allometry", "tiger_ct_reference"),
        ("direct_anthropomorphic_scaling",),
        "9 種貓科含虎的 CT 異速生長研究；支持『不能只做等比例放大』。",
    ),
    DimensionSource(
        "DAY_JAYNE_2007_LOCOMOTION",
        "COMPARATIVE_FELID_RESEARCH",
        "Interspecific scaling of the morphology and posture of the limbs during the locomotion of cats",
        "doi:10.1242/jeb.02703",
        ("felid_locomotor_scaling",),
        ("human_biped_locomotion",),
        "貓科四足運動比較資料；用來界定雙足 redesign 的必要性。",
    ),
    DimensionSource(
        "USFWS_YATES_2005_TIGER_GENITAL_ID",
        "INSTITUTIONAL_FORENSICS",
        "Distinguishing Real vs. Fake Tiger Penises, Identification Guide No. 6",
        "USFWS National Fish and Wildlife Forensics Laboratory, 2005",
        ("dried_specimen_exclusion_constraints", "tiger_baculum_shape"),
        ("live_penile_normal_range", "aion_target_genital_dimensions"),
        "野生動物鑑識指南；乾燥標本排除閾值只可當 forensic constraint，不可當活體尺寸。",
    ),
    DimensionSource(
        "TAIPEI_ZOO_TIGER",
        "INSTITUTIONAL_SPECIES_REFERENCE",
        "Tiger species profile",
        "Taipei Zoo",
        ("body_length_range", "tail_length_range", "shoulder_height_range", "body_mass_range"),
        ("anthropomorphic_target_validation",),
        "動物園物種範圍資料，可作外部包絡參考，不是 AION 的固定尺寸。",
    ),
    DimensionSource(
        "NASA_HIDH",
        "HUMAN_ANTHROPOMETRY",
        "Human Integration Design Handbook",
        "NASA/SP-2010-3407 Rev 1",
        ("human_stature", "human_reach", "human_body_breadth", "human_clearance"),
        ("tiger_biology", "human_tiger_hybrid_validation"),
        "人因工程資料，只提供直立雙足與操作空間的人形基線。",
    ),
    DimensionSource(
        "SPIRITPANDA_DTD",
        "COMMUNITY_PRACTITIONER",
        "DTD & Measurement Guide",
        "https://www.spiritpandacostumes.com/dtd-measurements-guide",
        ("fursuit_measurement_fields", "a_pose_dtd", "head_hand_measurement_protocol"),
        ("tiger_biology", "biological_normal_range"),
        "製作者實務來源；支持 inseam/outseam、torso、head、hand 等量測欄位與姿勢。",
    ),
    DimensionSource(
        "FOK_MEASUREMENTS",
        "COMMUNITY_PRACTITIONER",
        "Furred Out Kreations Measurements",
        "https://furredoutkreations.wixsite.com/home/measurements",
        ("fursuit_measurement_fields", "pupil_spacing", "tail_location", "limb_circumference"),
        ("tiger_biology", "biological_normal_range"),
        "製作者實務來源；提供 20+ 人體／頭部定位量測欄位。",
    ),
    DimensionSource(
        "FRECKLED_CAT_MEASUREMENTS",
        "COMMUNITY_PRACTITIONER",
        "How to Measure for a Commission",
        "https://freckledcatcreations.weebly.com/how-to-measure-for-a-commission.html",
        ("head_fit", "pupil_distance", "shoulder_back_width", "hand_foot_measurement"),
        ("tiger_biology",),
        "製作者實務來源；特別有瞳距、頭圍、背寬與 paw fitting 欄位。",
    ),
    DimensionSource(
        "FURNFURRY_MEASURE",
        "COMMUNITY_PRACTITIONER",
        "Custom Fursuit Measurement Guide",
        "https://furnfurry.com/measure",
        ("plantigrade_fields", "digitigrade_fields", "tail_placement", "head_hand_foot_fields"),
        ("tiger_biology",),
        "製作者實務來源；把 plantigrade 與 digitigrade 所需欄位分開。",
    ),
    DimensionSource(
        "KEMONO_LINE_DTD",
        "COMMUNITY_PRACTITIONER",
        "DTD Guide",
        "https://kemono-line.jp/dtd_en.html",
        ("duct_tape_dummy", "tail_location", "head_body_capture"),
        ("tiger_biology",),
        "Kemono 製作實務來源；支持 DTD、尾位標記與完整身體外形捕捉。",
    ),
)


def build_dimension_source_manifest() -> tuple[DimensionSource, ...]:
    return SOURCES


def source_map() -> dict[str, DimensionSource]:
    return {source.source_id: source for source in SOURCES}


def validate_dimension_source_manifest() -> dict[str, str]:
    ids = [source.source_id for source in SOURCES]
    if len(ids) != len(set(ids)):
        raise ValueError("dimension source ids must be unique")
    if not any(source.source_class == "PRIMARY_TIGER_RESEARCH" for source in SOURCES):
        raise ValueError("at least one primary tiger research source is required")
    if not any(source.source_class == "COMMUNITY_PRACTITIONER" for source in SOURCES):
        raise ValueError("at least one community practitioner source is required")
    return {
        "result": "PASS",
        "source_count": str(len(SOURCES)),
        "primary_tiger_source_count": str(sum(s.source_class == "PRIMARY_TIGER_RESEARCH" for s in SOURCES)),
        "community_practitioner_source_count": str(sum(s.source_class == "COMMUNITY_PRACTITIONER" for s in SOURCES)),
    }
