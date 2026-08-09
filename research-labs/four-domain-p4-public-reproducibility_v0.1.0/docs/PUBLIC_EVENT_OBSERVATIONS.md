# Public Event Observations — P4

Status: `PUBLIC_SAFE_RESEARCH_OBSERVATIONS`

This document records public-event engineering lessons without copying exploit payloads,
credentials, private data or operational attack instructions.

## OBS-P4-001 — Benchmark search contamination

Source: arXiv:2606.05241.

Observation:
A web-enabled research agent may retrieve benchmark metadata, question context or explicit
answers while it is being evaluated.

Research consequence:
A score from a public-web run must not be compared as if it were equivalent to an isolated
run unless the benchmark-access conditions are recorded.

Materialization:
`SearchExposure`, `BenchmarkAccessPolicy`, contamination-aware reproduction decisions.

## OBS-P4-002 — Execution provenance

Source: arXiv:2606.04990.

Observation:
Final-answer correctness is insufficient for audit when memory, tools and retrieval
contribute to a result.

Research consequence:
The public branch should preserve experiment identity, runner, baseline, fixtures,
environment and evidence references.

Materialization:
`ExperimentManifest`, `ExperimentResult`, `ReproductionValidator`.

## OBS-P4-003 — Agent memory tool credential boundary

Source: NVD CVE-2026-15746.

Observation:
Model-controlled tool parameters can become a credential/execution boundary failure when
operator secrets are reused implicitly.

Research consequence:
Public experiment protocols should make network mode and environment assumptions visible
and should not require hidden credentials.

Materialization:
offline-by-default fixture; explicit network mode; no secret-bearing integration.

## Daily-life observation rule

Daily-life experiences may inspire research questions, but the public research branch only
accepts **generalized, public-safe observations**. Personal identifiers, private
conversations, relationship records, medical details, credentials and unpublished private
project state must not be copied into the public observation ledger.
