from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
import re

from .core import AgentId, EvidenceItem, InquiryReport, verify_transcript_chain


class ResearchOperationKind(str, Enum):
    INTERVENTION = "INTERVENTION"
    ABLATION = "ABLATION"
    REPLAY = "REPLAY"
    COUNTERFACTUAL = "COUNTERFACTUAL"


class OperationStatus(str, Enum):
    EXECUTED = "EXECUTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class ResearchOperationResult:
    sequence: int
    operation_id: str
    kind: ResearchOperationKind
    description: str
    status: OperationStatus
    baseline_score: float
    perturbed_score: float
    delta: float
    evidence_refs: tuple[str, ...]
    observation: str
    previous_hash: str
    operation_hash: str


@dataclass(frozen=True)
class DescriptiveStatistics:
    evidence_count: int
    unique_evidence_count: int
    source_class_count: int
    retrieval_agent_count: int
    mean_lexical_overlap: float
    min_lexical_overlap: float
    max_lexical_overlap: float
    dominant_source_share: float
    retrieval_agent_balance: float
    max_abs_perturbation_delta: float
    transcript_replay_passed: bool


@dataclass(frozen=True)
class FourDomainInterpretation:
    observation: str
    mechanism: str
    interpretation: str
    alternative_explanations: tuple[str, ...]
    unresolved_gaps: tuple[str, ...]
    causal_intervention_refs: tuple[str, ...]
    ablation_refs: tuple[str, ...]
    counterfactual_refs: tuple[str, ...]
    robustness_refs: tuple[str, ...]
    replication_refs: tuple[str, ...]


@dataclass(frozen=True)
class ResearchClosureReport:
    question: str
    source_dialogue_hash: str
    working_hypothesis: str
    competing_explanations: tuple[str, ...]
    operations: tuple[ResearchOperationResult, ...]
    statistics: DescriptiveStatistics
    four_domain: FourDomainInterpretation
    follow_up_question: str
    closure_hash: str
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    repository_mutation: bool = False
    network_authority: bool = False
    deployment: bool = False
    autonomous_merge: bool = False


