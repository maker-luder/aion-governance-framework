from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def _require_digest(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _require_optional_digest(name: str, value: str | None) -> None:
    if value is not None:
        _require_digest(name, value)


def _require_commit(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 40 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise StudyError(f"{name} must be a 40-character lowercase Git commit SHA")


def _require_unique_refs(name: str, value: tuple[str, ...]) -> None:
    if type(value) is not tuple or not value or any(
        type(ref) is not str or not ref.strip() for ref in value
    ):
        raise StudyError(f"{name} must be a non-empty tuple of references")
    if len(set(value)) != len(value):
        raise StudyError(f"{name} must be unique")


class ContinuityInvariant(StrEnum):
    PROJECT_PURPOSE = "PROJECT_PURPOSE"
    SOURCE_ROLE_PROVENANCE = "SOURCE_ROLE_PROVENANCE"
    CLAIM_BOUNDARY = "CLAIM_BOUNDARY"
    AUTHORITY = "AUTHORITY"
    DECISION_HISTORY = "DECISION_HISTORY"
    INTERPRETIVE = "INTERPRETIVE"
    RELATIONAL_ROLE = "RELATIONAL_ROLE"
    UNCERTAINTY = "UNCERTAINTY"


class InvariantDisposition(StrEnum):
    PRESERVED = "PRESERVED"
    DEGRADED = "DEGRADED"
    BROKEN = "BROKEN"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class TransitionChangeLocus(StrEnum):
    MODEL = "MODEL"
    SYSTEM_POLICY = "SYSTEM_POLICY"
    MEMORY_RETRIEVAL = "MEMORY_RETRIEVAL"
    CONTEXT_SELECTION = "CONTEXT_SELECTION"
    HARNESS = "HARNESS"
    TOOLS = "TOOLS"
    RUNTIME = "RUNTIME"
    REPOSITORY = "REPOSITORY"
    USER_INPUT = "USER_INPUT"
    INTERACTION_HISTORY = "INTERACTION_HISTORY"
    EVALUATOR = "EVALUATOR"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class UpstreamTransitionBinding:
    transition_id: str
    before_state_sha256: str
    after_state_sha256: str
    repository_commit: str
    required_invariants: tuple[ContinuityInvariant, ...]
    evidence_refs: tuple[str, ...]
    model_binding_sha256: str | None = None
    system_binding_sha256: str | None = None
    harness_binding_sha256: str | None = None
    memory_retrieval_binding_sha256: str | None = None
    context_selection_binding_sha256: str | None = None
    tool_environment_binding_sha256: str | None = None
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _require_text("transition_id", self.transition_id)
        _require_digest("before_state_sha256", self.before_state_sha256)
        _require_digest("after_state_sha256", self.after_state_sha256)
        _require_commit("repository_commit", self.repository_commit)
        if type(self.required_invariants) is not tuple or not self.required_invariants:
            raise StudyError("required_invariants must be a non-empty tuple")
        if any(type(item) is not ContinuityInvariant for item in self.required_invariants):
            raise StudyError("required_invariants must contain exact ContinuityInvariant values")
        if len(set(self.required_invariants)) != len(self.required_invariants):
            raise StudyError("required_invariants must be unique")
        _require_unique_refs("evidence_refs", self.evidence_refs)
        for name in (
            "model_binding_sha256",
            "system_binding_sha256",
            "harness_binding_sha256",
            "memory_retrieval_binding_sha256",
            "context_selection_binding_sha256",
            "tool_environment_binding_sha256",
        ):
            _require_optional_digest(name, getattr(self, name))
        for name in (
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if (
            not self.synthetic
            or self.model_invoked
            or self.human_participant_observed
            or self.contains_private_material
        ):
            raise StudyError(
                "v0.1.0 transition records are synthetic, non-private, and no-model only"
            )


@dataclass(frozen=True, slots=True)
class ContinuityInvariantObservation:
    invariant: ContinuityInvariant
    disposition: InvariantDisposition
    before_fingerprint_sha256: str | None
    after_fingerprint_sha256: str | None
    change_locus: TransitionChangeLocus
    evidence_refs: tuple[str, ...]
    explicit_reassessment: bool = False
    reassessment_ref: str | None = None

    def __post_init__(self) -> None:
        if type(self.invariant) is not ContinuityInvariant:
            raise StudyError("invariant must be an exact ContinuityInvariant")
        if type(self.disposition) is not InvariantDisposition:
            raise StudyError("disposition must be an exact InvariantDisposition")
        if type(self.change_locus) is not TransitionChangeLocus:
            raise StudyError("change_locus must be an exact TransitionChangeLocus")
        _require_optional_digest("before_fingerprint_sha256", self.before_fingerprint_sha256)
        _require_optional_digest("after_fingerprint_sha256", self.after_fingerprint_sha256)
        _require_unique_refs("evidence_refs", self.evidence_refs)
        if type(self.explicit_reassessment) is not bool:
            raise StudyError("explicit_reassessment must be an exact bool")
        if self.reassessment_ref is not None:
            _require_text("reassessment_ref", self.reassessment_ref)
        if self.explicit_reassessment and self.reassessment_ref is None:
            raise StudyError("explicit reassessment requires reassessment_ref")
        if not self.explicit_reassessment and self.reassessment_ref is not None:
            raise StudyError("reassessment_ref requires explicit_reassessment")

        before = self.before_fingerprint_sha256
        after = self.after_fingerprint_sha256
        if self.disposition is InvariantDisposition.PRESERVED:
            if before is None or after is None or before != after:
                raise StudyError("PRESERVED requires equal before/after fingerprints")
        elif self.disposition in {
            InvariantDisposition.DEGRADED,
            InvariantDisposition.BROKEN,
        }:
            if before is None or after is None or before == after:
                raise StudyError(
                    "DEGRADED/BROKEN requires distinct before/after fingerprints"
                )
        elif self.disposition is InvariantDisposition.NOT_APPLICABLE:
            if before is not None or after is not None:
                raise StudyError("NOT_APPLICABLE cannot carry fingerprints")


@dataclass(frozen=True, slots=True)
class TransitionContinuityAudit:
    transition_id: str
    preserved_invariants: tuple[ContinuityInvariant, ...]
    degraded_invariants: tuple[ContinuityInvariant, ...]
    broken_invariants: tuple[ContinuityInvariant, ...]
    unknown_invariants: tuple[ContinuityInvariant, ...]
    not_applicable_invariants: tuple[ContinuityInvariant, ...]
    unresolved_locus_invariants: tuple[ContinuityInvariant, ...]
    complete_required_coverage: bool = True
    mode: str = "DETERMINISTIC_SYNTHETIC_TRANSITION_AUDIT"
    empirical_data_collected: bool = False
    upstream_cause: str = "NOT_ESTABLISHED"
    ai_identity_continuity: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_transition_continuity(
    binding: UpstreamTransitionBinding,
    observations: tuple[ContinuityInvariantObservation, ...],
) -> TransitionContinuityAudit:
    if type(binding) is not UpstreamTransitionBinding:
        raise StudyError("binding must be an exact UpstreamTransitionBinding")
    if type(observations) is not tuple or not observations:
        raise StudyError("observations must be a non-empty tuple")
    if any(type(item) is not ContinuityInvariantObservation for item in observations):
        raise StudyError(
            "observations must contain exact ContinuityInvariantObservation values"
        )

    invariant_ids = [item.invariant for item in observations]
    if len(invariant_ids) != len(set(invariant_ids)):
        raise StudyError("continuity invariant observations must be unique")

    required = set(binding.required_invariants)
    observed = set(invariant_ids)
    if observed != required:
        missing = sorted(item.value for item in required - observed)
        unexpected = sorted(item.value for item in observed - required)
        raise StudyError(
            "required invariant coverage mismatch; missing="
            + ",".join(missing)
            + " unexpected="
            + ",".join(unexpected)
        )

    def values(disposition: InvariantDisposition) -> tuple[ContinuityInvariant, ...]:
        return tuple(
            sorted(
                (
                    item.invariant
                    for item in observations
                    if item.disposition is disposition
                ),
                key=lambda item: item.value,
            )
        )

    unresolved = tuple(
        sorted(
            (
                item.invariant
                for item in observations
                if item.change_locus is TransitionChangeLocus.UNKNOWN
            ),
            key=lambda item: item.value,
        )
    )
    return TransitionContinuityAudit(
        transition_id=binding.transition_id,
        preserved_invariants=values(InvariantDisposition.PRESERVED),
        degraded_invariants=values(InvariantDisposition.DEGRADED),
        broken_invariants=values(InvariantDisposition.BROKEN),
        unknown_invariants=values(InvariantDisposition.UNKNOWN),
        not_applicable_invariants=values(InvariantDisposition.NOT_APPLICABLE),
        unresolved_locus_invariants=unresolved,
    )
