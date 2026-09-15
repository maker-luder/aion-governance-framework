# Epistemic accumulation and evidence-reuse firewall

Status: `BOUNDED_IMPLEMENTATION / STRUCTURALLY_TESTED / SCIENTIFIC_HOLD`

This minimal extension implements the research-method gap recorded by PR #106,
which is now merged, while reusing merged PR #93's longitudinal harness.

```text
IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
SPECIFICATION_PROVENANCE = PR #106 @ 570fb0f1c88f0d5db22493858f28fdab546b75cf
SPECIFICATION_STATUS = MERGED
PR106_MERGE_COMMIT = 60b2a620ecd703dbef314ee7d76bfbd3a96c3ef1
HISTORICAL_SYNCED_MAIN_COMMIT_SHA = 6e0ae579da9d09b3ba4041d52a7e9833ceb10ca1
```

Implemented: exact A-D fresh/summary/versioned/navigable condition packets;
typed dependency nodes and relations; exactly one graph `BASELINE` node bound by
`baseline_id`; claim/source/version/proposition/scope/support/ceiling manifests;
and a fail-closed evidence-reuse firewall when proposition, scope, currency,
canonical state, or empirical-result binding changes. Private transcript payloads
are rejected.

The A-D condition flags are not merely minimum requirements. Each condition must
match its preregistered control tuple exactly, so a fresh or flat-summary cell
cannot silently acquire provenance/navigation controls and a versioned cell
cannot silently lose them. Manifest enums and dependency relations are exact
typed values, and duplicate counterevidence identifiers are rejected.

This does not duplicate closed-unmerged PR #103's historical cross-dyad metrics.
The matrix output is a deterministic no-model fixture artifact and is admissible
only as structural QA, consistent with the structural-fixture evidence boundary
on `main`.

```text
CONDITION_LABEL != PREREGISTERED_CONTROL_BINDING
BASELINE_ID = UNIQUE_BASELINE_NODE
IMPLEMENTATION_REUSE != EVIDENCE_REUSE
SAME_TOPIC != SAME_SUPPORTED_PROPOSITION
UNMERGED_DRAFT != CANONICAL_EVIDENCE
MODE = DETERMINISTIC_SYNTHETIC_FIXTURE
MODEL_INVOKED = FALSE
EVIDENCE_ADMISSIBILITY = STRUCTURAL_QA_ONLY
SYNTHETIC_MATRIX_PASS != LONGITUDINAL_ACCUMULATION_EFFECT
MUTUAL_LEARNING = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
