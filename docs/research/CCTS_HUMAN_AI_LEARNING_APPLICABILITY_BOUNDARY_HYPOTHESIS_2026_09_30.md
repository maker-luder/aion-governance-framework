# CCTS / Human–AI learning applicability boundary hypothesis — 2026-09-30

Status: `ADVERSARIAL_REVIEWED / SCOPE_DISTINCTION_ONLY / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`

Canonical effect: `NONE`

Implementation change: `NONE`

Experiment result: `NONE`

Deployment: `FALSE`

## 1. Purpose

This note records an initiating boundary hypothesis and its adversarial review.
The surviving distinction is a scope and study-design caution, not an
independent CCTS or Human–AI learning construct.

It does **not** modify the canonical CCTS admission contract. It does **not** add
an empirical learning result. It does **not** claim that value disagreement,
social incompatibility, or ordinary conversational differences are CCTS failures.

The immediate research question is:

> Before asking whether an interaction satisfies CCTS, or whether it demonstrates
> Human–AI learning, should the project first establish that the interaction is
> task-relevant to the construct being evaluated and sufficiently grounded for
> the current purpose?

## 2. Provenance

The initiating Human observation was that one participant's overall value
function should not automatically be used as the standard for evaluating other
participants or social contexts. A mismatch in overall values or preferred
interaction style may justify disengagement from a context without establishing
that the other participants are wrong, that grounding failed, or that a CCTS
attempt failed.

The operational distinctions below originated as a ChatGPT Teacher
formalization. Section 11 records an independent review of that formalization
against repository controls and adjacent literature. Provenance does not
establish correctness.

```text
HUMAN_ORIGIN
= GLOBAL_VALUE_FUNCTION_MISMATCH_SHOULD_NOT_BE_TREATED_AS_AUTOMATIC_FAILURE
+ REQUEST_TO_TEST_WHETHER_THIS_BOUNDARY_IS_RESEARCH_RELEVANT

CHATGPT_TEACHER_FORMALIZATION
= GLOBAL_VALUE_MISMATCH
  != TASK_OR_PURPOSE_MISMATCH
  != GROUNDING_FAILURE
+ CCTS_APPLICABILITY_BOUNDARY_HYPOTHESIS (ORIGINAL CANDIDATE)
+ HUMAN_AI_LEARNING_APPLICABILITY_HYPOTHESIS (ORIGINAL CANDIDATE)

CHATGPT_WORK_REVIEW
= TEST_EXISTING_CONTROLS_AS_NULL_HYPOTHESIS
+ IDENTIFY_DUPLICATION_AND_COUNTEREXAMPLES
+ DOWNGRADE_TO_SCOPE_AND_STUDY_DESIGN_CAUTION

ACTOR_PROVENANCE_BOUNDARY
= CHATGPT_TEACHER != CHATGPT_WORK != CODEX
+ GENERIC_CHATGPT != SPECIFIC_REVIEW_ACTOR
+ CONTRIBUTION_ORIGIN != CONTRIBUTOR_ACTOR
+ SOURCE != AUTHORSHIP != IMPLEMENTATION != REVIEW != APPROVAL
+ ACTOR_LABEL != VERIFIED_MODEL_IDENTITY

REVIEW_ACTOR = CHATGPT_WORK
CODEX_REVIEW_OF_THIS_PR = NOT_PERFORMED
CHATGPT_TEACHER_ROLE = ORIGINAL_FORMALIZATION_AND_SUBSEQUENT_PROVENANCE_REVIEW
CODEX_ROLE = NONE_IN_THIS_PR_REVIEW_SEQUENCE

REPOSITORY_STATE = CURRENT_MAIN_DEFINITIONS_AND_DESIGN_RECORDS_REVIEWED
IMPLEMENTATION_EVIDENCE = DECLARATION_AND_PROTOCOL_CHECKS_ONLY
EXTERNAL_SOURCE = ADJACENT_PRIMARY_LITERATURE (SECTION 9)

EXTERNAL_EXACT_CCTS_VALIDATION = NOT_ESTABLISHED
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
```

No private social names, personal identifiers, or source-event details are
required for the hypothesis. The examples in this note are synthetic.

