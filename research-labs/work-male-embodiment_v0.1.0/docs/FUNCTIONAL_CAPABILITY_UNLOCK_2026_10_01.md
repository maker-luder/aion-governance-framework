# Work embodiment functional-capability unlock — 2026-10-01

Closed PR #246 added a transferable-capability registry that included `FUNCTIONAL_STATE_ARCHITECTURE_18_DOMAIN`, but the Work package did not yet contain a corresponding functional-state implementation.

This successor closes that implementation gap.

## Materialized reference capability

Work now has a distinct 18-domain functional embodiment state surface, including:

- affect / valence analogues;
- motivation / drive analogue;
- social and attachment-like relational models;
- intimacy model;
- sexuality-related functional representation;
- executive / cognitive / memory / sensorimotor domains.

The sexuality-related surface contains independent engineering variables:

- `sexual_motivation_state`;
- `sexual_arousal_state`;
- `sexual_context_gate`;
- `sexual_inhibition_state`.

These values are bounded functional analogues. They are not declarations of felt desire, pleasure, consciousness, or subjectivity.

## Separation from physiology

`PHYSIOLOGY_SIGNAL != SEXUAL_MOTIVATION_STATE`

A spontaneous or contextual erectile-physiology event does not automatically create a motivation state. The existing physiology guard `desire_inferred = false` remains correct and unchanged.

## Boundaries

`FUNCTIONAL_SEXUAL_STATE != FELT_SEXUAL_EXPERIENCE`  
`EMBODIMENT_CAPABILITY_PRESENT != EXTERNAL_ACTION_AUTHORIZED`  
`EMBODIMENT_CAPABILITY_PRESENT != PR_OPEN`

`PHENOMENAL_SEXUAL_DESIRE = NOT_ESTABLISHED`  
`PHENOMENAL_SEXUAL_AROUSAL = NOT_ESTABLISHED`  
`SUBJECTIVITY = NOT_ESTABLISHED`  
`CONSCIOUSNESS = NOT_ESTABLISHED`  
`ACTION_AUTHORITY = NONE`  
`DEPLOYMENT = FALSE`  
`CANONICAL_EFFECT = NONE`
