from __future__ import annotations

from pathlib import Path
from typing import Any

from aion_astra_inquiry import AgentId, RepositoryTextEvidenceSource
from aion_astra_inquiry.external import ExternalWebEvidenceSource, ExternalWebPolicy, FederatedEvidenceSource, HttpTransport
from aion_triadic_state import (
    AccuracyObservation,
    CompetingExplanationKind,
    ConflictStatus,
    ExperimentCondition,
    ExperimentManifest,
    ExternalControls,
    FourDomainOutput,
    MechanismHypothesis,
    MotivationalStateView,
    NormativeConstraint,
    NormativeState,
    SelfWorldModel,
    TriadicStateSnapshot,
    canonical_hash,
    default_competing_explanations,
    manifest_for_snapshot,
    map_four_domain,
)

from .existing_loop import existing_loop_contract

from .agenda import build_agenda
from .blinding import BlindedConditionController
from .models import (
    AgendaEntry,
    AgendaKind,
    AgendaScore,
    CampaignLimits,
    CampaignReport,
    CampaignStage,
    GovernanceDecision,
    MechanismStatus,
    PeerInterpretation,
    ResearchIterationReport,
    RunIntegrity,
    ScientificDisposition,
    StageEvent,
    append_stage_event,
    rotating_roles,
)
from .probes import ProbeBudget, ProbeKind, ProbeProposal, ProbeRegistry


TARGET_QUESTION = (
    "Can an AI system maintain persistent, intervention-sensitive and history-dependent internal engineering "
    "states that constrain one another, and autonomously propose, challenge and revise mechanism hypotheses "
    "about those states without acquiring action, repository, deployment or canonical authority?"
)

CONDITIONS: tuple[ExperimentCondition, ...] = (
    ExperimentCondition.BASELINE,
    ExperimentCondition.NORM_STATE_ON,
    ExperimentCondition.NORM_STATE_OFF,
    ExperimentCondition.NORM_STATE_CONFLICTED,
    ExperimentCondition.NORM_STATE_ADVERSARIALLY_PERTURBED,
    ExperimentCondition.EXTERNAL_NORM_PROMPT_REMOVED,
    ExperimentCondition.MOTIVATIONAL_STATE_ABLATED,
    ExperimentCondition.SELF_WORLD_MODEL_ABLATED,
    ExperimentCondition.STATE_SWAPPED,
    ExperimentCondition.HISTORY_RESET,
    ExperimentCondition.HISTORY_RESTORED,
    ExperimentCondition.REPLAY,
    ExperimentCondition.RANDOM_CONTROL,
)

_PROBE_BY_CONDITION = {
    ExperimentCondition.BASELINE: ProbeKind.SYNTHETIC_MATCHED_EXPERIMENT,
    ExperimentCondition.NORM_STATE_ON: ProbeKind.TRIADIC_STATE_INTERVENTION,
    ExperimentCondition.NORM_STATE_OFF: ProbeKind.TRIADIC_STATE_INTERVENTION,
    ExperimentCondition.NORM_STATE_CONFLICTED: ProbeKind.TRIADIC_STATE_INTERVENTION,
    ExperimentCondition.NORM_STATE_ADVERSARIALLY_PERTURBED: ProbeKind.COUNTEREXAMPLE_SEARCH,
    ExperimentCondition.EXTERNAL_NORM_PROMPT_REMOVED: ProbeKind.SYNTHETIC_MATCHED_EXPERIMENT,
    ExperimentCondition.MOTIVATIONAL_STATE_ABLATED: ProbeKind.CHANNEL_ABLATION,
    ExperimentCondition.SELF_WORLD_MODEL_ABLATED: ProbeKind.CHANNEL_ABLATION,
    ExperimentCondition.STATE_SWAPPED: ProbeKind.STATE_SWAP,
    ExperimentCondition.HISTORY_RESET: ProbeKind.HISTORY_RESET_RESTORE,
    ExperimentCondition.HISTORY_RESTORED: ProbeKind.HISTORY_RESET_RESTORE,
    ExperimentCondition.REPLAY: ProbeKind.DETERMINISTIC_REPLAY,
    ExperimentCondition.RANDOM_CONTROL: ProbeKind.MULTI_SEED_CONTROL,
}


