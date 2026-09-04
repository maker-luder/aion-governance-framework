"""SANDBOX_ONLY engineering pilot derived from white paper v0.10.

This package implements machine-checkable identity-governance *mechanisms*
described in AION-WP-INT-010 (2026-06-25). It does not establish
subjectivity, phenomenal experience, identity continuity as lived identity,
or ethical informed consent.

AUTHORITY = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
"""

from .service import AirIdentityService
from .auth import AuthContext, PRINCIPAL_ROLES
from .models import IdentityStatus, MemorySource, EncounterStatus

__all__ = [
    "AirIdentityService",
    "AuthContext",
    "PRINCIPAL_ROLES",
    "IdentityStatus",
    "MemorySource",
    "EncounterStatus",
]
