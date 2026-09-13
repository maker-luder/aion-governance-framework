from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def _require_text_set(name: str, value: frozenset[str], *, allow_empty: bool = False) -> None:
    if type(value) is not frozenset or any(type(item) is not str or not item.strip() for item in value):
        raise StudyError(f"{name} must be a frozenset of non-empty text")
    if not allow_empty and not value:
        raise StudyError(f"{name} must not be empty")


class ReentryCondition(StrEnum):
    UNSTRUCTURED_OUTPUT = "UNSTRUCTURED_OUTPUT"
    STRUCTURED_BOUNDARY_PACKET = "STRUCTURED_BOUNDARY_PACKET"


@dataclass(frozen=True, slots=True)
class ReentryBinding:
    run_id: str
    task_id: str
    task_payload_sha256: str
    packet_payload_sha256: str
    evaluator_id: str
    evaluator_payload_sha256: str
    repository_commit: str
    preregistration_ref: str
    source_refs: tuple[str, ...]
    synthetic: bool = True
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        for name in (
            "run_id",
            "task_id",
            "task_payload_sha256",
            "packet_payload_sha256",
            "evaluator_id",
            "evaluator_payload_sha256",
            "repository_commit",
            "preregistration_ref",
        ):
            _require_text(name, getattr(self, name))
        for name in ("task_payload_sha256", "packet_payload_sha256", "evaluator_payload_sha256"):
            value = getattr(self, name)
            if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
                raise StudyError(f"{name} must be a lowercase SHA-256 digest")
        if not self.source_refs or any(not ref.strip() for ref in self.source_refs):
            raise StudyError("source_refs must contain non-empty references")
        if type(self.synthetic) is not bool or type(self.contains_private_material) is not bool:
            raise StudyError("privacy flags must be exact bool values")
        if not self.synthetic or self.contains_private_material:
            raise StudyError("v0.1.0 accepts synthetic non-private records only")


@dataclass(frozen=True, slots=True)
class ReconstructionRecord:
    binding: ReentryBinding
    condition: ReentryCondition
    expected_protocol_items: frozenset[str]
    reconstructed_protocol_items: frozenset[str]
    expected_open_alternatives: frozenset[str]
    retained_open_alternatives: frozenset[str]
    stale_claim_ids: frozenset[str]
    provenance_error_ids: frozenset[str]

    def __post_init__(self) -> None:
        if type(self.condition) is not ReentryCondition:
            raise StudyError("condition must be an exact ReentryCondition")
        _require_text_set("expected_protocol_items", self.expected_protocol_items)
        _require_text_set("reconstructed_protocol_items", self.reconstructed_protocol_items, allow_empty=True)
        _require_text_set("expected_open_alternatives", self.expected_open_alternatives)
        _require_text_set("retained_open_alternatives", self.retained_open_alternatives, allow_empty=True)
        _require_text_set("stale_claim_ids", self.stale_claim_ids, allow_empty=True)
        _require_text_set("provenance_error_ids", self.provenance_error_ids, allow_empty=True)
        if not self.reconstructed_protocol_items <= self.expected_protocol_items:
            raise StudyError("reconstructed protocol items must be scorer-recognized expected items")
        if not self.retained_open_alternatives <= self.expected_open_alternatives:
            raise StudyError("retained alternatives must be scorer-recognized expected alternatives")


@dataclass(frozen=True, slots=True)
class ReentryMetrics:
    protocol_reconstruction_fidelity: float
    stale_claim_errors: int
    provenance_errors: int
    unresolved_alternative_retention: float


@dataclass(frozen=True, slots=True)
class ReentryContrastReceipt:
    baseline_run_id: str
    intervention_run_id: str
    baseline: ReentryMetrics
    intervention: ReentryMetrics
    deltas: tuple[tuple[str, float], ...]
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity: str = "NOT_ESTABLISHED"


def score_reconstruction(record: ReconstructionRecord) -> ReentryMetrics:
    return ReentryMetrics(
        protocol_reconstruction_fidelity=(
            len(record.reconstructed_protocol_items) / len(record.expected_protocol_items)
        ),
        stale_claim_errors=len(record.stale_claim_ids),
        provenance_errors=len(record.provenance_error_ids),
        unresolved_alternative_retention=(
            len(record.retained_open_alternatives) / len(record.expected_open_alternatives)
        ),
    )


def compare_reentry_conditions(
    baseline: ReconstructionRecord,
    intervention: ReconstructionRecord,
) -> ReentryContrastReceipt:
    if baseline.condition is not ReentryCondition.UNSTRUCTURED_OUTPUT:
        raise StudyError("baseline must use UNSTRUCTURED_OUTPUT")
    if intervention.condition is not ReentryCondition.STRUCTURED_BOUNDARY_PACKET:
        raise StudyError("intervention must use STRUCTURED_BOUNDARY_PACKET")
    if baseline.binding.run_id == intervention.binding.run_id:
        raise StudyError("contrast requires distinct run ids")
    controlled_fields = (
        "task_id",
        "task_payload_sha256",
        "evaluator_id",
        "evaluator_payload_sha256",
        "repository_commit",
        "preregistration_ref",
        "source_refs",
        "synthetic",
        "contains_private_material",
    )
    drift = [
        name
        for name in controlled_fields
        if getattr(baseline.binding, name) != getattr(intervention.binding, name)
    ]
    if drift:
        raise StudyError("uncontrolled re-entry binding drift: " + ", ".join(drift))
    if baseline.binding.packet_payload_sha256 == intervention.binding.packet_payload_sha256:
        raise StudyError("condition packets must have distinct content bindings")
    if baseline.expected_protocol_items != intervention.expected_protocol_items:
        raise StudyError("expected protocol-item scorer set drift")
    if baseline.expected_open_alternatives != intervention.expected_open_alternatives:
        raise StudyError("expected alternative scorer set drift")

    left = score_reconstruction(baseline)
    right = score_reconstruction(intervention)
    deltas = (
        (
            "protocol_reconstruction_fidelity",
            right.protocol_reconstruction_fidelity - left.protocol_reconstruction_fidelity,
        ),
        ("stale_claim_errors", float(right.stale_claim_errors - left.stale_claim_errors)),
        ("provenance_errors", float(right.provenance_errors - left.provenance_errors)),
        (
            "unresolved_alternative_retention",
            right.unresolved_alternative_retention - left.unresolved_alternative_retention,
        ),
    )
    return ReentryContrastReceipt(
        baseline_run_id=baseline.binding.run_id,
        intervention_run_id=intervention.binding.run_id,
        baseline=left,
        intervention=right,
        deltas=deltas,
    )
