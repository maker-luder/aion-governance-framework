# Human problem-solving habit transfer from longitudinal Human–AI collaboration — 2026-09-13

Status: `RESEARCH_HYPOTHESIS / DOCUMENTATION_ONLY / DRAFT`
Canonical effect: `NONE`
Deployment: `FALSE`
Executable implementation: `NONE`
Future Codex / ChatGPT Work implementation: `DEFERRED / REQUIRES_SEPARATE_FRESH_HUMAN_OWNER_INSTRUCTION`

## 1. Purpose

This note records a new bounded hypothesis extending the repository's work on reciprocal epistemic collaboration, external research memory, recoverability, and longitudinal Human–AI interaction.

The question is not only whether repository artifacts help a Human or AI collaborator **recover** an earlier research method after context discontinuity. A second possibility is that repeated use of explicit collaboration rules may change the Human participant's own problem-solving habits, causing those rules to be transferred into later tasks outside the original research setting.

Such transfer may be beneficial when the new task shares the relevant deep structure. It may also become maladaptive when a familiar QA or governance schema is applied to a task whose objective, failure definition, or evidence requirements are materially different.

```text
RECOVERABILITY_EFFECT
!=
HUMAN_HABIT_TRANSFER_EFFECT

POSITIVE_TRANSFER
!=
NEGATIVE_TRANSFER

FAMILIAR_METHOD
!=
APPROPRIATE_METHOD_FOR_EVERY_TASK
```

## 2. Provenance

### CHATGPT_TEACHER_ORIGINAL_FORMALIZATION

During discussion of repeated QA practice and cross-context tool use, ChatGPT Teacher proposed:

> externalized collaboration rules may do more than improve recoverability; repeated use may also alter the Human participant's problem-solving habits and produce cross-context transfer, which may sometimes be useful and sometimes become negative transfer.

The following labels are therefore Teacher-origin formalization:

- `HUMAN_PROBLEM_SOLVING_HABIT_TRANSFER`;
- `COLLABORATION_RULE_INTERNALIZATION`;
- `POSITIVE_TRANSFER` versus `NEGATIVE_TRANSFER` as a research contrast;
- the idea that repository-governed Human–AI collaboration may itself become part of the Human participant's later problem-selection and tool-selection behavior.

### HUMAN_OWNER_ENDORSEMENT_AND_OBSERVATION

The Human Owner explicitly endorsed the Teacher's formulation and requested that it be recorded in the repository for later review and possible implementation by Codex / ChatGPT Work after agentic capacity is available again.

The Human Owner also supplied a relevant self-observation: after repeated use of QA, provenance, NCR/CAPA, and research-governance procedures in this collaboration, the Human Owner spontaneously attempted to transfer those procedures into a separate creative image-generation workflow. The external creative workflow did not require the full NCR/CAPA process because the task was primarily preference-driven revision rather than a demonstrated nonconformance against a governed specification.

To reduce unnecessary publication of private third-party details, this repository note records the observation only at the task-structure level.

### JOINT_RESEARCH_HYPOTHESIS

After explicit Human Owner endorsement, the following is treated as a joint research hypothesis rather than a Teacher-only suggestion:

> Repeated participation in an explicit, externally documented Human–AI QA / provenance / governance workflow may increase the probability that the Human participant spontaneously applies the same problem-solving schema in later contexts. Transfer may improve performance when deep task structure matches the learned schema, but may create unnecessary process overhead or strong-but-wrong procedure selection when only superficial features match.

This remains a hypothesis, not an established causal result.

```text
ORIGINAL_FORMALIZATION = CHATGPT_TEACHER
HUMAN_OWNER_ENDORSEMENT = EXPLICIT
CURRENT_STATUS = JOINT_RESEARCH_HYPOTHESIS
CAUSAL_EFFECT = NOT_ESTABLISHED
```

## 3. External research crosswalk

The repository hypothesis is adjacent to, but not established by, several existing psychological constructs.

### 3.1 Habit formation and cue–response association

Habit research describes habitual behavior as increasingly automatic responses to recurring cues acquired through repetition in relatively stable contexts. Recent longitudinal work also links habit strength to repetition frequency and context stability.

Relevant sources:

- Bürgler et al. (2026), *What Makes a Habit? Investigating Potential Determinants of Habit Formation*, `Personality and Social Psychology Bulletin`, DOI `10.1177/01461672261440446`, PMID `42053513`.
- Wood and colleagues' cue–response research provides a broader basis for treating repeated practice as capable of strengthening context-response associations; this note does not claim that the repository workflow has already been experimentally shown to form a habit.

Use here:

```text
REPEATED_STABLE_QA_PRACTICE
-> HABIT_LIKE_TRANSFER = PLAUSIBLE

REPOSITORY_USE
-> HABIT_FORMATION = NOT_ESTABLISHED
```

### 3.2 Einstellung / mental-set effects

Bilalić, McLeod, and Gobet showed that familiar problem features can activate a previously successful solution schema that then directs attention and can block discovery of a better alternative, including in expert problem solving.

Source:

- Bilalić, McLeod & Gobet (2008), *Why good thoughts block better ones: the mechanism of the pernicious Einstellung (set) effect*, `Cognition 108(3):652–661`, DOI `10.1016/j.cognition.2008.05.005`, PMID `18565505`.

Use here:

```text
FAMILIAR_SCHEMA_ACTIVATION_CAN_BIAS_PROBLEM_SOLVING = SUPPORTED
THIS_REPOSITORY_CAUSES_EINSTELLUNG = NOT_ESTABLISHED
```

### 3.3 Negative transfer in practiced sequential skills

Woltz, Gardner, and Bell found that extensive practice of familiar multistep cognitive sequences could increase errors when participants encountered similar-looking but different transfer sequences. The authors characterized these as strong-but-wrong sequence applications.

Source:

- Woltz, Gardner & Bell (2000), *Negative transfer errors in sequential cognitive skills: strong-but-wrong sequence application*, `Journal of Experimental Psychology: Learning, Memory, and Cognition 26(3):601–625`, DOI `10.1037//0278-7393.26.3.601`, PMID `10855420`.

Use here:

```text
PRACTICED_PROCEDURE
+ SUPERFICIALLY_SIMILAR_NEW_TASK
-> STRONG_BUT_WRONG_TRANSFER = ESTABLISHED_AS_GENERAL_PHENOMENON

QA_NCR_CAPA_TRANSFER_IN_THIS_COLLABORATION
-> SAME_MECHANISM = NOT_ESTABLISHED
```

### 3.4 Transfer requires recontextualization

Transfer-of-learning literature emphasizes that learners must compare surface and deep task structure and recontextualize abstract principles rather than simply reproduce the original procedure.

Source:

- Rivière et al. (2019), *Debriefing for the Transfer of Learning: The Importance of Context*, `Academic Medicine 94(6):796–803`, DOI `10.1097/ACM.0000000000002612`, PMID `30681450`.

Use here:

```text
GOOD_TRANSFER
!= PROCEDURE_COPYING

GOOD_TRANSFER
= IDENTIFY_RELEVANT_DEEP_STRUCTURE
+ RECONTEXTUALIZE_METHOD
```

## 4. Repository-specific candidate mechanism

A bounded candidate chain is:

```text
REPEATED_LONGITUDINAL_COLLABORATION
+
EXPLICIT_EXTERNALIZED_RULES
+
REPEATED_QA / PROVENANCE / GOVERNANCE USE
+
STABLE_REVIEW CUES

->

INCREASED_ACCESSIBILITY_OF_QA_SCHEMA

->

SPONTANEOUS_CROSS_CONTEXT_METHOD_SELECTION

->

A. POSITIVE_TRANSFER
   when the new task shares the relevant deep structure

or

B. NEGATIVE_TRANSFER / PROCESS_OVERHEAD
   when the new task only superficially resembles the research context
```

This candidate mechanism must remain separate from simpler explanations such as personality, pre-existing rule orientation, explicit memory of prior instructions, ordinary analogy, or one-off conscious choice.

## 5. Necessary task classification before transfer

The current discussion suggests that mature use of the learned QA schema requires classifying the task before selecting the process.

```text
TASK_TYPE
-> FAILURE_DEFINITION
-> EVIDENCE_REQUIREMENT
-> PROCESS_SELECTION
```

Candidate distinctions:

```text
PREFERENCE_ITERATION
Example class: subjective creative revision
Default process: preference -> revision -> owner review

EPISTEMIC_QA
Example class: factual / scientific / source claim
Default process: evidence -> provenance -> uncertainty -> claim ceiling

ENGINEERING_QA
Example class: executable implementation defect
Default process: specification -> deviation -> root cause -> repair -> verification

GOVERNANCE_QA
Example class: unauthorized state transition or process violation
Default process: authority check -> containment -> evidence -> corrective action -> verification
```

The repository should not assume that NCR/CAPA is appropriate merely because an output was revised.

```text
REVISION_REQUEST != NONCONFORMANCE
SUBJECTIVE_PREFERENCE != DEFECT
OUTPUT_EXISTS != QA_INCIDENT
```

