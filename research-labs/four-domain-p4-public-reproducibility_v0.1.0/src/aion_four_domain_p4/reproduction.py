from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .manifest import ContaminationClass, ExperimentManifest, ExperimentResult


class ReproductionDecision(str, Enum):
    EXACT = "EXACT"
    REPRODUCED_WITH_ENVIRONMENT_VARIATION = "REPRODUCED_WITH_ENVIRONMENT_VARIATION"
    DIVERGED = "DIVERGED"
    NOT_COMPARABLE = "NOT_COMPARABLE"
    CONTAMINATED = "CONTAMINATED"


@dataclass(frozen=True, slots=True)
class ReproductionReport:
    decision: ReproductionDecision
    comparable_fields: tuple[str, ...]
    differing_fields: tuple[str, ...]
    output_hash_equal: bool
    contamination_classes: tuple[ContaminationClass, ContaminationClass]
    note: str = ""


class ReproductionValidator:
    CORE_FIELDS = (
        "protocol_version",
        "branch_name",
        "baseline_commit",
        "module_refs",
        "fixture_refs",
        "input_hash",
        "seed",
        "benchmark_refs",
        "benchmark_access_policy",
    )

    def compare(self, left_manifest: ExperimentManifest, left_result: ExperimentResult,
                right_manifest: ExperimentManifest, right_result: ExperimentResult) -> ReproductionReport:
        self._bind(left_manifest, left_result)
        self._bind(right_manifest, right_result)
        left_contam = left_result.contamination_class
        right_contam = right_result.contamination_class
        differences = tuple(field for field in self.CORE_FIELDS
                            if getattr(left_manifest, field) != getattr(right_manifest, field))
        if left_contam is not ContaminationClass.NONE or right_contam is not ContaminationClass.NONE:
            decision = ReproductionDecision.CONTAMINATED
            note = "At least one run contains benchmark search-time contamination evidence."
        elif differences:
            decision = ReproductionDecision.NOT_COMPARABLE
            note = "Core experimental conditions differ."
        elif left_result.output_hash != right_result.output_hash:
            decision = ReproductionDecision.DIVERGED
            note = "Core conditions match but output hashes differ."
        elif left_manifest.environment_fingerprint == right_manifest.environment_fingerprint:
            decision = ReproductionDecision.EXACT
            note = "Core conditions, environment fingerprint and output hash match."
        else:
            decision = ReproductionDecision.REPRODUCED_WITH_ENVIRONMENT_VARIATION
            note = "Core conditions and output hash match across different environment fingerprints."
        return ReproductionReport(decision, self.CORE_FIELDS, differences,
                                  left_result.output_hash == right_result.output_hash,
                                  (left_contam, right_contam), note)

    @staticmethod
    def _bind(manifest: ExperimentManifest, result: ExperimentResult) -> None:
        if manifest.experiment_id != result.experiment_id:
            raise ValueError("experiment_id mismatch")
        if manifest.fingerprint() != result.manifest_fingerprint:
            raise ValueError("result is not bound to supplied manifest")


@dataclass(frozen=True, slots=True)
class CrossAgentComparison:
    run_count: int
    runner_count: int
    exact_output_agreement: float
    contaminated_run_count: int
    status_counts: tuple[tuple[str, int], ...]


class CrossAgentComparator:
    def compare(self, runs: tuple[tuple[ExperimentManifest, ExperimentResult], ...]) -> CrossAgentComparison:
        if not runs:
            raise ValueError("runs must be non-empty")
        for manifest, result in runs:
            ReproductionValidator._bind(manifest, result)
        signatures = {(
            m.protocol_version, m.branch_name, m.baseline_commit, m.module_refs,
            m.fixture_refs, m.input_hash, m.seed, m.benchmark_refs,
            m.benchmark_access_policy,
        ) for m, _ in runs}
        if len(signatures) != 1:
            raise ValueError("cross-agent comparison requires the same core experiment")
        hashes = [result.output_hash for _, result in runs]
        majority = max(set(hashes), key=hashes.count)
        statuses: dict[str, int] = {}
        for _, result in runs:
            statuses[result.status.value] = statuses.get(result.status.value, 0) + 1
        return CrossAgentComparison(
            run_count=len(runs),
            runner_count=len({m.runner_id for m, _ in runs}),
            exact_output_agreement=hashes.count(majority) / len(hashes),
            contaminated_run_count=sum(r.contamination_class is not ContaminationClass.NONE for _, r in runs),
            status_counts=tuple(sorted(statuses.items())),
        )


@dataclass(frozen=True, slots=True)
class ResearchBundle:
    schema: str
    manifest_fingerprint: str
    experiment_id: str
    runner_id: str
    actor_kind: str
    baseline_commit: str
    module_refs: tuple[str, ...]
    fixture_refs: tuple[str, ...]
    network_mode: str
    benchmark_access_policy: str
    output_hash: str
    result_status: str
    contamination_class: str
    evidence_refs: tuple[str, ...]


class ResearchBundleExporter:
    def export(self, manifest: ExperimentManifest, result: ExperimentResult) -> ResearchBundle:
        ReproductionValidator._bind(manifest, result)
        return ResearchBundle(
            schema="AION-RESEARCH-BUNDLE-0.1",
            manifest_fingerprint=manifest.fingerprint(),
            experiment_id=manifest.experiment_id,
            runner_id=manifest.runner_id,
            actor_kind=manifest.actor_kind.value,
            baseline_commit=manifest.baseline_commit,
            module_refs=manifest.module_refs,
            fixture_refs=manifest.fixture_refs,
            network_mode=manifest.network_mode.value,
            benchmark_access_policy=manifest.benchmark_access_policy.value,
            output_hash=result.output_hash,
            result_status=result.status.value,
            contamination_class=result.contamination_class.value,
            evidence_refs=result.evidence_refs,
        )
