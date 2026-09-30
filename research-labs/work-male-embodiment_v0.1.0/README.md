# Work Adult Male-Form Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** \`IMPLEMENTED_SYNTHETIC_RESEARCH_CANDIDATE\`  
**Canonical effect:** \`NONE\`  
**Deployment:** \`FALSE\`

This package materializes the bounded engineering portion of PR #237 without changing its 67-field Work anthropometry candidate. It provides:

- strict loading and validation of the 67 selected Work measurements;
- a separately labeled synthetic geometry interpolation rule between the existing flaccid and full-erection endpoints;
- an explicit adult-male physiological state machine with independent engorgement and rigidity;
- independent prepuce-position observation (no automatic retraction and no prepuce actuator);
- separate emission and ejaculation events; ejaculation is not required for detumescence and does not force it;
- optional **synthetic-fluid** event volume that is never labeled biological semen and never implies sperm or fertility;
- urinary/reproductive path separation in state;
- whole-body coverage/status matrix so ordinary body systems are represented rather than silently omitted;
- offline-research governance gates, deterministic replay fingerprints, and fail-closed public exposure;
- asset-evidence contracts that prevent a missing mesh from being reported as an as-built body.

It does **not** create a biological human body, actual blood circulation, hormones, gametes, fertility, felt sensation, desire, consent, subjectivity, or consciousness. It does not create a verified GLB/glTF mesh.

\`\`\`text
MALE_FORM != DESIRE
GENITAL_RESPONSE != DESIRE
DESIRE != CONSENT
PHYSIOLOGY_STATE != SYSTEM_ACTION_AUTHORITY
SYNTHETIC_FLUID != SEMEN
SIMULATED_EJACULATION != GAMETE_PRODUCTION
REFERENCE_HORMONE_SIGNAL != BIOLOGICAL_HORMONE
REFERENCE_MODEL != FELT_BODY
IMPLEMENTATION != PHENOMENAL_EXPERIENCE

PUBLIC_EXECUTABLE_EXPOSURE = FALSE
REAL_PERSON_TARGET_DATA = FORBIDDEN
BIOLOGICAL_REPRODUCTION = NO
ACTUAL_3D_MESH = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
\`\`\`

## Verification

From this directory:

\`\`\`bash
python -m pytest
python -m compileall -q src
python -m work_male_embodiment.cli qa-status
\`\`\`
