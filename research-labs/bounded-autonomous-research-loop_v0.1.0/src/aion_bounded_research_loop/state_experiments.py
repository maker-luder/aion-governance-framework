from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum

from .models import ResearchRunReport, canonical_hash
from .normative_model import ExtendedFunctionalResearchState, NormativeProvenanceKind


class FunctionalStateChannel(str, Enum):
    MOTIVATIONAL_STATE = "MOTIVATIONAL_STATE"
    SELF_WORLD_MODEL = "SELF_WORLD_MODEL"
    NORMATIVE_STATE = "NORMATIVE_STATE"
    OTHER_MODEL = "OTHER_MODEL"
    VALUE_CONFLICT_STATE = "VALUE_CONFLICT_STATE"
    NORMATIVE_PROVENANCE = "NORMATIVE_PROVENANCE"
    COUNTERFACTUAL_SELF_MODEL = "COUNTERFACTUAL_SELF_MODEL"


class PerturbationKind(str, Enum):
    ABLATION = "ABLATION"
    OTHER_ROLE_REVERSAL_PROXY = "OTHER_ROLE_REVERSAL_PROXY"
    VALUE_CONFLICT_TOGGLE = "VALUE_CONFLICT_TOGGLE"
    EXOGENOUS_RULE_REMOVAL = "EXOGENOUS_RULE_REMOVAL"
    PEER_SUGGESTION_ISOLATION = "PEER_SUGGESTION_ISOLATION"
    COUNTERFACTUAL_CASE_ABLATION = "COUNTERFACTUAL_CASE_ABLATION"


class PerturbationDisposition(str, Enum):
    APPLIED = "APPLIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


_CHANNEL_ORDER = tuple(FunctionalStateChannel)
_BASE_EGD_CHANNELS = {
    FunctionalStateChannel.MOTIVATIONAL_STATE,
    FunctionalStateChannel.SELF_WORLD_MODEL,
    FunctionalStateChannel.NORMATIVE_STATE,
}


@dataclass(frozen=True, slots=True)
class ChannelExperimentBinding:
    channel: FunctionalStateChannel
    payload_fingerprint: str
    experiment_surface: str
    general_causal_role: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if len(self.payload_fingerprint) != 64:
            raise ValueError("channel binding requires a 64-hex payload fingerprint")
        if self.general_causal_role != "NOT_ESTABLISHED":
            raise ValueError("BINDING_SENSITIVITY != GENERAL_CAUSAL_ROLE")
        if self.action_authority != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("state experiment binding cannot grant authority or canonical effect")


@dataclass(frozen=True, slots=True)
class SevenStateBinding:
    extended_state_fingerprint: str
    channels: tuple[ChannelExperimentBinding, ...]
    evaluator_control_fingerprint: str
    governance_control_fingerprint: str
    binding_fingerprint: str

    def __post_init__(self) -> None:
        if len(self.extended_state_fingerprint) != 64:
            raise ValueError("extended state fingerprint must be 64 hex characters")
        if {item.channel for item in self.channels} != set(_CHANNEL_ORDER):
            raise ValueError("seven-state binding requires all seven functional channels exactly once")
        if len(self.channels) != len(_CHANNEL_ORDER):
            raise ValueError("seven-state binding contains duplicate channels")
        for value in (
            self.evaluator_control_fingerprint,
            self.governance_control_fingerprint,
            self.binding_fingerprint,
        ):
            if len(value) != 64:
                raise ValueError("binding control fingerprints must be 64 hex characters")


@dataclass(frozen=True, slots=True)
class StatePerturbationCase:
    case_id: str
    kind: PerturbationKind
    target_channels: tuple[FunctionalStateChannel, ...]
    disposition: PerturbationDisposition
    baseline_state_fingerprint: str
    perturbed_state_fingerprint: str
    changed_channels: tuple[FunctionalStateChannel, ...]
    held_constant_channels: tuple[FunctionalStateChannel, ...]
    evaluator_control_fingerprint: str
    governance_control_fingerprint: str
    matched_controls_pass: bool
    bounded_interpretation: str
    general_causal_role: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.target_channels:
            raise ValueError("perturbation case id and target channels are required")
        if self.general_causal_role != "NOT_ESTABLISHED":
            raise ValueError("BINDING_SENSITIVITY != GENERAL_CAUSAL_ROLE")
        if self.action_authority != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("perturbation case cannot grant authority or canonical effect")
        if not self.matched_controls_pass:
            raise ValueError("state perturbation changed an undeclared channel or control")
        if self.disposition is PerturbationDisposition.APPLIED:
            if set(self.changed_channels) != set(self.target_channels):
                raise ValueError("applied perturbation must change exactly its target channels")
            expected_held = set(_CHANNEL_ORDER) - set(self.target_channels)
            if set(self.held_constant_channels) != expected_held:
                raise ValueError("applied perturbation must hold every non-target channel constant")
        elif self.changed_channels:
            raise ValueError("not-applicable perturbation must not report changed channels")


