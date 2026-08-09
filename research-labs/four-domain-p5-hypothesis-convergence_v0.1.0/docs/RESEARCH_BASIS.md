# Research Basis — P5

Status: `RESEARCH_INPUT_ONLY`

## ReplicatorBench (2026)

Nguyen et al., *ReplicatorBench: Benchmarking LLM Agents for Replicability in Social and
Behavioral Sciences*, arXiv:2602.11354.

Engineering extraction:

- replication should be assessed end-to-end, not only by final output;
- replicable and non-replicable claims both matter;
- retrieval, experiment execution and interpretation are distinct stages;
- process evidence should remain inspectable.

P5 response:

- append-only replication registry;
- per-run provenance;
- divergent outcomes are first-class research results.

## DiscoUQ (2026)

Jiang, *DiscoUQ: Structured Disagreement Analysis for Uncertainty Quantification in LLM
Agent Ensembles*, arXiv:2603.20975.

Engineering extraction:

- simple vote counts discard structure in inter-agent disagreement;
- evidence overlap and disagreement structure are informative;
- weak disagreement can be different from substantive contradiction.

P5 response:

- explicit conclusion distribution;
- pairwise evidence overlap;
- explicit disagreement dimension tags;
- no hidden semantic adjudicator.

This module does not claim to reproduce DiscoUQ's learned models or embedding methods.

## OSF registrations / preregistration

The Open Science Framework describes preregistration as a time-stamped research plan and
registrations as frozen research records that can preserve the state of a project at
important lifecycle points.

Engineering extraction:

- hypotheses and falsification rules benefit from prior registration;
- later deviations or state changes should remain visible;
- withdrawal/closure should preserve history rather than rewrite it.

P5 response:

- formal hypothesis records require falsification criterion references;
- lifecycle transitions are append-only;
- falsification observations are distinct from canonical judgments.

## Responsible Agentic AI Requires Explicit Provenance (2026)

Hu et al., arXiv:2605.17169.

Engineering extraction:

- multi-agent outcomes require traceable lifecycle provenance;
- responsibility/attribution should not collapse across composed agents.

P5 response:

- runner identity is retained in disagreement and replication records;
- Human Owner convergence authority and ChatGPT engineering implementation are separate
  provenance roles.
