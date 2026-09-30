# CCTS / Human–AI learning applicability boundary hypothesis — 2026-09-30

Status: `HYPOTHESIS_GENERATING / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`

Canonical effect: `NONE`

Implementation change: `NONE`

Experiment result: `NONE`

Deployment: `FALSE`

## 1. Purpose

This note records a bounded research hypothesis about when the repository-defined
Co-Constructed Thinking Space (CCTS) construct and Human–AI learning claims are
applicable to an interaction.

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

The operational distinctions below are a ChatGPT Teacher formalization produced
after comparison with the current repository definition and adjacent literature.

```text
HUMAN_ORIGIN
= GLOBAL_VALUE_FUNCTION_MISMATCH_SHOULD_NOT_BE_TREATED_AS_AUTOMATIC_FAILURE
+ REQUEST_TO_TEST_WHETHER_THIS_BOUNDARY_IS_RESEARCH_RELEVANT

CHATGPT_TEACHER_FORMALIZATION
= GLOBAL_VALUE_MISMATCH
  != TASK_OR_PURPOSE_MISMATCH
  != GROUNDING_FAILURE
+ CCTS_APPLICABILITY_BOUNDARY_HYPOTHESIS
+ HUMAN_AI_LEARNING_APPLICABILITY_HYPOTHESIS

EXTERNAL_EXACT_CCTS_VALIDATION = NOT_ESTABLISHED
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
```

No private social names, personal identifiers, or source-event details are
required for the hypothesis. The examples in this note are synthetic.

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

The current repository does **not** yet explicitly define an independent
`CCTS_APPLICABILITY` construct or a pre-admission rule stating when CCTS should
not be evaluated at all.

## 4. Candidate distinctions

Three states must remain separable.

### 4.1 Global value mismatch

```text
GLOBAL_VALUE_MISMATCH
= participants differ in broad preferences, priorities, worldview,
  social style, or overall utility/value function
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

This may make CCTS evaluation inappropriate or may require repair before a CCTS
claim is meaningful.

The hypothesis does not require identical motives. For example, a Human may
seek to learn while an AI collaborator seeks to scaffold, challenge and review.
Those motives differ while remaining task-compatible.

```text
IDENTICAL_PURPOSE = NOT_REQUIRED
TASK_RELEVANT_COMPATIBILITY = CANDIDATE_PRECONDITION
```

### 4.3 Grounding failure

```text
GROUNDING_FAILURE
= participants purport to engage the same bounded problem,
  but their operative interpretations are materially misaligned
  and the mismatch remains unresolved
```

This state is already partly represented by the current CCTS grounding
checkpoint.

```text
TASK_OR_PURPOSE_MISMATCH != GROUNDING_FAILURE
GLOBAL_VALUE_MISMATCH != GROUNDING_FAILURE
```

## 5. CCTS applicability boundary hypothesis

Candidate hypothesis:

```text
CCTS_APPLICABILITY_HYPOTHESIS

GLOBAL_VALUE_ALIGNMENT = NOT_REQUIRED
IDENTICAL_PURPOSE = NOT_REQUIRED

BUT

BOUNDED_TASK_RELEVANCE
+ SUFFICIENT_PROBLEM_ALIGNMENT
+ GROUNDING_ADEQUATE_FOR_CURRENT_PURPOSE

= CANDIDATE_APPLICABILITY_PRECONDITIONS
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

This is a candidate boundary rule only. It is not canonical.

## 6. Human–AI learning applicability hypothesis

A separate but related hypothesis applies to learning claims.

```text
HUMAN_AI_LEARNING_APPLICABILITY_HYPOTHESIS

BEFORE_INTERPRETING_INTERACTION_AS_LEARNING_EVIDENCE:

BOUNDED_LEARNING_RELEVANT_TASK
+ EXPLICIT_OR_RECOVERABLE_LEARNING_TARGET
+ SUFFICIENT_GROUNDING_ABOUT_WHAT_IS_BEING_LEARNED
= CANDIDATE_PRECONDITIONS
```

The distinction matters because successful task completion is not equivalent to
Human learning.