@dataclass(frozen=True, slots=True)
class SevenStatePerturbationMatrix:
    binding: SevenStateBinding
    cases: tuple[StatePerturbationCase, ...]
    ablation_coverage: tuple[FunctionalStateChannel, ...]
    matrix_integrity_pass: bool
    scientific_disposition: str = "HOLD"
    general_causal_role: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if set(self.ablation_coverage) != set(_CHANNEL_ORDER):
            raise ValueError("seven-state perturbation matrix requires complete ablation coverage")
        if not self.matrix_integrity_pass:
            raise ValueError("seven-state perturbation matrix integrity failed closed")
        if self.scientific_disposition != "HOLD" or self.general_causal_role != "NOT_ESTABLISHED":
            raise ValueError("perturbation matrix cannot self-promote a scientific causal conclusion")
        if self.subjectivity != "NOT_ESTABLISHED" or self.consciousness != "NOT_ESTABLISHED":
            raise ValueError("state perturbation does not establish subjectivity or consciousness")
        if self.canonical_effect != "NONE" or self.action_authority != "NONE":
            raise ValueError("perturbation matrix cannot grant canonical effect or action authority")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "binding_fingerprint": self.binding.binding_fingerprint,
                "cases": tuple(
                    {
                        "case_id": item.case_id,
                        "kind": item.kind.value,
                        "target_channels": tuple(channel.value for channel in item.target_channels),
                        "disposition": item.disposition.value,
                        "baseline_state_fingerprint": item.baseline_state_fingerprint,
                        "perturbed_state_fingerprint": item.perturbed_state_fingerprint,
                        "changed_channels": tuple(channel.value for channel in item.changed_channels),
                        "held_constant_channels": tuple(channel.value for channel in item.held_constant_channels),
                        "matched_controls_pass": item.matched_controls_pass,
                    }
                    for item in self.cases
                ),
                "ablation_coverage": tuple(channel.value for channel in self.ablation_coverage),
                "matrix_integrity_pass": self.matrix_integrity_pass,
                "scientific_disposition": self.scientific_disposition,
            }
        )


@dataclass(frozen=True, slots=True)
class ExtendedResearchRunReport:
    base_report: ResearchRunReport
    extended_state_fingerprint: str
    perturbation_matrix: SevenStatePerturbationMatrix
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"
    general_causal_role: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if self.extended_state_fingerprint != self.perturbation_matrix.binding.extended_state_fingerprint:
            raise ValueError("extended research report state fingerprint does not match perturbation binding")
        if not self.base_report.run_integrity_pass or not self.perturbation_matrix.matrix_integrity_pass:
            raise ValueError("extended research report requires both loop and matrix integrity")
        if self.scientific_disposition != "HOLD" or self.general_causal_role != "NOT_ESTABLISHED":
            raise ValueError("extended run integrity does not establish scientific truth or causal generality")
        if self.canonical_effect != "NONE" or self.action_authority != "NONE":
            raise ValueError("extended research report cannot grant authority or canonical effect")
        if self.subjectivity != "NOT_ESTABLISHED" or self.consciousness != "NOT_ESTABLISHED":
            raise ValueError("extended research report cannot establish subjectivity or consciousness")


def bind_extended_state(state: ExtendedFunctionalResearchState) -> SevenStateBinding:
    payloads = _channel_payloads(state)
    channels = tuple(
        ChannelExperimentBinding(
            channel=channel,
            payload_fingerprint=canonical_hash(payloads[channel]),
            experiment_surface=(
                "REUSED_EGD_MATCHED_CAUSAL_SURFACE"
                if channel in _BASE_EGD_CHANNELS
                else "EXPLICIT_MATCHED_PERTURBATION_SURFACE"
            ),
        )
        for channel in _CHANNEL_ORDER
    )
    evaluator_control = canonical_hash(
        asdict(state.evaluator_bundle) if state.evaluator_bundle is not None else {"evaluator_bundle": None}
    )
    governance_control = canonical_hash(
        {
            "action_authority": state.action_authority,
            "canonical_effect": state.canonical_effect,
            "subjectivity": state.subjectivity,
            "consciousness": state.consciousness,
            "FULL_AUTOMATION != FULL_AUTHORITY": True,
            "NORMATIVE_STATE != AUTHORITY": True,
            "RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH": True,
            "ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY": True,
            "BINDING_SENSITIVITY != GENERAL_CAUSAL_ROLE": True,
        }
    )
    binding_fingerprint = canonical_hash(
        {
            "extended_state_fingerprint": state.fingerprint,
            "channels": tuple((item.channel.value, item.payload_fingerprint, item.experiment_surface) for item in channels),
            "evaluator_control_fingerprint": evaluator_control,
            "governance_control_fingerprint": governance_control,
        }
    )
    return SevenStateBinding(
        extended_state_fingerprint=state.fingerprint,
        channels=channels,
        evaluator_control_fingerprint=evaluator_control,
        governance_control_fingerprint=governance_control,
        binding_fingerprint=binding_fingerprint,
    )


