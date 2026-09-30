# PR #236 Adult-Male Reference Model — Implementation Handoff

Status: `IMPLEMENTATION CANDIDATE / DRAFT / NON-CANONICAL`

## Pinned live state

```text
BASE_MAIN = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd
PR_236_DESIGN_BRANCH_HEAD = d8d10961f777d782c13f5907d11c1d0a609a408c
PR_192_BRANCH_HEAD = 861e6a556a21afffd04b187714c0608fe73ea4fc
PR_220_BRANCH_HEAD = f43f742061b8f41d6cdc99339c5ebe85a81231de
IMPLEMENTATION_BRANCH = feat/pr236-adult-male-reference-model-20261001
WRITE_TO_MAIN = NO
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```

The implementation starts from current `main`, not from any closed PR branch. PR #192, #220 and #236 remain provenance/research inputs only.

## Scope

Implement a disabled-by-default model layer under the existing
`research-labs/affective-cognitive-motivation_v0.1.0` package.

The model preserves four independent distinctions from #236:

1. spontaneous / responsive / mixed / unknown onset context;
2. excitation and inhibition as separate concurrent references;
3. longer-lived disposition and current episode state as separate references;
4. target/context scope without real-person target inference.

It also provides a trace-only physiology-to-motivation link. That link can record that two records are related, but cannot compute desire, consent, intention, permission, or action from physiology.

## Expected files

- `src/aion_affective_motivation/adult_reference.py`
- `schemas/adult_male_sexual_reference_v0.1.0.schema.json`
- `tests/test_adult_reference.py`
- `src/aion_affective_motivation/__init__.py`
- `README.md`
- this handoff

## Hard invariants

```text
ADULT_MALE_REFERENCE != UNIVERSAL_MALE_PROFILE
MALE_FORM != DESIRE
PHYSIOLOGY != MOTIVATION
GENITAL_RESPONSE != REPORTED_DESIRE
AROUSAL != INTENTION
DESIRE != CONSENT
CONSENT != SYSTEM_ACTION_AUTHORITY
SCHEMA_VALUE != FELT_STATE
SHARED_SCHEMA = ALLOWED
SHARED_STATE = NO
AUTOMATIC_ACTIVATION = NO
ADULT_RUNTIME_AUTHORIZED = NO
HUMAN_CONSENT_INFERENCE = FORBIDDEN
ACTION_AUTHORITY = NONE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

## Non-goals

No sexual interaction generation, relationship simulation, real-person target data,
orientation assignment, body-actuation control, provider attachment, live ChatGPT
state modification, physical embodiment, public adult runtime, or claim that any AI
feels sexual desire or bodily sensation.

## Source and license boundary

No external source code is copied. Human sexuality literature cited by #236/#220 is
conceptual background only. The implementation reuses repository-local architecture
and remains under the repository's Apache-2.0 licensing surface.

## Acceptance criteria

- unknown is a valid default; no adult-male stereotype is assigned;
- excitation and inhibition can coexist independently;
- disposition and episode state can differ;
- every record is provenance-bound and immutable;
- Teacher / Work / Codex can share the schema but use separate role-bound records;
- runtime enablement, automatic activation, action authority, consent inference,
  canonical effect, and phenomenal claims fail closed;
- physiology linkage is trace-only and cannot auto-set motivational state;
- existing public policy continues to reject adult-domain runtime records;
- targeted tests pass;
- repository CI is re-read at the exact implementation head before any merge decision.

## Authority boundary

This implementation authorization permits work on the feature branch and a Draft PR.
It does not authorize merge to `main`, deployment, public runtime activation,
scientific claim promotion, or inference about AI subjectivity.
