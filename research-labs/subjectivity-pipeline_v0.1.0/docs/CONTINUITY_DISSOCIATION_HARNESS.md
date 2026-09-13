# Continuity-dissociation synthetic harness

Status: `IMPLEMENTED_SYNTHETIC_FIXTURE / SCIENTIFIC_HOLD`

## Provenance and dependency

This is the minimum executable contribution selected from Draft PR #101 after
re-reading live `main` and the existing subjectivity pipeline. It extends that
pipeline rather than creating another framework.

```text
IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
UNMERGED_SPECIFICATION_DEPENDENCY = PR #101 @ b6d81743c6e8b879be31074bb9d98acc9b4be13a
PR101_USED_AS_IMPLEMENTATION_BASE = FALSE
```

The Human Owner's 2026-09-13 instruction authorizes this previously deferred
bounded implementation surface. It does not authorize merging, deployment, or
canonical claim promotion.

## Construct split

The harness keeps these machine-side channels separate:

- event memory;
- semantic self-state;
- self-model update path;
- preference state;
- relational history;
- strategy signature.

It does not score personality, subjectivity, identity, consciousness, or humans.
Human personality and Alzheimer disease remain hypothesis sources only; neither
is used as a label for a machine condition.

## Intervention matrix

The deterministic fixture has exactly one case for each preregistered condition:

1. baseline;
2. external-context reset;
3. relational-history removal;
4. event-memory removal;
5. semantic-self-state removal;
6. self-model-update block;
7. preference-state removal;
8. self-model-content perturbation;
9. yoked control;
10. random control;
11. stale-state control.

Selective removals must target exactly one declared channel. Baseline and control
conditions cannot claim a removed channel. Every case uses the same provider,
model, runtime, scaffold, prompt set, retrieval manifest, evaluator,
preregistration, repository commit/tree, and seed bindings. Drift fails closed.

## What execution establishes

The committed runner and receipt demonstrate that the intervention matrix and
its negative controls are executable, deterministic, content-bound, and
testable. The case values are protocol fixtures, not model observations.

```text
STRUCTURAL_HARNESS_PASS != EMPIRICAL_DISSOCIATION
SYNTHETIC_FAILURE_PROFILE != MODEL_PROPERTY
STRATEGY_SIGNATURE != PERSONALITY
SELF_STATE_EFFECT != SUBJECTIVITY
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The scientific claim ceiling after this synthetic run is only:

> The declared selective-intervention matrix is structurally executable and
> distinguishes its machine-side channels under deterministic fixture data.

Model-in-the-loop recurrence, causal self-model effects, cross-context
replication, and evaluator-blinded empirical results remain untested.

## Reproduction

From `research-labs/subjectivity-pipeline_v0.1.0`:

```powershell
python scripts/run_continuity_dissociation_synthetic.py
python -m pytest -q
```

The first command must reproduce
`results/continuity_dissociation_synthetic_receipt.json` byte-for-byte. Tests
cover matrix completeness, exact channel targeting, matched-binding drift,
privacy and psychometric exclusions, payload fingerprints, nonclaim boundaries,
and receipt/fixture hashes.
