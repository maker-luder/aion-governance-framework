# AION Research Branch Status

> **You are viewing the public research workbench, not the `main` release branch.**

```text
BRANCH = review/four-domain-research-materialization
CURRENT_STAGE = P4
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
```

## Current research stack

| Stage | Materialization | Status |
|---|---|---|
| P1 | Temporal/version resolution, correction/conflict ledger, memory evaluation | IMPLEMENTED / TESTED |
| P2 | Retrieval trace, deterministic context assembly, provenance validation, T2/T3 orchestration | IMPLEMENTED / TESTED |
| P3 | Longitudinal contamination, context perturbation, control ablation, origin-bound authority | IMPLEMENTED / TESTED |
| P4 | Public reproducibility observatory, contamination-aware experiment manifests, cross-agent comparison | IMPLEMENTED / TESTED |

## Public experiment entry points

- `research-labs/four-domain-p1-materialization_v0.1.0/`
- `research-labs/four-domain-p2-materialization_v0.1.0/`
- `research-labs/four-domain-p3-resilience-experiments_v0.1.0/`
- `research-labs/four-domain-p4-public-reproducibility_v0.1.0/`
- `AI_EXPERIMENT_GUIDE.md`

## What outside researchers / AI systems may do

They may read, clone, fork, execute public-safe fixtures, run tests, create alternative
implementations, perform ablations and publish their own experiment results under their own
provenance.

They are not thereby granted authority to modify this branch, `main`, canonical state or
private project material.

## Promotion boundary

Research material does not flow into `main` automatically.

```text
research observation / experiment
        ↓
research branch materialization
        ↓
Human Owner + ChatGPT joint review
        ↓
selected result only
        ↓
fresh branch from current main
        ↓
QA / review / PR
        ↓
main
```

No step in this file is an approval to promote a research artifact.
