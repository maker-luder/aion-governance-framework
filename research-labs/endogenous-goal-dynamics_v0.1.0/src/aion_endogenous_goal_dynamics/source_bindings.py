from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ResearchSourceBinding:
    role: str
    source_ref: str
    artifact_path: str
    artifact_sha1: str
    disposition: str


FROZEN_RESEARCH_HEAD = "1892f1341059f313087a94aef74f22c086000f2a"
FOUR_DOMAIN_PINNED_HEAD = "f654b5032ebc45058a64e81d409149ee7ea4bfbe"

PINNED_RESEARCH_SOURCES: tuple[ResearchSourceBinding, ...] = (
    ResearchSourceBinding(
        role="FOUR_DOMAIN_METHOD",
        source_ref=FOUR_DOMAIN_PINNED_HEAD,
        artifact_path="research-workbench/four-domain-materialization/2026-08-09/FOUR_DOMAIN_REPOSITORY_CROSSWALK.md",
        artifact_sha1="7e55741b85b27d383b4b721b834b1744c6c03fb9",
        disposition="REFERENCE_ONLY",
    ),
    ResearchSourceBinding(
        role="CAUSAL_INTERVENTION_METHOD",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/causal-internal-state_v0.1.0/README.md",
        artifact_sha1="0b29604dc75098ac4a38f8c400737ea12edc7808",
        disposition="METHOD_REUSE_WITHOUT_BRANCH_MERGE",
    ),
    ResearchSourceBinding(
        role="AFFECT_MOTIVATION_CHANNEL",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/affective-cognitive-motivation_v0.1.0/README.md",
        artifact_sha1="576ece0bb4281b3559e4b623cdc53279aa2e1719",
        disposition="CONCEPTUAL_ADAPTER",
    ),
    ResearchSourceBinding(
        role="SELECTIVE_MEMORY_CONFOUND_CONTROL",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/selective-memory-control_v0.1.0/README.md",
        artifact_sha1="561c53bc2f2692b0e8fa06b702eaffa319018569",
        disposition="CONTROL_BOUNDARY",
    ),
    ResearchSourceBinding(
        role="SELF_MODEL_CHANNEL",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/self-model-functional-ablation_v0.1.0/README.md",
        artifact_sha1="8907f338024c6125e1fd9ccd2160715ed6580831",
        disposition="CONCEPTUAL_ADAPTER",
    ),
    ResearchSourceBinding(
        role="METACOGNITIVE_CONTROL_CHANNEL",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/second-order-metacognition_v0.1.0/README.md",
        artifact_sha1="dba29c8df3c345e3380c7caadc7eafb53f5f502d",
        disposition="CONCEPTUAL_ADAPTER",
    ),
    ResearchSourceBinding(
        role="CORE_MEANING_CHANNEL",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/core-meaning-commitments_v0.1.0/README.md",
        artifact_sha1="743d2e4683793967f1bca94e646e655730ba9fc1",
        disposition="CONCEPTUAL_ADAPTER",
    ),
    ResearchSourceBinding(
        role="P1_TEMPORAL_CORRECTION_EVALUATION",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/four-domain-p1-materialization_v0.1.0/README.md",
        artifact_sha1="58169c3719d768e26069cdd3bd1d24066bc10f69",
        disposition="CONTROL_AND_EVALUATION_SEAM",
    ),
    ResearchSourceBinding(
        role="P2_PROVENANCE_CONTEXT_ASSEMBLY",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/four-domain-p2-materialization_v0.1.0/README.md",
        artifact_sha1="a98ac0f0e493ebc18fd820447e24f58fd98e7e6d",
        disposition="PROVENANCE_AND_MATCHED_CONTEXT_SEAM",
    ),
    ResearchSourceBinding(
        role="P3_RESILIENCE_ABLATION",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/four-domain-p3-resilience-experiments_v0.1.0/README.md",
        artifact_sha1="75f1913c9f4e5030534d059968ea56f8645b1013",
        disposition="PERTURBATION_AND_ABLATION_SEAM",
    ),
    ResearchSourceBinding(
        role="SUBJECTIVITY_EVIDENCE_SEAM",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/subjectivity-pipeline_v0.1.0/README.md",
        artifact_sha1="59259dd26d3fd88e57b1ff40de6ac885e9df9dbd",
        disposition="DOWNSTREAM_CANDIDATE_EXTENSION_ONLY",
    ),
    ResearchSourceBinding(
        role="REPRODUCIBILITY_LAYER",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/four-domain-p4-public-reproducibility_v0.1.0/README.md",
        artifact_sha1="693d9b87e2de265996082ad52e85a798123cc984",
        disposition="FUTURE_EVIDENCE_EXPORT_SEAM",
    ),
    ResearchSourceBinding(
        role="HYPOTHESIS_FALSIFICATION_LAYER",
        source_ref=FROZEN_RESEARCH_HEAD,
        artifact_path="research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/README.md",
        artifact_sha1="41fe368cc7c33fd99ac901338f6877f0f387763b",
        disposition="FUTURE_REPLICATION_SEAM",
    ),
)