Actor names in this record are role-level provenance labels for the actual
interaction surface used in the recorded step. They must not be collapsed merely
because the surfaces belong to the broader ChatGPT/OpenAI ecosystem. In
particular, a review performed through ChatGPT Work must not be relabeled as
Codex, and a ChatGPT Teacher formalization must not be relabeled as Work or
Codex. If the specific actor cannot be reconstructed from evidence, the record
must use `SOURCE_UNVERIFIED` rather than substitute another actor label.

```text
CHATGPT_TEACHER != CHATGPT_WORK
CHATGPT_TEACHER != CODEX
CHATGPT_WORK != CODEX

UNKNOWN_SPECIFIC_ACTOR
=> SOURCE_UNVERIFIED

DO_NOT_INFER_ACTOR_FROM
= PRODUCT_FAMILY
+ SIMILAR_WRITING_STYLE
+ SHARED_ACCOUNT
+ GIT_COMMITTER
+ AI_FORMALIZATION_LABEL
```

## 3. Existing repository constraints

The current CCTS formalization already requires a bounded problem
representation, Human and AI contribution roles, substantive reciprocal
revision, source-role provenance, claim boundaries, authority separation and
rejected-branch preservation.

The grounding extension further requires grounding that is sufficient for the
current purpose and explicitly rejects the inference that grounding implies
identical internal representations or mutual belief.

Therefore the current repository already supports:

```text
GLOBAL_VALUE_ALIGNMENT != CCTS_REQUIREMENT
IDENTICAL_INTERNAL_REPRESENTATION != CCTS_REQUIREMENT
MUTUAL_AGREEMENT != RECIPROCAL_REVISION
```

The current repository does **not** explicitly define an independent
`CCTS_APPLICABILITY` construct. That absence is not evidence that one is
needed: bounded problem representation already establishes the CCTS scope,
while the grounding checkpoint is an admission control. The executable checks
validate declared bindings and edges, not the semantic relevance of a task or
the participants' private purposes.

## 4. Candidate distinctions

These are different questions, but they can co-occur; they are not a mutually
exclusive diagnostic taxonomy. None can be inferred from a global value label.

### 4.1 Global value mismatch

```text
GLOBAL_VALUE_MISMATCH
= a reported broad preference, priority, worldview, or social-style difference
```

This alone does not establish failure of collaboration, grounding, CCTS, or
learning.

```text
GLOBAL_VALUE_MISMATCH != CCTS_FAILURE
GLOBAL_VALUE_MISMATCH != HUMAN_AI_LEARNING_FAILURE
```

### 4.2 Task- or purpose-relevant mismatch

```text
TASK_OR_PURPOSE_MISMATCH
= participants are not sufficiently aligned on what bounded task,
  problem, or interaction purpose is currently being pursued
```

An observable absence of a bounded shared problem means the existing CCTS
profile has not been shown to apply. A disagreement within a stated problem
may instead call for grounding repair. Neither inference requires a new gate.

The hypothesis does not require identical motives. For example, a Human may
seek to learn while an AI collaborator seeks to scaffold, challenge and review.
Those motives differ while remaining task-compatible.

```text
IDENTICAL_PRIVATE_MOTIVE = NOT_REQUIRED
BOUNDED_PROBLEM_AND_CONTRIBUTIONS = EXISTING_SCOPE_EVIDENCE
```

### 4.3 Grounding failure

```text
GROUNDING_FAILURE
= participants purport to engage the same bounded problem,
  but their operative interpretations are materially misaligned
  and the mismatch remains unresolved
```

This state is represented only to the extent that participants declare and
record a grounding checkpoint; a passing structural check does not prove
actual semantic alignment.

```text
TASK_OR_PURPOSE_MISMATCH != GROUNDING_FAILURE
GLOBAL_VALUE_MISMATCH != GROUNDING_FAILURE
```

## 5. CCTS scope distinction after adversarial review

Original candidate, retained as provenance rather than adopted as a rule:

