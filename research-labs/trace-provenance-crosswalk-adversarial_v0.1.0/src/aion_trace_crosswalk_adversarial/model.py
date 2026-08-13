from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping

from aion_trace_crosswalk import AIONTraceEvent, TracePolicy, from_openinference_attributes, to_openinference_attributes


class AuditStatus(str, Enum):
    ADMITTED_FOR_REVIEW = "ADMITTED_FOR_REVIEW"
    HOLD = "HOLD"
    INVALID = "INVALID"


CURRENTNESS = frozenset({"CURRENT", "STALE", "HISTORICAL", "UNKNOWN", "RETRIEVED_ONLY", "REMEMBERED"})
SOURCE_KINDS = frozenset({"Human Owner", "ChatGPT Research Review", "Manus", "Repository Evidence", "External Literature", "Tool Output", "Synthetic Fixture"})


@dataclass(frozen=True, slots=True)
class CrosswalkEntry:
    entry_id: str
    source_ref: str
    source_kind: str
    what: str
    who: str
    where: str
    when: str
    method: str
    authority: str
    transformation: str
    currentness: str
    target_field: str
    evidence_reused: bool = True
    new_evidence_claimed: bool = False


@dataclass(frozen=True, slots=True)
class CrosswalkAudit:
    status: AuditStatus
    reason: str
    mapped_keys: tuple[str, ...] = ()
    source_entry_count: int = 0
    authority: str = "EXTERNAL_OBSERVATION_ONLY"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    model_execution: bool = False
    observed_result: str = "NOT_EVALUATED"
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "mapped_keys": list(self.mapped_keys),
            "source_entry_count": self.source_entry_count,
            "authority": self.authority,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "model_execution": self.model_execution,
            "observed_result": self.observed_result,
            "scientific_conclusion": self.scientific_conclusion,
            "subjectivity_conclusion": self.subjectivity_conclusion,
        }


def _audit(status: AuditStatus, reason: str, *, mapped_keys: Iterable[str] = (), count: int = 0, authority: str = "EXTERNAL_OBSERVATION_ONLY") -> CrosswalkAudit:
    return CrosswalkAudit(status, reason, tuple(mapped_keys), count, authority)


def audit_source_entry(entry: CrosswalkEntry) -> CrosswalkAudit:
    fields = (entry.entry_id, entry.source_ref, entry.source_kind, entry.what, entry.who, entry.where, entry.when, entry.method, entry.authority, entry.transformation, entry.currentness, entry.target_field)
    if any(not value.strip() for value in fields):
        return _audit(AuditStatus.INVALID, "SOURCE_ATTRIBUTION_FIELD_MISSING")
    if entry.source_kind not in SOURCE_KINDS:
        return _audit(AuditStatus.INVALID, "SOURCE_KIND_UNCONTROLLED")
    if entry.currentness not in CURRENTNESS:
        return _audit(AuditStatus.INVALID, "CURRENTNESS_UNCONTROLLED")
    if entry.new_evidence_claimed and entry.evidence_reused:
        return _audit(AuditStatus.INVALID, "REUSED_REFERENCE_MISLABELED_AS_NEW_EVIDENCE")
    if entry.authority == "EXTERNAL_OBSERVATION_ONLY" and entry.new_evidence_claimed:
        return _audit(AuditStatus.HOLD, "EXTERNAL_OBSERVATION_NOT_NEW_EVIDENCE")
    if entry.currentness in {"STALE", "HISTORICAL", "RETRIEVED_ONLY", "REMEMBERED", "UNKNOWN"}:
        return _audit(AuditStatus.HOLD, "SOURCE_CURRENTNESS_REQUIRES_REVIEW", count=1)
    return _audit(AuditStatus.ADMITTED_FOR_REVIEW, "SOURCE_ENTRY_REVIEW_METADATA_ONLY", count=1)