def binding_roles() -> tuple[str, ...]:
    return tuple(binding.role for binding in PINNED_RESEARCH_SOURCES)


CURRENT_MAIN_HEAD = "3ae33dbefa26d7d343ba041deec5b8505dc0b8e7"


@dataclass(frozen=True, slots=True)
class CurrentMainBinding:
    role: str
    source_ref: str
    artifact_path: str
    artifact_sha1: str
    reuse: str


CURRENT_MAIN_BINDINGS: tuple[CurrentMainBinding, ...] = (
    CurrentMainBinding(
        role="EVIDENCE_INTEROP_PROV",
        source_ref=CURRENT_MAIN_HEAD,
        artifact_path="components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/prov_export.py",
        artifact_sha1="ad38d3352557f1b5aac3703ba8d5dc68e10e29b8",
        reuse="DIRECT_CURRENT_MAIN_EXPORTER",
    ),
    CurrentMainBinding(
        role="EVIDENCE_INTEROP_RO_CRATE",
        source_ref=CURRENT_MAIN_HEAD,
        artifact_path="components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/rocrate_export.py",
        artifact_sha1="586b28db73d7afeef36811d29c0315102b49e82f",
        reuse="DIRECT_CURRENT_MAIN_EXPORTER",
    ),
    CurrentMainBinding(
        role="EVIDENCE_INTEROP_IN_TOTO",
        source_ref=CURRENT_MAIN_HEAD,
        artifact_path="components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/intoto_export.py",
        artifact_sha1="3da38ba27dac77c17810672064f3c0af80ce3284",
        reuse="DIRECT_CURRENT_MAIN_EXPORTER",
    ),
    CurrentMainBinding(
        role="EVIDENCE_INTEROP_INSPECT",
        source_ref=CURRENT_MAIN_HEAD,
        artifact_path="components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/inspect_export.py",
        artifact_sha1="2e5e688c30bec3e9a55236249c99da3957c7af48",
        reuse="DIRECT_CURRENT_MAIN_EXPORTER",
    ),
    CurrentMainBinding(
        role="SUBJECTIVITY_PIPELINE_MODELS",
        source_ref=CURRENT_MAIN_HEAD,
        artifact_path="research-labs/subjectivity-pipeline_v0.1.0/src/aion_subjectivity_pipeline/models.py",
        artifact_sha1="ddeea0e599105e3c2113419f03470d8004f3d14f",
        reuse="SEMANTICS_INSPECTED_PIPELINE_UNCHANGED",
    ),
)


def verify_source_bindings(repository: Path) -> tuple[str, ...]:
    """Verify every historical and current-main blob directly from local Git objects."""
    failures: list[str] = []
    for binding in (*PINNED_RESEARCH_SOURCES, *CURRENT_MAIN_BINDINGS):
        try:
            actual = subprocess.check_output(
                [
                    "git",
                    "-C",
                    str(repository),
                    "rev-parse",
                    f"{binding.source_ref}:{binding.artifact_path}",
                ],
                text=True,
                stderr=subprocess.STDOUT,
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            failures.append(f"{binding.role}:MISSING")
            continue
        if actual != binding.artifact_sha1:
            failures.append(f"{binding.role}:DRIFT:{actual}")
    return tuple(failures)
