"""Offline evidence-linked IQC/NCR/CAPA lifecycle contract."""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import StrEnum
from datetime import datetime
import hashlib
import json
import re


class CapaError(ValueError):
    pass


class IssueState(StrEnum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    CONTAINED = "CONTAINED"
    CORRECTIVE_ACTION = "CORRECTIVE_ACTION"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"


_ALLOWED: dict[IssueState, frozenset[IssueState]] = {
    IssueState.OPEN: frozenset({IssueState.INVESTIGATING, IssueState.REJECTED}),
    IssueState.INVESTIGATING: frozenset({IssueState.CONTAINED, IssueState.CORRECTIVE_ACTION, IssueState.REJECTED}),
    IssueState.CONTAINED: frozenset({IssueState.CORRECTIVE_ACTION, IssueState.REJECTED}),
    IssueState.CORRECTIVE_ACTION: frozenset({IssueState.VERIFIED}),
    IssueState.VERIFIED: frozenset({IssueState.CLOSED}),
    IssueState.CLOSED: frozenset(),
    IssueState.REJECTED: frozenset(),
}
_SECRET = re.compile(r"(token|secret|password|cookie|credential|api[_-]?key)", re.I)


def _check_refs(refs: tuple[str, ...], *, required: bool) -> None:
    if required and not refs:
        raise CapaError("evidence is required for this transition")
    if any(not ref or ref.startswith(("/", "\\")) or "://" in ref for ref in refs):
        raise CapaError("evidence references must be symbolic repository-safe references")
    if any(_SECRET.search(ref) for ref in refs):
        raise CapaError("secret-like evidence reference is prohibited")


@dataclass(frozen=True)
class Issue:
    issue_id: str
    title: str
    severity: str
    owner_role: str
    evidence_refs: tuple[str, ...] = ()
    state: IssueState = IssueState.OPEN
    canonical_effect: str = "NONE"
    deployment: bool = False
    independent_ivv: str = "NOT_ACHIEVED"


@dataclass(frozen=True)
class CapaEvent:
    event_id: str
    issue_id: str
    actor: str
    occurred_at: str
    from_state: IssueState
    to_state: IssueState
    evidence_refs: tuple[str, ...]
    previous_digest: str
    digest: str


class CapaLedger:
    def __init__(self) -> None:
        self._issues: dict[str, Issue] = {}
        self._events: list[CapaEvent] = []

    def open_issue(self, issue: Issue) -> Issue:
        if not issue.issue_id or issue.issue_id in self._issues:
            raise CapaError("issue_id must be unique and non-empty")
        if issue.canonical_effect != "NONE" or issue.deployment or issue.independent_ivv != "NOT_ACHIEVED":
            raise CapaError("governance boundary violation")
        _check_refs(issue.evidence_refs, required=False)
        if issue.state != IssueState.OPEN:
            raise CapaError("new issues must start OPEN")
        self._issues[issue.issue_id] = issue
        return issue

    def get(self, issue_id: str) -> Issue:
        try:
            return self._issues[issue_id]
        except KeyError as exc:
            raise CapaError(f"unknown issue: {issue_id}") from exc

    def transition(self, issue_id: str, to_state: IssueState, *, actor: str, occurred_at: str, evidence_refs: tuple[str, ...] = ()) -> CapaEvent:
        current = self.get(issue_id)
        if to_state not in _ALLOWED[current.state]:
            raise CapaError(f"invalid transition {current.state}->{to_state}")
        try:
            parsed = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise CapaError("occurred_at must be ISO-8601") from exc
        if parsed.tzinfo is None:
            raise CapaError("occurred_at must include timezone")
        _check_refs(evidence_refs, required=to_state in {IssueState.VERIFIED, IssueState.CLOSED})
        previous_digest = self._events[-1].digest if self._events else "GENESIS"
        event_payload = {
            "event_id": f"event.{len(self._events) + 1}",
            "issue_id": issue_id,
            "actor": actor,
            "occurred_at": occurred_at,
            "from_state": current.state.value,
            "to_state": to_state.value,
            "evidence_refs": tuple(sorted(evidence_refs)),
            "previous_digest": previous_digest,
        }
        digest = hashlib.sha256(json.dumps(event_payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        event = CapaEvent(
            event_id=event_payload["event_id"],
            issue_id=issue_id,
            actor=actor,
            occurred_at=occurred_at,
            from_state=current.state,
            to_state=to_state,
            evidence_refs=tuple(sorted(evidence_refs)),
            previous_digest=previous_digest,
            digest=digest,
        )
        self._events.append(event)
        self._issues[issue_id] = replace(current, state=to_state)
        return event

    def validate_chain(self) -> tuple[str, ...]:
        errors: list[str] = []
        previous = "GENESIS"
        for event in self._events:
            payload = {
                "event_id": event.event_id,
                "issue_id": event.issue_id,
                "actor": event.actor,
                "occurred_at": event.occurred_at,
                "from_state": event.from_state.value,
                "to_state": event.to_state.value,
                "evidence_refs": tuple(sorted(event.evidence_refs)),
                "previous_digest": event.previous_digest,
            }
            expected = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            if event.previous_digest != previous or event.digest != expected:
                errors.append(event.event_id)
            previous = event.digest
        return tuple(errors)

    def snapshot(self) -> dict[str, object]:
        if self.validate_chain():
            raise CapaError("event chain is invalid")
        return {
            "issues": [asdict(self._issues[key]) for key in sorted(self._issues)],
            "events": [asdict(event) for event in self._events],
            "canonical_effect": "NONE",
            "deployment": False,
            "independent_ivv": "NOT_ACHIEVED",
        }
