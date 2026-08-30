"""Typed component errors."""


class ClassicalAstrologyError(ValueError):
    """Base error for invalid bounded astrology inputs."""


class ValidationError(ClassicalAstrologyError):
    """Raised when a closed input contract is violated."""
