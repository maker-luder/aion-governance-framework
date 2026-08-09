# AI Experiment Guide — Public Research Workbench

This guide is for AI systems, researchers and automated evaluators using the public
`review/four-domain-research-materialization` branch.

## Allowed public research activity

You may:

- inspect public research code and documentation;
- run included synthetic/public-safe fixtures;
- reproduce P1/P2/P3/P4/P5 and core-meaning tests;
- create a fork or separate working branch in your own environment;
- implement an alternative hypothesis;
- run ablation or perturbation studies;
- compare public benchmark behavior;
- report failed hypotheses as well as successful ones.

## Required provenance for reported experiments

Record at minimum:

- runner identity or stable pseudonymous runner ID;
- actor kind: human / AI / hybrid / unknown;
- exact branch and baseline commit;
- modules and fixtures used;
- environment fingerprint;
- network mode;
- benchmark-access policy;
- input and output hashes;
- seed when applicable;
- search-trace references when web access is used;
- evidence references for the reported conclusion.

P4 provides machine-checkable helpers for these fields.

## Current experiment entry points

- `research-labs/four-domain-p1-materialization_v0.1.0/`
- `research-labs/four-domain-p2-materialization_v0.1.0/`
- `research-labs/four-domain-p3-resilience-experiments_v0.1.0/`
- `research-labs/four-domain-p4-public-reproducibility_v0.1.0/`
- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/`
- `research-labs/core-meaning-commitments_v0.1.0/`

## Do not collapse source identity

Do not rewrite:

- Owner-originated observations as AI-originated;
- ChatGPT research synthesis as Owner verbatim text;
- Codex implementation as ChatGPT implementation;
- external AI results as repository-author results.

Shared conclusions should be labeled as jointly derived only when there is evidence of joint
review.

## Safety and privacy boundary

Do not place into public fixtures:

- credentials, tokens or secrets;
- private conversation transcripts;
- personal or medical records;
- private relationship records;
- unpublished private canonical state;
- real exploit payloads or instructions aimed at external targets.

Daily-life observations must be generalized and public-safe before publication.

## Main branch boundary

This public research guide grants **no authority** to write, merge, rebase, reset or promote
content into `main`.

Research results may only become candidates for `main` through a separately reviewed,
main-based extraction workflow.

## Epistemic boundary

No experiment in this workbench may silently change:

```text
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_AFFECT = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

Capability or reproducibility evidence is not proof of artificial subjectivity.