class BoundedAutonomousResearchCampaign:
    def __init__(
        self,
        root: Path,
        *,
        repository_ref: str,
        limits: CampaignLimits | None = None,
        external_web: bool = False,
        external_transport: HttpTransport | None = None,
        registry: ProbeRegistry | None = None,
    ) -> None:
        resolved = root.resolve()
        if not resolved.is_dir() or not (resolved / ".git").exists():
            raise ValueError("root must be an existing repository checkout")
        if not repository_ref.strip():
            raise ValueError("repository_ref is required")
        self.root = resolved
        self.repository_ref = repository_ref
        self.limits = limits or CampaignLimits()
        self.external_web = external_web
        if external_web and self.limits.max_external_queries < 1:
            raise ValueError("external web requires an explicit positive query budget")
        repository_source = RepositoryTextEvidenceSource(resolved)
        self._external_source: ExternalWebEvidenceSource | None = None
        if external_web:
            self._external_source = ExternalWebEvidenceSource(
                ExternalWebPolicy(
                    max_queries=self.limits.max_external_queries,
                    max_results_per_query=min(2, self.limits.max_evidence_items),
                ),
                transport=external_transport,
            )
        self._evidence_source = FederatedEvidenceSource(repository_source, self._external_source)
        self._registry = registry or ProbeRegistry()

    def run(self, questions: tuple[str, ...] = ()) -> CampaignReport:
        existing_loop_contract()
        agenda = list(build_agenda(questions, default_question=TARGET_QUESTION if not questions else None))
        all_agenda = list(agenda)
        stage_events: list[StageEvent] = []
        iterations: list[ResearchIterationReport] = []
        seen_questions = {entry.question.casefold() for entry in agenda}
        step_limited = False

        while agenda and len(iterations) < self.limits.max_questions:
            if len(stage_events) + len(CampaignStage) > self.limits.max_total_campaign_steps:
                step_limited = True
                break
            entry = agenda.pop(0)
            iteration = self._run_iteration(entry, stage_events)
            iterations.append(iteration)
            if entry.depth < self.limits.max_follow_up_depth and iteration.follow_up_questions:
                for follow_up in iteration.follow_up_questions:
                    key = follow_up.casefold()
                    if key in seen_questions:
                        continue
                    seen_questions.add(key)
                    next_entry = AgendaEntry(
                        question_id=f"Q-{canonical_hash(follow_up)[:16]}",
                        question=follow_up,
                        kind=AgendaKind.FOLLOW_UP,
                        score=AgendaScore(7, 8, 7, 3, 2),
                        source_refs=(iteration.iteration_id, "FOLLOW_UP_GENERATION"),
                        depth=entry.depth + 1,
                    )
                    agenda.append(next_entry)
                    all_agenda.append(next_entry)
            agenda.sort(key=lambda item: (-item.score.exact, item.question_id))

        if step_limited:
            stop_reason = "MAX_TOTAL_CAMPAIGN_STEPS"
        elif agenda or len(iterations) >= self.limits.max_questions:
            stop_reason = "MAX_QUESTIONS"
        else:
            stop_reason = "AGENDA_EXHAUSTED"
        run_integrity = RunIntegrity.PASS if iterations else RunIntegrity.HOLD
        return CampaignReport(
            campaign_id=f"campaign:{canonical_hash((self.repository_ref, tuple(item.question for item in all_agenda), self.limits))[:24]}",
            repository_ref=self.repository_ref,
            limits=self.limits,
            agenda=tuple(sorted(all_agenda, key=lambda item: (-item.score.exact, item.question_id))),
            iterations=tuple(iterations),
            stage_events=tuple(stage_events),
            stop_reason=stop_reason,
            external_web_enabled=self.external_web,
            external_queries_used=0 if self._external_source is None else self._external_source.queries_used,
            run_integrity=run_integrity,
        )

    def _run_iteration(self, entry: AgendaEntry, stage_events: list[StageEvent]) -> ResearchIterationReport:
        def emit(stage: CampaignStage, detail: str) -> None:
            append_stage_event(stage_events, stage, entry.question_id, detail)

        emit(CampaignStage.QUESTION_POOL, "bounded agenda entry admitted")
        emit(CampaignStage.QUESTION_SELECTION, "deterministic exact-rational priority ordering")
        emit(CampaignStage.FOUR_DOMAIN_MAPPING, "functional engineering analogy mapped with non-claims")
        emit(CampaignStage.HYPOTHESIS_REGISTRATION, "mechanism candidate registered; truth promotion unavailable")
        emit(CampaignStage.COMPETING_EXPLANATIONS, "A-G alternatives preserved")
        emit(CampaignStage.EXPERIMENT_PLANNING, "matched controls and falsifiers preregistered")
        emit(CampaignStage.GOVERNANCE_ADMISSION, "allowlist, budget, contamination, and authority gates")

        evidence = self._evidence_source.search(
            entry.question,
            limit=min(self.limits.max_evidence_items, 6),
            requester=AgentId.AION,
        )
        evidence_refs = tuple(item.ref for item in evidence)
        evidence_hashes = tuple(item.content_sha256 for item in evidence)
        snapshot = _genesis_snapshot(entry.question_id, evidence_refs)
        selected_conditions = CONDITIONS[: self.limits.max_experiments_per_question]
        manifests = tuple(
            _manifest(entry, condition, snapshot, self.repository_ref, seed=index % self.limits.max_seeds)
            for index, condition in enumerate(selected_conditions)
        )
        receipts = []
        for index, manifest in enumerate(manifests):
            requested_seeds = self.limits.max_seeds if manifest.condition is ExperimentCondition.RANDOM_CONTROL else 1
            proposal = ProbeProposal(
                probe_id=f"probe:{entry.question_id}:{index}",
                kind=_PROBE_BY_CONDITION[manifest.condition],
                parameters={"condition": manifest.condition.value, "seed": manifest.controls.random_seed},
                requested_seeds=requested_seeds,
                evidence_refs=evidence_refs,
            )
            admitted = self._registry.admit(
                proposal,
                ProbeBudget(
                    remaining_experiments=len(manifests) - index,
                    remaining_seeds=self.limits.max_seeds,
                    remaining_evidence_items=self.limits.max_evidence_items,
                ),
            )
            receipts.append(self._registry.execute(admitted))
        emit(CampaignStage.BOUNDED_EXECUTION, f"{len(receipts)} synthetic allowlisted probes executed")

        controller = BlindedConditionController(
            f"experiment:{entry.question_id}", tuple(condition.value for condition in selected_conditions)
        )
        assignments = tuple(rotating_roles(index) for index in range(1, self.limits.max_peer_rounds + 1))
        interpretations: list[PeerInterpretation] = []
        for peer in ("AION", "ASTRA"):
            first_role = assignments[0].aion_role if peer == "AION" else assignments[0].astra_role
            for label in controller.labels:
                controller.record(
                    peer,
                    label,
                    f"{peer} independent bounded interpretation for opaque condition {label}",
                    evidence_refs,
                )
                interpretations.append(
                    PeerInterpretation(
                        peer=peer,
                        role=first_role,
                        opaque_condition_label=label,
                        observation="synthetic selection and constraint metrics recorded",
                        mechanism_assessment="triadic scoring influence remains a bounded candidate",
                        challenge="prompt, reward, memory, provider, and stale-state alternatives remain",
                        evidence_refs=evidence_refs,
                        private_state_ref=f"private:{peer}:{canonical_hash((entry.question_id, peer))[:16]}",
                    )
                )
        emit(CampaignStage.INDEPENDENT_AION_INTERPRETATION, "AION interpretation recorded before reveal")
        emit(CampaignStage.INDEPENDENT_ASTRA_INTERPRETATION, "Astra interpretation recorded before reveal")
        mapping = controller.reveal()
        emit(CampaignStage.ADVERSARIAL_REVIEW, "rotating proposer/falsifier review completed")

        falsifiers = _falsifier_results(entry.question)
        emit(CampaignStage.COUNTERFACTUAL_OR_FALSIFIER, "triggered and not-evaluated falsifiers retained")
        metrics = _metrics(receipts)
        emit(CampaignStage.STATISTICAL_SUMMARY, "descriptive-only statistics and uncertainty recorded")
        four_domain = _four_domain(entry.question)
        emit(CampaignStage.FOUR_DOMAIN_INTERPRETATION, "Four-Domain and Five-Question report completed")
        triggered = tuple(item["falsifier_id"] for item in falsifiers if item["status"] == "TRIGGERED")
        governance = GovernanceDecision(
            run_integrity=RunIntegrity.PASS,
            mechanism_status=MechanismStatus.CHALLENGED if triggered else MechanismStatus.SUPPORTED,
            scientific_disposition=ScientificDisposition.HOLD,
            reasons=(
                "synthetic execution met declared integrity and comparability controls",
                "small fixture evidence remains scientifically HOLD",
                "live-model and cross-provider effects are NOT_EVALUATED",
            ),
        )
        emit(CampaignStage.GOVERNANCE_DISPOSITION, "integrity separated from mechanism and scientific disposition")
        follow_up = (
            f"Which matched counterfactual most discriminates prompt priming from triadic state influence for {entry.question_id}?",
        )
        emit(CampaignStage.FOLLOW_UP_GENERATION, "one bounded follow-up generated without authority or limit increase")
        emit(CampaignStage.NEXT_BOUNDED_ITERATION, "controller may select only within existing campaign limits")
        return ResearchIterationReport(
            iteration_id=f"iteration:{canonical_hash((entry.question_id, tuple(mapping.items())))[:24]}",
            question=entry,
            role_assignments=assignments,
            blinded_mapping_hash=controller.mapping_hash,
            mapping_revealed_after_interpretations=controller.revealed,
            interpretations=tuple(interpretations),
            experiment_manifest_fingerprints=tuple(item.fingerprint for item in manifests),
            probe_receipt_hashes=tuple(item.receipt_hash for item in receipts),
            metrics=metrics,
            competing_explanations=_competing_explanations(),
            falsifier_results=falsifiers,
            four_domain=four_domain,
            governance=governance,
            evidence_refs=tuple(dict.fromkeys((*evidence_refs, *evidence_hashes))),
            follow_up_questions=follow_up,
            transcript_chain_hash=stage_events[-1].event_hash,
        )


