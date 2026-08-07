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

__all__ = [
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
]
