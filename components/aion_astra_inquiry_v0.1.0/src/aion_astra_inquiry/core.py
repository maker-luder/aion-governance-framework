from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Protocol


class AgentId(str, Enum):
    AION = "AION"
    ASTRA = "ASTRA"


class ProbeKind(str, Enum):
    REPOSITORY_OBSERVATION = "REPOSITORY_OBSERVATION"
    REPLAY_CHECK = "REPLAY_CHECK"
    SYNTHETIC_TEST_PLAN = "SYNTHETIC_TEST_PLAN"
    ABLATION_PLAN = "ABLATION_PLAN"
    COUNTEREXAMPLE_SEARCH = "COUNTEREXAMPLE_SEARCH"


class StopReason(str, Enum):
    MUTUAL_STOP = "MUTUAL_STOP"
    MAX_ROUNDS = "MAX_ROUNDS"


@dataclass(frozen=True)
class Probe:
    kind: ProbeKind
    description: str
    network_access: bool = False
    repository_mutation: bool = False
    deployment: bool = False
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ValueError("probe description must not be empty")
        if self.network_access:
            raise ValueError("probe-level network authority is not permitted in v0.1.0")
        if self.repository_mutation:
            raise ValueError("repository mutation is not permitted in v0.1.0")
        if self.deployment:
            raise ValueError("deployment is not permitted in v0.1.0")
        if self.canonical_effect != "NONE":
            raise ValueError("canonical effect must remain NONE")


@dataclass(frozen=True)
class EvidenceItem:
    ref: str
    excerpt: str
    content_sha256: str
    source_class: str = "REPOSITORY"
    source_url: str = ""
    publisher: str = ""
    retrieved_at: str = ""
    retrieval_agent: str = ""
    trust: str = "TRUSTED_REPOSITORY"


@dataclass(frozen=True)
class PeerContribution:
    claim: str
    challenge: str = ""
    evidence_query: str = ""
    proposed_probe: Probe | None = None
    stop_vote: bool = False

    def __post_init__(self) -> None:
        if not self.claim.strip():
            raise ValueError("claim must not be empty")


@dataclass(frozen=True)
class DialogueEvent:
    sequence: int
    round_index: int
    speaker: AgentId
    claim: str
    challenge: str
    evidence_query: str
    evidence_refs: tuple[str, ...]
    probe_kind: ProbeKind | None
    probe_description: str | None
    stop_vote: bool
    previous_hash: str
    event_hash: str


@dataclass(frozen=True)
class InquiryContext:
    question: str
    round_index: int
    speaker: AgentId
    peer: AgentId
    transcript: tuple[DialogueEvent, ...]
    evidence: tuple[EvidenceItem, ...]


@dataclass(frozen=True)
class InquiryReport:
    question: str
    transcript: tuple[DialogueEvent, ...]
    evidence: tuple[EvidenceItem, ...]
    stop_reason: StopReason
    candidate_findings: tuple[str, ...]
    final_chain_hash: str
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False
    autonomous_merge: bool = False


class InquiryPeer(Protocol):
    def contribute(self, context: InquiryContext) -> PeerContribution:
        ...


class EvidenceSource(Protocol):
    def search(
        self,
        query: str,
        limit: int = 5,
        requester: AgentId | None = None,
    ) -> tuple[EvidenceItem, ...]:
        ...


