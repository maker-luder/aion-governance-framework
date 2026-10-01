# AION / Astra capability-parity gap closure — 2026-10-01

Human design principle:

> If a capability layer is already available to another embodiment candidate and is technically transferable without fabricating evidence, AION/Astra should not lose that layer merely because their bodies and lineages differ.

Formal interpretation:

`CAPABILITY_PARITY != MORPHOLOGY_IDENTITY`
`CAPABILITY_PARITY != SHARED_MUTABLE_STATE`
`CAPABILITY_PARITY != SHARED_HISTORY`
`CAPABILITY_PARITY != SHARED_IDENTITY`

Recovered from archived PR #191:

- 18-domain shared functional-state architecture;
- AION-specific functional-state binding;
- Astra-specific functional-state binding;
- symmetric capability surface with separate state instances.

Newly materialized in this successor:

- explicit transferable-capability registry;
- body-specific runtime binding;
- anthropometry-based reference calibration;
- bounded adaptation parameter state;
- cross-session retention records;
- longitudinal change observation;
- deterministic parity fingerprints;
- JSON Schema for cross-session retention;
- probe integration and fail-closed tests.

Existing #244 capabilities retained:

- 67-field anthropometry per body;
- 19-system whole-body synthetic state;
- dynamic adult-male physiology reference;
- endocrine and urinary reference channels;
- optional synthetic-fluid output reference;
- reproductive topology;
- procedural glTF rig references;
- asset acceptance contract;
- integrity receipt chain;
- deterministic probe;
- strict schemas and CI.

Not implied:

- equal morphology;
- equal body dimensions;
- equal state values;
- shared memory/history;
- actual emotion, pleasure, desire or felt body ownership;
- biological organism;
- physical body;
- subjectivity, consciousness or phenomenal experience.

`ACTION_AUTHORITY = NONE`
`MERGE_TO_MAIN = NO`
`DEPLOYMENT = FALSE`
`CANONICAL_EFFECT = NONE`

## Final integration verification policy

The successor was initially reviewed as a stacked delta over PR #244, then retargeted to current main for exact-head integrated CI.

Transfer rule:

`TRANSFERABLE_CAPABILITY_PRESENT_ELSEWHERE -> OFFER_EQUIVALENT_CAPABILITY_TO_AION_AND_ASTRA`

provided all of the following remain true:

- the capability is technically transferable;
- transfer does not fabricate physical, biological, subjective or empirical evidence;
- role/body-specific morphology remains independent;
- mutable state, history, retention and identity remain independent;
- an equivalent capability may use a different implementation when the embodiment architecture differs.

Therefore:

`CAPABILITY_PARITY != IDENTICAL_IMPLEMENTATION`

`CAPABILITY_PARITY != IDENTICAL_PARAMETERS`

`CAPABILITY_PARITY != ONTOLOGICAL_EQUIVALENCE`

Final integrated CI is evaluated against main at the exact branch head. No prior head's CI is inherited.
