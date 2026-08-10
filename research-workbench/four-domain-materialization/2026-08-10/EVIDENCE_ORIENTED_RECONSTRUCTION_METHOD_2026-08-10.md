# Evidence-Oriented Reconstruction Method — 2026-08-10

```text
STATUS = RESEARCH_METHOD_CANDIDATE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

## Purpose

This method was derived from repeated IQC/reconstruction work across metacognitive, self/other, motivation, embodiment, handoff, continuity, encounter, and longitudinal candidates.

It is intended to reduce a recurring failure mode: an implementation adopts a psychologically rich label first, then fills the code with manually asserted values that look like the construct but do not operationalize it.

## Core sequence

```text
1. CONSTRUCT / PHENOMENON
2. RESEARCH QUESTION
3. OPERATIONAL UNIT
4. SOURCE / EVIDENCE CONTRACT
5. MEASUREMENT CONTRACT
6. EXECUTABLE MECHANISM
7. CONTROL / ABLATION
8. CAUSAL ORDER
9. REPRODUCIBILITY
10. CLAIM BOUNDARY
```

A candidate may stop at any earlier level. If a later level is absent, it must be reported as `NOT_IMPLEMENTED`, `NOT_EXECUTED`, `NOT_ASSESSED`, or `NOT_ESTABLISHED` rather than simulated through labels.

## 1. Construct is not an implementation

Human/cognitive constructs may provide research questions and comparison language, but they do not automatically define artificial-agent state variables.

```text
HUMAN_CONSTRUCT != AI_MECHANISM
BIOLOGICAL_CORRELATE != AI_ARCHITECTURE
CLASS_NAME != EVIDENCE
```

Examples of invalid shortcuts:

- naming a float `trust`, `consciousness`, `identity`, `affect`, or `stability` without a measurement contract;
- naming a class `SelfState` and treating its existence as evidence of selfhood;
- importing a biological taxonomy as if it were a validated artificial-agent mechanism.

## 2. Operational unit first

Prefer the smallest auditable unit that actually exists in the experiment.

Examples from this cycle:

```text
relationship narrative
    -> EncounterRecord

continuity score
    -> EvidenceArtifact + LineageRelation + dimension assessment

development trajectory
    -> timestamped ObservationSet + ChangeEvidence

embodiment story
    -> CapabilityChannel + ObservationSample + ActionCommand

motivation story
    -> source-bound signal primitives
```

The operational unit should be representable without requiring the scientific conclusion to already be true.

## 3. Evidence and provenance before interpretation

Every important measurement or event should make source lineage inspectable.

A useful minimum question set is:

```text
WHAT
WHERE
WHO / SOURCE
WHEN
TRANSFORMATION
AUTHORITY_STATUS
```

Common structural fields include:

- `evidence_refs`
- `provenance_refs`
- `source_ref`
- `method_ref`
- subject/context/lineage/encounter/run refs when needed.

`ATTRIBUTION != APPROVAL_AUTHORITY` remains a hard boundary.

## 4. Measurement semantics

The numeric output must mean exactly what its name says.

Research checks:

```text
CAPABILITY_ESTIMATE != SUCCESS_PROBABILITY
SUCCESS_RATE != PREDICTION_RELIABILITY
OBSERVED_SUBSET_RATE != GLOBAL_RATE
MISSING != ZERO
UNKNOWN != FALSE
```

A numeric value requires, as applicable:

- operational definition;
- unit or scale;
- production method;
- comparison/ground-truth contract;
- evidence refs;
- provenance refs;
- uncertainty or missing-data semantics.

If those are unresolved:

```text
MEASUREMENT_CONTRACT = UNRESOLVED
```

Do not place the value in the scientific core merely because it is convenient for a demo.

## 5. Causal order

A mechanism can be code-correct and still be causally invalid.

For an online trial `t`:

```text
history through t-1
    -> state / modulation for t
    -> action_t
    -> outcome_t observed
    -> update available for t+1
```

Hard rule:

```text
OUTCOME_t MUST NOT AFFECT ACTION_t
```

Anti-lookahead regression tests should change `outcome_t` while holding pre-trial history fixed and verify that the current action does not change.

## 6. Ablation is a causal experiment

Deleting a config entry, participant, dimension, or stored state is not automatically functional ablation.

A functional ablation asks whether removing or perturbing the mechanism changes an operational output under matched conditions.

A common research control family is:

```text
PRESENT
ABLATED
RANDOMIZED
STALE
```

But these labels must only be used when each condition has an explicit causal implementation and matched experiment design.

```text
NULL_RESULT = VALID_RESULT
```

## 7. Keep state lineage honest

Recurring mutable-manager defects from rejected/reworked candidates include:

```text
initialize(A)
initialize(B)
    -> second false NULL root

restore()
    -> from_state_id = RESTORED

deterministic_seed
    + hidden wall clock

ablation
    -> untraced state mutation
```

Preferred design when possible:

- immutable evidence records;
- pure functions;
- explicit transitions;
- caller-supplied timestamps/clock;
- explicit source state lineage.

A lifecycle manager should exist only if the mechanism requires one.

## 8. Condition isolation

Matched conditions must not share mutable experimental state unless shared state is itself the controlled variable.

```text
CONDITION_A_STATE
MUST NOT LEAK INTO
CONDITION_B_STATE
```

Fresh model instances and stable baseline parameters are required when the underlying first-order model mutates during observation.

## 9. Tests have layers

A test suite should distinguish:

```text
OBJECT_CONSTRUCTION
VALIDATION
REFERENTIAL_INTEGRITY
MEASUREMENT_RECOMPUTATION
CAUSAL_ORDER
CONTROL_ISOLATION
NEGATIVE_CASES
NON_CLAIMS
```

Passing construction tests alone is insufficient evidence for mechanism validity.

```text
TEST_PASS != SEMANTIC_VALIDITY
TEST_PASS != CAUSAL_VALIDITY
```

## 10. Claim boundary

Each module must explicitly state what its strongest valid conclusion can be.

Examples:

```text
ENCOUNTER_RECORD
!= RELATIONSHIP_FORMATION

LINEAGE_GRAPH
!= PERSONAL_IDENTITY

FUNCTIONAL_HANDOFF
!= IDENTITY_CONTINUITY

NUMERIC_CHANGE
!= PSYCHOLOGICAL_GROWTH

MOTIVATIONAL_SIGNAL
!= FELT_DESIRE

FUNCTIONAL_SELF_MODEL_CONTRIBUTION
!= SUBJECTIVITY
```

## IQC stack

The current working stack is:

```text
CODE CORRECTNESS
    -> MEASUREMENT SEMANTICS
    -> CAUSAL VALIDITY
    -> EVIDENCE VALIDITY
    -> CLAIM BOUNDARY
```

A candidate may be rejected even when code runs if a lower layer is invalid.

## Disposition vocabulary

Use precise status terms:

```text
IMPLEMENTED / NOT_IMPLEMENTED
EXECUTED / NOT_EXECUTED
PASS / FAIL / HOLD / REJECT
NOT_ESTABLISHED / NOT_ASSESSED / MISSING / NOT_APPLICABLE
NONE
SALVAGE_ONLY
ARCHITECTURAL_HYPOTHESIS
```

## Provenance

This method is a joint research synthesis from Human Research Owner review decisions and ChatGPT IQC/reconstruction work across the 2026-08-10 candidate cycle. Source agent implementations retain their own provenance and are not reattributed by this method record.
