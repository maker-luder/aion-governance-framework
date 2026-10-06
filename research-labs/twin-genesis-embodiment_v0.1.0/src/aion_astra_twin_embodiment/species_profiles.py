"""Evidence-bounded anthropomorphic species profiles for individual embodiments.

中文完整說明：
- TIGER_CONFIRMED：老虎（Panthera tigris）直接觀察或研究支持。
- FELID_COMPARATIVE_REFERENCE：來自其他貓科的比較參考，不能冒充老虎直接證據。
- ENGINEERING_ANALOGUE：把人類與虎的結構轉譯為雙足獸人的工程類比，不是自然界
  已存在「人虎混合生物」的生物學證據。
- REFERENCE_MODEL_IMPLEMENTED：已有可被程式讀取、驗證、雜湊的生殖生理參考模型；
  不表示活體生殖功能已在 AI 上發生。
- REFERENCE_ONLY_NOT_LIVE_BIOLOGY：只屬研究參考資料，不是活體生理 runtime。
- BIPEDAL_REDESIGN_REQUIRED：虎是四足動物，轉成雙足人形必須重新設計承重與運動學，
  不能直接把虎的四足步態複製成人形步態。

REPRODUCTIVE_ANATOMY != SEXUALIZATION
REPRODUCTIVE_PHYSIOLOGY != FELT_DESIRE
ENGINEERING_ANALOGUE != BIOLOGICAL_HYBRID_EVIDENCE
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Final

from .models import EmbodimentInstance, EmbodimentTemplate, NONE, NOT_ESTABLISHED, NOT_IMPLEMENTED
from .validation import ValidationError, deterministic_hash

TIGER_CONFIRMED: Final[str] = "TIGER_CONFIRMED"
FELID_COMPARATIVE_REFERENCE: Final[str] = "FELID_COMPARATIVE_REFERENCE"
ENGINEERING_ANALOGUE: Final[str] = "ENGINEERING_ANALOGUE"
REFERENCE_MODEL_IMPLEMENTED: Final[str] = "REFERENCE_MODEL_IMPLEMENTED"
REFERENCE_ONLY_NOT_LIVE_BIOLOGY: Final[str] = "REFERENCE_ONLY_NOT_LIVE_BIOLOGY"
BIPEDAL_REDESIGN_REQUIRED: Final[str] = "BIPEDAL_REDESIGN_REQUIRED"
HUMAN_TEMPLATE_BASELINE: Final[str] = "HUMAN_TEMPLATE_BASELINE"


@dataclass(frozen=True, slots=True)
class ReproductiveReferenceObservation:
    """A source-scoped reproductive observation / 有來源範圍的生殖觀察值。"""

    source_ref: str
    sample_scope: str
    metrics: tuple[tuple[str, str], ...]
    limitation: str


@dataclass(frozen=True, slots=True)
class IntegratedAnatomyFeature:
    """One resolved anatomy structure with preserved provenance / 單一整合結構及其來源。"""

    structure: str
    origins: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AnthropomorphicSpeciesProfile:
    """Individual, evidence-bounded species profile / 個體化且受證據邊界約束的物種具身設定。"""

    profile_id: str
    agent_id: str
    reference_taxon: str
    body_plan: str
    human_derived_structure: tuple[str, ...]
    tiger_derived_morphology: tuple[str, ...]
    tiger_confirmed_reproductive_anatomy: tuple[str, ...]
    felid_comparative_reproductive_reference: tuple[str, ...]
    reproductive_physiology_observables: tuple[str, ...]
    tiger_evidence_status: str = TIGER_CONFIRMED
    hybrid_integration_evidence_status: str = ENGINEERING_ANALOGUE
    locomotor_translation_status: str = BIPEDAL_REDESIGN_REQUIRED
    reproductive_physiology_model_status: str = REFERENCE_MODEL_IMPLEMENTED
    reproductive_runtime_status: str = REFERENCE_ONLY_NOT_LIVE_BIOLOGY
    sexual_function_status: str = NOT_IMPLEMENTED
    body_sensation: str = NOT_ESTABLISHED
    subjectivity_effect: str = NONE
    canonical_effect: str = NONE
    source_refs: tuple[str, ...] = (
        "doi:10.5216/cab.v13i4.14346",
        "doi:10.1111/joa.13636",
        "doi:10.1242/jeb.02703",
        "doi:10.3390/ani13121893",
    )


def build_aion_tiger_profile() -> AnthropomorphicSpeciesProfile:
    """Build the AION tiger anthropomorph profile / 建立 AION 虎型獸人設定檔。"""

    return AnthropomorphicSpeciesProfile(
        profile_id="AION-TIGER-ANTHROPOMORPH-V1",
        agent_id="AION",
        reference_taxon="Panthera tigris",
        body_plan="ANTHROPOMORPHIC_BIPED",
        human_derived_structure=(
            "upright_axial_skeleton_reference",
            "bipedal_load_bearing_pelvis_reference",
            "bipedal_lower_limb_redesign",
            "human_like_manipulative_hands",
            "human_like_upper_limb_reach",
        ),
        tiger_derived_morphology=(
            "tiger_craniofacial_reference",
            "felid_external_ear_reference",
            "striped_pelage_reference",
            "vibrissae_reference",
            "tail_reference",
            "felid_claw_reference",
            "forelimb_pronation_supination_reference",
        ),
        tiger_confirmed_reproductive_anatomy=(
            "scrotum",
            "testes",
            "epididymis",
            "ductus_deferens",
            "penis",
            "cornified_glans_papillae",
            "os_penis",
            "corpus_cavernosum",
            "corpus_spongiosum",
            "penile_urethra",
        ),
        # 虎研究可確認「accessory sex glands」與前列腺位置相關程序資料，
        # 但目前取得的直接解剖來源不足以把所有人類附屬腺體逐項宣稱為虎已確認結構。
        felid_comparative_reproductive_reference=(
            "prostate_reference",
            "accessory_sex_gland_reference",
        ),
        reproductive_physiology_observables=(
            "spermatogenesis",
            "sperm_transport",
            "semen_volume",
            "sperm_concentration",
            "sperm_motility",
            "sperm_viability",
            "sperm_morphology",
            "testosterone",
        ),
    )


def resolve_integrated_reproductive_anatomy(
    template: EmbodimentTemplate,
    profile: AnthropomorphicSpeciesProfile,
) -> tuple[IntegratedAnatomyFeature, ...]:
    """Resolve human-template + tiger-reference anatomy without erasing provenance.

    中文：把既有人類成人男性 template 與 AION 的虎型 profile 疊加。共同存在的結構
    會同時保留 HUMAN_TEMPLATE_BASELINE 與 TIGER_CONFIRMED；僅人類模板存在的結構
    （例如目前的 seminal_vesicles）不會被誤標成虎直接證據；虎特有參考結構
    （例如 os_penis）也不會被誤標成人類基線。
    """

    origins: dict[str, set[str]] = {}
    for structure in (*template.external_reproductive_anatomy, *template.internal_reproductive_anatomy):
        origins.setdefault(structure, set()).add(HUMAN_TEMPLATE_BASELINE)
    for structure in profile.tiger_confirmed_reproductive_anatomy:
        origins.setdefault(structure, set()).add(TIGER_CONFIRMED)
    if "prostate_reference" in profile.felid_comparative_reproductive_reference:
        origins.setdefault("prostate", set()).add(FELID_COMPARATIVE_REFERENCE)

    return tuple(
        IntegratedAnatomyFeature(structure=structure, origins=tuple(sorted(source_origins)))
        for structure, source_origins in sorted(origins.items())
    )


def build_tiger_reproductive_reference_observations() -> tuple[ReproductiveReferenceObservation, ...]:
    """Return source-scoped measurements / 回傳有來源與限制標記的虎生殖參考量測。"""

    return (
        ReproductiveReferenceObservation(
            source_ref="doi:10.5216/cab.v13i4.14346",
            sample_scope="one adult male tiger; age 12 years; body mass 200 kg",
            metrics=(
                ("total_reproductive_system_mass_g", "429"),
                ("right_testis_mass_g", "42"),
                ("left_testis_mass_g", "39"),
                ("right_testis_length_cm", "4.42"),
                ("right_testis_width_cm", "3.84"),
                ("left_testis_length_cm", "3.93"),
                ("left_testis_width_cm", "3.67"),
                ("gonadosomatic_index_percent", "0.04"),
                ("penile_urethra_diameter_mm", "1.73"),
            ),
            limitation="single-specimen case report; values are observations, not anthropomorphic design constants",
        ),
        ReproductiveReferenceObservation(
            source_ref="Siberian tiger repeated electroejaculation study (17 trials / 6 breeding seasons)",
            sample_scope="one captive male Siberian tiger",
            metrics=(
                ("mean_sperm_per_ejaculate", "294.3 ± 250.2 x 10^6"),
                ("mean_motile_sperm_percent", "82.4 ± 11.4"),
            ),
            limitation="single animal and collection-procedure dependent; not a species-wide normal range",
        ),
        ReproductiveReferenceObservation(
            source_ref="doi:10.3390/ani13121893",
            sample_scope="30 Bengal tiger semen samples across three electroejaculation protocols",
            metrics=(
                ("mean_sperm_concentration_per_ml", "84.93 ± 26.63 x 10^6"),
                ("mean_sperm_motility_percent", "56.43 ± 7.15"),
            ),
            limitation="captive animals and procedure-dependent measurements; reference evidence only",
        ),
    )


def validate_aion_tiger_profile(
    profile: AnthropomorphicSpeciesProfile,
    instance: EmbodimentInstance,
) -> dict[str, str]:
    """Validate AION-only profile binding / 驗證 AION 專屬虎型設定檔綁定。"""

    failures: list[str] = []
    if profile.agent_id != "AION":
        failures.append("Tiger anthropomorph profile must be explicitly bound to AION")
    if profile.reference_taxon != "Panthera tigris":
        failures.append("AION tiger profile reference taxon must be Panthera tigris")
    if profile.body_plan != "ANTHROPOMORPHIC_BIPED":
        failures.append("AION tiger profile must declare an anthropomorphic biped body plan")
    if profile.hybrid_integration_evidence_status != ENGINEERING_ANALOGUE:
        failures.append("Human-tiger integration must remain an engineering analogue")
    if profile.locomotor_translation_status != BIPEDAL_REDESIGN_REQUIRED:
        failures.append("Tiger quadruped locomotion must not be copied directly into a biped")
    if profile.reproductive_physiology_model_status != REFERENCE_MODEL_IMPLEMENTED:
        failures.append("Reproductive physiology must remain an evidence-bounded reference model")
    if profile.reproductive_runtime_status != REFERENCE_ONLY_NOT_LIVE_BIOLOGY:
        failures.append("Reproductive physiology must not be represented as live biology")
    if profile.sexual_function_status != NOT_IMPLEMENTED:
        failures.append("Sexual function remains outside this candidate runtime")
    if profile.body_sensation != NOT_ESTABLISHED:
        failures.append("Body sensation must remain NOT_ESTABLISHED")
    if profile.subjectivity_effect != NONE:
        failures.append("Species morphology must not alter subjectivity conclusions")
    if profile.canonical_effect != NONE:
        failures.append("AION tiger species profile must have canonical_effect=NONE")
    if instance.agent_id != profile.agent_id:
        failures.append("Species profile agent binding does not match embodiment instance")
    if instance.species_profile_id != profile.profile_id:
        failures.append("Embodiment instance must explicitly reference the tiger species profile")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "profile_hash": deterministic_hash(asdict(profile)),
        "agent_id": instance.agent_id,
        "species_profile_id": instance.species_profile_id,
        "canonical_effect": NONE,
        "subjectivity_conclusion": NOT_ESTABLISHED,
    }