```text
TASK_SUCCESS != HUMAN_LEARNING
JOINT_PERFORMANCE_GAIN != INDEPENDENT_HUMAN_GAIN
AI_SUPPORT != HUMAN_LEARNING
```

A Human may seek only task completion while a researcher incorrectly interprets
the interaction as a learning episode. Low retention or transfer in that case
would not, by itself, show that CCTS failed to support learning.

```text
HUMAN_OBJECTIVE = TASK_COMPLETION
RESEARCH_INTERPRETATION = LEARNING_EPISODE

=> POSSIBLE_OBJECTIVE_MISMATCH
=> POSSIBLE_DESIGN_CONFOUND
```

This candidate boundary is additive to, not a substitute for, the repository's
existing requirements concerning independent Human assessment, retention,
transfer, testing exposure, prior knowledge and realized interaction traces.

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

CCTS_APPLICABILITY = PLAUSIBLE
```

### Case B — ordinary social interaction

Participant H seeks analytical resolution. Participant P is engaged only in
casual social exchange. No joint epistemic task has been established.

```text
CCTS_APPLICABILITY = NOT_YET_ESTABLISHED
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

The next review should prefer the smallest change that preserves the distinction.

## 9. External adjacent literature

The hypothesis is adjacent to, but not validated by, several established
literatures:

1. Clark & Brennan (1991), *Grounding in Communication* — grounding is
   coordinated toward a criterion sufficient for the current purpose.
2. Roschelle & Teasley (1995), *The Construction of Shared Knowledge in
   Collaborative Problem Solving*, DOI: `10.1007/978-3-642-85098-1_5` —
   collaborative problem solving is analyzed through a Joint Problem Space.
3. Järvelä, Nguyen & Hadwin (2023), *Human and artificial intelligence
   collaboration for socially shared regulation in learning*, DOI:
   `10.1111/bjet.13325` — Human–AI collaboration is situated within regulation
   of learning rather than treated as equivalent to learning by default.
4. Samuel (2026), *Learning with machines: Toward a theory of epistemic
   co-agency*, DOI: `10.1016/j.caeai.2026.100573` — adjacent theory emphasizes
   dialectical Human engagement and epistemic responsibility.
5. Shaikh, Mozannar, Bansal et al. (2025), *Navigating Rifts in Human-LLM
   Grounding: Study and Benchmark*, DOI: `10.18653/v1/2025.acl-long.1016` —
   Human–LLM grounding failures are empirically studied as interaction
   breakdown risks.

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

## 11. Proposed review questions

A later independent review should answer:

```text
Q1
Does current grounding admission already subsume this entire hypothesis?

Q2
Is "applicability" a useful precondition,
or only a documentation-level scope reminder?

Q3
Can task relevance and learning relevance be operationalized
using observable interaction artifacts rather than inferred motives?

Q4
Would adding an applicability gate improve false-positive control,
or merely duplicate existing admission checks?

Q5
Should CCTS applicability and Human–AI learning applicability remain
separate hypotheses even if they share grounding requirements?
```

Until those questions survive independent review:

```text
CCTS_APPLICABILITY_BOUNDARY = HYPOTHESIS
HUMAN_AI_LEARNING_APPLICABILITY = HYPOTHESIS
CANONICAL_RULE = NO
IMPLEMENTATION = NO
EMPIRICAL_EFFECT = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```

## 12. Repository relationship and authority boundary

Related current records include:

- `CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`
- `CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`
- `CCTS_LEARNING_CONTRAST_STRENGTHENING_2026-09-28.md`
- `INTERACTION_ROUTING_DRIFT_OBSERVATION_2026_09_30.md`

This note does not supersede them.

```text
DOCUMENTATION_EXISTS != CANONICAL_ADMISSION_CHANGE
HYPOTHESIS_RECORDED != HYPOTHESIS_CONFIRMED
REPOSITORY_RECORD != SCIENTIFIC_VALIDATION
CI_PASS != SCIENTIFIC_VALIDATION
AI_REVIEW != HUMAN_OWNER_APPROVAL
MERGE_TO_MAIN = NO
```
