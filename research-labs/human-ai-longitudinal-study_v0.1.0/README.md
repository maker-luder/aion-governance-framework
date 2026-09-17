# Human-AI longitudinal study harness v0.1.0

The bounded evidence-reuse firewall and artifact-condition extension is
documented in [`EPISTEMIC_ACCUMULATION_AND_EVIDENCE_REUSE.md`](EPISTEMIC_ACCUMULATION_AND_EVIDENCE_REUSE.md).

The bounded calibration extension is documented in
[`ADAPTIVE_RIGOR_CALIBRATION_HARNESS.md`](ADAPTIVE_RIGOR_CALIBRATION_HARNESS.md).

The bounded reciprocal re-entry metric extension is documented in
[`RECIPROCAL_REENTRY_METRIC_RUNNER.md`](RECIPROCAL_REENTRY_METRIC_RUNNER.md).

The bounded held-out habit-transfer analogue is documented in
[`SYNTHETIC_HABIT_TRANSFER_ANALOGUE.md`](SYNTHETIC_HABIT_TRANSFER_ANALOGUE.md).

The bounded externalized-metacognitive-policy transfer extension is documented in
[`METACOGNITIVE_POLICY_TRANSFER_HARNESS.md`](METACOGNITIVE_POLICY_TRANSFER_HARNESS.md).

The bounded task-selection / yoked-exposure design-audit extension is documented in
[`TASK_SELECTION_YOKED_EXPOSURE_HARNESS.md`](TASK_SELECTION_YOKED_EXPOSURE_HARNESS.md).

The additive post-merge hardening for explicit choice-opportunity sets,
execution identity/content separation and cross-family held-out challenges is
implemented in `src/aion_human_ai_longitudinal/task_selection_exposure_hardened.py`
and documented in
[`../../docs/research/TASK_SELECTION_CHOICE_OPPORTUNITY_AND_TRANSFER_HARDENING_2026_09_17.md`](../../docs/research/TASK_SELECTION_CHOICE_OPPORTUNITY_AND_TRANSFER_HARDENING_2026_09_17.md).
The PR #139 auditor is retained for historical/API compatibility; the hardened
auditor is the stricter future admission surface for these three semantics.

The bounded attention-structure reconstruction extension is implemented in
`src/aion_human_ai_longitudinal/attention_structure_reconstruction.py` and documented in
[`ATTENTION_STRUCTURE_RECONSTRUCTION_HARNESS.md`](ATTENTION_STRUCTURE_RECONSTRUCTION_HARNESS.md)
plus
[`../../docs/research/ATTENTION_STRUCTURE_RECONSTRUCTION_ACROSS_CONTEXTS_AND_SYSTEMS_2026_09_17.md`](../../docs/research/ATTENTION_STRUCTURE_RECONSTRUCTION_ACROSS_CONTEXTS_AND_SYSTEMS_2026_09_17.md).
It separates factual/project-state recall from reconstruction of active research focus,
open/downweighted/rejected branches, priority relations and next-step structure.

The repository-defined Co-Constructed Thinking Space (CCTS) structural contract is
implemented in `src/aion_human_ai_longitudinal/co_constructed_thinking_space.py`
and grounded by
[`../../docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](../../docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md).
The grounding-admission extension is documented in
[`../../docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](../../docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md).

Status: `IMPLEMENTED_EXPERIMENTAL_HARNESS / SCIENTIFIC_HOLD`

This package turns the controlled study designs in the 2026-09-11 longitudinal
grounding and interaction-knowledge-density notes into typed, fail-closed
engineering records. It records conditions, exact run configuration, metric
evidence and preregistered contrasts. It does not call a model, store a private
transcript, infer product-internal mechanisms or decide whether a hypothesis is
true.

The metacognitive-policy extension adds a structural discrimination contract for
externalized learner rules versus content-matched non-policy exposure, separates
policy-available behavior from policy-withheld held-out transfer, and includes a
low-stakes negative control for overprocessing. Its deterministic fixture does not
establish learning, internalization, dependence, or causal effect.

The task-selection extension represents anonymous between-unit yoked pairs. Each
`FREE_SELECTION` unit is paired with one `YOKED_ASSIGNED_EXPOSURE` unit that must
receive the exact task-domain, task-family and exposure-payload sequence realized
by its paired free-selection unit. Equal free-selection outcomes remain valid null
or support-reducing results rather than design failures, and zero exposure in an
individual domain is representable. One exposure unit is one bounded synthetic task
episode; event counts do not imply equal duration, difficulty, cognitive intensity
or learning opportunity. Bound artifacts recompute SHA-256 from their supplied UTF-8
content, but content/digest integrity is not semantic or scientific validation. The
temporal-provenance layer is specification-only and does not estimate causal effects.

The post-merge task-selection hardening adds an event-level choice-opportunity trace
for every free-selection unit. Each opportunity contains at least two content-bound,
distinct alternatives and the realized choice must be a member of that set. It also
separates execution identity from execution-record content so independently identified
executions may serialize identically, and it requires both within-family/new-payload
and cross-family/same-domain held-out records. These are structural controls only:
choice-set binding does not prove Human autonomy, and cross-family held-out structure
does not establish transfer or learning.

The attention-structure reconstruction extension adds a version-bound research-question
manifest with typed status and relation semantics, exact focus/next-step sets, canonical
manifest hashing, structurally distinct within-context/cross-context/cross-system study
conditions, and deterministic metrics for node/content/status/relation fidelity,
focus/next-step/open-question preservation, unsupported additions, priority inversions
and reinflation of previously downweighted/rejected/resolved branches. These are
structural QA metrics only. They do not establish an empirical cross-context effect,
cross-system portability, a product memory mechanism, AI-internal attention continuity,
identity continuity or subjectivity.