```text
CCTS_APPLICABILITY_HYPOTHESIS

GLOBAL_VALUE_ALIGNMENT = NOT_REQUIRED
IDENTICAL_PURPOSE = NOT_REQUIRED

BUT

BOUNDED_TASK_RELEVANCE
+ SUFFICIENT_PROBLEM_ALIGNMENT
+ GROUNDING_ADEQUATE_FOR_CURRENT_PURPOSE

= PROPOSED_APPLICABILITY_PRECONDITIONS (NOT ADOPTED)
```

Interpretation:

Before treating an interaction as a CCTS candidate, the project may need to
establish that the interaction contains a bounded task or problem to which CCTS
is relevant. Ordinary social interaction, parallel presence, casual
conversation, or relationship maintenance should not be labeled a failed CCTS
merely because they do not satisfy an epistemic-collaboration construct.

```text
INTERACTION_EXISTS != CCTS_APPLICABLE
SOCIAL_RELATIONSHIP != EPISTEMIC_CO_CONSTRUCTION_TASK
NO_SHARED_EPISTEMIC_TASK != FAILED_CCTS
```

The existing bounded-problem requirement supplies the scope distinction, and
the existing grounding checkpoint handles recorded mismatch for CCTS
admission. `SUFFICIENT_PROBLEM_ALIGNMENT` duplicates those controls unless it
has an independently observable definition, which this note does not provide.
An interaction without a common epistemic task need not be labeled a *failed*
CCTS attempt; equally, a missing CCTS manifest cannot prove that no joint
epistemic task occurred. The safe disposition is `CCTS_CLAIM_NOT_ESTABLISHED`,
with scope checked against artifacts, not a new applicability gate.

```text
INDEPENDENT_CCTS_APPLICABILITY_CONSTRUCT = NOT_JUSTIFIED
NEW_CCTS_ADMISSION_RULE = NO
```

## 6. Human–AI learning interpretation caution

A separate inference concerns learning claims. The original candidate was:

```text
HUMAN_AI_LEARNING_APPLICABILITY_HYPOTHESIS

BEFORE_INTERPRETING_INTERACTION_AS_LEARNING_EVIDENCE:

BOUNDED_LEARNING_RELEVANT_TASK
+ EXPLICIT_OR_RECOVERABLE_LEARNING_TARGET
+ SUFFICIENT_GROUNDING_ABOUT_WHAT_IS_BEING_LEARNED
= PROPOSED_PRECONDITIONS (NOT ADOPTED)
```

The distinction matters because successful task completion is not equivalent to
Human learning.

```text
TASK_SUCCESS != HUMAN_LEARNING
JOINT_PERFORMANCE_GAIN != INDEPENDENT_HUMAN_GAIN
AI_SUPPORT != HUMAN_LEARNING
```

A Human may seek only task completion while a researcher interprets the
interaction as a learning episode. That mismatch is an ordinary protocol and
task-framing issue. A participant may also learn incidentally without an
explicit learning objective, so the proposed preconditions are not necessary
conditions for learning. An artifact's success or a participant's stated goal
alone cannot establish or exclude independent Human learning.

```text
HUMAN_OBJECTIVE = TASK_COMPLETION
RESEARCH_INTERPRETATION = LEARNING_EPISODE

=> POSSIBLE_OBJECTIVE_MISMATCH
=> POSSIBLE_DESIGN_CONFOUND (TO RECORD AND CONTROL, NOT A NEW CONSTRUCT)
```

The existing study design already specifies independent Human assessment,
retention, transfer, task matching, exposure, prior knowledge and realized
interaction traces. The empirical gate prohibits using CCTS structural status
as HTECR measurement eligibility. A target or framing should be
documented when it changes an estimand or interpretation, but the repository
has no evidence that an additional eligibility gate improves inference.

```text
INDEPENDENT_LEARNING_APPLICABILITY_CONSTRUCT = NOT_JUSTIFIED
CCTS_STATUS_AS_HTECR_MEASUREMENT_GATE = PROHIBITED
LEARNING_EFFECT = NOT_ESTABLISHED
```

## 7. Synthetic boundary cases

### Case A — different values, compatible epistemic task

Participant H and Participant A disagree strongly about preferred methods and
initial hypotheses, but both address the same bounded system-failure question.
They identify evidence, challenge each other and revise the working model.

