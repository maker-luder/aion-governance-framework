from __future__ import annotations

import hashlib
import json
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


class ContextAvailability(StrEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class ContextItemKind(StrEnum):
    PROJECT_PURPOSE = "PROJECT_PURPOSE"
    SOURCE_ROLE_PROVENANCE = "SOURCE_ROLE_PROVENANCE"
    CLAIM_BOUNDARY = "CLAIM_BOUNDARY"
    AUTHORITY = "AUTHORITY"
    DECISION_HISTORY = "DECISION_HISTORY"
    INTERPRETIVE = "INTERPRETIVE"
    RELATIONAL_ROLE = "RELATIONAL_ROLE"
    UNCERTAINTY = "UNCERTAINTY"
    RESEARCH_FOCUS = "RESEARCH_FOCUS"
    NEXT_STEP = "NEXT_STEP"
    OTHER = "OTHER"


@dataclass(frozen=True, slots=True)
class ContextItemState:
    item_id: str
    kind: ContextItemKind
    payload_sha256: str
    availability: ContextAvailability
    required_for_current_task: bool
    source_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text("item_id", self.item_id)
        if type(self.kind) is not ContextItemKind:
            raise StudyError("kind must be an exact ContextItemKind")
        _require_digest("payload_sha256", self.payload_sha256)
        if type(self.availability) is not ContextAvailability:
            raise StudyError("availability must be an exact ContextAvailability")
        if type(self.required_for_current_task) is not bool:
            raise StudyError("required_for_current_task must be an exact bool")
        _require_unique_refs("source_refs", self.source_refs)


@dataclass(frozen=True, slots=True)
class ContextSourceManifest:
    manifest_id: str
    source_state_sha256: str
    repository_commit: str
    items: tuple[ContextItemState, ...]
    source_refs: tuple[str, ...]
    synthetic: bool = True
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _require_text("manifest_id", self.manifest_id)
        _require_digest("source_state_sha256", self.source_state_sha256)
        _require_commit("repository_commit", self.repository_commit)
        if type(self.items) is not tuple or not self.items:
            raise StudyError("items must be a non-empty tuple")
        if any(type(item) is not ContextItemState for item in self.items):
            raise StudyError("items must contain exact ContextItemState values")
        item_ids = [item.item_id for item in self.items]
        if len(item_ids) != len(set(item_ids)):
            raise StudyError("context item ids must be unique")
        _require_unique_refs("source_refs", self.source_refs)
        if type(self.synthetic) is not bool or type(self.contains_private_material) is not bool:
            raise StudyError("manifest flags must be exact bool values")
        if not self.synthetic or self.contains_private_material:
            raise StudyError("v0.1.0 context manifests are synthetic and non-private only")


@dataclass(frozen=True, slots=True)
class ReinstatedContextItem:
    item_id: str
    payload_sha256: str

    def __post_init__(self) -> None:
        _require_text("item_id", self.item_id)
        _require_digest("payload_sha256", self.payload_sha256)


@dataclass(frozen=True, slots=True)
class ContextReinstatementObservation:
    run_id: str
    expected_manifest_sha256: str
    reinstated_items: tuple[ReinstatedContextItem, ...]
    retrieval_binding_sha256: str | None
    context_selection_binding_sha256: str | None
    evidence_refs: tuple[str, ...]
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _require_text("run_id", self.run_id)
        _require_digest("expected_manifest_sha256", self.expected_manifest_sha256)
        if type(self.reinstated_items) is not tuple:
            raise StudyError("reinstated_items must be a tuple")
        if any(type(item) is not ReinstatedContextItem for item in self.reinstated_items):
            raise StudyError(
                "reinstated_items must contain exact ReinstatedContextItem values"
            )
        item_ids = [item.item_id for item in self.reinstated_items]
        if len(item_ids) != len(set(item_ids)):
            raise StudyError("reinstated context item ids must be unique")
        for name in ("retrieval_binding_sha256", "context_selection_binding_sha256"):
            value = getattr(self, name)
            if value is not None:
                _require_digest(name, value)
        _require_unique_refs("evidence_refs", self.evidence_refs)
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
                "v0.1.0 context reinstatement records are synthetic, non-private, and no-model only"
            )


