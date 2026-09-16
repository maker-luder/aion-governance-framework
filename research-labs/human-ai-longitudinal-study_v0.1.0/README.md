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

The repository-defined Co-Constructed Thinking Space (CCTS) structural contract is
implemented in `src/aion_human_ai_longitudinal/co_constructed_thinking_space.py`
and grounded by
[`../../docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](../../docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md).

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

The CCTS extension formalizes a repository-local relational construct rather than
claiming a new external scientific taxonomy. Its core profile requires an explicit
problem representation, Human and AI contribution roles, reciprocal Human<->AI
`REVISES` or `CHALLENGES` paths, provenance, claim-boundary, authority-policy and
rejected-branch bindings. `CLARIFIES` edges may mediate the connected revision graph
but do not, by themselves, satisfy the substantive reciprocity requirement. Its
stronger longitudinal repository profile additionally requires external-evidence,
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
CCTS_STRUCTURAL_CONFORMANCE != EMPIRICAL_MECHANISM
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