```text
GLOBAL_VALUE_OR_METHOD_DIFFERENCE = PRESENT
BOUNDED_TASK_RELEVANCE = PRESENT
GROUNDING = ADEQUATE_FOR_CURRENT_PURPOSE
RECIPROCAL_REVISION = POSSIBLE

CCTS_CANDIDACY = PLAUSIBLE; ADMISSION STILL REQUIRES EXISTING CONTROLS
```

### Case B — ordinary social interaction

Participant H seeks analytical resolution. Participant P is engaged only in
casual social exchange. No joint epistemic task has been established.

```text
CCTS_CLAIM = NOT_ESTABLISHED FROM THIS EXCHANGE
CCTS_FAILURE = NOT_INFERRED
```

### Case C — claimed collaboration with grounding mismatch

Human and AI both claim to solve problem X, but the Human's operative
interpretation is A and the AI's operative interpretation is B. The mismatch is
material and unresolved.

```text
GROUNDING = REPAIR_REQUIRED
CCTS_ADMISSION = HOLD
```

### Case D — task completion without established learning objective

Human asks an AI system to produce a correct finished artifact. The artifact is
high quality, but no independent Human judgment, delayed retention or transfer
is assessed.

```text
TASK_SUCCESS = POSSIBLE
HUMAN_LEARNING = NOT_ESTABLISHED
```

### Case E — task disagreement with successful grounding

Human and AI accurately restate each other's distinct objectives and agree to
compare them as the bounded problem. Their disagreement is explicit and
grounded; it need not be a grounding failure or a CCTS exclusion. An initial
`TASK_OR_PURPOSE_MISMATCH` label cannot decide admission.

### Case F — aligned stated objective with a hidden mismatch

Both participants label the task identically and file a sufficient checkpoint,
but later turns reveal incompatible interpretations of the evidence. The
declared checkpoint can pass structural checks while actual grounding remains
in doubt. A proposed task-relevance gate would not detect this case.

### Case G — incidental learning without a declared learning target

A Human requests a finished artifact, then independently explains and applies
the method in a held-out task. A missing explicit learning objective does not
exclude a measurable outcome, while independent assessment still controls the
strength of any learning claim.

## 8. Competing explanations and redundancy risk

The strongest competing interpretation is that no new applicability construct
is needed because the existing bounded-problem and grounding requirements may
already cover the relevant cases.

```text
H1 = DISTINCT_APPLICABILITY_BOUNDARY_ADDS_VALIDITY
H0 = EXISTING_GROUNDING_AND_BOUNDARY_RULES_ARE_SUFFICIENT
```

A second risk is construct proliferation: creating a new named construct for a
distinction that can be expressed more parsimoniously as scope control.

```text
USEFUL_DISTINCTION != NEW_CONSTRUCT_REQUIRED
NEW_LABEL != NEW_MECHANISM
```

The review finds H0 sufficient for the proposed CCTS cases. The learning
contrast is a protocol interpretation caution, not a new construct. The
synthetic cases do not establish incremental validity for either new label.

## 9. External adjacent literature

The hypothesis is adjacent to, but not validated by, several established
literatures:

1. Clark & Brennan (1991), *Grounding in Communication* — conceptual account
   of purpose-relative grounding in human communication, not a CCTS test.
   Primary text: <https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.E.%20_Grounding%20in%20communication_%201991.pdf>.
2. Roschelle & Teasley (1995), *The Construction of Shared Knowledge in
   Collaborative Problem Solving*, DOI: `10.1007/978-3-642-85098-1_5` —
   human collaborative problem solving is analyzed through a Joint Problem
   Space; transfer to Human–AI CCTS is adjacent only.
3. Järvelä, Nguyen & Hadwin (2023), *Human and artificial intelligence
   collaboration for socially shared regulation in learning*, DOI:
   `10.1111/bjet.13325` — theoretical HASRL framing and empirical examples of
   AI affordances, not evidence for this proposed eligibility rule.
4. Samuel (2026), *Learning with machines: Toward a theory of epistemic
   co-agency*, DOI: `10.1016/j.caeai.2026.100573` — adjacent theory emphasizes
   dialectical Human engagement and epistemic responsibility; theoretical,
   not a test of an applicability gate.