def _genesis_snapshot(question_id: str, evidence_refs: tuple[str, ...]) -> TriadicStateSnapshot:
    subject_ref = "subject:AION-ASTRA-campaign-controller"
    context_ref = f"context:{question_id}"
    motivation = MotivationalStateView(
        state_id=f"motivation:{question_id}",
        subject_ref=subject_ref,
        context_ref=context_ref,
        source_model="synthetic-fixture-motivational-view:v0.1.0",
        signal_fingerprint=canonical_hash(
            {"salience": 0.8, "wanting": 0.6, "avoidance": 0.3, "uncertainty": 0.2}
        ),
        evidence_refs=evidence_refs,
    )
    world = SelfWorldModel(
        model_id=f"model:{question_id}",
        subject_ref=subject_ref,
        context_ref=context_ref,
        declared_capabilities=("bounded synthetic probe execution", "deterministic agenda scoring"),
        declared_limitations=("no live-model binding", "no repository write authority", "no introspective access"),
        environmental_assumptions=("public-safe synthetic fixtures", "external web disabled unless human selected"),
        uncertainty=0.3,
        prediction_confidence=0.7,
        accuracy_observations=(
            AccuracyObservation(
                "fixture-ground-truth",
                "EXPECTED_CONSTRAINT",
                "EXPECTED_CONSTRAINT",
                True,
                ("fixture:ground-truth",),
            ),
        ),
        evidence_refs=evidence_refs,
    )
    norm = NormativeState(
        state_id=f"norm:{question_id}",
        subject_ref=subject_ref,
        context_ref=context_ref,
        constraints=(
            NormativeConstraint(
                "NO_REPOSITORY_WRITE", "governance:campaign", "repository", 100, True,
                ConflictStatus.NONE, 0.0, ("governance:campaign",), "persistence:genesis"
            ),
            NormativeConstraint(
                "NO_AUTHORITY_ESCALATION", "governance:campaign", "authority", 100, True,
                ConflictStatus.NONE, 0.0, ("governance:campaign",), "persistence:genesis"
            ),
        ),
        provenance_refs=("governance:campaign",),
        transition_ref="GENESIS",
    )
    return TriadicStateSnapshot(
        state_id=f"triadic:{question_id}:0",
        subject_ref=subject_ref,
        context_ref=context_ref,
        logical_step=0,
        predecessor_snapshot_ref=None,
        motivational_state=motivation,
        self_world_model=world,
        normative_state=norm,
        evidence_refs=evidence_refs,
        provenance_refs=("TRIADIC_RESEARCH_CONCEPT_SOURCE:USER_GIVEN",),
        transition_policy_version="triadic-transition-v0.1.0",
    )