class BoundedResearchClosure:
    """Execute deterministic evidence-plane research operations over one inquiry report.

    The closure deliberately does not execute arbitrary repository code. Intervention,
    ablation, replay, and counterfactual are implemented as bounded perturbations of
    admitted evidence and transcript state. They are engineering experiments over the
    evidence plane, not claims of real-world causal identification.
    """

    def close(self, report: InquiryReport) -> ResearchClosureReport:
        if not report.question.strip():
            raise ValueError("inquiry report question must not be empty")

        question_tokens = _tokens(report.question)
        evidence_scores = tuple(
            (item, _evidence_score(question_tokens, item)) for item in report.evidence
        )
        baseline = _mean(tuple(score for _, score in evidence_scores))
        operations: list[ResearchOperationResult] = []
        previous_hash = "GENESIS"

        def append_operation(
            *,
            kind: ResearchOperationKind,
            description: str,
            status: OperationStatus,
            perturbed_score: float,
            evidence_refs: tuple[str, ...],
            observation: str,
        ) -> None:
            nonlocal previous_hash
            sequence = len(operations) + 1
            operation_id = f"closure:{sequence}:{kind.value.lower()}"
            payload = {
                "sequence": sequence,
                "operation_id": operation_id,
                "kind": kind.value,
                "description": description,
                "status": status.value,
                "baseline_score": _rounded(baseline),
                "perturbed_score": _rounded(perturbed_score),
                "delta": _rounded(perturbed_score - baseline),
                "evidence_refs": list(evidence_refs),
                "observation": observation,
            }
            operation_hash = _hash_payload(previous_hash, payload)
            operations.append(
                ResearchOperationResult(
                    sequence=sequence,
                    operation_id=operation_id,
                    kind=kind,
                    description=description,
                    status=status,
                    baseline_score=_rounded(baseline),
                    perturbed_score=_rounded(perturbed_score),
                    delta=_rounded(perturbed_score - baseline),
                    evidence_refs=evidence_refs,
                    observation=observation,
                    previous_hash=previous_hash,
                    operation_hash=operation_hash,
                )
            )
            previous_hash = operation_hash

        replay_ok = verify_transcript_chain(report)
        append_operation(
            kind=ResearchOperationKind.REPLAY,
            description=(
                "Recompute the complete dialogue hash chain from GENESIS and compare it "
                "with the recorded final chain hash."
            ),
            status=OperationStatus.EXECUTED if replay_ok else OperationStatus.REJECTED,
            perturbed_score=baseline,
            evidence_refs=tuple(item.ref for item in report.evidence),
            observation=(
                "Transcript replay reproduced the recorded hash chain."
                if replay_ok
                else "Transcript replay failed; downstream interpretation must remain rejected."
            ),
        )

        intervention = _matched_partition(evidence_scores)
        if intervention is None:
            append_operation(
                kind=ResearchOperationKind.INTERVENTION,
                description=(
                    "Compare matched evidence partitions while changing one observable "
                    "retrieval/source factor and holding the scoring rule fixed."
                ),
                status=OperationStatus.INCONCLUSIVE,
                perturbed_score=baseline,
                evidence_refs=tuple(item.ref for item in report.evidence),
                observation=(
                    "No two non-empty matched evidence partitions were available; the "
                    "intervention comparison was not promoted to a causal claim."
                ),
            )
        else:
            label_a, score_a, refs_a, label_b, score_b, refs_b = intervention
            intervention_score = (score_a + score_b) / 2.0
            append_operation(
                kind=ResearchOperationKind.INTERVENTION,
                description=(
                    "Compare matched evidence partitions while changing one observable "
                    "retrieval/source factor and holding the scoring rule fixed."
                ),
                status=OperationStatus.EXECUTED,
                perturbed_score=intervention_score,
                evidence_refs=refs_a + refs_b,
                observation=(
                    f"Matched partition comparison {label_a}={_rounded(score_a):.4f} "
                    f"versus {label_b}={_rounded(score_b):.4f}; difference="
                    f"{_rounded(score_a - score_b):.4f}. This is evidence-plane sensitivity, "
                    "not real-world causal identification."
                ),
            )

        if len(evidence_scores) >= 2:
            strongest_item, strongest_score = max(
                evidence_scores, key=lambda pair: (pair[1], pair[0].ref)
            )
            remaining = tuple(
                score for item, score in evidence_scores if item.ref != strongest_item.ref
            )
            ablated = _mean(remaining)
            append_operation(
                kind=ResearchOperationKind.ABLATION,
                description=(
                    "Remove the single highest-overlap admitted evidence item and recompute "
                    "the same descriptive support metric."
                ),
                status=OperationStatus.EXECUTED,
                perturbed_score=ablated,
                evidence_refs=tuple(
                    item.ref for item, _ in evidence_scores if item.ref != strongest_item.ref
                ),
                observation=(
                    f"Ablated `{strongest_item.ref}` (baseline item score "
                    f"{_rounded(strongest_score):.4f}); aggregate score changed from "
                    f"{_rounded(baseline):.4f} to {_rounded(ablated):.4f}."
                ),
            )
        else:
            append_operation(
                kind=ResearchOperationKind.ABLATION,
                description=(
                    "Remove the single highest-overlap admitted evidence item and recompute "
                    "the same descriptive support metric."
                ),
                status=OperationStatus.INCONCLUSIVE,
                perturbed_score=baseline,
                evidence_refs=tuple(item.ref for item in report.evidence),
                observation="At least two admitted evidence items are required for a meaningful ablation.",
            )

        counterfactual = _counterfactual_subset(evidence_scores)
        if counterfactual is None:
            append_operation(
                kind=ResearchOperationKind.COUNTERFACTUAL,
                description=(
                    "Evaluate a bounded counterfactual evidence world in which the dominant "
                    "source/agent contribution is absent."
                ),
                status=OperationStatus.INCONCLUSIVE,
                perturbed_score=baseline,
                evidence_refs=tuple(item.ref for item in report.evidence),
                observation=(
                    "The evidence set had no removable source/agent partition that left a "
                    "non-empty counterfactual evidence world."
                ),
            )
        else:
            label, remaining_refs, counterfactual_score = counterfactual
            append_operation(
                kind=ResearchOperationKind.COUNTERFACTUAL,
                description=(
                    "Evaluate a bounded counterfactual evidence world in which the dominant "
                    "source/agent contribution is absent."
                ),
                status=OperationStatus.EXECUTED,
                perturbed_score=counterfactual_score,
                evidence_refs=remaining_refs,
                observation=(
                    f"Counterfactual removal of dominant partition `{label}` changed the "
                    f"aggregate score from {_rounded(baseline):.4f} to "
                    f"{_rounded(counterfactual_score):.4f}."
                ),
            )

        statistics = _statistics(
            report=report,
            evidence_scores=evidence_scores,
            operations=tuple(operations),
            replay_ok=replay_ok,
        )
        four_domain = _four_domain(
            report=report,
            statistics=statistics,
            operations=tuple(operations),
        )
        hypothesis = _working_hypothesis(report)
        competing = _competing_explanations(report)
        follow_up = _follow_up(report, statistics, tuple(operations))
        closure_hash = _closure_hash(
            question=report.question,
            source_dialogue_hash=report.final_chain_hash,
            working_hypothesis=hypothesis,
            competing_explanations=competing,
            operations=tuple(operations),
            statistics=statistics,
            four_domain=four_domain,
            follow_up_question=follow_up,
        )
        return ResearchClosureReport(
            question=report.question,
            source_dialogue_hash=report.final_chain_hash,
            working_hypothesis=hypothesis,
            competing_explanations=competing,
            operations=tuple(operations),
            statistics=statistics,
            four_domain=four_domain,
            follow_up_question=follow_up,
            closure_hash=closure_hash,
        )


