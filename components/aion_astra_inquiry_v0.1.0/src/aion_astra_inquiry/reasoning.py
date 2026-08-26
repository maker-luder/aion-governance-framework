from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Protocol

from .core import AgentId, InquiryContext, PeerContribution, Probe, ProbeKind


@dataclass(frozen=True)
class ReasoningDecision:
    claim: str
    challenge: str
    evidence_query: str
    probe_kind: ProbeKind
    probe_description: str
    stop_vote: bool
    private_note: str


class ReasoningProvider(Protocol):
    """Reasoning boundary for one exact AION or ASTRA peer."""

    @property
    def agent_id(self) -> AgentId:
        ...

    def decide(self, context: InquiryContext, private_notes: tuple[str, ...]) -> ReasoningDecision:
        ...


class ProviderBackedPeer:
    """Bind one independent reasoning provider to the InquiryPeer protocol.

    Private notes stay on the provider-specific peer instance and are not copied into
    the shared dialogue context. The shared transcript remains explicit evidence;
    private notes are merely local engineering state, not hidden-chain-of-thought
    evidence and not an identity claim.
    """

    def __init__(self, provider: ReasoningProvider, *, max_private_notes: int = 12) -> None:
        if not 1 <= max_private_notes <= 100:
            raise ValueError("max_private_notes must be between 1 and 100")
        self._provider = provider
        self._max_private_notes = max_private_notes
        self._private_notes: list[str] = []

    @property
    def agent_id(self) -> AgentId:
        return self._provider.agent_id

    @property
    def private_notes(self) -> tuple[str, ...]:
        return tuple(self._private_notes)

    def contribute(self, context: InquiryContext) -> PeerContribution:
        if context.speaker is not self.agent_id:
            raise ValueError("reasoning provider is bound to the wrong inquiry speaker")
        decision = self._provider.decide(context, tuple(self._private_notes))
        if not isinstance(decision, ReasoningDecision):
            raise TypeError("reasoning provider must return ReasoningDecision")
        note = decision.private_note.strip()
        if note:
            self._private_notes.append(note[:1_000])
            if len(self._private_notes) > self._max_private_notes:
                self._private_notes = self._private_notes[-self._max_private_notes :]
        return PeerContribution(
            claim=decision.claim,
            challenge=decision.challenge,
            evidence_query=decision.evidence_query,
            proposed_probe=Probe(decision.probe_kind, decision.probe_description),
            stop_vote=decision.stop_vote,
        )


