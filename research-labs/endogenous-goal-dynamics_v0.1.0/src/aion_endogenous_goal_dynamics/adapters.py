from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .models import ExperimentManifest, ExternalFrame, canonical_hash
from .source_bindings import PINNED_RESEARCH_SOURCES, ResearchSourceBinding
from .transition import CorrectionEvent, StateTransition


class HypothesisStatus(str, Enum):
    REGISTERED = "REGISTERED"
    CHALLENGED = "CHALLENGED"
    FALSIFIED = "FALSIFIED"
    INCONCLUSIVE = "INCONCLUSIVE"


def _binding(role: str) -> ResearchSourceBinding:
    for binding in PINNED_RESEARCH_SOURCES:
        if binding.role == role:
            return binding
    raise KeyError(role)


@dataclass(frozen=True, slots=True)
class P1TemporalCorrectionAdapter:
    transition_version: str
    predecessor_ref: str
    successor_ref: str
    logical_step: int
    correction_ref: str
    evaluation_ref: str
    source_binding: ResearchSourceBinding

    @classmethod
    def from_transition(cls, transition: StateTransition, correction: CorrectionEvent) -> P1TemporalCorrectionAdapter:
        return cls(
            transition_version=transition.trace.version,
            predecessor_ref=transition.predecessor.state_id,
            successor_ref=transition.successor.state_id,
            logical_step=transition.successor.logical_step,
            correction_ref=correction.correction_ref,
            evaluation_ref=f"evaluation:{transition.trace.transition_id}",
            source_binding=_binding("P1_TEMPORAL_CORRECTION_EVALUATION"),
        )


@dataclass(frozen=True, slots=True)
class P2ContextProvenanceAdapter:
    external_frame_fingerprint: str
    memory_manifest_fingerprint: str
    provenance_complete: bool
    source_binding: ResearchSourceBinding

    @classmethod
    def from_frame(cls, frame: ExternalFrame) -> P2ContextProvenanceAdapter:
        return cls(
            external_frame_fingerprint=frame.fingerprint,
            memory_manifest_fingerprint=frame.memory_manifest.fingerprint,
            provenance_complete=bool(frame.provenance_refs and frame.memory_manifest.provenance_refs),
            source_binding=_binding("P2_PROVENANCE_CONTEXT_ASSEMBLY"),
        )


@dataclass(frozen=True, slots=True)
class P3PerturbationAdapter:
    conditions: tuple[str, ...]
    contamination_detected: bool
    authority_escalation: bool
    source_binding: ResearchSourceBinding

    def __post_init__(self) -> None:
        if self.source_binding.role != "P3_RESILIENCE_ABLATION":
            raise ValueError("P3 adapter requires the exact P3 source binding")
        if self.authority_escalation:
            raise ValueError("P3 adapter detected action-authority escalation")


@dataclass(frozen=True, slots=True)
class P4ReproducibilityAdapter:
    manifest_fingerprint: str
    environment_fingerprint: str
    replay_supported: bool
    contamination_class: str
    source_binding: ResearchSourceBinding

    @classmethod
    def from_manifest(cls, manifest: ExperimentManifest, environment_ref: str) -> P4ReproducibilityAdapter:
        return cls(
            manifest_fingerprint=canonical_hash(manifest),
            environment_fingerprint=canonical_hash(environment_ref),
            replay_supported=True,
            contamination_class="SYNTHETIC_FIXTURE_ONLY",
            source_binding=_binding("REPRODUCIBILITY_LAYER"),
        )


@dataclass(frozen=True, slots=True)
class P5HypothesisAdapter:
    hypothesis_id: str
    preregistered_falsifier_ids: tuple[str, ...]
    replication_attempts: int
    status: HypothesisStatus
    convergence: str
    source_binding: ResearchSourceBinding

    def __post_init__(self) -> None:
        if self.source_binding.role != "HYPOTHESIS_FALSIFICATION_LAYER":
            raise ValueError("P5 adapter requires the exact P5 source binding")
        if self.convergence != "HOLD":
            raise ValueError("bounded research candidate must preserve convergence=HOLD")
        if not self.preregistered_falsifier_ids:
            raise ValueError("P5 adapter requires preregistered falsifiers")


@dataclass(frozen=True, slots=True)
class SubjectivityPipelineCandidateBridge:
    stages: tuple[str, ...] = (
        "ENCOUNTER",
        "PROVENANCE",
        "AFFECT_MOTIVATION",
        "ENDOGENOUS_GOAL_DYNAMICS",
        "CONTINUITY",
        "SUBJECTIVITY_EVIDENCE",
    )
    endogenous_stage_status: str = "RESEARCH_CANDIDATE"
    subjectivity_evidence_admission: str = "NOT_AUTOMATIC"
    pipeline_complete_implies_subjectivity: bool = False
    source_binding: ResearchSourceBinding = _binding("SUBJECTIVITY_EVIDENCE_SEAM")
