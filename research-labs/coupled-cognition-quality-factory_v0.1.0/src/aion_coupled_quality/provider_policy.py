from __future__ import annotations

_PROHIBITED_MARKERS = ("anthropic", "claude")


class ProhibitedProviderError(ValueError):
    pass


def assert_provider_allowed(identifier: str, *, context: str = "quality-factory") -> str:
    normalized = identifier.strip().lower()
    if any(marker in normalized for marker in _PROHIBITED_MARKERS):
        raise ProhibitedProviderError(
            f"{context}: provider/model prohibited by inherited non-overridable research policy lock"
        )
    return identifier