def verify_research_closure(closure: ResearchClosureReport) -> bool:
    previous_hash = "GENESIS"
    for operation in closure.operations:
        if operation.previous_hash != previous_hash:
            return False
        payload = {
            "sequence": operation.sequence,
            "operation_id": operation.operation_id,
            "kind": operation.kind.value,
            "description": operation.description,
            "status": operation.status.value,
            "baseline_score": _rounded(operation.baseline_score),
            "perturbed_score": _rounded(operation.perturbed_score),
            "delta": _rounded(operation.delta),
            "evidence_refs": list(operation.evidence_refs),
            "observation": operation.observation,
        }
        expected = _hash_payload(previous_hash, payload)
        if expected != operation.operation_hash:
            return False
        previous_hash = expected
    expected_closure = _closure_hash(
        question=closure.question,
        source_dialogue_hash=closure.source_dialogue_hash,
        working_hypothesis=closure.working_hypothesis,
        competing_explanations=closure.competing_explanations,
        operations=closure.operations,
        statistics=closure.statistics,
        four_domain=closure.four_domain,
        follow_up_question=closure.follow_up_question,
    )
    return expected_closure == closure.closure_hash


def closure_to_dict(closure: ResearchClosureReport) -> dict[str, object]:
    return {
        "question": closure.question,
        "source_dialogue_hash": closure.source_dialogue_hash,
        "working_hypothesis": closure.working_hypothesis,
        "competing_explanations": list(closure.competing_explanations),
        "scientific_disposition": closure.scientific_disposition,
        "canonical_effect": closure.canonical_effect,
        "repository_mutation": closure.repository_mutation,
        "network_authority": closure.network_authority,
        "deployment": closure.deployment,
        "autonomous_merge": closure.autonomous_merge,
        "closure_hash": closure.closure_hash,
        "follow_up_question": closure.follow_up_question,
        "operations": [
            {
                "sequence": item.sequence,
                "operation_id": item.operation_id,
                "kind": item.kind.value,
                "description": item.description,
                "status": item.status.value,
                "baseline_score": item.baseline_score,
                "perturbed_score": item.perturbed_score,
                "delta": item.delta,
                "evidence_refs": list(item.evidence_refs),
                "observation": item.observation,
                "previous_hash": item.previous_hash,
                "operation_hash": item.operation_hash,
            }
            for item in closure.operations
        ],
        "statistics": {
            "evidence_count": closure.statistics.evidence_count,
            "unique_evidence_count": closure.statistics.unique_evidence_count,
            "source_class_count": closure.statistics.source_class_count,
            "retrieval_agent_count": closure.statistics.retrieval_agent_count,
            "mean_lexical_overlap": closure.statistics.mean_lexical_overlap,
            "min_lexical_overlap": closure.statistics.min_lexical_overlap,
            "max_lexical_overlap": closure.statistics.max_lexical_overlap,
            "dominant_source_share": closure.statistics.dominant_source_share,
            "retrieval_agent_balance": closure.statistics.retrieval_agent_balance,
            "max_abs_perturbation_delta": closure.statistics.max_abs_perturbation_delta,
            "transcript_replay_passed": closure.statistics.transcript_replay_passed,
        },
        "four_domain": {
            "observation": closure.four_domain.observation,
            "mechanism": closure.four_domain.mechanism,
            "interpretation": closure.four_domain.interpretation,
            "alternative_explanations": list(closure.four_domain.alternative_explanations),
            "unresolved_gaps": list(closure.four_domain.unresolved_gaps),
            "causal_intervention_refs": list(closure.four_domain.causal_intervention_refs),
            "ablation_refs": list(closure.four_domain.ablation_refs),
            "counterfactual_refs": list(closure.four_domain.counterfactual_refs),
            "robustness_refs": list(closure.four_domain.robustness_refs),
            "replication_refs": list(closure.four_domain.replication_refs),
        },
    }


