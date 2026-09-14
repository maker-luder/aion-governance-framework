# Epistemic co-development workflow and quality line — 2026-09-13

Status: `RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT`
Canonical effect: `NONE`
Deployment: `FALSE`
Executable implementation: `NONE`

## 1. Purpose

This note closes a documentation gap identified during review of the current Human–AI research workflow.

Three items had been discussed but were not all preserved with source-role precision:

1. the Teacher's informal contrast between simple answer retrieval and longitudinal epistemic collaboration;
2. the Teacher's compact diagram linking Human working model, Teacher working model, external evidence, repository state, implementation evidence, and Codex / ChatGPT Work output;
3. why this collaboration requires a full quality-management line rather than only ad hoc correction.

This note records those items without turning local working language into an external scientific taxonomy.

## 2. Terminology audit: `answer-seeking`

### CHATGPT_TEACHER_WORKING_TERM

`answer-seeking` was used conversationally by ChatGPT Teacher as a compact contrast for interactions whose main objective is obtaining a usable answer and then closing the task.

It was **not** introduced as the name of a validated learner type, personality category, or a direct quotation from one paper.

```text
ANSWER_SEEKING = CHATGPT_TEACHER_WORKING_TERM
ANSWER_SEEKING = NOT_A_REPOSITORY_VALIDATED_TAXONOMY
ANSWER_SEEKING = NOT_A_PERSONALITY_CLASS
```

The closest external constructs are broader and should not be collapsed into the Teacher's shorthand:

- `information seeking` — behavior directed toward finding information;
- `question answering / help seeking` — metacognitive regulation of whether to answer, seek help, or withhold an answer;
- `epistemic agency` — active participation in shaping, evaluating, justifying, and revising knowledge rather than merely receiving output;
- `evaluativist epistemic stance` — treating claims as requiring evidence, comparison, and justification;
- `epistemic co-agency` — recent Human–AI learning literature's proposal that the learner may engage AI dialectically, challenge assumptions, surface contradictions, and retain epistemic responsibility.

Useful external anchors include:

- Wu, Lee, Chai & Tsai (2025), *Strengthening Human Epistemic Agency in the Symbiotic Learning Partnership With Generative Artificial Intelligence*, Educational Researcher 54(6):358–368, DOI `10.3102/0013189X251333628`.
- *Learning with machines: Toward a theory of epistemic co-agency* (2026), Computers and Education: Artificial Intelligence 10:100573, DOI `10.1016/j.caeai.2026.100573`.
- Undorf, Livneh & Ackerman (2021), *Metacognitive control processes in question answering: help seeking and withholding answers*, Metacognition and Learning 16:431–458.

The repository should therefore use `answer-seeking` only when explicitly marked as Teacher shorthand.

## 3. Current collaboration model

### CHATGPT_TEACHER_FORMALIZATION

The earlier compact diagram was:

```text
USER MODEL
↕ correction
TEACHER MODEL
↕ external evidence
REPOSITORY STATE
↕ implementation evidence
CODEX / WORK OUTPUT
```

That diagram is Teacher-origin shorthand, not a claim about hidden model internals.

To avoid confusing `USER MODEL` with a psychological profile or machine-internal user model, the safer repository form is:

```text
HUMAN WORKING MODEL OF THE PROBLEM
↕ reciprocal correction
CHATGPT TEACHER WORKING MODEL OF THE PROBLEM
↕ source checking / counterevidence / external literature
EXTERNAL EVIDENCE
↕ provenance / claim ceiling / revision
REPOSITORY RESEARCH STATE
↕ specification / implementation evidence / tests
CODEX OR CHATGPT WORK OUTPUT
↕ independent review / QA / governance
HUMAN OWNER + CHATGPT TEACHER REVIEW
```

This is not a linear command chain. It is a revision loop in which no node receives automatic epistemic authority.

```text
HUMAN_ASSERTION != TRUTH
TEACHER_ASSERTION != TRUTH
EXTERNAL_SOURCE != AUTOMATIC_TRUTH
REPOSITORY_PERSISTENCE != CURRENT_TRUTH
IMPLEMENTATION_SUCCESS != SCIENTIFIC_VALIDATION
MUTUAL_AGREEMENT != TRUTH
```

The role of the Human Owner remains distinct from epistemic correctness: the Human Owner holds governance and merge authority, while factual and scientific claims remain evidence-constrained.

## 4. Why the full quality-management line is unusually important here

### HUMAN_OWNER_ORIGINAL_DIRECTION

The Human Owner introduced the idea of applying prior quality-assurance experience to Human–LLM research and later explicitly required the full quality line rather than only final inspection. The standing concern was that Human and LLM may mutually reinforce the same error, become increasingly coherent, and still be wrong.

The repository had externalized this by 2026-08-23 as a coupled-cognition quality factory.

### Existing repository rationale

The canonical research-quality factory already states the characteristic failure mode:

> Human and LLM can agree, become mutually coherent, and still be wrong.

It therefore uses:

```text
Idea / observation
  -> IQC: source / scope / provenance intake
  -> hypothesis + explicit falsifier
  -> AI work
  -> human review / correction
  -> IPQC: in-process epistemic inspection
  -> COUNTEREVIDENCE LANE
  -> implementation / experiment
  -> verification
  -> FINAL QA
  -> RELEASE or HOLD
                         |
                         +-> NCR -> containment -> root-cause hypothesis
                                  -> CAPA plan -> CAPA applied
                                  -> effectiveness verification -> NCR close
```

### Why one final check is insufficient

This collaboration has several different failure surfaces:

