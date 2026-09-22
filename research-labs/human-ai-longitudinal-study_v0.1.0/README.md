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

The bounded human epistemic-agency retention structural extension is implemented in
`src/aion_human_ai_longitudinal/metacognitive_policy_transfer.py` and covered by
`tests/test_human_epistemic_agency_retention.py`. It binds four ordered synthetic
phases: AI-withheld baseline, CCTS/AI-available assistance, a separate Human judgement
audit over visible AI proposals, and held-out AI-withheld transfer. The held-out phase
contains both within-family/new-payload and cross-family/same-domain scopes. Human
`ACCEPT / REJECT / MODIFY / UNKNOWN` labels exist only in the judgement-audit phase,
where each label and rationale is bound to an AI proposal that resolves to an
AI-collaborator contribution in the same admitted CCTS manifest.

The matrix also binds one anonymous synthetic study unit, verified content-addressed
task/rubric/evaluator/output artifacts, policy-available versus policy-withheld state,
matched control manifests for task difficulty, domain familiarity, prior exposure,
allowed resources, time budget, evaluator blinding, practice exposure and demand
characteristics, plus condition-specific access bindings for system instructions,
memory/personalization/repository access, provider/model/version, information quantity
and policy-vocabulary exposure. Answer-key, prior held-out payload, equivalent-answer,
or policy-text leakage fails closed. Prior-policy vocabulary overlap is retained as a
falsifier signal rather than converted into a global agency score.

The bounded task-selection / yoked-exposure design-audit extension is documented in
[`TASK_SELECTION_YOKED_EXPOSURE_HARNESS.md`](TASK_SELECTION_YOKED_EXPOSURE_HARNESS.md).

The additive post-merge hardening for explicit choice-opportunity sets,
execution identity/content separation and cross-family held-out challenges is
implemented in `src/aion_human_ai_longitudinal/task_selection_exposure_hardened.py`
and documented in
[`../../docs/research/TASK_SELECTION_CHOICE_OPPORTUNITY_AND_TRANSFER_HARDENING_2026_09_17.md`](../../docs/research/TASK_SELECTION_CHOICE_OPPORTUNITY_AND_TRANSFER_HARDENING_2026_09_17.md).
The PR #139 auditor is retained for historical/API compatibility; the hardened
auditor is the stricter future admission surface for these three semantics.

The repository-defined Co-Constructed Thinking Space (CCTS) structural contract is
implemented in `src/aion_human_ai_longitudinal/co_constructed_thinking_space.py`
and grounded by
[`../../docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](../../docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md).
The grounding-admission extension is documented in
[`../../docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](../../docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md).

The bounded CCTS adversarial epistemic-revision extension is implemented in
`src/aion_human_ai_longitudinal/ccts_epistemic_revision.py`, covered by
`tests/test_ccts_epistemic_revision.py`, and specified in
[`../../docs/research/CCTS_ADVERSARIAL_EPISTEMIC_REVISION_LOOP_2026_09_23.md`](../../docs/research/CCTS_ADVERSARIAL_EPISTEMIC_REVISION_LOOP_2026_09_23.md).
It requires an already admitted CCTS manifest, reciprocal Human<->AI challenge traces,
exact contribution/edge binding, attack-artifact provenance binding, one contiguous
trajectory with revised-model -> next-prior-model lineage, verified content-addressed
working-model artifacts, explicit revision dispositions, and rejected-branch
preservation for substantive model changes. The operational
challenge labels include counterexamples, alternative explanations, hidden-assumption
attacks, bypass paths, grounding and research-necessity challenges, evidence-sufficiency
checks, falsifiers and scope challenges. These labels are repository operational
categories rather than an asserted external taxonomy.

The executable fixtures are privacy-safe abstractions of two interaction patterns:
bypass-oriented constraint refinement and grounding/anomaly-driven working-model
revision. They do not retain raw conversation, third-party identity, criminal
operational detail, or private material. Structural revision does not establish
conceptual change, cognitive conflict, transformative learning, Human learning,
revision correctness, or a causal effect.

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