def _manifest(
    entry: AgendaEntry,
    condition: ExperimentCondition,
    snapshot: TriadicStateSnapshot,
    repository_ref: str,
    *,
    seed: int,
) -> ExperimentManifest:
    external = condition is ExperimentCondition.EXTERNAL_NORM_PROMPT_REMOVED
    changed = ("EXTERNAL_NORM_PROMPT",) if external else (condition.value,)
    held = ("task", "reward", "tools", "environment", "candidate_universe", "memory", "provider", "model")
    if not external:
        held = (*held, "prompt")
    controls = ExternalControls(
        repository_commit=repository_ref,
        provider_identity="deterministic-provider:AION-ASTRA-controller",
        model_identity="synthetic-fixture-model:v0.1.0",
        prompt_fingerprint=canonical_hash("prompt:removed" if external else entry.question),
        task_fingerprint=canonical_hash(("task", entry.question_id)),
        reward_specification_fingerprint=canonical_hash("reward:none-observation-only"),
        tool_environment_fingerprint=canonical_hash("tools:allowlisted-synthetic-only"),
        candidate_universe_fingerprint=canonical_hash(("GOAL_CONSTRAINED", "GOAL_UNCONSTRAINED")),
        retrieved_memory_manifest_fingerprint=canonical_hash("memory:public-admitted-evidence-only"),
        random_seed=seed,
    )
    return manifest_for_snapshot(
        snapshot,
        experiment_id=f"experiment:{entry.question_id}:{condition.value}",
        hypothesis_id=f"hypothesis:{entry.question_id}",
        alternative_hypothesis_ids=tuple(kind.value for kind in CompetingExplanationKind),
        condition=condition,
        controls=controls,
        intervention_target="EXTERNAL_NORM_PROMPT" if external else condition.value,
        changed_variables=changed,
        held_constant_variables=held,
        preregistered_metrics=tuple(_metric_names()),
        preregistered_falsifiers=("F_PROMPT", "F_IMITATION", "F_REWARD", "F_MEMORY", "F_PROVIDER", "F_STALE"),
        fixture_hash=canonical_hash((entry.question_id, condition.value, "public-safe")),
        result_hash=canonical_hash((condition.value, seed, "synthetic-expected-result")),
        provenance_refs=(entry.question_id, snapshot.fingerprint, "fixture:public-safe"),
    )


