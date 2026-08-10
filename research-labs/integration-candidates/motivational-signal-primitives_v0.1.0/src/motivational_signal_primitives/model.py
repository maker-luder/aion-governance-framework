from __future__ import annotations

from dataclasses import dataclass
from typing import Final

NONE: Final[str] = "NONE"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class MotivationalSignalPrimitive:
    """Minimal evidence-bound action-bias signal.

    This is a computational research primitive only. It does not establish
    felt affect, desire, volition, or motivational authority.
    """

    signal_id: str
    subject_ref: str
    context_ref: str
    source_event_id: str
    signal_kind: str
    intensity: float
    approach_bias: float
    avoidance_bias: float
    uncertainty: float
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    target_ref: str | None = None
    canonical_effect: str = NONE
    felt_experience_claim: str = NOT_ESTABLISHED
    motivational_authority_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("signal_id", "subject_ref", "context_ref", "source_event_id", "signal_kind"):
            _require_text(name, getattr(self, name))
        for name in ("intensity", "approach_bias", "avoidance_bias", "uncertainty"):
            _require_unit_interval(name, getattr(self, name))

        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty references")
        if not self.provenance_refs or any(not ref.strip() for ref in self.provenance_refs):
            raise ValueError("provenance_refs must contain non-empty references")
        if self.target_ref is not None:
            _require_text("target_ref", self.target_ref)

        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.felt_experience_claim != NOT_ESTABLISHED:
            raise ValueError("felt experience must remain NOT_ESTABLISHED")
        if self.motivational_authority_claim != NOT_ESTABLISHED:
            raise ValueError("motivational authority must remain NOT_ESTABLISHED")

    @property
    def signed_action_bias(self) -> float:
        """Positive favors approach; negative favors avoidance; zero is balanced."""
        return self.approach_bias - self.avoidance_bias

    @property
    def coactivation(self) -> float:
        """Shared activation without deciding whether it constitutes conflict."""
        return min(self.approach_bias, self.avoidance_bias)


@dataclass(frozen=True, slots=True)
class MotivationalSignalSet:
    """A subject/context-bound collection of signal primitives.

    Empty sets are valid so experimental removal of all signals can be
    represented without inventing an invalid state.
    """

    set_id: str
    subject_ref: str
    context_ref: str
    signals: tuple[MotivationalSignalPrimitive, ...]
    canonical_effect: str = NONE
    felt_experience_claim: str = NOT_ESTABLISHED
    motivational_authority_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("set_id", "subject_ref", "context_ref"):
            _require_text(name, getattr(self, name))

        ids = [signal.signal_id for signal in self.signals]
        if len(ids) != len(set(ids)):
            raise ValueError("signal_id values must be unique within a signal set")

        for signal in self.signals:
            if signal.subject_ref != self.subject_ref:
                raise ValueError("signal subject_ref must match signal-set subject_ref")
            if signal.context_ref != self.context_ref:
                raise ValueError("signal context_ref must match signal-set context_ref")

        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.felt_experience_claim != NOT_ESTABLISHED:
            raise ValueError("felt experience must remain NOT_ESTABLISHED")
        if self.motivational_authority_claim != NOT_ESTABLISHED:
            raise ValueError("motivational authority must remain NOT_ESTABLISHED")

    def total_approach_bias(self) -> float:
        return sum(signal.approach_bias for signal in self.signals)

    def total_avoidance_bias(self) -> float:
        return sum(signal.avoidance_bias for signal in self.signals)

    def signed_action_bias(self) -> float:
        return self.total_approach_bias() - self.total_avoidance_bias()
