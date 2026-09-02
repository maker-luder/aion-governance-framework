"""AION/Astra Bazi Core candidate public surface."""

from .database import Database
from .engine import (
    calculate_annual_cycle,
    calculate_four_pillars,
    calculate_luck_cycles,
    calculate_monthly_cycle,
    calculate_natal_profile,
    verify_derivation_hash,
)
from .repository import BaziCore
from .integrity import (
    SERIALIZATION_SCHEMA_VERSION,
    canonical_materialized_json,
    materialized_facts_hash,
)
from .traditional_extensions import (
    BirthSexMarker,
    DistributionFact,
    LuckStartFact,
    SOLAR_TERM_LONGITUDES,
    element_distribution_fact,
    independent_gregorian_day_pillar,
    luck_start_from_boundary_interval,
    ten_god_distribution_fact,
    traditional_luck_direction,
    validate_solar_term_sequence,
)
from .school_evidence import (
    BaziSchoolEvidence,
    SeasonalEvidenceFact,
    TransformationCandidateFact,
    build_bazi_school_evidence,
    derive_seasonal_evidence,
    derive_transformation_candidates,
    validate_school_evidence_tables,
)

from .month_structure import derive_month_structure, ziping_month_structure_profile

__all__ = [
    "derive_month_structure",
    "ziping_month_structure_profile",
    "BaziCore",
    "Database",
    "calculate_annual_cycle",
    "calculate_four_pillars",
    "calculate_luck_cycles",
    "calculate_monthly_cycle",
    "calculate_natal_profile",
    "verify_derivation_hash",
    "SERIALIZATION_SCHEMA_VERSION",
    "canonical_materialized_json",
    "materialized_facts_hash",
    "BirthSexMarker",
    "DistributionFact",
    "LuckStartFact",
    "SOLAR_TERM_LONGITUDES",
    "element_distribution_fact",
    "independent_gregorian_day_pillar",
    "luck_start_from_boundary_interval",
    "ten_god_distribution_fact",
    "traditional_luck_direction",
    "validate_solar_term_sequence",
    "BaziSchoolEvidence",
    "SeasonalEvidenceFact",
    "TransformationCandidateFact",
    "build_bazi_school_evidence",
    "derive_seasonal_evidence",
    "derive_transformation_candidates",
    "validate_school_evidence_tables",
]
