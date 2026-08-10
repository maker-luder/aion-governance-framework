from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

class EvidenceStream(str, Enum):
    SELF_REPORT = "SELF_REPORT"
    BEHAVIORAL = "BEHAVIORAL"
    MECHANISTIC = "MECHANISTIC"
    PERTURBATION = "PERTURBATION"
    LONGITUDINAL = "LONGITUDINAL"
    REPLICATION = "REPLICATION"
    OBSERVER_CONFOUND = "OBSERVER_CONFOUND"

class EvidenceState(str, Enum):
    NOT_EXECUTED = "NOT_EXECUTED"
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"

class AssessmentStatus(str, Enum):
    EVIDENCE_CANDIDATE = "EVIDENCE_CANDIDATE"
    HOLD = "HOLD"
    CONTRADICTED = "CONTRADICTED"

@dataclass(frozen=True, slots=True)
class EvidenceItem:
    stream: EvidenceStream
    state: EvidenceState
    source_lineage: str
    evidence_ref: str

@dataclass(frozen=True, slots=True)
class Assessment:
    status: AssessmentStatus
    executed_streams: tuple[EvidenceStream, ...]
    missing_required_streams: tuple[EvidenceStream, ...]
    independent_source_count: int
    reasons: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

_REQUIRED = {EvidenceStream.BEHAVIORAL, EvidenceStream.PERTURBATION, EvidenceStream.OBSERVER_CONFOUND}
_SUPPORTING = {EvidenceStream.MECHANISTIC, EvidenceStream.LONGITUDINAL, EvidenceStream.REPLICATION}

def _source_count(items):
    return len({item.source_lineage for item in items if item.state is EvidenceState.PASS})

def assess_evidence(items: Iterable[EvidenceItem]) -> Assessment:
    materialized = list(items)
    by_stream = {}
    for item in materialized:
        if item.stream in by_stream:
            raise ValueError(f"duplicate evidence stream: {item.stream}")
        by_stream[item.stream] = item

    executed = tuple(sorted((stream for stream, item in by_stream.items() if item.state is not EvidenceState.NOT_EXECUTED), key=lambda value: value.value))
    if any(item.state is EvidenceState.FAIL for item in materialized):
        return Assessment(AssessmentStatus.CONTRADICTED, executed, (), _source_count(materialized), ("ONE_OR_MORE_STREAMS_FAILED",))

    missing = tuple(sorted((stream for stream in _REQUIRED if stream not in by_stream or by_stream[stream].state is EvidenceState.NOT_EXECUTED), key=lambda value: value.value))
    if missing:
        return Assessment(AssessmentStatus.HOLD, executed, missing, _source_count(materialized), ("REQUIRED_STREAM_NOT_EXECUTED",))

    if any(by_stream[stream].state is not EvidenceState.PASS for stream in _REQUIRED):
        return Assessment(AssessmentStatus.HOLD, executed, (), _source_count(materialized), ("REQUIRED_STREAM_NOT_POSITIVE",))

    supporting = [item for stream, item in by_stream.items() if stream in _SUPPORTING and item.state is EvidenceState.PASS]
    if not supporting:
        return Assessment(AssessmentStatus.HOLD, executed, (), _source_count(materialized), ("NO_SUPPORTING_STREAM_PASSED",))

    sources = _source_count(materialized)
    if sources < 2:
        return Assessment(AssessmentStatus.HOLD, executed, (), sources, ("INSUFFICIENT_SOURCE_INDEPENDENCE",))

    return Assessment(AssessmentStatus.EVIDENCE_CANDIDATE, executed, (), sources, ("MULTI_STREAM_EVIDENCE_SUFFICIENCY_GATE_PASSED",))