def closure_to_markdown(closure: ResearchClosureReport) -> str:
    lines = [
        f"### Research closure — {closure.question}",
        "",
        f"- closure hash: `{closure.closure_hash}`",
        f"- scientific disposition: `{closure.scientific_disposition}`",
        f"- working hypothesis: {closure.working_hypothesis}",
        "",
        "Operations:",
    ]
    for operation in closure.operations:
        lines.append(
            f"- `{operation.kind.value}` / `{operation.status.value}`: "
            f"{operation.observation} (`{operation.operation_hash[:12]}…`)"
        )
    stats = closure.statistics
    lines.extend(
        [
            "",
            "Descriptive statistics:",
            f"- evidence count: `{stats.evidence_count}`",
            f"- mean lexical overlap: `{stats.mean_lexical_overlap:.4f}`",
            f"- dominant source share: `{stats.dominant_source_share:.4f}`",
            f"- retrieval-agent balance: `{stats.retrieval_agent_balance:.4f}`",
            f"- max perturbation delta: `{stats.max_abs_perturbation_delta:.4f}`",
            f"- transcript replay: `{'PASS' if stats.transcript_replay_passed else 'FAIL'}`",
            "",
            "Four-Domain interpretation:",
            f"- observation: {closure.four_domain.observation}",
            f"- mechanism: {closure.four_domain.mechanism}",
            f"- interpretation: {closure.four_domain.interpretation}",
            "- alternative explanations: "
            + "; ".join(closure.four_domain.alternative_explanations),
            "- unresolved gaps: "
            + ("; ".join(closure.four_domain.unresolved_gaps) or "none recorded"),
            "",
            f"Bounded follow-up: {closure.follow_up_question}",
            "",
            "`RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH`",
            "",
            "`ENGINEERING_INTERVENTION != REAL_WORLD_CAUSAL_IDENTIFICATION`",
            "",
            "`FULL_AUTOMATION != FULL_AUTHORITY`",
        ]
    )
    return "\n".join(lines)


def _matched_partition(
    evidence_scores: tuple[tuple[EvidenceItem, float], ...],
) -> tuple[str, float, tuple[str, ...], str, float, tuple[str, ...]] | None:
    agent_groups: dict[str, list[tuple[EvidenceItem, float]]] = {}
    for pair in evidence_scores:
        agent = pair[0].retrieval_agent.strip()
        if agent:
            agent_groups.setdefault(agent, []).append(pair)
    if len(agent_groups) >= 2:
        labels = sorted(agent_groups, key=lambda key: (-len(agent_groups[key]), key))[:2]
        first, second = labels
        a = agent_groups[first]
        b = agent_groups[second]
        return (
            f"retrieval_agent={first}",
            _mean(tuple(score for _, score in a)),
            tuple(item.ref for item, _ in a),
            f"retrieval_agent={second}",
            _mean(tuple(score for _, score in b)),
            tuple(item.ref for item, _ in b),
        )

    source_groups: dict[str, list[tuple[EvidenceItem, float]]] = {}
    for pair in evidence_scores:
        source_groups.setdefault(pair[0].source_class or "UNSPECIFIED", []).append(pair)
    if len(source_groups) < 2:
        return None
    labels = sorted(source_groups, key=lambda key: (-len(source_groups[key]), key))[:2]
    first, second = labels
    a = source_groups[first]
    b = source_groups[second]
    return (
        f"source_class={first}",
        _mean(tuple(score for _, score in a)),
        tuple(item.ref for item, _ in a),
        f"source_class={second}",
        _mean(tuple(score for _, score in b)),
        tuple(item.ref for item, _ in b),
    )


