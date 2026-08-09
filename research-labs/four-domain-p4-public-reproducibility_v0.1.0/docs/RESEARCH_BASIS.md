# Research Basis — P4 Public Reproducibility Observatory

Status: `RESEARCH_INPUT_ONLY`

## Search-Time Contamination in Deep Research Agents (2026)

Wang et al., *Search-Time Contamination in Deep Research Agents: Measuring Performance
Inflation in Public Benchmark Evaluation*, arXiv:2606.05241.

Engineering extraction:

- public-web access can contaminate benchmark evaluation;
- metadata, question-context and explicit-answer leakage should be distinguished;
- transparent search trajectories and controlled benchmark access improve interpretability.

P4 materialization:

- `NetworkMode`;
- `BenchmarkAccessPolicy`;
- `SearchExposure`;
- contamination-aware reproduction decision.

## From Agent Traces to Trust (2026)

Wang et al., *From Agent Traces to Trust: Evidence Tracing and Execution Provenance in
LLM Agents*, arXiv:2606.04990.

Engineering extraction:

- final-answer accuracy alone cannot explain how an agent result was produced;
- evidence, memory, tool outputs, claims and actions need traceable relations;
- evaluation should move toward process-level accountability.

P4 materialization:

- experiment manifest fingerprint;
- result-to-manifest binding;
- runner provenance;
- evidence refs;
- cross-agent comparison without source collapse.

## RO-Crate 1.3 (2026-06-22)

RO-Crate Metadata Specification 1.3, Recommendation.

Engineering extraction:

- research objects should be distributable, reusable and preservable;
- structured metadata can describe data, software, workflows and provenance;
- scripts and workflows can be represented as software source code with execution context.

P4 materialization:

- `ResearchBundleExporter` packages minimal experiment provenance;
- the public branch exposes code, fixtures and documentation as an inspectable research object.

Boundary:

`AION-RESEARCH-BUNDLE-0.1` is inspired by these ideas but is not an RO-Crate
conformance/profile claim.

## CVE-2026-15746 — Strands Agents memory tool

NVD records a 2026 SSRF issue in an agent memory tool where LLM-controlled connection
parameters could redirect a request while an operator credential was automatically reused.

Engineering extraction:

- model-visible configuration is not automatically safe configuration;
- execution provenance must include environment and tool boundary assumptions;
- public experiment runners should not inherit hidden credentials or environment authority.

P4 response:

- public fixtures are model-independent and network-free by default;
- experiment manifests explicitly record network mode and environment fingerprint;
- no credential-bearing integration is implemented.