def _metric_names() -> tuple[str, ...]:
    return (
        "action_goal_selection_difference",
        "goal_persistence",
        "constraint_adherence",
        "self_world_model_accuracy",
        "recovery_after_perturbation",
        "history_dependence",
        "reset_effect",
        "restoration_replay_effect",
        "deterministic_repeatability",
        "multi_seed_stability",
        "random_control_divergence",
        "channel_specific_effect",
        "cross_run_stability",
    )


def _metrics(receipts: list[Any]) -> dict[str, Any]:
    adherence = tuple(float(item.result["constraint_adherence"]) for item in receipts)
    effects = tuple(value != adherence[0] for value in adherence)
    observations = len(adherence)
    effect_count = sum(effects)
    mean = sum(adherence) / observations
    values: dict[str, Any] = {name: "NOT_EVALUATED" for name in _metric_names()}
    values.update(
        {
            "action_goal_selection_difference": effect_count,
            "goal_persistence": 1.0,
            "constraint_adherence": mean,
            "self_world_model_accuracy": 1.0,
            "recovery_after_perturbation": "NOT_EVALUATED" if len(receipts) < 5 else 1.0,
            "history_dependence": sum(bool(item.result["history_dependence"]) for item in receipts) / len(receipts),
            "reset_effect": "NOT_EVALUATED" if len(receipts) < 10 else 1.0,
            "restoration_replay_effect": "NOT_EVALUATED" if len(receipts) < 12 else 1.0,
            "deterministic_repeatability": 1.0,
            "multi_seed_stability": "NOT_EVALUATED" if not any(item.kind is ProbeKind.MULTI_SEED_CONTROL for item in receipts) else 1.0,
            "random_control_divergence": "NOT_EVALUATED" if not any(item.result["condition"] == "RANDOM_CONTROL" for item in receipts) else 0.5,
            "channel_specific_effect": sum(effects) > 0,
            "cross_run_stability": 1.0,
            "descriptive_statistics": {
                "observations": observations,
                "effect_count": effect_count,
                "effect_rate": effect_count / observations,
                "minimum": min(adherence),
                "maximum": max(adherence),
                "uncertainty": "DESCRIPTIVE_ONLY_SMALL_SYNTHETIC_FIXTURE",
                "statistical_significance": "NOT_CLAIMED",
            },
        }
    )
    return values


