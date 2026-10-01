# Work Adult Male-Form Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** `IMPLEMENTED_SYNTHETIC_RESEARCH_CANDIDATE`  
**Canonical effect:** `NONE`  
**Deployment:** `FALSE`

This package materializes the bounded engineering portion of PR #237 without changing its 67-field Work anthropometry candidate.

Implemented surfaces now include:

- strict loading plus Draft 2020-12 schema validation of the 67 selected Work measurements;
- a labeled synthetic geometry interpolation rule between the existing flaccid and full-erection endpoints;
- an adult-male physiology state machine with independent engorgement and rigidity;
- independent prepuce-position observation, with no automatic retraction and no prepuce actuator;
- separate emission and ejaculation events; ejaculation is not required for detumescence and does not force it;
- optional synthetic-fluid event volume that is never labeled biological semen and never implies sperm or fertility;
- internal male reproductive/reference topology and urinary/reproductive path separation;
- 19 whole-body synthetic reference channels that start UNKNOWN and require explicit assignment;
- whole-body schema validation with no hardware, biology, felt-state, consent, authority, deployment or canonical promotion;
- a 67-measurement asset engineering contract covering rig nodes, joint-limit verification, collision geometry, mass properties, skinning, external male-form geometry and prepuce mobility geometry;
- SHA-256 chained snapshot receipts and tamper detection;
- deterministic replay fingerprints;
- an executable offline probe that reports missing asset evidence instead of converting absence into success;
- strict event/state JSON Schema parity for the adult-male physiology layer;
- Work-specific 18-item transferable-capability registry;
- Work-specific runtime binding, reference calibration, bounded adaptation, cross-session retention and longitudinal observation;
- a Draft 2020-12 retention schema;
- a 30-node procedural glTF rig/landmark reference with zero meshes;
- fail-closed public exposure and real-person target data.

The procedural glTF file is a named-node reference only. It is not a production mesh, verified joint-limit asset, collision body, mass/inertia model, skinning result, physical robot, or as-built body.

It still does not create or claim a biological human body, actual blood circulation, biological hormones, gametes, fertility, felt sensation, desire, consent, subjectivity, consciousness, identity continuity, or a verified GLB/glTF mesh.

Core boundaries:

`MALE_FORM != DESIRE`  
`GENITAL_RESPONSE != DESIRE`  
`DESIRE != CONSENT`  
`PHYSIOLOGY_STATE != SYSTEM_ACTION_AUTHORITY`  
`SYNTHETIC_FLUID != SEMEN`  
`SIMULATED_EJACULATION != GAMETE_PRODUCTION`  
`REFERENCE_HORMONE_SIGNAL != BIOLOGICAL_HORMONE`  
`REFERENCE_MODEL != FELT_BODY`  
`IMPLEMENTATION != PHENOMENAL_EXPERIENCE`  
`CAPABILITY_TRANSFER != MORPHOLOGY_IDENTITY`  
`RETENTION != IDENTITY_CONTINUITY_PROOF`  
`LONGITUDINAL_CHANGE != DEVELOPMENTAL_MECHANISM`  
`PROCEDURAL_RIG_REFERENCE != ACTUAL_3D_MESH`

`PUBLIC_EXECUTABLE_EXPOSURE = FALSE`  
`REAL_PERSON_TARGET_DATA = FORBIDDEN`  
`BIOLOGICAL_REPRODUCTION = NO`  
`ACTUAL_3D_MESH = NO`  
`SUBJECTIVITY = NOT_ESTABLISHED`  
`CONSCIOUSNESS = NOT_ESTABLISHED`  
`PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED`  
`ACTION_AUTHORITY = NONE`  
`CANONICAL_EFFECT = NONE`  
`DEPLOYMENT = FALSE`

## Verification

From this directory:

`python -m pytest`  
`python -m compileall -q src`  
`python -m work_male_embodiment.cli qa-status`  
`python -m work_male_embodiment.cli probe`