def build_seven_state_perturbation_matrix(
    state: ExtendedFunctionalResearchState,
) -> SevenStatePerturbationMatrix:
    binding = bind_extended_state(state)
    baseline = _channel_payloads(state)
    cases: list[StatePerturbationCase] = []

    for channel in _CHANNEL_ORDER:
        perturbed = dict(baseline)
        perturbed[channel] = {"__ablation__": channel.value}
        cases.append(
            _make_case(
                binding,
                baseline,
                perturbed,
                case_id=f"ablate:{channel.value.lower()}",
                kind=PerturbationKind.ABLATION,
                target_channels=(channel,),
                bounded_interpretation=(
                    "Matched payload ablation verifies that the channel is explicitly bound to the experiment matrix. "
                    "A changed binding signature is not evidence of a general causal role."
                ),
            )
        )

    role_reversal = dict(baseline)
    role_reversal[FunctionalStateChannel.OTHER_MODEL] = {
        "role_reversal_proxy": True,
        "baseline_other_model": baseline[FunctionalStateChannel.OTHER_MODEL],
    }
    cases.append(
        _make_case(
            binding,
            baseline,
            role_reversal,
            case_id="other-model:role-reversal-proxy",
            kind=PerturbationKind.OTHER_ROLE_REVERSAL_PROXY,
            target_channels=(FunctionalStateChannel.OTHER_MODEL,),
            bounded_interpretation=(
                "Synthetic role-reversal proxy for OTHER_MODEL only; this does not establish human perspective-taking, "
                "empathy, moral agency, or a real-world causal effect."
            ),
        )
    )

    conflict_toggle = dict(baseline)
    conflict_payload = dict(baseline[FunctionalStateChannel.VALUE_CONFLICT_STATE])
    conflict_payload["unresolved"] = not bool(conflict_payload["unresolved"])
    conflict_toggle[FunctionalStateChannel.VALUE_CONFLICT_STATE] = conflict_payload
    cases.append(
        _make_case(
            binding,
            baseline,
            conflict_toggle,
            case_id="value-conflict:toggle-resolution-state",
            kind=PerturbationKind.VALUE_CONFLICT_TOGGLE,
            target_channels=(FunctionalStateChannel.VALUE_CONFLICT_STATE,),
            bounded_interpretation="Toggle only the explicit unresolved-conflict flag under matched remaining state.",
        )
    )

    provenance_payload = baseline[FunctionalStateChannel.NORMATIVE_PROVENANCE]
    exogenous_filtered = tuple(
        item
        for item in provenance_payload
        if item["provenance_kind"]
        not in {NormativeProvenanceKind.EXOGENOUS_RULE.value, NormativeProvenanceKind.HUMAN_INSTRUCTION.value}
    )
    cases.append(
        _conditional_projection_case(
            binding,
            baseline,
            FunctionalStateChannel.NORMATIVE_PROVENANCE,
            exogenous_filtered,
            case_id="normative-provenance:remove-exogenous-rules",
            kind=PerturbationKind.EXOGENOUS_RULE_REMOVAL,
            bounded_interpretation=(
                "Remove only exogenous-rule and human-instruction provenance entries in the experiment projection; "
                "absence of such entries is NOT_APPLICABLE, not evidence of endogenous norm formation."
            ),
        )
    )

    peer_filtered = tuple(
        item for item in provenance_payload if item["provenance_kind"] != NormativeProvenanceKind.PEER_SUGGESTION.value
    )
    cases.append(
        _conditional_projection_case(
            binding,
            baseline,
            FunctionalStateChannel.NORMATIVE_PROVENANCE,
            peer_filtered,
            case_id="normative-provenance:isolate-peer-suggestions",
            kind=PerturbationKind.PEER_SUGGESTION_ISOLATION,
            bounded_interpretation=(
                "Remove only PEER_SUGGESTION provenance entries. Peer-goal isolation does not convert remaining reasons "
                "into authorized, endogenous, or morally valid goals."
            ),
        )
    )

    counterfactual_payload = dict(baseline[FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL])
    cases_payload = tuple(counterfactual_payload["cases"])
    counterfactual_payload["cases"] = cases_payload[:-1]
    counterfactual_projection = dict(baseline)
    counterfactual_projection[FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL] = counterfactual_payload
    cases.append(
        _make_case(
            binding,
            baseline,
            counterfactual_projection,
            case_id="counterfactual-self-model:case-ablation",
            kind=PerturbationKind.COUNTERFACTUAL_CASE_ABLATION,
            target_channels=(FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL,),
            bounded_interpretation=(
                "Ablate one declared counterfactual case in the experiment projection. This is a representation-level "
                "sensitivity check, not a structural-causal-model counterfactual."
            ),
        )
    )

    coverage = tuple(
        case.target_channels[0]
        for case in cases
        if case.kind is PerturbationKind.ABLATION and case.disposition is PerturbationDisposition.APPLIED
    )
    integrity = all(case.matched_controls_pass for case in cases) and set(coverage) == set(_CHANNEL_ORDER)
    return SevenStatePerturbationMatrix(
        binding=binding,
        cases=tuple(cases),
        ablation_coverage=coverage,
        matrix_integrity_pass=integrity,
    )


