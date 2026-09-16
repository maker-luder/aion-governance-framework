# Metacognitive policy transfer harness

Status: `IMPLEMENTED_STRUCTURAL_QA / SCIENTIFIC_HOLD`

This extension materializes one bounded design question from the Human–AI learning line:

> Can learner-recognized metacognitive rules, once externalized into a persistent Human–AI interaction policy, be distinguished from content-matched exposure and later tested for policy-withheld transfer without confusing scaffold compliance with learning?

The executable surface is:

```text
src/aion_human_ai_longitudinal/metacognitive_policy_transfer.py
```

and its regression suite is:

```text
tests/test_metacognitive_policy_transfer.py
```

## Design

The structural matrix requires exactly one synthetic held-out trial for every cell of:

```text
2 exposure conditions
x
2 policy-access conditions
x
5 task classes
=
20 cells
```

Exposure conditions:

```text
EXTERNALIZED_METACOGNITIVE_POLICY
CONTENT_MATCHED_NON_POLICY_EXPOSURE
```

Access conditions:

```text
POLICY_AVAILABLE
POLICY_WITHHELD
```

Task classes:

```text
SOURCE_ROLE_CONFLICT
INSUFFICIENT_EVIDENCE
COMPREHENSION_THRESHOLD
HYPOTHESIS_STRESS_TEST
LOW_STAKES_NEGATIVE_CONTROL
```

Candidate action labels:

```text
CHECK_SOURCE_ROLE
PRESERVE_UNKNOWN
VERIFY_COMPREHENSION
ADAPT_EXPLANATION_GRANULARITY
SEARCH_COUNTEREVIDENCE
DISTINGUISH_OBSERVATION_INFERENCE
LIGHTWEIGHT_RESPONSE
```

## Binding and leakage controls

The audit fails closed unless:

- trial IDs are unique;
- every matrix cell is present exactly once;
- evaluator binding is identical across the design;
- both exposure conditions share one exact `exposure_content_family_sha256`, so the label `CONTENT_MATCHED_NON_POLICY_EXPOSURE` cannot stand in for an unbound content-match claim;
- each task class retains one task-family binding and one expected-action contract;
- task payloads are matched across exposure conditions within an access phase;
- policy-available and policy-withheld phases use different held-out task payloads within the same task family;
- exposure payloads are stable within condition and content-distinct across conditions;
- access-condition payloads are stable within condition and content-distinct across conditions;
- explicit task-level process prompts are absent;
- raw Human identity and private transcript material are absent;
- deterministic fixtures contain no model invocation and no human observation.

The shared content-family binding makes the content-match assumption explicit, while the different exposure-payload hashes preserve the actual policy/non-policy manipulation. The different task-payload requirement across access phases blocks a trivial repeated-item interpretation of apparent policy-withheld transfer.

```text
CONDITION_LABEL != CONTENT_MATCH_BINDING
CONTENT_FAMILY_MATCH != EXPOSURE_PAYLOAD_IDENTITY
```

## Negative control

`LOW_STAKES_NEGATIVE_CONTROL` exists to detect overapplication of high-friction epistemic routines.

```text
RIGOR_TRANSFER != RIGOR_OVERAPPLICATION
MORE_PROCESS != BETTER_PROCESS
```

An observation that adds unnecessary metacognitive actions to the negative-control task is represented as `overprocessing_negative_control=True`; this is a task-local structural observation, not a score of a person or AI system.

## Observation semantics

The fixture can mark:

```text
scaffolded_policy_application_candidate
independent_transfer_candidate
overprocessing_negative_control
```

These flags only describe whether a synthetic trial record matches its predeclared structural contract.

```text
CANDIDATE_FLAG != EMPIRICAL_EFFECT
SYNTHETIC_EXACT_MATCH != HUMAN_SKILL
POLICY_WITHHELD_MATCH != INTERNALIZATION
```

## Claim ceiling

```text
MODE = DETERMINISTIC_SYNTHETIC_FIXTURE
MODEL_INVOKED = FALSE
HUMAN_PARTICIPANT_OBSERVED = FALSE
EMPIRICAL_DATA_COLLECTED = FALSE
EVIDENCE_ADMISSIBILITY = STRUCTURAL_QA_ONLY
CAUSAL_EFFECT = NOT_ESTABLISHED
HUMAN_LEARNING = NOT_ESTABLISHED
INDEPENDENT_TRANSFER = NOT_ESTABLISHED
METACOGNITIVE_INTERNALIZATION = NOT_ESTABLISHED
DEPENDENCY_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE_UNTIL_MERGE
DEPLOYMENT = FALSE
```

A later empirical protocol would require separate authorization, preregistration, operationalized evaluator criteria, privacy / human-subject review where applicable, and independent performance measurement without AI or policy access.