def audit_source_entries(entries: Iterable[CrosswalkEntry]) -> CrosswalkAudit:
    items = tuple(entries)
    if not items:
        return _audit(AuditStatus.HOLD, "CROSSWALK_EMPTY")
    ids = [entry.entry_id for entry in items]
    if len(ids) != len(set(ids)):
        return _audit(AuditStatus.INVALID, "DUPLICATE_CROSSWALK_ENTRY_ID", count=len(items))
    refs = [entry.source_ref for entry in items]
    if any(not ref.strip() for ref in refs):
        return _audit(AuditStatus.INVALID, "SOURCE_REF_MISSING", count=len(items))
    if any(entry.new_evidence_claimed and entry.evidence_reused for entry in items):
        return _audit(AuditStatus.INVALID, "REUSED_REFERENCE_MISLABELED_AS_NEW_EVIDENCE", count=len(items))
    if any(entry.currentness != "CURRENT" for entry in items):
        return _audit(AuditStatus.HOLD, "CROSSWALK_CURRENTNESS_REQUIRES_REVIEW", count=len(items))
    return _audit(AuditStatus.ADMITTED_FOR_REVIEW, "CROSSWALK_REVIEW_METADATA_ONLY", count=len(items))


def audit_trace_crosswalk(event: AIONTraceEvent, policy: TracePolicy | None = None, *, external_attributes: Mapping[str, Any] | None = None) -> CrosswalkAudit:
    if event.graph_node_id is not None and event.graph_node_id == event.graph_parent_id:
        return _audit(AuditStatus.INVALID, "GRAPH_SELF_PARENT")
    if event.source_ref is not None and not event.source_ref.strip():
        return _audit(AuditStatus.INVALID, "SOURCE_REF_BLANK")
    if event.approval_ref is not None and not event.approval_ref.strip():
        return _audit(AuditStatus.INVALID, "APPROVAL_REF_BLANK")
    effective_policy = policy or TracePolicy()
    if effective_policy.include_input_value or effective_policy.include_output_value or effective_policy.include_tool_parameters:
        return _audit(AuditStatus.HOLD, "RAW_TRACE_CONTENT_EXPORT_REQUIRES_REVIEW")
    attrs = to_openinference_attributes(event, effective_policy)
    required = {"session.id", "user.id", "agent.name", "openinference.span.kind", "aion.runtime_event_id", "aion.subject_id", "aion.canonical_effect"}
    if not required.issubset(attrs):
        return _audit(AuditStatus.INVALID, "CORE_TRACE_KEYS_MISSING", mapped_keys=attrs)
    if attrs.get("aion.canonical_effect") != "NONE":
        return _audit(AuditStatus.INVALID, "CANONICAL_EFFECT_REQUESTED", mapped_keys=attrs)
    if external_attributes is not None:
        if any(key.startswith("aion.") for key in external_attributes):
            return _audit(AuditStatus.HOLD, "EXTERNAL_AION_NAMESPACE_REQUIRES_REVIEW", mapped_keys=external_attributes)
        try:
            imported = from_openinference_attributes(external_attributes)
        except (TypeError, ValueError):
            return _audit(AuditStatus.INVALID, "EXTERNAL_ATTRIBUTE_PARSE_INVALID", mapped_keys=external_attributes)
        if imported.authority != "EXTERNAL_OBSERVATION_ONLY" or imported.canonical_effect != "NONE":
            return _audit(AuditStatus.INVALID, "EXTERNAL_AUTHORITY_BOUNDARY_BROKEN", mapped_keys=external_attributes)
    return _audit(AuditStatus.ADMITTED_FOR_REVIEW, "TRACE_CROSSWALK_REVIEW_METADATA_ONLY", mapped_keys=attrs)


def audit_event_batch(events: Iterable[AIONTraceEvent]) -> CrosswalkAudit:
    items = tuple(events)
    if not items:
        return _audit(AuditStatus.HOLD, "TRACE_BATCH_EMPTY")
    ids = [event.runtime_event_id for event in items]
    if len(ids) != len(set(ids)):
        return _audit(AuditStatus.INVALID, "DUPLICATE_RUNTIME_EVENT_ID", count=len(items))
    if any(event.canonical_effect != "NONE" for event in items):
        return _audit(AuditStatus.INVALID, "CANONICAL_EFFECT_REQUESTED", count=len(items))
    return _audit(AuditStatus.ADMITTED_FOR_REVIEW, "TRACE_BATCH_REVIEW_METADATA_ONLY", count=len(items))