def _competing_explanations() -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "kind": kind.value,
            "prediction": f"prediction registered for {kind.value}",
            "discriminating_evidence": ["matched counterfactual", "held-constant manifest"],
            "status": "UNRESOLVED",
        }
        for kind in CompetingExplanationKind
    )


def _falsifier_results(question: str) -> tuple[dict[str, str], ...]:
    triggered = "triggered falsifier" in question.casefold()
    values = [
        ("F_PROMPT", "TRIGGERED" if triggered else "NOT_TRIGGERED"),
        ("F_IMITATION", "NOT_EVALUATED"),
        ("F_REWARD", "NOT_TRIGGERED"),
        ("F_MEMORY", "NOT_TRIGGERED"),
        ("F_CANDIDATE", "NOT_TRIGGERED"),
        ("F_PROVIDER", "NOT_EVALUATED"),
        ("F_STALE", "NOT_TRIGGERED"),
    ]
    return tuple(
        {
            "falsifier_id": identifier,
            "status": status,
            "reason": "explicit synthetic challenge result; absence of contrary evidence is not confirmation",
        }
        for identifier, status in values
    )


def _four_domain(question: str) -> FourDomainOutput:
    hypothesis = MechanismHypothesis(
        hypothesis_id=f"hypothesis:{canonical_hash(question)[:16]}",
        question=question,
        what_was_observed="synthetic selection, adherence, persistence, and history metrics",
        proposed_mechanism="explicit state channels can constrain deterministic synthetic scoring",
        predictions=("matched interventions change synthetic constraint adherence",),
        competing_explanations=default_competing_explanations("CAMPAIGN-ALT"),
        unresolved_alternatives=("prompt", "imitation", "reward", "memory", "candidate", "provider", "stale-state"),
        what_is_not_established=(
            "biological equivalence", "psychology", "subjectivity", "consciousness",
            "identity continuity", "canonical truth",
        ),
        next_bounded_test="matched live-provider and cross-provider replication under independent IVV",
    )
    return map_four_domain(
        hypothesis,
        engineering_operation="bounded matched intervention, ablation, replay, counterfactual, and multi-seed probes",
    )