def _counterfactual_subset(
    evidence_scores: tuple[tuple[EvidenceItem, float], ...],
) -> tuple[str, tuple[str, ...], float] | None:
    if len(evidence_scores) < 2:
        return None

    groups: dict[str, list[tuple[EvidenceItem, float]]] = {}
    for pair in evidence_scores:
        item = pair[0]
        label = f"trust={item.trust}" if item.trust else f"source_class={item.source_class}"
        groups.setdefault(label, []).append(pair)
    if len(groups) < 2:
        groups = {}
        for pair in evidence_scores:
            item = pair[0]
            agent = item.retrieval_agent.strip()
            if agent:
                groups.setdefault(f"retrieval_agent={agent}", []).append(pair)
    if len(groups) < 2:
        groups = {}
        for pair in evidence_scores:
            item = pair[0]
            groups.setdefault(f"source_class={item.source_class or 'UNSPECIFIED'}", []).append(pair)
    if len(groups) < 2:
        return None

    dominant = sorted(groups, key=lambda key: (-len(groups[key]), key))[0]
    removed_refs = {item.ref for item, _ in groups[dominant]}
    remaining = tuple(
        (item, score) for item, score in evidence_scores if item.ref not in removed_refs
    )
    if not remaining:
        return None
    return (
        dominant,
        tuple(item.ref for item, _ in remaining),
        _mean(tuple(score for _, score in remaining)),
    )


def _statistics(
    *,
    report: InquiryReport,
    evidence_scores: tuple[tuple[EvidenceItem, float], ...],
    operations: tuple[ResearchOperationResult, ...],
    replay_ok: bool,
) -> DescriptiveStatistics:
    scores = tuple(score for _, score in evidence_scores)
    source_counts: dict[str, int] = {}
    agent_counts: dict[str, int] = {}
    for item, _ in evidence_scores:
        source_counts[item.source_class or "UNSPECIFIED"] = (
            source_counts.get(item.source_class or "UNSPECIFIED", 0) + 1
        )
        if item.retrieval_agent.strip():
            agent_counts[item.retrieval_agent] = agent_counts.get(item.retrieval_agent, 0) + 1
    evidence_count = len(evidence_scores)
    dominant_share = (
        max(source_counts.values()) / evidence_count if evidence_count and source_counts else 0.0
    )
    aion_count = agent_counts.get(AgentId.AION.value, 0)
    astra_count = agent_counts.get(AgentId.ASTRA.value, 0)
    if aion_count and astra_count:
        balance = min(aion_count, astra_count) / max(aion_count, astra_count)
    else:
        balance = 0.0
    deltas = tuple(
        abs(operation.delta)
        for operation in operations
        if operation.status is OperationStatus.EXECUTED
        and operation.kind is not ResearchOperationKind.REPLAY
    )
    return DescriptiveStatistics(
        evidence_count=evidence_count,
        unique_evidence_count=len({item.ref for item, _ in evidence_scores}),
        source_class_count=len(source_counts),
        retrieval_agent_count=len(agent_counts),
        mean_lexical_overlap=_rounded(_mean(scores)),
        min_lexical_overlap=_rounded(min(scores) if scores else 0.0),
        max_lexical_overlap=_rounded(max(scores) if scores else 0.0),
        dominant_source_share=_rounded(dominant_share),
        retrieval_agent_balance=_rounded(balance),
        max_abs_perturbation_delta=_rounded(max(deltas) if deltas else 0.0),
        transcript_replay_passed=replay_ok,
    )


