"""Explicit fail-closed domain errors."""


class BaziError(Exception):
    """Base Bazi component error."""


class ValidationError(BaziError):
    """Input or rule profile is invalid."""


class UnsupportedRangeError(BaziError):
    """Date falls outside the reviewed support range."""


class RuleProfileError(BaziError):
    """Rule profile is incomplete or unsupported."""


class RepositoryError(BaziError):
    """Persistence or integrity operation failed."""


class OwnerGateRequiredError(BaziError):
    """An operation requires explicit Owner approval."""
