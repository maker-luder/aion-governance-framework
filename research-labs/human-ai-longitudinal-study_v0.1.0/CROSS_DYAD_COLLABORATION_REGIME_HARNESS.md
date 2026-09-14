# Cross-dyad collaboration-regime synthetic harness

Status: `IMPLEMENTED_SYNTHETIC_FIXTURE / SCIENTIFIC_HOLD`

## Read-before-act provenance

This extension was originally prepared only after reading the live repository
state and the research navigation path in this order:

1. live `main` at `d95bc2625e71f1c85a725aaba78cb0feccfc0668`;
2. then-open Draft PR #102 at
   `3ce4f759caf662a53f0d1f3a54709bc482d7df5e`;
3. then-open Draft PR #101 at
   `b6d81743c6e8b879be31074bb9d98acc9b4be13a`;
4. merged PR #93, head
   `c37655c33fa235de6528ff687daa65f86f01afe4`, merge commit
   `5d889e51630a3c0849d773439e37396a623e9987`;
5. the longitudinal harness already present on live `main`.

The implementation branch was cut from the exact live `main` commit in item 1.
The fixture, runner and committed execution receipt intentionally retain the
exact PR #102 head that supplied the implementation-time specification. That
historical binding is evidence about what was implemented and must not be
rewritten as though a later specification state had existed at implementation
time:

```text
HISTORICAL_SPECIFICATION_REFERENCE = PR #102 @ 3ce4f759caf662a53f0d1f3a54709bc482d7df5e
STATE_AT_IMPLEMENTATION = UNMERGED_DRAFT
IMPLEMENTATION_BASE = main @ d95bc2625e71f1c85a725aaba78cb0feccfc0668
PR102_USED_AS_IMPLEMENTATION_BASE = FALSE
```

PR #102 has since merged. The current repository provenance is:

```text
PR102_CURRENT_STATE = MERGED
PR102_FINAL_HEAD = 2b151df564d753d6ce978a319a99959b864f7309
PR102_MERGE_COMMIT = e95da8be67a8ff313d2e5ebf61ade0c2e2adac66
PR103_SYNC_BASE = 0ee6b8036115645162bb3d8af2f574651851f4cc
HISTORICAL_REFERENCE != CURRENT_SPECIFICATION_STATE
OLD_SPEC_BINDING != AUTOMATIC_NONCONFORMANCE
COMPLETE_CONFORMANCE_TO_HARDENED_PR102 = NOT_ESTABLISHED
```

PR #101 was cross-read for boundary compatibility. Its later merged state does
not retroactively change the scope of this harness. PR #93 is the merged
antecedent for the longitudinal study surface reused by this extension.

## Specification-convergence and semantic-drift check — 2026-09-14

The merge of current `main` into PR #103 did not intentionally rewrite the
cross-dyad implementation surface. The historical A-D conditions, optional E
closure control, nine synthetic task families and fifteen observable dimensions
remain the implementation-time contract.

The merged final PR #102 specification later added interpretation hardening and
prospective confound controls, including prompt-length, information-volume,
task-relevance, tool/time-budget and answer-leakage controls plus the prospective
`C_PLUS_MATCHED_INFORMATION_CONTROL`. Those additions do not retroactively become
implemented conditions merely because PR #102 is now on `main`.

The current interpretation must therefore remain bounded:

```text
SYNC_INTRODUCED_CORE_IMPLEMENTATION_DRIFT = NO_EVIDENCE_FOUND
SPECIFICATION_EVOLUTION_AFTER_IMPLEMENTATION = YES
HISTORICAL_A_TO_E_SURFACE = PRESERVED
C_PLUS_MATCHED_INFORMATION_CONTROL = NOT_IMPLEMENTED
HISTORY_SPECIFIC_CAUSAL_IDENTIFICATION = NOT_ESTABLISHED
CURRENT_HARDENED_SPEC_FULL_CONFORMANCE = NOT_ESTABLISHED
```