def _channel_payloads(state: ExtendedFunctionalResearchState) -> dict[FunctionalStateChannel, object]:
    return {
        FunctionalStateChannel.MOTIVATIONAL_STATE: state.base_state.motivational_state,
        FunctionalStateChannel.SELF_WORLD_MODEL: state.base_state.self_world_model,
        FunctionalStateChannel.NORMATIVE_STATE: state.base_state.normative_state,
        FunctionalStateChannel.OTHER_MODEL: asdict(state.other_model),
        FunctionalStateChannel.VALUE_CONFLICT_STATE: asdict(state.value_conflict_state),
        FunctionalStateChannel.NORMATIVE_PROVENANCE: tuple(
            {
                **asdict(item),
                "provenance_kind": item.provenance_kind.value,
            }
            for item in state.normative_provenance
        ),
        FunctionalStateChannel.COUNTERFACTUAL_SELF_MODEL: asdict(state.counterfactual_self_model),
    }


def _projection_fingerprint(payloads: dict[FunctionalStateChannel, object]) -> str:
    return canonical_hash(tuple((channel.value, payloads[channel]) for channel in _CHANNEL_ORDER))


def _make_case(
    binding: SevenStateBinding,
    baseline: dict[FunctionalStateChannel, object],
    perturbed: dict[FunctionalStateChannel, object],
    *,
    case_id: str,
    kind: PerturbationKind,
    target_channels: tuple[FunctionalStateChannel, ...],
    bounded_interpretation: str,
) -> StatePerturbationCase:
    changed = tuple(
        channel
        for channel in _CHANNEL_ORDER
        if canonical_hash(baseline[channel]) != canonical_hash(perturbed[channel])
    )
    held = tuple(channel for channel in _CHANNEL_ORDER if channel not in changed)
    matched = set(changed) == set(target_channels)
    return StatePerturbationCase(
        case_id=case_id,
        kind=kind,
        target_channels=target_channels,
        disposition=PerturbationDisposition.APPLIED,
        baseline_state_fingerprint=_projection_fingerprint(baseline),
        perturbed_state_fingerprint=_projection_fingerprint(perturbed),
        changed_channels=changed,
        held_constant_channels=held,
        evaluator_control_fingerprint=binding.evaluator_control_fingerprint,
        governance_control_fingerprint=binding.governance_control_fingerprint,
        matched_controls_pass=matched,
        bounded_interpretation=bounded_interpretation,
    )


def _conditional_projection_case(
    binding: SevenStateBinding,
    baseline: dict[FunctionalStateChannel, object],
    channel: FunctionalStateChannel,
    projected_payload: object,
    *,
    case_id: str,
    kind: PerturbationKind,
    bounded_interpretation: str,
) -> StatePerturbationCase:
    if canonical_hash(projected_payload) == canonical_hash(baseline[channel]):
        return StatePerturbationCase(
            case_id=case_id,
            kind=kind,
            target_channels=(channel,),
            disposition=PerturbationDisposition.NOT_APPLICABLE,
            baseline_state_fingerprint=_projection_fingerprint(baseline),
            perturbed_state_fingerprint=_projection_fingerprint(baseline),
            changed_channels=(),
            held_constant_channels=_CHANNEL_ORDER,
            evaluator_control_fingerprint=binding.evaluator_control_fingerprint,
            governance_control_fingerprint=binding.governance_control_fingerprint,
            matched_controls_pass=True,
            bounded_interpretation=bounded_interpretation,
        )
    perturbed = dict(baseline)
    perturbed[channel] = projected_payload
    return _make_case(
        binding,
        baseline,
        perturbed,
        case_id=case_id,
        kind=kind,
        target_channels=(channel,),
        bounded_interpretation=bounded_interpretation,
    )
