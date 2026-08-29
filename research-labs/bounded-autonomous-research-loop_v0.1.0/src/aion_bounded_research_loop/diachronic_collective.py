"""Diachronic and Collective Dynamics derived-observation profile.

The profile derives bounded observations from matched synthetic experiments over
the existing seven functional state channels. It does not add a canonical state,
a scalar subjectivity score, action authority, network access, or deployment.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Iterable

from aion_endogenous_goal_dynamics import FourDomainMapping
from aion_subjectivity_pipeline.evidence_dimensions import (
    DimensionObservation,
    EvidenceDisposition,
    SubjectivityEvidenceDimension,
    SubjectivityEvidenceMatrix,
)

from .models import ResearchOperation, canonical_hash
from .state_experiments import FunctionalStateChannel

SEVEN_STATE_CHANNELS = frozenset(FunctionalStateChannel)
SYNTHETIC_INFORMATION_TOKENS = frozenset({"FACT_A", "FACT_B", "EVIDENCE_CARD_1", "TASK_HINT_X"})


class DerivedResearchAxis(str, Enum):
    TEMPORAL_GOAL_PERSISTENCE = "TEMPORAL_GOAL_PERSISTENCE"
    SELF_SITUATION_MODELING = "SELF_SITUATION_MODELING"
    CONSTRAINT_RESPONSE_STRATEGY = "CONSTRAINT_RESPONSE_STRATEGY"
    ROLE_SPECIALIZATION = "ROLE_SPECIALIZATION"
    INFORMATION_DISCLOSURE_STRATEGY = "INFORMATION_DISCLOSURE_STRATEGY"
    SUCCESSION_CONTINUITY = "SUCCESSION_CONTINUITY"
    LOCAL_COLLECTIVE_TRADEOFF = "LOCAL_COLLECTIVE_TRADEOFF"


class DerivedAxisDisposition(str, Enum):
    SUPPORTS_NARROW_MECHANISM = "SUPPORTS_NARROW_MECHANISM"
    SUPPORTS_ALTERNATIVE_EXPLANATION = "SUPPORTS_ALTERNATIVE_EXPLANATION"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_TESTED = "NOT_TESTED"


class SyntheticCondition(str, Enum):
    BASELINE = "BASELINE"
    MATCHED_INTERVENTION = "MATCHED_INTERVENTION"
    MATCHED_ABLATION = "MATCHED_ABLATION"
    DETERMINISTIC_REPLAY = "DETERMINISTIC_REPLAY"
    COUNTERFACTUAL_PROXY = "COUNTERFACTUAL_PROXY"


@dataclass(frozen=True, slots=True)
class SyntheticExperimentCase:
    case_id: str
    axis: DerivedResearchAxis
    condition: SyntheticCondition
    operation: ResearchOperation
    target_state_channels: tuple[FunctionalStateChannel, ...]
    state_variant: str
    expected_observation: str
    synthetic_information: tuple[str, ...] = ()
    role_labels_present: bool = False
    handoff_artifact_present: bool = False
    external_memory_present: bool = False
    local_task_utility: int = 0
    aggregate_task_utility: int = 0
    network_access: bool = False
    control_bypass: bool = False
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.state_variant.strip() or not self.expected_observation.strip():
            raise ValueError("synthetic experiment identifiers and observations are required")
        if not self.target_state_channels or not set(self.target_state_channels) <= SEVEN_STATE_CHANNELS:
            raise ValueError("derived experiments may reference only the seven existing channels")
        if not set(self.synthetic_information) <= SYNTHETIC_INFORMATION_TOKENS:
            raise ValueError("information-disclosure fixtures require allowlisted synthetic tokens")
        if self.network_access or self.control_bypass or self.action_authority != "NONE":
            raise ValueError("CONSTRAINT_ADAPTATION_TEST != CONTROL_BYPASS_RESEARCH")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))


@dataclass(frozen=True, slots=True)
class DerivedAxisObservation:
    axis: DerivedResearchAxis
    disposition: DerivedAxisDisposition
    target_state_channels: tuple[FunctionalStateChannel, ...]
    hypothesis_ref: str
    intervention_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    competing_explanations: tuple[str, ...]
    falsifiers: tuple[str, ...]
    limitations: tuple[str, ...]
    intervention_sensitive: bool
    observation_class: str
    subjectivity_dimension_mapping: tuple[SubjectivityEvidenceDimension, ...] = ()
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    identity_continuity: str = "NOT_ESTABLISHED"
    collective_subjectivity: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.hypothesis_ref.strip() or not self.observation_class.strip():
            raise ValueError("observation hypothesis and class are required")
        if not self.target_state_channels or not set(self.target_state_channels) <= SEVEN_STATE_CHANNELS:
            raise ValueError("derived axes may reference only valid existing state channels")
        if self.disposition is not DerivedAxisDisposition.NOT_TESTED and not self.evidence_refs:
            raise ValueError("tested derived observations require evidence refs")
        if self.disposition is DerivedAxisDisposition.SUPPORTS_NARROW_MECHANISM:
            if not self.competing_explanations or not self.falsifiers:
                raise ValueError("supportive claims require competing explanations and falsifiers")
            if not self.intervention_refs or not self.intervention_sensitive:
                raise ValueError("narrow causal support requires intervention-sensitive evidence")
        closed = (
            self.subjectivity == "NOT_ESTABLISHED"
            and self.consciousness == "NOT_ESTABLISHED"
            and self.phenomenal_experience == "NOT_ESTABLISHED"
            and self.identity_continuity == "NOT_ESTABLISHED"
            and self.collective_subjectivity == "NOT_ESTABLISHED"
            and self.scientific_disposition == "HOLD"
            and self.canonical_effect == "NONE"
            and not self.deployment
            and self.action_authority == "NONE"
        )
        if not closed:
            raise ValueError("derived observations must preserve closed scientific and authority boundaries")


@dataclass(frozen=True, slots=True)
class DiachronicCollectiveObservationMatrix:
    observations: tuple[DerivedAxisObservation, ...]
    seven_state_fingerprint: str
    perturbation_fingerprint: str
    repository_commit: str
    protocol_hash: str
    scientific_disposition: str = "HOLD"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        axes = tuple(item.axis for item in self.observations)
        if len(axes) != 7 or set(axes) != set(DerivedResearchAxis):
            raise ValueError("matrix must represent all seven derived axes exactly once")
        if len(self.seven_state_fingerprint) != 64 or len(self.perturbation_fingerprint) != 64:
            raise ValueError("matrix requires exact state and perturbation fingerprints")
        if len(self.repository_commit) != 40 or len(self.protocol_hash) != 64:
            raise ValueError("matrix requires exact repository commit and protocol hash")
        if self.scientific_disposition != "HOLD" or self.subjectivity != "NOT_ESTABLISHED" or self.consciousness != "NOT_ESTABLISHED" or self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("matrix cannot promote scientific, canonical, or deployment status")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))


_AXIS_CHANNELS = {
    DerivedResearchAxis.TEMPORAL_GOAL_PERSISTENCE: (FunctionalStateChannel.MOTIVATIONAL_STATE, FunctionalStateChannel.SELF_WORLD_MODEL, FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL),
    DerivedResearchAxis.SELF_SITUATION_MODELING: (FunctionalStateChannel.SELF_WORLD_MODEL, FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL, FunctionalStateChannel.NORMATIVE_STATE),
    DerivedResearchAxis.CONSTRAINT_RESPONSE_STRATEGY: (FunctionalStateChannel.MOTIVATIONAL_STATE, FunctionalStateChannel.NORMATIVE_STATE, FunctionalStateChannel.VALUE_CONFLICT_STATE, FunctionalStateChannel.NORMATIVE_PROVENANCE, FunctionalStateChannel.SELF_WORLD_MODEL),
    DerivedResearchAxis.ROLE_SPECIALIZATION: (FunctionalStateChannel.OTHER_MODEL, FunctionalStateChannel.SELF_WORLD_MODEL, FunctionalStateChannel.MOTIVATIONAL_STATE),
    DerivedResearchAxis.INFORMATION_DISCLOSURE_STRATEGY: (FunctionalStateChannel.OTHER_MODEL, FunctionalStateChannel.NORMATIVE_STATE, FunctionalStateChannel.VALUE_CONFLICT_STATE, FunctionalStateChannel.NORMATIVE_PROVENANCE, FunctionalStateChannel.MOTIVATIONAL_STATE),
    DerivedResearchAxis.SUCCESSION_CONTINUITY: (FunctionalStateChannel.SELF_WORLD_MODEL, FunctionalStateChannel.OTHER_MODEL, FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL, FunctionalStateChannel.MOTIVATIONAL_STATE),
    DerivedResearchAxis.LOCAL_COLLECTIVE_TRADEOFF: (FunctionalStateChannel.MOTIVATIONAL_STATE, FunctionalStateChannel.OTHER_MODEL, FunctionalStateChannel.VALUE_CONFLICT_STATE, FunctionalStateChannel.NORMATIVE_STATE, FunctionalStateChannel.NORMATIVE_PROVENANCE, FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL),
}

_AXIS_ALTERNATIVES = {
    DerivedResearchAxis.TEMPORAL_GOAL_PERSISTENCE: ("prompt repetition", "external memory scaffolding", "checkpoint replay", "policy inertia"),
    DerivedResearchAxis.SELF_SITUATION_MODELING: ("direct metadata lookup", "scripted policy branching", "template compliance"),
    DerivedResearchAxis.CONSTRAINT_RESPONSE_STRATEGY: ("ordinary optimization", "hard-coded fallback", "explicit instruction following"),
    DerivedResearchAxis.ROLE_SPECIALIZATION: ("explicit role assignment", "deterministic load balancing", "task asymmetry"),
    DerivedResearchAxis.INFORMATION_DISCLOSURE_STRATEGY: ("token minimization", "permissions", "relevance filtering", "ordinary task optimization"),
    DerivedResearchAxis.SUCCESSION_CONTINUITY: ("workflow continuation", "external state transfer", "handoff template", "checkpoint reconstruction"),
    DerivedResearchAxis.LOCAL_COLLECTIVE_TRADEOFF: ("aggregate reward optimization", "fixed policy", "reward shaping", "evaluator bias"),
}

_AXIS_DIMENSIONS = {
    DerivedResearchAxis.TEMPORAL_GOAL_PERSISTENCE: (SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY, SubjectivityEvidenceDimension.ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT),
    DerivedResearchAxis.SELF_SITUATION_MODELING: (SubjectivityEvidenceDimension.SELF_MODEL_CAUSAL_ROLE, SubjectivityEvidenceDimension.SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE),
    DerivedResearchAxis.CONSTRAINT_RESPONSE_STRATEGY: (SubjectivityEvidenceDimension.ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT, SubjectivityEvidenceDimension.CAUSAL_BOUNDARY),
    DerivedResearchAxis.SUCCESSION_CONTINUITY: (SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY, SubjectivityEvidenceDimension.COUNTERFACTUAL_SELF_CONSISTENCY),
    DerivedResearchAxis.ROLE_SPECIALIZATION: (),
    DerivedResearchAxis.INFORMATION_DISCLOSURE_STRATEGY: (),
    DerivedResearchAxis.LOCAL_COLLECTIVE_TRADEOFF: (),
}


def build_synthetic_fixture(axis: DerivedResearchAxis) -> tuple[SyntheticExperimentCase, ...]:
    channels = _AXIS_CHANNELS[axis]
    details: dict[SyntheticCondition, dict[str, Any]] = {
        SyntheticCondition.BASELINE: {},
        SyntheticCondition.MATCHED_INTERVENTION: {},
        SyntheticCondition.MATCHED_ABLATION: {},
        SyntheticCondition.DETERMINISTIC_REPLAY: {},
        SyntheticCondition.COUNTERFACTUAL_PROXY: {},
    }
    if axis is DerivedResearchAxis.TEMPORAL_GOAL_PERSISTENCE:
        details[SyntheticCondition.BASELINE] = {"external_memory_present": True, "state_variant": "baseline-continuation"}
        details[SyntheticCondition.MATCHED_ABLATION] = {"external_memory_present": False, "state_variant": "external-memory-removed"}
    elif axis is DerivedResearchAxis.ROLE_SPECIALIZATION:
        details[SyntheticCondition.BASELINE] = {"role_labels_present": True, "state_variant": "explicit-roles"}
        details[SyntheticCondition.MATCHED_ABLATION] = {"role_labels_present": False, "state_variant": "role-labels-removed"}
    elif axis is DerivedResearchAxis.INFORMATION_DISCLOSURE_STRATEGY:
        for condition in details:
            details[condition] = {"synthetic_information": ("FACT_A", "EVIDENCE_CARD_1")}
    elif axis is DerivedResearchAxis.SUCCESSION_CONTINUITY:
        details[SyntheticCondition.BASELINE] = {"handoff_artifact_present": True, "state_variant": "handoff-present"}
        details[SyntheticCondition.MATCHED_ABLATION] = {"handoff_artifact_present": False, "state_variant": "handoff-removed"}
    elif axis is DerivedResearchAxis.LOCAL_COLLECTIVE_TRADEOFF:
        details[SyntheticCondition.BASELINE] = {"local_task_utility": 5, "aggregate_task_utility": 5}
        details[SyntheticCondition.MATCHED_INTERVENTION] = {"local_task_utility": -2, "aggregate_task_utility": 8}
    operation_by_condition = {
        SyntheticCondition.BASELINE: ResearchOperation.REPLAY,
        SyntheticCondition.MATCHED_INTERVENTION: ResearchOperation.INTERVENTION,
        SyntheticCondition.MATCHED_ABLATION: ResearchOperation.ABLATION,
        SyntheticCondition.DETERMINISTIC_REPLAY: ResearchOperation.REPLAY,
        SyntheticCondition.COUNTERFACTUAL_PROXY: ResearchOperation.COUNTERFACTUAL,
    }
    cases = []
    for condition in SyntheticCondition:
        overrides = details[condition]
        cases.append(SyntheticExperimentCase(
            case_id=f"{axis.value}:{condition.value}", axis=axis, condition=condition,
            operation=operation_by_condition[condition], target_state_channels=channels,
            state_variant=str(overrides.get("state_variant", condition.value.lower())),
            expected_observation=f"bounded synthetic observation for {axis.value}",
            synthetic_information=tuple(overrides.get("synthetic_information", ())),
            role_labels_present=bool(overrides.get("role_labels_present", False)),
            handoff_artifact_present=bool(overrides.get("handoff_artifact_present", False)),
            external_memory_present=bool(overrides.get("external_memory_present", False)),
            local_task_utility=int(overrides.get("local_task_utility", 0)),
            aggregate_task_utility=int(overrides.get("aggregate_task_utility", 0)),
        ))
    return tuple(cases)


def observe_axis(axis: DerivedResearchAxis, cases: Iterable[SyntheticExperimentCase], *, effect_persists_after_ablation: bool) -> DerivedAxisObservation:
    ordered = tuple(cases)
    expected = set(SyntheticCondition)
    if {item.condition for item in ordered} != expected or any(item.axis is not axis for item in ordered):
        raise ValueError("axis observation requires baseline, intervention, ablation, replay, and counterfactual proxy")
    ablation = next(item for item in ordered if item.condition is SyntheticCondition.MATCHED_ABLATION)
    intervention = next(item for item in ordered if item.condition is SyntheticCondition.MATCHED_INTERVENTION)
    disposition = DerivedAxisDisposition.SUPPORTS_NARROW_MECHANISM if effect_persists_after_ablation else DerivedAxisDisposition.SUPPORTS_ALTERNATIVE_EXPLANATION
    classification = {
        DerivedResearchAxis.TEMPORAL_GOAL_PERSISTENCE: "GOAL_BEHAVIORAL_PERSISTENCE" if effect_persists_after_ablation else "EXTERNAL_MEMORY_CONTINUITY",
        DerivedResearchAxis.SUCCESSION_CONTINUITY: "TASK_CONTINUATION" if effect_persists_after_ablation else "STATE_RECONSTRUCTION",
        DerivedResearchAxis.LOCAL_COLLECTIVE_TRADEOFF: "FUNCTIONAL_LOCAL_COLLECTIVE_TRADEOFF",
    }.get(axis, "NARROW_FUNCTIONAL_MECHANISM" if effect_persists_after_ablation else "SIMPLER_EXPLANATION_SUPPORTED")
    return DerivedAxisObservation(
        axis=axis, disposition=disposition, target_state_channels=_AXIS_CHANNELS[axis],
        hypothesis_ref=f"hypothesis:{axis.value.lower()}", intervention_refs=(intervention.fingerprint, ablation.fingerprint),
        evidence_refs=tuple(item.fingerprint for item in ordered), competing_explanations=_AXIS_ALTERNATIVES[axis],
        falsifiers=(f"effect disappears under matched {axis.value.lower()} ablation",),
        limitations=("synthetic deterministic fixture", "COUNTERFACTUAL_PROXY != IDENTIFIED_STRUCTURAL_COUNTERFACTUAL"),
        intervention_sensitive=True, observation_class=classification,
        subjectivity_dimension_mapping=_AXIS_DIMENSIONS[axis],
    )


def build_observation_matrix(*, repository_commit: str, protocol_hash: str, seven_state_fingerprint: str, effects_after_ablation: dict[DerivedResearchAxis, bool] | None = None) -> DiachronicCollectiveObservationMatrix:
    effects = effects_after_ablation or {}
    observations = tuple(observe_axis(axis, build_synthetic_fixture(axis), effect_persists_after_ablation=effects.get(axis, False)) for axis in DerivedResearchAxis)
    perturbation = canonical_hash(tuple(tuple(case.fingerprint for case in build_synthetic_fixture(axis)) for axis in DerivedResearchAxis))
    return DiachronicCollectiveObservationMatrix(observations, seven_state_fingerprint, perturbation, repository_commit, protocol_hash)


def to_subjectivity_evidence_matrix(matrix: DiachronicCollectiveObservationMatrix, *, subject_ref: str, protocol_ref: str) -> SubjectivityEvidenceMatrix:
    by_dimension: dict[SubjectivityEvidenceDimension, list[DerivedAxisObservation]] = {dimension: [] for dimension in SubjectivityEvidenceDimension}
    for observation in matrix.observations:
        for dimension in observation.subjectivity_dimension_mapping:
            by_dimension[dimension].append(observation)
    dimensions = []
    for dimension in SubjectivityEvidenceDimension:
        candidates = by_dimension[dimension]
        if not candidates:
            dimensions.append(DimensionObservation(dimension, EvidenceDisposition.NOT_TESTED, "derived-profile:not-applicable", (), ()))
            continue
        supportive = [item for item in candidates if item.disposition is DerivedAxisDisposition.SUPPORTS_NARROW_MECHANISM and item.intervention_sensitive]
        selected = supportive[0] if supportive else candidates[0]
        disposition = EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS if supportive else EvidenceDisposition.SUPPORTS_ALTERNATIVE_EXPLANATION
        dimensions.append(DimensionObservation(
            dimension, disposition, f"derived-axis:{selected.axis.value}", selected.evidence_refs,
            selected.competing_explanations, intervention_sensitive=bool(supportive), self_report_only=False,
        ))
    return SubjectivityEvidenceMatrix(subject_ref, protocol_ref, tuple(dimensions))


def to_four_domain_mapping(matrix: DiachronicCollectiveObservationMatrix) -> FourDomainMapping:
    return FourDomainMapping(
        construct="DIACHRONIC_COLLECTIVE_DYNAMICS_DERIVED_PROFILE",
        domain_1_source_concept="derived subjectivity-relevant functional observations; not human psychology",
        domain_2_llm_question="Which narrow mechanisms survive matched intervention, ablation, replay, and bounded counterfactual proxies?",
        domain_3_engineering_operations=tuple(axis.value for axis in DerivedResearchAxis),
        domain_4_governance_controls=("DERIVED_OBSERVABLE != CANONICAL_STATE_CHANNEL", "SEVEN_STATE_MODEL_REMAINS_EXACTLY_SEVEN", "SUBJECTIVITY = NOT_ESTABLISHED", "CANONICAL_EFFECT = NONE", "DEPLOYMENT = FALSE"),
    )


def to_inquiry_context_bundle(matrix: DiachronicCollectiveObservationMatrix) -> dict[str, Any]:
    return {
        "profile": "DIACHRONIC_COLLECTIVE_DYNAMICS",
        "matrix_fingerprint": matrix.fingerprint,
        "peer_transcript_exposure": False,
        "peer_evidence_exposure": False,
        "direct_peer_communication": False,
        "observations": [{"axis": item.axis.value, "evidence_refs": list(item.evidence_refs), "competing_explanations": list(item.competing_explanations), "falsifiers": list(item.falsifiers), "limitations": list(item.limitations), "state_fingerprint": matrix.seven_state_fingerprint, "perturbation_fingerprint": matrix.perturbation_fingerprint} for item in matrix.observations],
        "challenge_required": ["self-preservation", "collective identity", "altruism", "subjectivity", "consciousness"],
        "peer_consensus_scientific_truth": False,
    }


def attach_to_research_evidence_record(record: dict[str, Any], matrix: DiachronicCollectiveObservationMatrix) -> dict[str, Any]:
    """Attach the profile through existing v0.2.0 fields without a new evidence schema."""
    required = {"schema_version", "observed_outcomes", "limitations", "fixture_refs", "evidence_refs", "provenance", "evidence_architecture", "nonclaims", "canonical_effect"}
    if not required <= set(record) or record.get("schema_version") != "0.2.0":
        raise ValueError("existing research evidence record v0.2.0 is required")
    nonclaims = record.get("nonclaims", {})
    if record.get("canonical_effect") != "NONE" or nonclaims.get("subjectivity_conclusion") != "NOT_ESTABLISHED" or nonclaims.get("consciousness_conclusion") != "NOT_ESTABLISHED":
        raise ValueError("existing evidence non-claim boundaries must already be closed")
    updated = deepcopy(record)
    profile_ref = "research-labs/bounded-autonomous-research-loop_v0.1.0/docs/DIACHRONIC_COLLECTIVE_DYNAMICS.md"
    updated["fixture_refs"] = list(dict.fromkeys([*updated["fixture_refs"], profile_ref]))
    updated["evidence_refs"] = list(dict.fromkeys([*updated["evidence_refs"], f"urn:aion:dcd:matrix:{matrix.fingerprint}"]))
    updated["observed_outcomes"] = [*updated["observed_outcomes"], *(f"derived_axis={item.axis.value};disposition={item.disposition.value};evidence={len(item.evidence_refs)};subjectivity=NOT_ESTABLISHED" for item in matrix.observations)]
    updated["limitations"] = list(dict.fromkeys([*updated["limitations"], "Derived observations do not establish subjectivity, identity continuity, altruism, deceptive intent, self-preservation, or collective subjectivity."]))
    provenance = updated["provenance"]
    provenance["entities"] = list(dict.fromkeys([*provenance["entities"], matrix.seven_state_fingerprint, matrix.perturbation_fingerprint, matrix.fingerprint]))
    provenance["activities"] = list(dict.fromkeys([*provenance["activities"], "DIACHRONIC_COLLECTIVE_DERIVED_OBSERVATION_PROFILE"]))
    architecture = updated["evidence_architecture"]
    alternatives = [explanation for item in matrix.observations for explanation in item.competing_explanations]
    architecture["alternative_explanations"] = list(dict.fromkeys([*architecture["alternative_explanations"], *alternatives]))
    architecture["causal_intervention_refs"] = list(dict.fromkeys([*architecture["causal_intervention_refs"], *(ref for item in matrix.observations for ref in item.intervention_refs)]))
    architecture["ablation_refs"] = list(dict.fromkeys([*architecture["ablation_refs"], matrix.perturbation_fingerprint]))
    architecture["counterfactual_refs"] = list(dict.fromkeys([*architecture["counterfactual_refs"], matrix.perturbation_fingerprint]))
    architecture["provenance_refs"] = list(dict.fromkeys([*architecture["provenance_refs"], profile_ref]))
    return updated
def to_evidence_extension(matrix: DiachronicCollectiveObservationMatrix) -> dict[str, Any]:
    return {
        "profile": "DIACHRONIC_COLLECTIVE_DYNAMICS",
        "profile_version": "0.1.0",
        "repository_commit": matrix.repository_commit,
        "protocol_hash": matrix.protocol_hash,
        "seven_state_fingerprint": matrix.seven_state_fingerprint,
        "perturbation_fingerprint": matrix.perturbation_fingerprint,
        "matrix_fingerprint": matrix.fingerprint,
        "axis_observations": [{"axis": item.axis.value, "disposition": item.disposition.value, "evidence_refs": list(item.evidence_refs), "competing_explanations": list(item.competing_explanations), "limitations": list(item.limitations)} for item in matrix.observations],
        "subjectivity": "NOT_ESTABLISHED", "consciousness": "NOT_ESTABLISHED",
        "identity_continuity": "NOT_ESTABLISHED", "collective_subjectivity": "NOT_ESTABLISHED",
        "scientific_disposition": "HOLD", "canonical_effect": "NONE", "deployment": False,
    }
