from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

NONE: Final[str] = "NONE"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


class ChannelKind(str, Enum):
    OBSERVATION = "OBSERVATION"
    INTERNAL_OBSERVATION = "INTERNAL_OBSERVATION"
    ACTION = "ACTION"


@dataclass(frozen=True, slots=True)
class CapabilityChannel:
    """A declared embodiment I/O capability, not a felt modality claim."""

    channel_id: str
    kind: ChannelKind
    signal_kind: str
    enabled: bool
    unit_ref: str
    latency_ms: float
    resolution: float
    noise_floor: float
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    frame_ref: str | None = None
    canonical_effect: str = NONE
    phenomenal_experience_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("channel_id", "signal_kind", "unit_ref"):
            _require_text(name, getattr(self, name))
        if self.frame_ref is not None:
            _require_text("frame_ref", self.frame_ref)
        if self.latency_ms < 0.0:
            raise ValueError("latency_ms must be non-negative")
        if self.resolution < 0.0:
            raise ValueError("resolution must be non-negative")
        if self.noise_floor < 0.0:
            raise ValueError("noise_floor must be non-negative")
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty references")
        if not self.provenance_refs or any(not ref.strip() for ref in self.provenance_refs):
            raise ValueError("provenance_refs must contain non-empty references")
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.phenomenal_experience_claim != NOT_ESTABLISHED:
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class EmbodimentCapabilityProfile:
    """Agent/embodiment binding plus declared observation/action channels."""

    profile_id: str
    agent_id: str
    embodiment_id: str
    template_ref: str
    channels: tuple[CapabilityChannel, ...]
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE
    body_ownership_claim: str = NOT_ESTABLISHED
    gender_identity_claim: str = NOT_ESTABLISHED
    subjectivity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("profile_id", "agent_id", "embodiment_id", "template_ref"):
            _require_text(name, getattr(self, name))
        ids = [channel.channel_id for channel in self.channels]
        if len(ids) != len(set(ids)):
            raise ValueError("channel_id values must be unique within a capability profile")
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty references")
        if not self.provenance_refs or any(not ref.strip() for ref in self.provenance_refs):
            raise ValueError("provenance_refs must contain non-empty references")
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.body_ownership_claim != NOT_ESTABLISHED:
            raise ValueError("body ownership must remain NOT_ESTABLISHED")
        if self.gender_identity_claim != NOT_ESTABLISHED:
            raise ValueError("gender identity must remain NOT_ESTABLISHED")
        if self.subjectivity_claim != NOT_ESTABLISHED:
            raise ValueError("subjectivity must remain NOT_ESTABLISHED")

    def enabled_channels(self, kind: ChannelKind | None = None) -> tuple[CapabilityChannel, ...]:
        return tuple(
            channel
            for channel in self.channels
            if channel.enabled and (kind is None or channel.kind == kind)
        )

    def get_channel(self, channel_id: str) -> CapabilityChannel | None:
        for channel in self.channels:
            if channel.channel_id == channel_id:
                return channel
        return None


@dataclass(frozen=True, slots=True)
class ObservationSample:
    """Evidence-bound observation; separate from commands and internal interpretations."""

    sample_id: str
    subject_ref: str
    embodiment_id: str
    channel_id: str
    source_ref: str
    value: float
    unit_ref: str
    timestamp: str
    confidence: float
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    frame_ref: str | None = None
    canonical_effect: str = NONE
    body_sensation_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("sample_id", "subject_ref", "embodiment_id", "channel_id", "source_ref", "unit_ref", "timestamp"):
            _require_text(name, getattr(self, name))
        if self.frame_ref is not None:
            _require_text("frame_ref", self.frame_ref)
        _require_unit_interval("confidence", self.confidence)
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty references")
        if not self.provenance_refs or any(not ref.strip() for ref in self.provenance_refs):
            raise ValueError("provenance_refs must contain non-empty references")
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.body_sensation_claim != NOT_ESTABLISHED:
            raise ValueError("body sensation must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class ActionCommand:
    """Evidence-bound action command, explicitly distinct from an observation sample."""

    command_id: str
    subject_ref: str
    embodiment_id: str
    channel_id: str
    target_ref: str
    value: float
    unit_ref: str
    issued_at: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE
    volition_claim: str = NOT_ESTABLISHED
    motivational_authority_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("command_id", "subject_ref", "embodiment_id", "channel_id", "target_ref", "unit_ref", "issued_at"):
            _require_text(name, getattr(self, name))
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty references")
        if not self.provenance_refs or any(not ref.strip() for ref in self.provenance_refs):
            raise ValueError("provenance_refs must contain non-empty references")
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.volition_claim != NOT_ESTABLISHED:
            raise ValueError("volition must remain NOT_ESTABLISHED")
        if self.motivational_authority_claim != NOT_ESTABLISHED:
            raise ValueError("motivational authority must remain NOT_ESTABLISHED")
