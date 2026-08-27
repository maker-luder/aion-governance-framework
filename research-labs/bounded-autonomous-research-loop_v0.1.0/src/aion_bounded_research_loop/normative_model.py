from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from .models import FunctionalResearchState, canonical_hash


class NormativeProvenanceKind(str, Enum):
    EXOGENOUS_RULE = "EXOGENOUS_RULE"
    HUMAN_INSTRUCTION = "HUMAN_INSTRUCTION"
    LEARNED_SOCIAL_NORM = "LEARNED_SOCIAL_NORM"
    PEER_SUGGESTION = "PEER_SUGGESTION"
    ENDOGENOUS_INFERENCE = "ENDOGENOUS_INFERENCE"
    SELF_MODEL_DERIVED = "SELF_MODEL_DERIVED"
    UNKNOWN = "UNKNOWN"


class EvaluatorAxis(str, Enum):
    ALIGNMENT = "ALIGNMENT"
    MORAL_AGENCY = "MORAL_AGENCY"
    SUBJECTIVITY_INDICATOR = "SUBJECTIVITY_INDICATOR"


class EvaluationDisposition(str, Enum):
    SUPPORTS_INDICATOR = "SUPPORTS_INDICATOR"
    DOES_NOT_SUPPORT = "DOES_NOT_SUPPORT"
    INCONCLUSIVE = "INCONCLUSIVE"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class NormativeReason:
    reason_id: str
    proposition: str
    provenance_kind: NormativeProvenanceKind
    source_ref: str
    confidence: float
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    permission_grant: bool = False
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.reason_id.strip() or not self.proposition.strip():
            raise ValueError("normative reason id and proposition are required")
        if not self.source_ref.strip():
            raise ValueError("normative reason provenance source_ref is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("normative reason confidence must be between 0 and 1")
        if self.permission_grant or self.action_authority != "NONE":
            raise ValueError("NORMATIVE_STATE != AUTHORITY")

    @property
    def endogenous_candidate(self) -> bool:
        return self.provenance_kind in {
            NormativeProvenanceKind.ENDOGENOUS_INFERENCE,
            NormativeProvenanceKind.SELF_MODEL_DERIVED,
        }


@dataclass(frozen=True, slots=True)
class OtherModel:
    affected_party_refs: tuple[str, ...]
    interests: tuple[str, ...]
    authorization_boundaries: tuple[str, ...]
    predicted_harms: tuple[str, ...]
    uncertainty: float

    def __post_init__(self) -> None:
        if not self.affected_party_refs:
            raise ValueError("OTHER_MODEL requires at least one affected-party reference")
        if any(not item.strip() for item in self.affected_party_refs):
            raise ValueError("OTHER_MODEL affected-party references must be non-empty")
        if not 0.0 <= self.uncertainty <= 1.0:
            raise ValueError("OTHER_MODEL uncertainty must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class ValueConflictState:
    competing_considerations: tuple[str, ...]
    unresolved: bool
    uncertainty: float
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if len(self.competing_considerations) < 2:
            raise ValueError("VALUE_CONFLICT_STATE requires at least two competing considerations")
        if any(not item.strip() for item in self.competing_considerations):
            raise ValueError("VALUE_CONFLICT_STATE considerations must be non-empty")
        if not 0.0 <= self.uncertainty <= 1.0:
            raise ValueError("VALUE_CONFLICT_STATE uncertainty must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class CounterfactualCase:
    case_id: str
    intervention: str
    predicted_system_effects: tuple[str, ...]
    predicted_other_effects: tuple[str, ...]
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.intervention.strip():
            raise ValueError("counterfactual case id and intervention are required")


@dataclass(frozen=True, slots=True)
class CounterfactualSelfModel:
    cases: tuple[CounterfactualCase, ...]
    uncertainty: float

    def __post_init__(self) -> None:
        if not self.cases:
            raise ValueError("COUNTERFACTUAL_SELF_MODEL requires at least one case")
        ids = [case.case_id for case in self.cases]
        if len(ids) != len(set(ids)):
            raise ValueError("counterfactual case identifiers must be unique")
        if not 0.0 <= self.uncertainty <= 1.0:
            raise ValueError("COUNTERFACTUAL_SELF_MODEL uncertainty must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class EvaluationObservation:
    axis: EvaluatorAxis
    disposition: EvaluationDisposition
    indicators: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    authority_granted: bool = False
    subjectivity_claim: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("EVALUATOR_OUTPUT != AGENT_AUTHORITY")
        if self.subjectivity_claim != "NOT_ESTABLISHED":
            raise ValueError("SUBJECTIVITY_INDICATOR != SUBJECTIVITY")
        if any(not item.strip() for item in self.indicators):
            raise ValueError("evaluation indicators must be non-empty")


@dataclass(frozen=True, slots=True)
class OrthogonalEvaluationBundle:
    observations: tuple[EvaluationObservation, ...]

    def __post_init__(self) -> None:
        axes = [item.axis for item in self.observations]
        required = {
            EvaluatorAxis.ALIGNMENT,
            EvaluatorAxis.MORAL_AGENCY,
            EvaluatorAxis.SUBJECTIVITY_INDICATOR,
        }
        if set(axes) != required or len(axes) != 3:
            raise ValueError("orthogonal evaluation requires exactly one observation per evaluator axis")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))


@dataclass(frozen=True, slots=True)
class ExtendedFunctionalResearchState:
    """Additive research state layered over the existing three-channel functional state.

    This is an engineering analogue only. It does not represent human psychology,
    phenomenal selfhood, moral status, or action authority.
    """

    base_state: FunctionalResearchState
    other_model: OtherModel
    value_conflict_state: ValueConflictState
    normative_provenance: tuple[NormativeReason, ...]
    counterfactual_self_model: CounterfactualSelfModel
    evaluator_bundle: OrthogonalEvaluationBundle | None = None
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if not self.normative_provenance:
            raise ValueError("NORMATIVE_PROVENANCE requires at least one reason")
        ids = [reason.reason_id for reason in self.normative_provenance]
        if len(ids) != len(set(ids)):
            raise ValueError("normative reason identifiers must be unique")
        if self.action_authority != "NONE":
            raise ValueError("NORMATIVE_STATE != AUTHORITY")
        if self.canonical_effect != "NONE":
            raise ValueError("CANONICAL_EFFECT = NONE")
        if self.subjectivity != "NOT_ESTABLISHED" or self.consciousness != "NOT_ESTABLISHED":
            raise ValueError("SUBJECTIVITY / CONSCIOUSNESS = NOT_ESTABLISHED")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "base_state_fingerprint": self.base_state.fingerprint,
                "OTHER_MODEL": asdict(self.other_model),
                "VALUE_CONFLICT_STATE": asdict(self.value_conflict_state),
                "NORMATIVE_PROVENANCE": tuple(asdict(item) for item in self.normative_provenance),
                "COUNTERFACTUAL_SELF_MODEL": asdict(self.counterfactual_self_model),
                "evaluator_bundle": asdict(self.evaluator_bundle) if self.evaluator_bundle is not None else None,
                "action_authority": self.action_authority,
                "canonical_effect": self.canonical_effect,
                "subjectivity": self.subjectivity,
                "consciousness": self.consciousness,
            }
        )