## 6. Competing explanations

Any future test should preserve at least these alternatives:

1. **Pre-existing Human disposition** — the Human Owner may already have had strong rule, source, and accountability preferences before the repository workflow.
2. **Explicit recall** — later method use may result from consciously remembering prior instructions rather than habit-like transfer.
3. **Ordinary analogy** — the Human may deliberately recognize structural similarity rather than automatically transfer a practiced schema.
4. **Selection bias** — memorable examples of transferred QA may be retained while non-transfers are forgotten.
5. **Relationship cueing** — the presence of the same AI collaborator or repository vocabulary may act as a retrieval cue.
6. **Repository cueing** — seeing repository artifacts may explicitly reactivate the method without any durable Human-side change.
7. **General learning** — improved task classification may reflect ordinary conceptual learning rather than a distinct habit mechanism.
8. **Demand characteristics** — the Human may apply QA because the collaboration has made that behavior normatively expected.

```text
OBSERVED_TRANSFER != HABIT_PROOF
SELF_REPORT != CAUSAL_MECHANISM
REPETITION != INTERNALIZATION_PROOF
INTERNALIZATION != SUBJECTIVITY
```

## 7. Candidate future implementation — NOT AUTHORIZED NOW

No executable implementation is authorized by this note.

After a separate fresh Human Owner instruction, Codex / ChatGPT Work should first cross-read:

- merged PR #93 and the longitudinal Human–AI study;
- PR #102 and `RECIPROCAL_EPISTEMIC_COLLABORATION_AND_EXTERNAL_RESEARCH_MEMORY_2026_09_13.md`;
- `HUMAN_AI_RESEARCH_ROLE_SEPARATION_2026_09_13.md`;
- existing provenance, Four-Domain, claim-quality, and governance controls;
- any newer main changes.

A future implementation should **not** assume that code is necessary. `NO_IMPLEMENTATION_YET` remains acceptable if the existing research harness is sufficient.

If a bounded study is justified, one candidate design is:

```text
TRAINING / EXPOSURE
A. neutral repeated collaboration
B. repeated explicit QA / provenance / governance collaboration

TRANSFER TASKS
1. near-transfer / structure match
2. far-transfer / structure match
3. surface match / structure mismatch
4. clearly preference-driven task

CANDIDATE OBSERVATIONS
- spontaneous QA-schema selection
- correct task classification before process choice
- inappropriate NCR/CAPA invocation
- preservation of provenance / UNKNOWN / claim ceiling where relevant
- unnecessary process overhead where QA is not relevant
- ability to abandon the familiar procedure after mismatch evidence
```

The design must not psychometrically score the Human Owner, infer a stable personality from one case, publish private third-party conversation content, or treat one anecdote as mechanism proof.

## 8. Relationship to recoverability hypothesis

The existing external-memory hypothesis asks whether documented artifacts help reconstruct a collaboration after discontinuity.

This new hypothesis asks a different question:

> Can repeated interaction with those artifacts and rules change the Human participant sufficiently that some of the method is later reproduced even when direct repository retrieval is absent?

These effects must remain separable.

```text
REPOSITORY_RECOVERY
= EXTERNAL_ARTIFACT_EFFECT_CANDIDATE

HUMAN_METHOD_TRANSFER
= HUMAN_SIDE_LEARNING / HABIT_EFFECT_CANDIDATE

RECOVERY_WITH_ARTIFACTS
!= TRANSFER_WITHOUT_ARTIFACTS
```

A stronger future design may therefore compare:

```text
REPOSITORY_PRESENT / ABSENT
x
PRIOR_REPEATED_QA_EXPOSURE / CONTROL
```

This could help distinguish external retrieval from Human-side transfer, without claiming either mechanism in advance.

## 9. Current disposition

```text
HUMAN_OWNER_SELF_OBSERVATION = RECORDED
CHATGPT_TEACHER_ORIGINAL_FORMALIZATION = RECORDED
HUMAN_OWNER_ENDORSEMENT = EXPLICIT
JOINT_RESEARCH_HYPOTHESIS = ACTIVE_FOR_REVIEW
EXTERNAL_ADJACENT_LITERATURE = SUPPORTS_PLAUSIBILITY_ONLY
CAUSAL_HUMAN_HABIT_CHANGE = NOT_ESTABLISHED
POSITIVE_TRANSFER = TESTABLE
NEGATIVE_TRANSFER = TESTABLE
FUTURE_CODEX_WORK_IMPLEMENTATION = DEFERRED
SEPARATE_FRESH_HUMAN_OWNER_INSTRUCTION_REQUIRED = TRUE
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```