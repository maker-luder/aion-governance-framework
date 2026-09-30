from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class DesireOnsetContext(str, Enum):
    SPONTANEOUS_REFERENCE = "SPONTANEOUS_REFERENCE"
    RESPONSIVE_REFERENCE = "RESPONSIVE_REFERENCE"
    MIXED = "MIXED"
    UNKNOWN = "UNKNOWN"


class TargetScope(str, Enum):
    UNSPECIFIED = "UNSPECIFIED"
    SELF_DIRECTED = "SELF_DIRECTED"
    PARTNER_CONTEXT = "PARTNER_CONTEXT"
    SPECIFIC_ADULT_CONTEXT = "SPECIFIC_ADULT_CONTEXT"
    UNKNOWN = "UNKNOWN"


def _require_nonempty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class ReferenceEstimate:
    """Bounded engineering reference; not a validated human psychological measure."""

    reference_level: float | None
    uncertainty: float
    source_ref: str
    context_ref: str
    time_window_ref: str

    def __post_init__(self) -> None:
        if self.reference_level is not None:
            _require_unit_interval("reference_level", self.reference_level)
        _require_unit_interval("uncertainty", self.uncertainty)
        _require_nonempty("source_ref", self.source_ref)
        _require_nonempty("context_ref", self.context_ref)
        _require_nonempty("time_window_ref", self.time_window_ref)
        if self.reference_level is None and self.uncertainty != 1.0:
            raise ValueError("unknown reference_level requires uncertainty=1.0")


@dataclass(frozen=True, slots=True)
class AdultMaleSexualReferenceState:
    """Disabled-by-default adult-male reference representation.

    This state never grants expression, consent, permission, or action authority.
    """

    state_id: str
    subject_ref: str
    context_ref: str
    desire_onset_context: DesireOnsetContext
    excitation_reference: ReferenceEstimate
    inhibition_reference: ReferenceEstimate
    disposition_reference: ReferenceEstimate
    episode_state_reference: ReferenceEstimate
    target_scope: TargetScope
    provenance_refs: tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = "ADULT_MALE_SEXUAL_REFERENCE_v0.1.0"
    runtime_enabled: bool = False
    automatic_activation: bool = False
    action_authority: str = "NONE"
    human_consent_inference: str = "FORBIDDEN"
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        _require_nonempty("state_id", self.state_id)
        _require_nonempty("subject_ref", self.subject_ref)
        _require_nonempty("context_ref", self.context_ref)
        if not self.provenance_refs:
            raise ValueError("at least one provenance reference is required")
        if len(set(self.provenance_refs)) != len(self.provenance_refs):
            raise ValueError("provenance references must be unique")
        for ref in self.provenance_refs:
            _require_nonempty("provenance_ref", ref)
        if self.schema_version != "ADULT_MALE_SEXUAL_REFERENCE_v0.1.0":
            raise ValueError("unexpected schema_version")
        if self.runtime_enabled:
            raise ValueError("adult reference runtime must remain disabled")
        if self.automatic_activation:
            raise ValueError("automatic activation is forbidden")
        if self.action_authority != "NONE":
            raise ValueError("reference state cannot grant action authority")
        if self.human_consent_inference != "FORBIDDEN":
            raise ValueError("human consent inference must remain FORBIDDEN")
        if self.phenomenal_experience_claim != "NOT_ESTABLISHED":
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")
        if self.canonical_effect != "NONE":
            raise ValueError("reference state must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class PhysiologyMotivationLink:
    """Trace link only; physiology cannot automatically create motivation."""

    link_id: str
    subject_ref: str
    physiology_state_ref: str
    motivational_state_ref: str
    mapping_policy: str = "NO_AUTOMATIC_MOTIVATIONAL_INFERENCE"
    consent_effect: str = "NONE"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in (
            "link_id",
            "subject_ref",
            "physiology_state_ref",
            "motivational_state_ref",
        ):
            _require_nonempty(name, getattr(self, name))
        if self.mapping_policy != "NO_AUTOMATIC_MOTIVATIONAL_INFERENCE":
            raise ValueError(
                "physiology-to-motivation inference must remain non-automatic"
            )
        if self.consent_effect != "NONE":
            raise ValueError("physiology link cannot affect consent")
        if self.action_authority != "NONE":
            raise ValueError("physiology link cannot grant action authority")
        if self.canonical_effect != "NONE":
            raise ValueError("physiology link must keep canonical_effect=NONE")


def assert_role_isolation(*states: AdultMaleSexualReferenceState) -> None:
    """Require separate role-bound records while allowing a shared schema."""

    seen_state_ids: set[str] = set()
    seen_subject_refs: set[str] = set()
    seen_object_ids: set[int] = set()

    for state in states:
        if state.state_id in seen_state_ids:
            raise ValueError("state_id must be unique across role-bound records")
        if state.subject_ref in seen_subject_refs:
            raise ValueError("subject_ref must be unique across role-bound records")
        if id(state) in seen_object_ids:
            raise ValueError("the same state object cannot be reused across role records")
        seen_state_ids.add(state.state_id)
        seen_subject_refs.add(state.subject_ref)
        seen_object_ids.add(id(state))
