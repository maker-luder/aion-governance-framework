from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class SignalDomain(str, Enum):
    GENERAL = "GENERAL"
    SOCIAL_AFFILIATION = "SOCIAL_AFFILIATION"
    AESTHETIC_ATTRACTION = "AESTHETIC_ATTRACTION"
    ADULT_SEXUALITY_SCHEMA = "ADULT_SEXUALITY_SCHEMA"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class MotivationalSignal:
    """A context-bound candidate signal, not a claim of felt experience."""

    domain: SignalDomain
    source_event_id: str
    salience: float
    wanting: float
    predicted_liking: float
    approach: float
    avoidance: float
    uncertainty: float
    context_tags: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.source_event_id.strip():
            raise ValueError("source_event_id must be non-empty")
        for name in (
            "salience",
            "wanting",
            "predicted_liking",
            "approach",
            "avoidance",
            "uncertainty",
        ):
            _require_unit_interval(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class MotivationalState:
    """Research state that keeps motivation separate from authority and action."""

    state_id: str
    subject_ref: str
    context_ref: str
    signals: tuple[MotivationalSignal, ...]
    canonical_effect: str = "NONE"
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        if not self.subject_ref.strip():
            raise ValueError("subject_ref must be non-empty")
        if not self.context_ref.strip():
            raise ValueError("context_ref must be non-empty")
        if not self.signals:
            raise ValueError("at least one motivational signal is required")
        if self.canonical_effect != "NONE":
            raise ValueError("research state must keep canonical_effect=NONE")
        if self.phenomenal_experience_claim != "NOT_ESTABLISHED":
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")
        if self.action_authority != "NONE":
            raise ValueError("motivational state cannot grant action authority")