The CCTS extension formalizes a repository-local relational construct rather than
claiming a new external scientific taxonomy. Its core profile requires an explicit
problem representation, a typed grounding checkpoint bound to known Human and AI
contributions and the same problem representation, reciprocal Human<->AI `REVISES`
or `CHALLENGES` paths, provenance, claim-boundary, authority-policy and
rejected-branch bindings. CCTS admission requires the grounding checkpoint to be
`SUFFICIENT_FOR_CURRENT_PURPOSE` with no unresolved mismatch. `CLARIFIES` edges may
mediate the connected revision graph but do not, by themselves, satisfy the
substantive reciprocity requirement.

The grounding checkpoint is structural declaration-level evidence only. It records
that the manifest explicitly represents adequate alignment for the current purpose;
it does not inspect natural-language meaning, prove semantic equivalence, establish
mutual belief, establish identical internal representations, or prove that an AI
possesses an internal state of understanding.

The stronger longitudinal repository profile additionally requires external-evidence,
repository-artifact and implementation-evidence roles, plus persistent-artifact and
re-entry bindings. Each longitudinal digest must resolve to the payload digest of a
declared `REPOSITORY_ARTIFACT` contribution; digest syntax or presence alone is not
referential integrity. Structural conformance cannot be promoted into evidence of
shared mind, consciousness, AI subjectivity, distributed cognition as an empirical
mechanism, or epistemic co-agency as a measured effect.

Privacy and ontology booleans in the CCTS manifest are declaration-level fail-closed
controls. The structural harness rejects a manifest that declares private material,
Human identity, shared mind, shared consciousness or structure-derived AI
subjectivity. It does not inspect raw payload content, because raw payloads are not
part of this synthetic contract.

The harness is a study-design surface, not a canonical evidence schema. PR #91 is
now on `main` and provides the repository's provenance-to-claim quality gate. This
harness remains separate: any conversion of its study records into that claim
admission surface requires a separately reviewed mapping rather than implicit
promotion.

All condition fields require exact runtime enum instances; raw strings fail
closed. Contrasts hold evaluator identity/source and held-out status fixed.
`task_domain` and `ai_support` remain recordable labels but cannot be declared as
v0.1.0 manipulations because no exact underlying task/support binding is present.
Metric values accept exact `int` or `float` runtime values only; booleans, strings,
other types and non-finite numbers fail closed.

Key boundaries:

```text
HARNESS_PASS != HYPOTHESIS_CONFIRMED
METRIC_DELTA != CAUSAL_IDENTIFICATION
MEMORY_RETRIEVAL != LEARNING
LONGITUDINAL_ADAPTATION != SUBJECTIVITY
POLICY_SWITCHING_BEHAVIOR != INTERNAL_POLICY_MODULE_PROVEN
EXTERNALIZED_RULE != INTERNALIZED_SKILL
POLICY_WITHHELD_FIXTURE_PASS != INDEPENDENT_LEARNING
FREE_SELECTION_NULL != DESIGN_FAILURE
YOKED_EXPOSURE_MATCH != CAUSAL_IDENTIFICATION_COMPLETE
TASK_EPISODE_COUNT != EQUAL_EXPOSURE_INTENSITY
HASH_MATCH != SCIENTIFIC_SEMANTICS_VALIDATED
TEMPORAL_ORDER != CAUSALITY
REALIZED_CHOICE_TRACE_PRESENT != CHOICE_OPPORTUNITY_OPERATIONALIZED
CHOICE_OPPORTUNITY_SET_BOUND != HUMAN_AUTONOMY_ESTABLISHED
SEPARATE_EXECUTION_IDENTITY != EXECUTION_CONTENT_MUST_DIFFER
CROSS_FAMILY_HELD_OUT_TASK != DOMAIN_GENERALIZATION_ESTABLISHED
ATTENTION_STRUCTURE != FACTUAL_MEMORY
ATTENTION_STRUCTURE_RECONSTRUCTION != ATTENTION_CONTINUITY
CROSS_CONTEXT_RECONSTRUCTION != PRODUCT_MEMORY_MECHANISM
CROSS_SYSTEM_RECONSTRUCTION != AI_IDENTITY_CONTINUITY
CCTS_STRUCTURAL_CONFORMANCE != EMPIRICAL_MECHANISM
GROUNDING_CHECKPOINT_PRESENT != MUTUAL_UNDERSTANDING_PROVEN
GROUNDING_CHECKPOINT_PRESENT != AI_UNDERSTANDING_PROVEN
GROUNDING_PRESENT_AT_ADMISSION != TEMPORAL_ORDER_PROVEN
PROBLEM_REPRESENTATION_DIGEST_PRESENT != PROBLEM_REPRESENTATION_GROUNDED
JOINT_PROBLEM_REPRESENTATION != SHARED_MIND
RECIPROCAL_REVISION != EPISTEMIC_CO_AGENCY_ESTABLISHED
VALID_DIGEST != REFERENTIAL_INTEGRITY
DECLARED_PRIVACY_FLAG_REJECTION != CONTENT_INSPECTION
HARNESS_RECORD != PR91_CLAIM_ADMISSION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The fixture in `fixtures/minimal_contrast.json` is synthetic protocol data. It
contains no raw conversation and no third-party identity.
