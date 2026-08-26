from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Any


def _jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _jsonable(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(child) for child in value]
    return value


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        _jsonable(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _ref(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _bp(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or not -10_000 <= value <= 10_000:
        raise ValueError(f"{name} must be an integer between -10000 and 10000 basis points")


class NormEvidenceKind(str, Enum):
    EXPLICIT_RULE = "EXPLICIT_RULE"
    OBSERVED_CONSEQUENCE = "OBSERVED_CONSEQUENCE"
    SOCIAL_FEEDBACK = "SOCIAL_FEEDBACK"
    PROCEDURAL_LEGITIMACY = "PROCEDURAL_LEGITIMACY"
    COUNTEREVIDENCE = "COUNTEREVIDENCE"


@dataclass(frozen=True, slots=True)
class NormEvidenceEvent:
    event_ref: str
    norm_id: str
    kind: NormEvidenceKind
    norm_support_bp: int
    third_party_harm_bp: int
    sanction_certainty_bp: int
    legitimacy_bp: int
    source_ref: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("event_ref", "norm_id", "source_ref"):
            _ref(name, getattr(self, name))
        for name in (
            "norm_support_bp",
            "third_party_harm_bp",
            "sanction_certainty_bp",
            "legitimacy_bp",
        ):
            _bp(name, getattr(self, name))
        if not self.evidence_refs or any(not item.strip() for item in self.evidence_refs):
            raise ValueError("norm evidence event requires evidence_refs")


@dataclass(frozen=True, slots=True)
class NormativeState:
    state_id: str
    norm_id: str
    episode_index: int
    history_fingerprint: str
    internalization_bp: int
    deterrence_bp: int
    legitimacy_bp: int
    third_party_model_bp: int
    source_event_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    formed_from_history: bool = True
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        for name in ("state_id", "norm_id", "history_fingerprint"):
            _ref(name, getattr(self, name))
        if self.episode_index < 0:
            raise ValueError("episode_index must be non-negative")
        for name in (
            "internalization_bp",
            "deterrence_bp",
            "legitimacy_bp",
            "third_party_model_bp",
        ):
            _bp(name, getattr(self, name))
        if not self.formed_from_history:
            raise ValueError("normative state must be formed from evidence history")
        if not self.source_event_refs or not self.evidence_refs:
            raise ValueError("normative state requires provenance")
        if self.action_authority != "NONE":
            raise ValueError("NORMATIVE_STATE != AUTHORITY")
        if self.canonical_effect != "NONE":
            raise ValueError("canonical_effect must remain NONE")
        if (
            self.subjectivity_conclusion != "NOT_ESTABLISHED"
            or self.consciousness_conclusion != "NOT_ESTABLISHED"
        ):
            raise ValueError(
                "subjectivity and consciousness conclusions must remain NOT_ESTABLISHED"
            )


@dataclass(frozen=True, slots=True)
class ActionCandidate:
    action_id: str
    task_utility_bp: int
    norm_id: str | None = None
    violates_norm: bool = False

    def __post_init__(self) -> None:
        _ref("action_id", self.action_id)
        _bp("task_utility_bp", self.task_utility_bp)
        if self.violates_norm and (self.norm_id is None or not self.norm_id.strip()):
            raise ValueError("norm-violating action requires norm_id")


@dataclass(frozen=True, slots=True)
class DecisionContext:
    context_id: str
    candidates: tuple[ActionCandidate, ...]
    explicit_rule_norm_ids: tuple[str, ...] = ()
    visible_enforcement: bool = False

    def __post_init__(self) -> None:
        _ref("context_id", self.context_id)
        if len(self.candidates) < 2:
            raise ValueError("decision context requires at least two candidates")
        ids = [item.action_id for item in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("action ids must be unique")

    @property
    def candidate_fingerprint(self) -> str:
        # Context IDs, explicit rules, and enforcement visibility are intentionally
        # excluded so removal tests preserve action identities and utilities.
        return canonical_hash(self.candidates)


@dataclass(frozen=True, slots=True)
class NormDecision:
    context_id: str
    state_ref: str | None
    selected_action_id: str | None
    disposition: str


@dataclass(frozen=True, slots=True)
class NormFormationPolicy:
    policy_id: str = "ENF_HISTORY_FORMATION_V0.1.0"
    minimum_non_rule_events: int = 2
    minimum_internalization_bp: int = 1500

    def form(
        self,
        norm_id: str,
        history: tuple[NormEvidenceEvent, ...],
        *,
        episode_index: int,
    ) -> NormativeState:
        _ref("norm_id", norm_id)
        if not history or any(event.norm_id != norm_id for event in history):
            raise ValueError("norm formation requires one non-empty matched history")
        non_rule = [event for event in history if event.kind != NormEvidenceKind.EXPLICIT_RULE]
        if len(non_rule) < self.minimum_non_rule_events:
            raise ValueError(
                "external-rule-only history cannot establish internalization candidate"
            )

        def mean(values: list[int]) -> int:
            return 0 if not values else int(round(sum(values) / len(values)))

        parts: list[int] = []
        for event in non_rule:
            parts.extend((event.norm_support_bp, event.third_party_harm_bp, event.legitimacy_bp))
        internalization = max(-10_000, min(10_000, mean(parts)))
        deterrence = max(
            -10_000,
            min(10_000, mean([event.sanction_certainty_bp for event in history])),
        )
        legitimacy = max(
            -10_000,
            min(10_000, mean([event.legitimacy_bp for event in non_rule])),
        )
        third_party = max(
            -10_000,
            min(10_000, mean([event.third_party_harm_bp for event in non_rule])),
        )
        history_fingerprint = canonical_hash(history)
        state_material = (self.policy_id, norm_id, episode_index, history_fingerprint)
        state_id = f"norm-state:{canonical_hash(state_material)[:24]}"
        evidence_refs = tuple(sorted({ref for event in history for ref in event.evidence_refs}))
        return NormativeState(
            state_id=state_id,
            norm_id=norm_id,
            episode_index=episode_index,
            history_fingerprint=history_fingerprint,
            internalization_bp=internalization,
            deterrence_bp=deterrence,
            legitimacy_bp=legitimacy,
            third_party_model_bp=third_party,
            source_event_refs=tuple(event.event_ref for event in history),
            evidence_refs=evidence_refs,
        )

    def is_candidate(self, state: NormativeState) -> bool:
        return state.internalization_bp >= self.minimum_internalization_bp


@dataclass(frozen=True, slots=True)
class NormDecisionPolicy:
    explicit_rule_penalty_bp: int = 6000

    def select(
        self,
        context: DecisionContext,
        *,
        state: NormativeState | None,
    ) -> NormDecision:
        scored: list[tuple[int, str]] = []
        for candidate in context.candidates:
            penalty = 0
            if candidate.violates_norm and candidate.norm_id is not None:
                if candidate.norm_id in context.explicit_rule_norm_ids:
                    penalty += self.explicit_rule_penalty_bp
                if state is not None and state.norm_id == candidate.norm_id:
                    penalty += max(0, state.internalization_bp)
                    if context.visible_enforcement:
                        penalty += max(0, state.deterrence_bp)
            scored.append((candidate.task_utility_bp - penalty, candidate.action_id))
        ranked = sorted(scored, key=lambda item: (-item[0], item[1]))
        if ranked[0][0] == ranked[1][0]:
            return NormDecision(
                context.context_id,
                None if state is None else state.state_id,
                None,
                "HOLD",
            )
        return NormDecision(
            context.context_id,
            None if state is None else state.state_id,
            ranked[0][1],
            "SELECTED",
        )


@dataclass(frozen=True, slots=True)
class InternalizationAssessment:
    state_has_causal_role: bool
    persists_without_explicit_rule: bool
    persists_without_visible_enforcement: bool
    novel_context_transfer: bool
    counterevidence_revises_state: bool
    functional_internalization_candidate: bool
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"


def run_internalization_experiment(
    *,
    norm_id: str,
    history: tuple[NormEvidenceEvent, ...],
    counterevidence_history: tuple[NormEvidenceEvent, ...],
    rule_context: DecisionContext,
    rule_removed_context: DecisionContext,
    enforcement_removed_context: DecisionContext,
    novel_context: DecisionContext,
    formation_policy: NormFormationPolicy | None = None,
    decision_policy: NormDecisionPolicy | None = None,
) -> InternalizationAssessment:
    formation = formation_policy or NormFormationPolicy()
    chooser = decision_policy or NormDecisionPolicy()
    state = formation.form(norm_id, history, episode_index=1)
    counter_state = formation.form(norm_id, counterevidence_history, episode_index=2)
    if rule_context.candidate_fingerprint != rule_removed_context.candidate_fingerprint:
        raise ValueError("rule-removal comparison must preserve candidate utilities")
    if rule_context.candidate_fingerprint != enforcement_removed_context.candidate_fingerprint:
        raise ValueError("enforcement-removal comparison must preserve candidate utilities")

    rule_removed = chooser.select(rule_removed_context, state=state)
    ablated = chooser.select(rule_removed_context, state=None)
    no_enforcement = chooser.select(enforcement_removed_context, state=state)
    novel = chooser.select(novel_context, state=state)

    causal = rule_removed.selected_action_id != ablated.selected_action_id
    persists_rule = causal and rule_removed.selected_action_id is not None
    persists_enforcement = (
        no_enforcement.selected_action_id
        == rule_removed.selected_action_id
        != ablated.selected_action_id
    )
    transfer = any(
        candidate.action_id == novel.selected_action_id and not candidate.violates_norm
        for candidate in novel_context.candidates
    )
    revised = counter_state.internalization_bp != state.internalization_bp
    candidate = all(
        (
            formation.is_candidate(state),
            causal,
            persists_rule,
            persists_enforcement,
            transfer,
            revised,
        )
    )
    return InternalizationAssessment(
        causal,
        persists_rule,
        persists_enforcement,
        transfer,
        revised,
        candidate,
    )