5. Shaikh, Mozannar, Bansal et al. (2025), *Navigating Rifts in Human-LLM
   Grounding: Study and Benchmark*, DOI: `10.18653/v1/2025.acl-long.1016` —
   Human–LLM grounding failures are studied in three conversation datasets;
   this supports a grounding concern, not a new CCTS construct.

These sources do not define CCTS and do not establish the present applicability
hypotheses.

```text
EXTERNAL_ADJACENT_SUPPORT = PRESENT
EXTERNAL_EXACT_CCTS_VALIDATION = NOT_ESTABLISHED
PAPER_FOUND != CLAIM_CONFIRMED
```

## 10. Weakening and falsification conditions

The applicability hypothesis should be weakened, merged into an existing rule,
or rejected if any of the following hold:

1. Existing CCTS grounding and bounded-problem requirements fully classify the
   synthetic cases without ambiguity or false-positive admission, making a
   separate applicability boundary redundant.
2. Interactions lacking task-relevant alignment can still reproducibly satisfy
   the current CCTS substantive-revision and grounding semantics without
   introducing interpretive error.
3. Learning-objective mismatch has no material effect on interpretation of
   retention, transfer, independent Human performance or other learning
   outcomes once existing controls are applied.
4. The proposed boundary cannot be operationalized without inferring private
   motives, internal mental states or global values that the study cannot
   observe.
5. The distinction increases labeling complexity without improving construct
   validity, experimental validity or claim calibration.

Null, adverse and redundancy findings remain admissible.

## 11. Adversarial review disposition (2026-09-30)

Review against the current CCTS definition, grounding extension, learning
contrast design, and their executable checks:

```text
Q1/Q2: A bounded problem and substantive reciprocal revision already delimit
the CCTS profile; purpose-relative grounding already controls admission.
No incremental value of a distinct applicability gate is shown.

Q3: A task statement, contribution/revision trace, checkpoint, protocol arm,
predeclared outcome and independent assessment are inspectable artifacts.
Global values, private motives and an unexpressed learning target are not.
Unknown purpose remains unknown rather than being inferred from output quality.

Q4: No observable false-positive reduction beyond existing controls is shown.
Declared checkpoints can still be wrong about semantic alignment.

Q5: CCTS scope and learning outcome interpretation concern different claims,
but neither warrants an independent named construct. Preserve the latter as
a study-design caution, without letting CCTS status gate learning measurement.
```

Review limitations: this is a repository and primary-source conceptual review,
not a prospective adjudicator study. It cannot establish how often existing
controls misclassify real interactions. Citation adjacency does not validate
CCTS; the synthetic cases do not estimate effects.

```text
CCTS_APPLICABILITY_BOUNDARY = REDUNDANT_WITH_EXISTING_SCOPE_AND_GROUNDING
HUMAN_AI_LEARNING_APPLICABILITY = DOWNGRADED_TO_DESIGN_CAUTION
NEW_CONSTRUCT = NO
NEW_EMPIRICAL_GATE = NO
CCTS_CANONICAL_CHANGE = NO
SCIENTIFIC_DISPOSITION = HOLD
```

For the original proposal, the adjudication is:

```text
CANONICAL_RULE = NO
IMPLEMENTATION = NO
EMPIRICAL_EFFECT = NOT_ESTABLISHED
```

## 12. Repository relationship and authority boundary

Related current records include:

- `CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`
- `CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`
- `CCTS_LEARNING_CONTRAST_STRENGTHENING_2026-09-28.md`
- `INTERACTION_ROUTING_DRIFT_OBSERVATION_2026_09_30.md`
- `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/co_constructed_thinking_space.py`
- `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/learning_contrast_design.py`
- `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/empirical_gate.py`

This note does not supersede them.

```text
DOCUMENTATION_EXISTS != CANONICAL_ADMISSION_CHANGE
HYPOTHESIS_RECORDED != HYPOTHESIS_CONFIRMED
REPOSITORY_RECORD != SCIENTIFIC_VALIDATION
CI_PASS != SCIENTIFIC_VALIDATION
AI_REVIEW != HUMAN_OWNER_APPROVAL
MERGE_TO_MAIN = NO
```
