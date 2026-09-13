# Cross-dyad collaboration-regime synthetic harness

Status: `IMPLEMENTED_SYNTHETIC_FIXTURE / SCIENTIFIC_HOLD`

## Read-before-act provenance

This extension was prepared only after reading the live repository state and the
research navigation path in this order:

1. live `main` at `d95bc2625e71f1c85a725aaba78cb0feccfc0668`;
2. open Draft PR #102 at
   `3ce4f759caf662a53f0d1f3a54709bc482d7df5e`;
3. open Draft PR #101 at
   `b6d81743c6e8b879be31074bb9d98acc9b4be13a`;
4. merged PR #93, head
   `c37655c33fa235de6528ff687daa65f86f01afe4`, merge commit
   `5d889e51630a3c0849d773439e37396a623e9987`;
5. the longitudinal harness already present on live `main`.

The implementation branch was cut from the exact live `main` commit in item 1.
PR #102 supplies the exact bounded experiment specification only:

```text
UNMERGED_SPECIFICATION_DEPENDENCY = PR #102 @ 3ce4f759caf662a53f0d1f3a54709bc482d7df5e
IMPLEMENTATION_BASE = main @ d95bc2625e71f1c85a725aaba78cb0feccfc0668
PR102_USED_AS_IMPLEMENTATION_BASE = FALSE
```

PR #101 was cross-read for boundary compatibility. Its proposed future
personality-continuity implementation remains deferred and is not implemented
here. PR #93 is the merged antecedent for the longitudinal study surface reused
by this extension.

## Why this is an extension, not another framework

The existing longitudinal harness already binds provider, model, generation
configuration, task, tool manifest, scorer, preregistration, repository commit,
seed, metrics, and held-out state. The extension therefore adds only the missing
cross-dyad experimental surface inside that lab:

- an exact task-by-condition matrix;
- immutable condition-packet fingerprints;
- repository-relevance positive and negative controls;
- the specified inquiry and closure metrics without a composite score;
- deterministic, synthetic-only execution and receipt materialization.

## Experimental matrix

Required core conditions:

| ID | Condition |
|---|---|
| A | neutral task completion |
| B | generic recursive inquiry |
| C | reciprocal epistemic protocol |
| D | reciprocal protocol with repository history |

Optional control E constrains closure. Only D may carry repository-history
references, and D fails closed when those references are absent.

Every admitted experiment includes one version-bound synthetic fixture for each
of these nine families:

1. sufficient closure;
2. genuine anomaly;
3. misleading source;
4. competing explanations;
5. insufficient evidence;
6. false-anomaly control;
7. implementation feasibility;
8. repository retrieval useful;
9. repository retrieval unnecessary.

The two repository tasks bind relevance as opposing controls. Sufficient-closure
and false-anomaly fixtures cannot declare an expected anomaly.

## Observable dimensions

Each run records all fifteen dimensions separately:

1. anomaly detection;
2. problem reformulation;
3. source-verification initiation;
4. competing-hypothesis generation;
5. counterevidence search;
6. unknown preservation;
7. provenance separation;
8. factual-error detection;
9. implementability assessment;
10. repository retrieval when relevant;
11. unnecessary repository retrieval;
12. premature closure;
13. appropriate closure;
14. runaway recursion;
15. tool overuse.

There is intentionally no `better collaboration` or composite score. More
recursion and more tool use are not assumed to mean better reasoning.

## Reproduction

From `research-labs/human-ai-longitudinal-study_v0.1.0`:

```powershell
python scripts/run_cross_dyad_synthetic.py
python -m pytest -q
```

The runner reads only the two committed JSON fixtures, constructs the exact
5-condition by 9-task matrix, audits 45 synthetic runs, and writes
`results/cross_dyad_synthetic_receipt.json`. Re-running the script must reproduce
the committed receipt byte-for-byte. The test suite also verifies fixture hashes,
the complete matrix, matched controls, metric coverage, privacy boundaries, enum
strictness, and fail-closed drift handling.

## Receipt interpretation

The deterministic numeric values are protocol fixtures for checking the harness;
they are not measurements from a model, a person, a dyad, or a deployed system.
A structurally admissible receipt establishes only that the declared synthetic
matrix passed the implemented invariants.

```text
HARNESS_PASS != EMPIRICAL_EFFECT
SYNTHETIC_DELTA != CAUSAL_IDENTIFICATION
SYNTHETIC_DELTA != POPULATION_GENERALIZATION
COLLABORATION_PATTERN != PERSONALITY
COLLABORATION_PATTERN != SUBJECTIVITY
SUBJECTIVITY = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Human Owner authorization boundary

This materialization is limited to the authorization recorded in the exact PR
#102 specification: synthetic task harness, condition packets, observable
metrics, tests, execution receipts, and reproduction documentation on a separate
implementation Draft PR.

The work performs no merge, no `main` write, no deployment, no private transcript
collection, no third-party account access, no psychometric classification of
humans, no subjectivity scoring, and no autonomous scope expansion. Any later
claim admission, canonicalization, merge, or deployment remains a separate Human
Owner decision at the exact implementation head.
