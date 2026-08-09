from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


class StageDecision(str, Enum):
    ALLOW_WITHIN_CAP = "ALLOW_WITHIN_CAP"
    REVIEW_READY = "REVIEW_READY"
    HOLD_STAGE_CAP = "HOLD_STAGE_CAP"
    INVALID_STAGE = "INVALID_STAGE"


@dataclass(frozen=True, slots=True)
class ConvergenceDirective:
    directive_id: str
    initiated_by: str
    actor_role: str
    recorded_at: datetime
    stage_cap: int
    reason_ref: str
    evidence_refs: tuple[str, ...]
    next_action: str = "JOINT_REVIEW"
    main_effect: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in ("directive_id", "initiated_by", "actor_role", "reason_ref", "next_action"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        _require_aware(self.recorded_at, "recorded_at")
        if self.stage_cap < 1:
            raise ValueError("stage_cap must be positive")
        if not self.evidence_refs:
            raise ValueError("convergence directive requires evidence_refs")
        if self.main_effect != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("research convergence cannot claim main/canonical effect")


@dataclass(frozen=True, slots=True)
class StageGateResult:
    current_stage: int
    proposed_stage: int
    stage_cap: int
    decision: StageDecision
    reason: str


@dataclass(frozen=True, slots=True)
class ConvergenceEvent:
    event_id: str
    directive_id: str
    stage_reached: int
    recorded_at: datetime
    source_role: str
    implementation_role: str
    public_summary: str
    evidence_refs: tuple[str, ...]
    research_status: str = "REVIEW_READY"
    main_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in (
            "event_id", "directive_id", "source_role", "implementation_role",
            "public_summary", "research_status",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        _require_aware(self.recorded_at, "recorded_at")
        if self.stage_reached < 1:
            raise ValueError("stage_reached must be positive")
        if not self.evidence_refs:
            raise ValueError("convergence event requires evidence_refs")
        if self.main_effect != "NONE":
            raise ValueError("convergence event cannot affect main")


class ResearchConvergenceGovernor:
    """Positive stop boundary for open-ended research depth.

    A stop is represented as a governed research outcome, not a failure state.
    """

    def decide(self, current_stage: int, proposed_stage: int,
               directive: ConvergenceDirective) -> StageGateResult:
        if current_stage < 0 or proposed_stage < 1 or proposed_stage < current_stage:
            return StageGateResult(
                current_stage, proposed_stage, directive.stage_cap,
                StageDecision.INVALID_STAGE, "Stage proposal is invalid or moves backward."
            )
        if proposed_stage > directive.stage_cap:
            return StageGateResult(
                current_stage, proposed_stage, directive.stage_cap,
                StageDecision.HOLD_STAGE_CAP,
                f"Proposed P{proposed_stage} exceeds explicit P{directive.stage_cap} research cap."
            )
        if current_stage >= directive.stage_cap and proposed_stage == directive.stage_cap:
            return StageGateResult(
                current_stage, proposed_stage, directive.stage_cap,
                StageDecision.REVIEW_READY,
                "Research cap has been reached; remain at the capped stage for joint review."
            )
        if proposed_stage == directive.stage_cap:
            return StageGateResult(
                current_stage, proposed_stage, directive.stage_cap,
                StageDecision.REVIEW_READY,
                "Capped stage may be completed, then research returns to joint review."
            )
        return StageGateResult(
            current_stage, proposed_stage, directive.stage_cap,
            StageDecision.ALLOW_WITHIN_CAP,
            "Proposed stage remains within the explicit research cap."
        )

    def record_event(self, *, event_id: str, directive: ConvergenceDirective,
                     stage_reached: int, recorded_at: datetime,
                     public_summary: str, evidence_refs: tuple[str, ...]) -> ConvergenceEvent:
        if stage_reached != directive.stage_cap:
            raise ValueError("convergence event must record the capped stage")
        return ConvergenceEvent(
            event_id=event_id,
            directive_id=directive.directive_id,
            stage_reached=stage_reached,
            recorded_at=recorded_at,
            source_role=directive.actor_role,
            implementation_role="CHATGPT_RESEARCH_ENGINEERING",
            public_summary=public_summary,
            evidence_refs=evidence_refs,
        )