class EvidenceDrivenReasoningProvider:
    """Offline deterministic reasoning provider over the bounded shared evidence.

    It is deliberately modest: it forms a working interpretation, identifies an
    epistemic gap, asks the repository for the next evidence slice, and challenges
    the peer's latest public claim. It performs no model call, network call, shell
    execution, repository mutation, deployment, or canonical write.
    """

    _STOPWORDS = {
        "about",
        "after",
        "again",
        "also",
        "because",
        "could",
        "does",
        "from",
        "have",
        "into",
        "should",
        "that",
        "their",
        "there",
        "these",
        "this",
        "what",
        "when",
        "where",
        "which",
        "with",
        "would",
        "研究",
        "證據",
        "是否",
        "什麼",
        "怎麼",
        "如何",
    }

    def __init__(self, agent_id: AgentId, *, min_evidence_before_stop: int = 2) -> None:
        if min_evidence_before_stop < 1:
            raise ValueError("min_evidence_before_stop must be positive")
        self._agent_id = agent_id
        self._min_evidence_before_stop = min_evidence_before_stop

    @property
    def agent_id(self) -> AgentId:
        return self._agent_id

    def decide(self, context: InquiryContext, private_notes: tuple[str, ...]) -> ReasoningDecision:
        if context.speaker is not self._agent_id:
            raise ValueError("context speaker does not match reasoning provider")
        keywords = _keywords(context.question)
        latest_peer_claim = next(
            (
                event.claim
                for event in reversed(context.transcript)
                if event.speaker is context.peer
            ),
            "",
        )
        evidence_summary = _evidence_summary(context)
        if self._agent_id is AgentId.AION:
            return self._aion_decision(
                context=context,
                keywords=keywords,
                latest_peer_claim=latest_peer_claim,
                evidence_summary=evidence_summary,
                private_notes=private_notes,
            )
        return self._astra_decision(
            context=context,
            keywords=keywords,
            latest_peer_claim=latest_peer_claim,
            evidence_summary=evidence_summary,
            private_notes=private_notes,
        )

    def _aion_decision(
        self,
        *,
        context: InquiryContext,
        keywords: tuple[str, ...],
        latest_peer_claim: str,
        evidence_summary: str,
        private_notes: tuple[str, ...],
    ) -> ReasoningDecision:
        if context.evidence:
            claim = (
                "AION working synthesis: the current repository evidence indicates "
                f"{evidence_summary}. The interpretation remains provisional until a direct "
                "counterexample or matched control is checked."
            )
        else:
            claim = (
                "AION working hypothesis: answer the question from repository evidence first, "
                "then distinguish an implemented mechanism from documentation, expectation, or claim."
            )
        challenge = ""
        if latest_peer_claim:
            challenge = (
                "AION response to ASTRA: preserve the challenge, but test it at the smallest causal "
                f"point rather than treating it as settled: {_clip(latest_peer_claim, 220)}"
            )
        evidence_query = _query(
            keywords,
            extras=("test", "evidence", "falsifier", "validation") if context.round_index > 1 else (),
        )
        probe_kind = ProbeKind.REPOSITORY_OBSERVATION if context.round_index == 1 else ProbeKind.ABLATION_PLAN
        probe_description = (
            "Locate the smallest repository evidence surface that directly bears on the working hypothesis."
            if context.round_index == 1
            else "Form a bounded ablation or matched-control plan around the strongest remaining alternative explanation."
        )
        stop_vote = self._should_stop(context)
        private_note = (
            f"AION round {context.round_index}; evidence={len(context.evidence)}; "
            f"prior_private_notes={len(private_notes)}; next_query={evidence_query}"
        )
        return ReasoningDecision(
            claim=claim,
            challenge=challenge,
            evidence_query=evidence_query,
            probe_kind=probe_kind,
            probe_description=probe_description,
            stop_vote=stop_vote,
            private_note=private_note,
        )

    def _astra_decision(
        self,
        *,
        context: InquiryContext,
        keywords: tuple[str, ...],
        latest_peer_claim: str,
        evidence_summary: str,
        private_notes: tuple[str, ...],
    ) -> ReasoningDecision:
        if context.evidence:
            claim = (
                "ASTRA critical synthesis: the available evidence supports only a bounded engineering "
                f"reading: {evidence_summary}. It does not by itself establish the strongest interpretation."
            )
        else:
            claim = (
                "ASTRA critical hypothesis: the first useful result may be identifying what evidence is "
                "missing, contradictory, or confounded rather than forcing a positive answer."
            )
        challenge = (
            "ASTRA challenge: search for a counterexample, confound, stale assumption, or test that would "
            "make the current interpretation fail."
        )
        if latest_peer_claim:
            challenge += f" Target the public AION claim: {_clip(latest_peer_claim, 220)}"
        evidence_query = _query(keywords, extras=("confound", "counterexample", "HOLD", "NOT_ESTABLISHED", "falsifier"))
        probe_kind = ProbeKind.COUNTEREXAMPLE_SEARCH
        probe_description = "Search for repository evidence that would weaken or falsify the current working interpretation."
        stop_vote = self._should_stop(context)
        private_note = (
            f"ASTRA round {context.round_index}; evidence={len(context.evidence)}; "
            f"prior_private_notes={len(private_notes)}; next_query={evidence_query}"
        )
        return ReasoningDecision(
            claim=claim,
            challenge=challenge,
            evidence_query=evidence_query,
            probe_kind=probe_kind,
            probe_description=probe_description,
            stop_vote=stop_vote,
            private_note=private_note,
        )

    def _should_stop(self, context: InquiryContext) -> bool:
        return context.round_index >= 2 and len(context.evidence) >= self._min_evidence_before_stop


def _keywords(text: str, *, limit: int = 8) -> tuple[str, ...]:
    tokens = re.findall(r"[A-Za-z0-9_./:-]{3,}|[\u4e00-\u9fff]{2,}", text.lower())
    unique: list[str] = []
    for token in tokens:
        if token in EvidenceDrivenReasoningProvider._STOPWORDS or token in unique:
            continue
        unique.append(token)
        if len(unique) >= limit:
            break
    return tuple(unique)


def _query(keywords: tuple[str, ...], *, extras: tuple[str, ...]) -> str:
    terms = list(keywords[:6])
    for term in extras:
        if term not in terms:
            terms.append(term)
    return " ".join(terms[:10]) or "research evidence falsifier"


def _evidence_summary(context: InquiryContext) -> str:
    if not context.evidence:
        return "no direct repository evidence has been retrieved yet"
    items = [f"{item.ref}: {_clip(item.excerpt, 150)}" for item in context.evidence[:2]]
    return "; ".join(items)


def _clip(text: str, limit: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"