1. **Input / source failure** — a premise, source, ownership attribution, or scope may already be wrong before reasoning starts. This requires IQC-like intake control.
2. **Reasoning drift** — Human and Teacher may converge on a coherent but unsupported explanation during the conversation. This requires in-process inspection and an explicit counterevidence lane.
3. **Implementation drift** — Codex or ChatGPT Work may faithfully implement the wrong question, stale specification, or over-broad claim. This requires specification binding, exact-state checking, tests, and later independent review.
4. **Evidence inflation** — passing tests may be promoted into a scientific or ontological conclusion that the tests cannot support. This requires claim ceilings and final QA.
5. **Authority leakage** — a technically correct branch or successful CI run may be mistaken for Human Owner approval or merge authority. This requires governance separation.
6. **Correction-without-learning** — a CAPA may be applied but the failure can recur if effectiveness is not independently checked. This requires effectiveness verification before closure.
7. **Longitudinal staleness** — repository artifacts may persist after assumptions, models, sources, or code have changed. This requires revision traceability and re-entry checks.
8. **Method over-transfer** — repeated QA practice may itself be transferred into tasks where the deep structure does not justify the full process. This requires meta-QA on process selection.

Hence:

```text
FINAL_QA_ONLY = INSUFFICIENT

QUALITY_LINE_NEEDED
= INPUT_CONTROL
+ IN_PROCESS_CONTROL
+ COUNTEREVIDENCE
+ IMPLEMENTATION_VERIFICATION
+ FINAL_QA
+ NCR / CAPA
+ EFFECTIVENESS_VERIFICATION
+ GOVERNANCE_BOUNDARY
```

## 5. External quality-method anchors already in the repository

The repository does not claim certification or regulatory compliance. It uses bounded analogies from established quality and risk-management sources.

### NIST AI RMF 1.0

The repository crosswalk maps:

```text
GOVERN -> authority, boundaries, source policy, claim ceiling
MAP -> construct, machine question, locus, alternatives, affected context
MEASURE -> preregistration, controls, execution evidence, counterevidence
MANAGE -> HOLD/release decision, NCR/CAPA, effectiveness verification, iteration
```

This supports lifecycle-wide governance and continual risk management, but does not itself validate the repository's research claims.

### FDA QSIT CAPA guide

The repository uses the transferable quality-method analogy:

```text
nonconformity
-> containment
-> root-cause account
-> corrective action
-> preventive action
-> effectiveness test
-> evidence
-> closure
```

This is a method reference only:

```text
FDA_GUIDE_REFERENCE != FDA_COMPLIANCE
CAPA_CLOSURE != SCIENTIFIC_TRUTH
```

## 6. Existing repository coverage audit

As of this review:

```text
ANSWER_SEEKING_EXACT_TERM
= NOT_PREVIOUSLY_RECORDED

ANSWER_SEEKING_AS_FORMAL_EXTERNAL_TAXONOMY
= NOT_ESTABLISHED

EXACT_HUMAN↔TEACHER↔EVIDENCE↔REPOSITORY↔IMPLEMENTATION_DIAGRAM
= NOT_PREVIOUSLY_RECORDED_AS_ONE_MODEL

PROBLEM_DECOMPOSITION_DISCIPLINE
= RECORDED

SOURCE_ROLE_PROVENANCE
= RECORDED

RECIPROCAL_CORRECTION / CONTESTABILITY
= RECORDED

COUPLED_COGNITION_QUALITY_FACTORY
= RECORDED_AND_IMPLEMENTED_AS_BOUNDED_RESEARCH_CONTROL

IQC / IPQC / QC / QA / NCR / CAPA
= RECORDED

COUNTEREVIDENCE_LANE
= RECORDED

ROLE_SEPARATION_FOR_HUMAN_OWNER / TEACHER / CODEX / WORK / GITHUB_ACTIONS
= RECORDED_IN_DRAFT_PR_102

HUMAN_PROBLEM_SOLVING_HABIT_TRANSFER
= RECORDED_IN_DRAFT_PR_102
```

Therefore the repository already contained most components, but not the exact conceptual integration requested in the current discussion. This note fills that documentation gap.

## 7. Relationship to epistemic co-development

The existing co-development note already distinguishes longitudinal inquiry from simple answer volume or agreement. It proposes that useful long-term Human–AI collaboration should preserve or improve the Human participant's ability to decompose questions, distinguish observation from inference, inspect sources, generate alternatives, identify falsifiers, correct the AI, and independently restate or transfer the method.

The present note does not create a new scientific claim that this collaboration has achieved those outcomes. It clarifies the process model under which they are being studied.

```text
LONG_INTERACTION != EPISTEMIC_DEVELOPMENT
AI_HELP != LEARNING
MORE_TOOLS != BETTER_REASONING
RECIPROCAL_CORRECTION != SCIENTIFIC_VALIDATION
QUALITY_CONTROL != TRUTH_MACHINE
```

## 8. Current disposition

```text
ANSWER_SEEKING = CHATGPT_TEACHER_WORKING_TERM
EXACT_WORKFLOW_DIAGRAM = CHATGPT_TEACHER_FORMALIZATION
HUMAN_OWNER_QUALITY_LINE_DIRECTION = RECORDED
FULL_QA_LINE_RATIONALE = REPOSITORY_SUPPORTED
EXACT_INTEGRATED_DOCUMENTATION_GAP = NOW_RECORDED_IN_PR_102
EXECUTABLE_CHANGE = NONE
FUTURE_IMPLEMENTATION = DEFERRED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```