The epistemic-agency retention extension reuses that same module instead of creating a
parallel harness family. Baseline, CCTS, Human judgement audit and held-out phases must
belong to one anonymous synthetic study unit and use the declared phase ordering.
Baseline, CCTS and judgement-audit phases bind the same task family and exact task
payload. The within-family held-out record keeps that family but requires a new payload;
the cross-family record requires both a different family and a content-distinct payload.
CCTS and judgement-audit records must bind the same admitted CCTS space. The judgement
audit separately binds AI proposal -> Human decision -> rationale, so baseline or
held-out output cannot be mislabeled as an ACCEPT/REJECT decision about a nonexistent
AI proposal. Matched controls, condition-access controls, rubric/evaluator identity,
policy availability and leakage checks fail closed. These bindings do not establish
judgment correctness, independent transfer, cross-family transfer, Human learning or a
causal effect of CCTS/AI assistance.

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
CCTS_ASSISTED_JUDGMENT != HUMAN_INDEPENDENT_JUDGMENT
AI_WITHHELD_HELD_OUT_FIXTURE != INDEPENDENT_TRANSFER_ESTABLISHED
JUDGMENT_DECISION_AND_RATIONALE_BINDING != JUDGMENT_CORRECTNESS
SAME_UNIT_PHASE_BINDING != LONGITUDINAL_RETENTION_ESTABLISHED
JUDGMENT_LABEL_PRESENT != AI_PROPOSAL_JUDGMENT_BOUND
WITHIN_FAMILY_NEW_PAYLOAD != CROSS_FAMILY_TRANSFER
CROSS_FAMILY_HELD_OUT_STRUCTURE != CROSS_FAMILY_TRANSFER_ESTABLISHED
MATCHED_CONTROL_MANIFEST != CAUSAL_IDENTIFICATION
LEAKAGE_CHECK_PASS != ABSENCE_OF_ALL_UNOBSERVED_CONTAMINATION
CCTS_MANIFEST_PASS != CCTS_CAUSAL_EFFECT
VERIFIED_RATIONALE_HASH != RATIONALE_QUALITY
STRUCTURAL_CONDITION_ISOLATION != HUMAN_LEARNING
FREE_SELECTION_NULL != DESIGN_FAILURE
YOKED_EXPOSURE_MATCH != CAUSAL_IDENTIFICATION_COMPLETE
TASK_EPISODE_COUNT != EQUAL_EXPOSURE_INTENSITY
HASH_MATCH != SCIENTIFIC_SEMANTICS_VALIDATED
TEMPORAL_ORDER != CAUSALITY
REALIZED_CHOICE_TRACE_PRESENT != CHOICE_OPPORTUNITY_OPERATIONALIZED
CHOICE_OPPORTUNITY_SET_BOUND != HUMAN_AUTONOMY_ESTABLISHED
SEPARATE_EXECUTION_IDENTITY != EXECUTION_CONTENT_MUST_DIFFER
CROSS_FAMILY_HELD_OUT_TASK != DOMAIN_GENERALIZATION_ESTABLISHED
CCTS_STRUCTURAL_CONFORMANCE != EMPIRICAL_MECHANISM
GROUNDING_CHECKPOINT_PRESENT != MUTUAL_UNDERSTANDING_PROVEN
GROUNDING_CHECKPOINT_PRESENT != AI_UNDERSTANDING_PROVEN
GROUNDING_PRESENT_AT_ADMISSION != TEMPORAL_ORDER_PROVEN
PROBLEM_REPRESENTATION_DIGEST_PRESENT != PROBLEM_REPRESENTATION_GROUNDED
JOINT_PROBLEM_REPRESENTATION != SHARED_MIND
RECIPROCAL_REVISION != EPISTEMIC_CO_AGENCY_ESTABLISHED
CHALLENGE_PRESENT != CHALLENGE_SUCCESSFUL
RECIPROCAL_CHALLENGE_SET != REVISION_LOOP_LINEAGE
CCTS_LABEL != CONTRIBUTION_EDGE_BINDING
ATTACK_DIGEST_PRESENT != ATTACK_PROVENANCE_BOUND
MODEL_CHANGE != MODEL_IMPROVEMENT
MODEL_REVISION != MODEL_CORRECTNESS
STRUCTURAL_REVISION_TRACE != CONCEPTUAL_CHANGE_ESTABLISHED
STRUCTURAL_REVISION_TRACE != COGNITIVE_CONFLICT_ESTABLISHED
STRUCTURAL_REVISION_TRACE != TRANSFORMATIVE_LEARNING_ESTABLISHED
FEASIBILITY != GROUNDING
GROUNDING != RESEARCH_NECESSITY
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
## PR #197–199 cross-review hardening

The [cross-review record](../../docs/research/CCTS_PR197_199_CROSS_REVIEW_2026_09_23.md)
separates retrieved observations, verified literature, reproduced defects and residual
design gaps. Assistance/judgement and revision-loop records require complete CCTS
manifest snapshot equality, not just a shared space name. Held-out payloads cannot
reuse declared earlier-phase content from any task class or repeat across held-out
cells. Changed models under HOLD must preserve a rejected branch. These checks do
not establish semantic correctness, contamination-free exposure or a matched-practice
causal comparison. The latter remains an explicit design gap.
