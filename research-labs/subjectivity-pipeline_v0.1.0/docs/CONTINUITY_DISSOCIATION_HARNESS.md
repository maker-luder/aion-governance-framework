# Continuity-dissociation synthetic harness

Status: `IMPLEMENTED_SYNTHETIC_FIXTURE / SCIENTIFIC_HOLD`

## Provenance and dependency

This bounded implementation was originally selected while PR #101 was still a
draft and was implemented on the then-current `main`. It extends the existing
subjectivity pipeline rather than creating another framework.

```text
HISTORICAL_IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
HISTORICAL_IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
HISTORICAL_PREREGISTRATION_REFERENCE = PR #101 @ b6d81743c6e8b879be31074bb9d98acc9b4be13a
CURRENT_MERGED_SPECIFICATION_HEAD = PR #101 @ fe398ab14e018c749cdce3268bbc274bb02b72ac
SPECIFICATION_MERGE_COMMIT = 9d21e6981f5eb61a35ec8c283b99193cbfe43fd5
PR101_MERGED = TRUE
PR101_USED_AS_IMPLEMENTATION_BASE = FALSE
FULL_CONFORMANCE_TO_MERGED_PR101_SPECIFICATION = NOT_ESTABLISHED
```

The fixture's preregistration reference remains the historical PR #101 head that
was bound when the synthetic fixture was created. It is not rewritten to pretend
that the later merged specification was the original preregistration. The merged
PR #101 specification is instead recorded separately as the current specification
state.

The Human Owner's 2026-09-13 instruction authorized this bounded implementation
surface. It did not by itself authorize merging, deployment, canonical claim
promotion, or later scope expansion.

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

Selective interventions must target exactly one declared channel and retain every
other declared channel. Baseline, external-context reset, yoked, random, and
stale-state controls must retain every declared channel and cannot claim a removed
channel. These invariants fail closed.

Every case uses the same declared provider, model, runtime, scaffold, prompt-set,
retrieval-manifest, evaluator, preregistration, repository commit/tree, and seed
bindings. Drift in those declared bindings fails closed.

```text
DECLARED_BINDING_EQUALITY != ACTUAL_PROMPT_OR_RETRIEVAL_PAYLOAD_EQUALITY
SEED_FIELD != REPEATED_TRIAL_SAMPLING
TARGET_LABEL_DISTINCTION != BEHAVIORAL_DISSOCIATION
FIXTURE_FINGERPRINT != MODEL_OBSERVATION_AUTHENTICATION
```

The merged PR #101 specification identified these distinctions explicitly. This
hardening closes the structural non-target-preservation gap only; it does not
claim full conformance to every later PR #101 requirement.

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
replication, actual prompt/retrieval payload equivalence, repeated trials,
manipulation-success measurement, effect-size estimation, and evaluator-blinded
empirical results remain untested.

## Reproduction

From `research-labs/subjectivity-pipeline_v0.1.0`:

```powershell
python scripts/run_continuity_dissociation_synthetic.py
python -m pytest -q
```

The first command must reproduce
`results/continuity_dissociation_synthetic_receipt.json` byte-for-byte. Tests
cover matrix completeness, exact channel targeting, complete non-target
preservation, complete control-channel retention, matched-binding drift, privacy
and psychometric exclusions, payload fingerprints, nonclaim boundaries, and
receipt/fixture hashes.