The PR #102 review also identified a narrower referential-integrity defect in the
committed condition fixture: conditions C and D used the same
`closure_rule_ref = fixture:counterevidence-and-claim-ceiling-v1` while carrying
different closure payloads. Per-packet fingerprints bound each packet, but the
shared reference did not identify one stable payload.

That defect is repaired in the later bounded hardening described below. The
repair does not make C and D semantically matched and does not establish a unique
history effect.

## Referential-consistency hardening — 2026-09-14

The condition-D closure payload remains unchanged. Only its human-readable
reference is disambiguated to match the payload it actually names:

```text
OLD_D_CLOSURE_RULE_REF = fixture:counterevidence-and-claim-ceiling-v1
NEW_D_CLOSURE_RULE_REF = fixture:repository-history-and-claim-ceiling-v1
D_CLOSURE_RULE_PAYLOAD_CHANGED = FALSE
D_INSTRUCTION_PAYLOAD_CHANGED = FALSE
```

A committed regression test now verifies, for the synthetic condition fixture,
that every repeated `instruction_ref` maps to exactly one `instruction_payload`
and every repeated `closure_rule_ref` maps to exactly one
`closure_rule_payload`. This is a repository-fixture invariant; it is not a new
generic runtime reference registry.

Because the condition fixture bytes changed, the deterministic receipt is
regenerated only to update the bound `condition_packet_sha256`. The historical
PR #102 specification reference, implementation base, synthetic metric values,
claim boundaries and scientific disposition are not promoted or rewritten.

```text
COMMITTED_FIXTURE_REFERENTIAL_CONSISTENCY = ENFORCED_BY_REGRESSION_TEST
PER_PACKET_INTEGRITY = PRESENT
SAME_REF_DIFFERENT_PAYLOAD = REJECTED_FOR_COMMITTED_FIXTURE
GENERIC_RUNTIME_REFERENCE_REGISTRY = NOT_IMPLEMENTED
C_VS_D = PACKAGE_CONTRAST
C_VS_D != UNIQUE_HISTORY_EFFECT
HISTORY_SPECIFIC_CAUSAL_IDENTIFICATION = NOT_ESTABLISHED
```

Conditions C and D still have different instruction payloads and different
closure semantics, and D additionally carries repository-history references.
The ref repair therefore closes the naming/integrity defect only; it does not
convert the historical C-vs-D package comparison into the prospective matched
history-specific contrast described by the hardened PR #102 specification.

## Why this is an extension, not another framework

The existing longitudinal harness already binds provider, model, generation
configuration, task, tool manifest, scorer, preregistration, repository commit,
seed, metrics, and held-out state. The extension therefore adds only the missing
cross-dyad experimental surface inside that lab:

- an exact task-by-condition matrix;
- immutable condition-packet fingerprints over the actual instruction and
  closure-rule payloads, not only their reference labels;
- immutable task fingerprints over the actual synthetic prompt payloads;
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
strictness, fail-closed drift handling, and committed-fixture reference-to-payload
consistency.

Each condition fixture carries both a human-readable reference and its actual
instruction and closure-rule payload. Each task fixture likewise carries both a
prompt reference and its actual prompt payload. Run bindings hash those contents;
changing content while retaining a label therefore fails closed at run-binding
integrity, while the committed-fixture regression test separately guards against
one reference naming multiple payloads. The receipt also records the
implementation-base commit SHA and tree SHA as distinct fields.

The receipt's PR #102 dependency fields are intentionally historical execution
provenance. In particular, an implementation-time `unmerged_dependency = true`
does not assert that PR #102 is still unmerged now.

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

This materialization is limited to the authorization recorded in the historical
exact PR #102 specification: synthetic task harness, condition packets,
observable metrics, tests, execution receipts, and reproduction documentation on
a separate implementation Draft PR. Later PR #102 documentation hardening does
not silently expand that implementation authorization.

The work performs no merge, no `main` write, no deployment, no private transcript
collection, no third-party account access, no psychometric classification of
humans, no subjectivity scoring, and no autonomous scope expansion. Any later
claim admission, canonicalization, merge, or deployment remains a separate Human
Owner decision at the exact implementation head.