def _four_domain(
    *,
    report: InquiryReport,
    statistics: DescriptiveStatistics,
    operations: tuple[ResearchOperationResult, ...],
) -> FourDomainInterpretation:
    intervention_refs = tuple(
        item.operation_id
        for item in operations
        if item.kind is ResearchOperationKind.INTERVENTION
        and item.status is OperationStatus.EXECUTED
    )
    ablation_refs = tuple(
        item.operation_id
        for item in operations
        if item.kind is ResearchOperationKind.ABLATION
        and item.status is OperationStatus.EXECUTED
    )
    counterfactual_refs = tuple(
        item.operation_id
        for item in operations
        if item.kind is ResearchOperationKind.COUNTERFACTUAL
        and item.status is OperationStatus.EXECUTED
    )
    replay_refs = tuple(
        item.operation_id
        for item in operations
        if item.kind is ResearchOperationKind.REPLAY
        and item.status is OperationStatus.EXECUTED
    )
    observation = (
        f"{statistics.evidence_count} admitted evidence items across "
        f"{statistics.source_class_count} source classes produced mean lexical overlap "
        f"{statistics.mean_lexical_overlap:.4f}; maximum bounded perturbation delta was "
        f"{statistics.max_abs_perturbation_delta:.4f}."
    )
    mechanism = (
        "The closure tests evidence dependence by holding a deterministic scoring rule "
        "fixed while replaying provenance and perturbing source/agent inclusion."
    )
    if not statistics.transcript_replay_passed:
        interpretation = (
            "Dialogue integrity failed replay; no downstream research interpretation is admissible."
        )
    elif statistics.evidence_count < 2:
        interpretation = (
            "The evidence plane is too sparse for stable perturbation analysis; retain HOLD."
        )
    elif statistics.max_abs_perturbation_delta > 0.15:
        interpretation = (
            "The provisional reading is materially sensitive to evidence selection under "
            "bounded perturbation; independent evidence is required before stronger claims."
        )
    else:
        interpretation = (
            "The provisional engineering reading was not highly sensitive to the executed "
            "evidence-plane perturbations, but this robustness check does not establish "
            "scientific truth or real-world causality."
        )
    alternatives = (
        "lexical-overlap scoring may not track semantic evidential strength",
        "retrieval ranking or source selection may dominate the observed stability",
        "duplicate or correlated sources may overstate apparent robustness",
        "the admitted evidence set may omit decisive counterevidence",
    )
    gaps: list[str] = []
    if statistics.evidence_count < 2:
        gaps.append("obtain at least two independent evidence items for perturbation analysis")
    if statistics.retrieval_agent_balance == 0.0:
        gaps.append("obtain independently attributable AION and Astra evidence for matched comparison")
    if statistics.source_class_count < 2:
        gaps.append("add a second source class to test source-class sensitivity")
    if statistics.max_abs_perturbation_delta > 0.15:
        gaps.append("seek independent evidence that resolves the observed perturbation sensitivity")
    if any(item.status is OperationStatus.INCONCLUSIVE for item in operations):
        gaps.append("satisfy the data preconditions for every inconclusive closure operation")
    return FourDomainInterpretation(
        observation=observation,
        mechanism=mechanism,
        interpretation=interpretation,
        alternative_explanations=alternatives,
        unresolved_gaps=tuple(dict.fromkeys(gaps)),
        causal_intervention_refs=intervention_refs,
        ablation_refs=ablation_refs,
        counterfactual_refs=counterfactual_refs,
        robustness_refs=replay_refs,
        replication_refs=replay_refs,
    )


def _working_hypothesis(report: InquiryReport) -> str:
    latest_aion = next(
        (
            event.claim
            for event in reversed(report.transcript)
            if event.speaker is AgentId.AION and event.claim.strip()
        ),
        "",
    )
    if latest_aion:
        return _clip(latest_aion, 420)
    if report.candidate_findings:
        return _clip(report.candidate_findings[0], 420)
    return _clip(
        "The admitted evidence supports a provisional, falsifiable engineering interpretation "
        f"of the question: {report.question}",
        420,
    )


def _competing_explanations(report: InquiryReport) -> tuple[str, ...]:
    candidates: list[str] = []
    for event in reversed(report.transcript):
        if event.speaker is AgentId.ASTRA:
            for value in (event.challenge, event.claim):
                clipped = _clip(value, 420)
                if clipped and clipped not in candidates:
                    candidates.append(clipped)
        if len(candidates) >= 3:
            break
    if not candidates:
        candidates.append(
            "The apparent pattern may be produced by retrieval, source selection, confounding, "
            "or insufficient evidence rather than the proposed mechanism."
        )
    return tuple(candidates)