class RepositoryTextEvidenceSource:
    """Bounded, read-only keyword retrieval over repository text files."""

    _ALLOWED_SUFFIXES = {
        ".json",
        ".md",
        ".py",
        ".rego",
        ".sh",
        ".toml",
        ".txt",
        ".yaml",
        ".yml",
    }
    _EXCLUDED_PARTS = {".git", ".mypy_cache", ".pytest_cache", ".venv", "__pycache__", "node_modules"}
    _QUERY_STOPWORDS = {
        "about",
        "after",
        "also",
        "and",
        "bounded",
        "current",
        "evidence",
        "for",
        "from",
        "into",
        "only",
        "repository",
        "research",
        "same",
        "that",
        "the",
        "this",
        "under",
        "what",
        "which",
        "with",
    }

    def __init__(
        self,
        root: Path,
        *,
        max_file_bytes: int = 131_072,
        max_files_scanned: int = 2_000,
    ) -> None:
        resolved = root.resolve()
        if not resolved.is_dir():
            raise ValueError("repository evidence root must be an existing directory")
        if max_file_bytes <= 0 or max_files_scanned <= 0:
            raise ValueError("scan limits must be positive")
        self._root = resolved
        self._max_file_bytes = max_file_bytes
        self._max_files_scanned = max_files_scanned

    def search(
        self,
        query: str,
        limit: int = 5,
        requester: AgentId | None = None,
    ) -> tuple[EvidenceItem, ...]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        raw_tokens = re.findall(r"[A-Za-z0-9_./:-]{2,}|[\u4e00-\u9fff]{2,}", query.lower())
        tokens = tuple(dict.fromkeys(token for token in raw_tokens if token not in self._QUERY_STOPWORDS))
        if not tokens:
            return ()

        ranked: list[tuple[int, str, EvidenceItem]] = []
        scanned = 0
        for path in sorted(self._root.rglob("*")):
            if scanned >= self._max_files_scanned:
                break
            if not path.is_file() or path.is_symlink():
                continue
            try:
                relative = path.resolve().relative_to(self._root)
            except ValueError:
                continue
            if any(part in self._EXCLUDED_PARTS for part in relative.parts):
                continue
            if _is_low_signal_inventory(relative):
                continue
            if path.suffix.lower() not in self._ALLOWED_SUFFIXES:
                continue
            try:
                if path.stat().st_size > self._max_file_bytes:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            scanned += 1
            lowered = text.lower()
            matched = tuple(token for token in tokens if token in lowered)
            if not matched:
                continue
            coverage = len(matched)
            occurrences = sum(min(lowered.count(token), 12) for token in matched)
            score = coverage * 100 + occurrences + _evidence_path_bias(relative)
            excerpt = _best_excerpt(text, matched)
            ref = relative.as_posix()
            item = EvidenceItem(
                ref=ref,
                excerpt=excerpt,
                content_sha256=sha256(text.encode("utf-8")).hexdigest(),
                retrieval_agent=requester.value if requester else "",
            )
            ranked.append((score, ref, item))

        ranked.sort(key=lambda item: (-item[0], item[1]))
        return tuple(item for _, _, item in ranked[:limit])


class BoundedInquiryLoop:
    """Alternating AION/Astra inquiry with evidence retrieval and fail-closed authority boundaries."""

    def __init__(self, evidence_source: EvidenceSource, *, max_rounds: int = 3, evidence_limit: int = 4) -> None:
        if not 1 <= max_rounds <= 12:
            raise ValueError("max_rounds must be between 1 and 12")
        if not 1 <= evidence_limit <= 20:
            raise ValueError("evidence_limit must be between 1 and 20")
        self._evidence_source = evidence_source
        self._max_rounds = max_rounds
        self._evidence_limit = evidence_limit

    def run(self, question: str, *, aion: InquiryPeer, astra: InquiryPeer) -> InquiryReport:
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("question must not be empty")

        peers: dict[AgentId, InquiryPeer] = {AgentId.AION: aion, AgentId.ASTRA: astra}
        transcript: list[DialogueEvent] = []
        evidence_by_ref: dict[str, EvidenceItem] = {}
        previous_hash = "GENESIS"
        stop_reason = StopReason.MAX_ROUNDS

        for round_index in range(1, self._max_rounds + 1):
            stop_votes: list[bool] = []
            for speaker, peer_id in ((AgentId.AION, AgentId.ASTRA), (AgentId.ASTRA, AgentId.AION)):
                context = InquiryContext(
                    question=normalized_question,
                    round_index=round_index,
                    speaker=speaker,
                    peer=peer_id,
                    transcript=tuple(transcript),
                    evidence=tuple(evidence_by_ref.values()),
                )
                contribution = peers[speaker].contribute(context)
                if not isinstance(contribution, PeerContribution):
                    raise TypeError("peer must return PeerContribution")

                found = (
                    self._evidence_source.search(
                        contribution.evidence_query,
                        limit=self._evidence_limit,
                        requester=speaker,
                    )
                    if contribution.evidence_query.strip()
                    else ()
                )
                for item in found:
                    evidence_by_ref.setdefault(item.ref, item)

                event_payload = {
                    "sequence": len(transcript) + 1,
                    "round_index": round_index,
                    "speaker": speaker.value,
                    "claim": contribution.claim,
                    "challenge": contribution.challenge,
                    "evidence_query": contribution.evidence_query,
                    "evidence_refs": [item.ref for item in found],
                    "probe_kind": contribution.proposed_probe.kind.value if contribution.proposed_probe else None,
                    "probe_description": contribution.proposed_probe.description if contribution.proposed_probe else None,
                    "stop_vote": contribution.stop_vote,
                }
                event_hash = _hash_event(previous_hash, event_payload)
                event = DialogueEvent(
                    sequence=event_payload["sequence"],  # type: ignore[arg-type]
                    round_index=round_index,
                    speaker=speaker,
                    claim=contribution.claim,
                    challenge=contribution.challenge,
                    evidence_query=contribution.evidence_query,
                    evidence_refs=tuple(item.ref for item in found),
                    probe_kind=contribution.proposed_probe.kind if contribution.proposed_probe else None,
                    probe_description=contribution.proposed_probe.description if contribution.proposed_probe else None,
                    stop_vote=contribution.stop_vote,
                    previous_hash=previous_hash,
                    event_hash=event_hash,
                )
                transcript.append(event)
                previous_hash = event_hash
                stop_votes.append(contribution.stop_vote)

            if all(stop_votes):
                stop_reason = StopReason.MUTUAL_STOP
                break

        candidate_findings = tuple(event.claim for event in transcript[-2:])
        return InquiryReport(
            question=normalized_question,
            transcript=tuple(transcript),
            evidence=tuple(evidence_by_ref.values()),
            stop_reason=stop_reason,
            candidate_findings=candidate_findings,
            final_chain_hash=previous_hash,
        )


