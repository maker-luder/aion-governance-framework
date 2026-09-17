from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .attention_maintenance import AttentionMaintenanceAudit
from .context_reinstatement import ContextReinstatementAudit
from .drift_attribution import DriftAttributionAudit
from .harness import AdmissionDisposition, StudyError
from .transition_continuity import ContinuityInvariant, TransitionContinuityAudit


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


class CouplingPattern(StrEnum):
    REQUIRED_CONTINUITY_PRESERVED_ATTENTION_PRESERVED = (
        "REQUIRED_CONTINUITY_PRESERVED_ATTENTION_PRESERVED"
    )
    REQUIRED_CONTINUITY_PRESERVED_ATTENTION_DEGRADED = (
        "REQUIRED_CONTINUITY_PRESERVED_ATTENTION_DEGRADED"
    )
    REQUIRED_CONTINUITY_DEGRADED_ATTENTION_PRESERVED = (
        "REQUIRED_CONTINUITY_DEGRADED_ATTENTION_PRESERVED"
    )
    REQUIRED_CONTINUITY_AND_ATTENTION_DEGRADED = (
        "REQUIRED_CONTINUITY_AND_ATTENTION_DEGRADED"
    )
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class ContinuityAttentionCouplingSpec:
    coupling_id: str
    transition_id: str
    context_run_id: str
    attention_spec_id: str
    required_continuity_invariants: tuple[ContinuityInvariant, ...]

    def __post_init__(self) -> None:
        for name in (
            "coupling_id",
            "transition_id",
            "context_run_id",
            "attention_spec_id",
        ):
            _require_text(name, getattr(self, name))
        if (
            type(self.required_continuity_invariants) is not tuple
            or not self.required_continuity_invariants
        ):
            raise StudyError(
                "required_continuity_invariants must be a non-empty tuple"
            )
        if any(
            type(item) is not ContinuityInvariant
            for item in self.required_continuity_invariants
        ):
            raise StudyError(
                "required_continuity_invariants must contain exact ContinuityInvariant values"
            )
        if len(set(self.required_continuity_invariants)) != len(
            self.required_continuity_invariants
        ):
            raise StudyError("required_continuity_invariants must be unique")


@dataclass(frozen=True, slots=True)
class ContinuityAttentionCouplingAudit:
    coupling_id: str
    pattern: CouplingPattern
    required_continuity_failure_invariants: tuple[ContinuityInvariant, ...]
    required_continuity_unknown_invariants: tuple[ContinuityInvariant, ...]
    missing_required_context_item_ids: tuple[str, ...]
    payload_mismatch_context_item_ids: tuple[str, ...]
    attention_maintenance_preserved: bool
    diagnostic_flags: tuple[str, ...]
    mode: str = "DETERMINISTIC_SYNTHETIC_COUPLING_AUDIT"
    empirical_data_collected: bool = False
    coupling_mechanism: str = "NOT_ESTABLISHED"
    causal_direction: str = "NOT_ESTABLISHED"
    model_capability_ordering: str = "NOT_ESTABLISHED"
    ai_identity_continuity: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_continuity_attention_coupling(
    spec: ContinuityAttentionCouplingSpec,
    continuity: TransitionContinuityAudit,
    context: ContextReinstatementAudit,
    attention: AttentionMaintenanceAudit,
    drift: DriftAttributionAudit | None = None,
) -> ContinuityAttentionCouplingAudit:
    if type(spec) is not ContinuityAttentionCouplingSpec:
        raise StudyError("spec must be an exact ContinuityAttentionCouplingSpec")
    if type(continuity) is not TransitionContinuityAudit:
        raise StudyError("continuity must be an exact TransitionContinuityAudit")
    if type(context) is not ContextReinstatementAudit:
        raise StudyError("context must be an exact ContextReinstatementAudit")
    if type(attention) is not AttentionMaintenanceAudit:
        raise StudyError("attention must be an exact AttentionMaintenanceAudit")
    if drift is not None and type(drift) is not DriftAttributionAudit:
        raise StudyError("drift must be an exact DriftAttributionAudit when provided")

    if spec.transition_id != continuity.transition_id:
        raise StudyError("transition_id does not match continuity audit")
    if spec.context_run_id != context.run_id:
        raise StudyError("context_run_id does not match context audit")
    if spec.attention_spec_id != attention.spec_id:
        raise StudyError("attention_spec_id does not match attention audit")

    preserved = set(continuity.preserved_invariants)
    degraded = set(continuity.degraded_invariants)
    broken = set(continuity.broken_invariants)
    unknown = set(continuity.unknown_invariants)
    not_applicable = set(continuity.not_applicable_invariants)
    observed = preserved | degraded | broken | unknown | not_applicable
    required = set(spec.required_continuity_invariants)
    if not required <= observed:
        missing = sorted(item.value for item in required - observed)
        raise StudyError(
            "coupling spec references invariants absent from continuity audit: "
            + ",".join(missing)
        )

    failures = tuple(sorted(required & (degraded | broken), key=lambda item: item.value))
    unknown_required = tuple(
        sorted(required & (unknown | not_applicable), key=lambda item: item.value)
    )
    continuity_preserved = required <= preserved
    continuity_degraded = bool(failures)
    attention_preserved = attention.maintenance_preserved

    if unknown_required or (not continuity_preserved and not continuity_degraded):
        pattern = CouplingPattern.INDETERMINATE
    elif continuity_preserved and attention_preserved:
        pattern = CouplingPattern.REQUIRED_CONTINUITY_PRESERVED_ATTENTION_PRESERVED
    elif continuity_preserved and not attention_preserved:
        pattern = CouplingPattern.REQUIRED_CONTINUITY_PRESERVED_ATTENTION_DEGRADED
    elif continuity_degraded and attention_preserved:
        pattern = CouplingPattern.REQUIRED_CONTINUITY_DEGRADED_ATTENTION_PRESERVED
    else:
        pattern = CouplingPattern.REQUIRED_CONTINUITY_AND_ATTENTION_DEGRADED

    flags: list[str] = []
    context_gap = bool(
        context.missing_required_item_ids
        or context.payload_mismatch_item_ids
        or context.unavailable_item_ids_reinstated
    )
    if continuity_preserved and context_gap:
        flags.append("CONTINUITY_AVAILABLE_CONTEXT_REINSTATEMENT_GAP")
    if not context_gap and not attention_preserved:
        flags.append("CONTEXT_REINSTATED_ATTENTION_MAINTENANCE_GAP")
    if continuity_degraded and attention_preserved:
        flags.append("ATTENTION_PRESERVED_DESPITE_CONTINUITY_GAP")
    if attention.local_subgoal_takeover_checkpoint_ids:
        flags.append("LOCAL_SUBGOAL_TAKEOVER_OBSERVED")
    if drift is not None and drift.unknown_locus_record_ids:
        flags.append("CAUSAL_LOCUS_UNRESOLVED")
    if drift is None:
        flags.append("DRIFT_ATTRIBUTION_NOT_SUPPLIED")

    return ContinuityAttentionCouplingAudit(
        coupling_id=spec.coupling_id,
        pattern=pattern,
        required_continuity_failure_invariants=failures,
        required_continuity_unknown_invariants=unknown_required,
        missing_required_context_item_ids=context.missing_required_item_ids,
        payload_mismatch_context_item_ids=context.payload_mismatch_item_ids,
        attention_maintenance_preserved=attention_preserved,
        diagnostic_flags=tuple(flags),
    )