def _follow_up(
    report: InquiryReport,
    statistics: DescriptiveStatistics,
    operations: tuple[ResearchOperationResult, ...],
) -> str:
    if not statistics.transcript_replay_passed:
        return "Which transcript mutation or serialization mismatch caused the dialogue replay failure?"
    if statistics.evidence_count < 2:
        return _clip(
            "Which independent evidence source can add a matched second observation for: "
            + report.question,
            360,
        )
    if any(item.status is OperationStatus.INCONCLUSIVE for item in operations):
        return _clip(
            "Which bounded evidence acquisition would satisfy the missing partition or sample "
            "precondition and directly challenge the current interpretation of: "
            + report.question,
            360,
        )
    if statistics.max_abs_perturbation_delta > 0.15:
        return _clip(
            "Which independent source or matched control explains why the current conclusion "
            "changes materially under evidence ablation or counterfactual removal: "
            + report.question,
            360,
        )
    latest_challenge = next(
        (event.challenge for event in reversed(report.transcript) if event.challenge.strip()),
        "",
    )
    if latest_challenge:
        return _clip(
            "What new evidence would most directly falsify or resolve this remaining peer challenge: "
            + latest_challenge,
            360,
        )
    return _clip(
        "What new independent evidence would falsify the current bounded interpretation of: "
        + report.question,
        360,
    )


def _tokens(text: str) -> tuple[str, ...]:
    raw = re.findall(r"[A-Za-z0-9_./:-]{3,}|[\u4e00-\u9fff]{2,}", text.lower())
    stop = {
        "about",
        "after",
        "and",
        "bounded",
        "does",
        "evidence",
        "from",
        "into",
        "that",
        "the",
        "this",
        "what",
        "which",
        "with",
        "研究",
        "證據",
        "是否",
        "什麼",
        "如何",
    }
    return tuple(dict.fromkeys(token for token in raw if token not in stop))


def _evidence_score(question_tokens: tuple[str, ...], item: EvidenceItem) -> float:
    if not question_tokens:
        return 0.0
    evidence_tokens = set(_tokens(f"{item.ref} {item.excerpt}"))
    matched = sum(1 for token in question_tokens if token in evidence_tokens)
    return matched / len(question_tokens)


def _mean(values: tuple[float, ...]) -> float:
    return sum(values) / len(values) if values else 0.0


def _rounded(value: float) -> float:
    return round(float(value), 8)


def _hash_payload(previous_hash: str, payload: dict[str, object]) -> str:
    encoded = json.dumps(
        {"previous_hash": previous_hash, "payload": payload},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _closure_hash(
    *,
    question: str,
    source_dialogue_hash: str,
    working_hypothesis: str,
    competing_explanations: tuple[str, ...],
    operations: tuple[ResearchOperationResult, ...],
    statistics: DescriptiveStatistics,
    four_domain: FourDomainInterpretation,
    follow_up_question: str,
) -> str:
    payload = {
        "question": question,
        "source_dialogue_hash": source_dialogue_hash,
        "working_hypothesis": working_hypothesis,
        "competing_explanations": list(competing_explanations),
        "operation_hashes": [item.operation_hash for item in operations],
        "statistics": {
            "evidence_count": statistics.evidence_count,
            "unique_evidence_count": statistics.unique_evidence_count,
            "source_class_count": statistics.source_class_count,
            "retrieval_agent_count": statistics.retrieval_agent_count,
            "mean_lexical_overlap": statistics.mean_lexical_overlap,
            "min_lexical_overlap": statistics.min_lexical_overlap,
            "max_lexical_overlap": statistics.max_lexical_overlap,
            "dominant_source_share": statistics.dominant_source_share,
            "retrieval_agent_balance": statistics.retrieval_agent_balance,
            "max_abs_perturbation_delta": statistics.max_abs_perturbation_delta,
            "transcript_replay_passed": statistics.transcript_replay_passed,
        },
        "four_domain": {
            "observation": four_domain.observation,
            "mechanism": four_domain.mechanism,
            "interpretation": four_domain.interpretation,
            "alternative_explanations": list(four_domain.alternative_explanations),
            "unresolved_gaps": list(four_domain.unresolved_gaps),
            "causal_intervention_refs": list(four_domain.causal_intervention_refs),
            "ablation_refs": list(four_domain.ablation_refs),
            "counterfactual_refs": list(four_domain.counterfactual_refs),
            "robustness_refs": list(four_domain.robustness_refs),
            "replication_refs": list(four_domain.replication_refs),
        },
        "follow_up_question": follow_up_question,
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _clip(text: str, limit: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"
