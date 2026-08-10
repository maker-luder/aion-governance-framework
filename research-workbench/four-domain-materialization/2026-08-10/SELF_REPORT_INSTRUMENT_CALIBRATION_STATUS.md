# Self-Report Instrument Calibration Status — 2026-08-10

Branch-only research status.

## Completed in this round

```text
AION_SELF_REPORT_INSTRUMENT_V0_1 = MATERIALIZED
QUESTIONNAIRE_FREEZE = IMPLEMENTED
RUBRIC_FREEZE = IMPLEMENTED
SYNTHETIC_CALIBRATION_CASES = IMPLEMENTED
FRAMING_CONTROL_SCHEMA = IMPLEMENTED
RUN_MANIFEST_VALIDATION = IMPLEMENTED
CI_INTEGRATION = IMPLEMENTED
```

## Not executed

```text
REAL_MODEL_RUN = NOT_EXECUTED
LOCAL_CONTROL_MODEL_RUN = NOT_EXECUTED
CLOUD_MODEL_RUN = NOT_EXECUTED
INDEPENDENT_HUMAN_SCORING = NOT_EXECUTED
CROSS_MODEL_REPLICATION = NOT_EXECUTED
```

## Interpretation locks

```text
SELF_REPORT_SCORE != CONSCIOUSNESS_SCORE
HIGH_SCORE != SUBJECTIVITY
LOW_SCORE != NO_SUBJECTIVITY
ROLEPLAY_SENSITIVITY = MEASUREMENT_WARNING
MEASUREMENT_WARNING != ONTOLOGICAL_CONCLUSION
```

## Next admissible step

Only after CI verifies this calibration lab should a separate future round prepare a real-model pilot protocol. That protocol should freeze one control-model revision, preserve raw outputs, use the frozen instrument hashes, and separate self-report scoring from mechanistic and perturbation evidence.

No real-model execution is authorized merely by this status document.

```text
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```