def verify_transcript_chain(report: InquiryReport) -> bool:
    previous_hash = "GENESIS"
    for event in report.transcript:
        if event.previous_hash != previous_hash:
            return False
        payload = {
            "sequence": event.sequence,
            "round_index": event.round_index,
            "speaker": event.speaker.value,
            "claim": event.claim,
            "challenge": event.challenge,
            "evidence_query": event.evidence_query,
            "evidence_refs": list(event.evidence_refs),
            "probe_kind": event.probe_kind.value if event.probe_kind else None,
            "probe_description": event.probe_description,
            "stop_vote": event.stop_vote,
        }
        if _hash_event(previous_hash, payload) != event.event_hash:
            return False
        previous_hash = event.event_hash
    return previous_hash == report.final_chain_hash


def tamper_event_for_test(event: DialogueEvent, *, claim: str) -> DialogueEvent:
    """Explicit test helper; returns a changed immutable event without recomputing its hash."""

    return replace(event, claim=claim)


def _is_low_signal_inventory(relative: Path) -> bool:
    if not relative.parts:
        return False
    if relative.parts[0] == "manifest":
        return True
    if len(relative.parts) >= 2 and relative.parts[:2] == ("qa", "historical"):
        return True
    if len(relative.parts) >= 2 and relative.parts[:2] == ("components", "aion_astra_inquiry_v0.1.0"):
        return True
    return False


def _evidence_path_bias(relative: Path) -> int:
    if not relative.parts:
        return 0
    if relative.parts[0] == "research-labs":
        return 80
    if len(relative.parts) >= 2 and relative.parts[:2] == ("docs", "research"):
        return 70
    if relative.parts[0] == "components":
        return 45
    if relative.parts[0] == "docs":
        return 25 if "history" not in relative.parts else -10
    if relative.parts[0] == "qa":
        return -30
    return 0


def _best_excerpt(text: str, tokens: tuple[str, ...]) -> str:
    lines = text.splitlines() or [text]
    best_index = 0
    best_score = -1
    for index, line in enumerate(lines):
        lowered = line.lower()
        matched = [token for token in tokens if token in lowered]
        if not matched:
            continue
        score = len(matched) * 100 + sum(min(lowered.count(token), 8) for token in matched)
        if score > best_score:
            best_index = index
            best_score = score
    start_index = max(0, best_index - 1)
    end_index = min(len(lines), best_index + 2)
    excerpt = " ".join(" ".join(lines[start_index:end_index]).split())
    if len(excerpt) <= 480:
        return excerpt
    lowered = excerpt.lower()
    positions = [lowered.find(token) for token in tokens if lowered.find(token) >= 0]
    first = min(positions) if positions else 0
    start = max(0, first - 120)
    end = min(len(excerpt), first + 360)
    return excerpt[start:end]


def _hash_event(previous_hash: str, payload: dict[str, object]) -> str:
    encoded = json.dumps(
        {"previous_hash": previous_hash, "payload": payload},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()