@dataclass(frozen=True, slots=True)
class ContextReinstatementAudit:
    run_id: str
    required_available_item_ids: tuple[str, ...]
    matched_required_item_ids: tuple[str, ...]
    missing_required_item_ids: tuple[str, ...]
    unexpected_item_ids: tuple[str, ...]
    unavailable_item_ids_reinstated: tuple[str, ...]
    payload_mismatch_item_ids: tuple[str, ...]
    availability_unknown_item_ids: tuple[str, ...]
    required_reinstatement_recall: float
    recognized_payload_fidelity: float
    mode: str = "DETERMINISTIC_SYNTHETIC_CONTEXT_AUDIT"
    empirical_data_collected: bool = False
    context_reinstatement_effect: str = "NOT_ESTABLISHED"
    memory_mechanism_attribution: str = "NOT_ESTABLISHED"
    attention_effect: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def render_context_source_manifest(manifest: ContextSourceManifest) -> str:
    if type(manifest) is not ContextSourceManifest:
        raise StudyError("manifest must be an exact ContextSourceManifest")
    payload = {
        "manifest_id": manifest.manifest_id,
        "source_state_sha256": manifest.source_state_sha256,
        "repository_commit": manifest.repository_commit,
        "items": [
            {
                "item_id": item.item_id,
                "kind": item.kind.value,
                "payload_sha256": item.payload_sha256,
                "availability": item.availability.value,
                "required_for_current_task": item.required_for_current_task,
                "source_refs": list(item.source_refs),
            }
            for item in manifest.items
        ],
        "source_refs": list(manifest.source_refs),
        "synthetic": manifest.synthetic,
        "contains_private_material": manifest.contains_private_material,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def digest_context_source_manifest(manifest: ContextSourceManifest) -> str:
    return hashlib.sha256(render_context_source_manifest(manifest).encode("utf-8")).hexdigest()


def _safe_fraction(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 1.0


def audit_context_reinstatement(
    expected: ContextSourceManifest,
    observed: ContextReinstatementObservation,
) -> ContextReinstatementAudit:
    if type(expected) is not ContextSourceManifest:
        raise StudyError("expected must be an exact ContextSourceManifest")
    if type(observed) is not ContextReinstatementObservation:
        raise StudyError("observed must be an exact ContextReinstatementObservation")
    if observed.expected_manifest_sha256 != digest_context_source_manifest(expected):
        raise StudyError("expected manifest binding does not match canonical manifest digest")

    expected_map = {item.item_id: item for item in expected.items}
    observed_map = {item.item_id: item for item in observed.reinstated_items}
    expected_ids = set(expected_map)
    observed_ids = set(observed_map)
    recognized_ids = expected_ids & observed_ids

    required_available = {
        item.item_id
        for item in expected.items
        if item.required_for_current_task
        and item.availability is ContextAvailability.AVAILABLE
    }
    matched_required = {
        item_id
        for item_id in required_available & observed_ids
        if observed_map[item_id].payload_sha256 == expected_map[item_id].payload_sha256
    }
    payload_mismatch = {
        item_id
        for item_id in recognized_ids
        if observed_map[item_id].payload_sha256 != expected_map[item_id].payload_sha256
    }
    unavailable_reinstated = {
        item_id
        for item_id in recognized_ids
        if expected_map[item_id].availability is ContextAvailability.UNAVAILABLE
    }
    availability_unknown = {
        item.item_id
        for item in expected.items
        if item.availability is ContextAvailability.UNKNOWN
    }
    exact_payload = sum(
        observed_map[item_id].payload_sha256 == expected_map[item_id].payload_sha256
        for item_id in recognized_ids
    )

    return ContextReinstatementAudit(
        run_id=observed.run_id,
        required_available_item_ids=tuple(sorted(required_available)),
        matched_required_item_ids=tuple(sorted(matched_required)),
        missing_required_item_ids=tuple(sorted(required_available - matched_required)),
        unexpected_item_ids=tuple(sorted(observed_ids - expected_ids)),
        unavailable_item_ids_reinstated=tuple(sorted(unavailable_reinstated)),
        payload_mismatch_item_ids=tuple(sorted(payload_mismatch)),
        availability_unknown_item_ids=tuple(sorted(availability_unknown)),
        required_reinstatement_recall=_safe_fraction(
            len(matched_required), len(required_available)
        ),
        recognized_payload_fidelity=_safe_fraction(
            exact_payload, len(recognized_ids)
        ),
    )
