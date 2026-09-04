# White Paper v0.10 Engineering Pilot

Status: `SANDBOX_ONLY`

```
AUTHORITY = NONE
BASELINE_DOCUMENT = AION-WP-INT-010 / v0.10 / 2026-06-25
DOCUMENT_CLASS = EXTERNAL_HISTORICAL_RECORD
WORKSPACE = grok/experimental-sandbox
PR = #84 (draft; not merged)
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
GAP_CLOSURE_CAMPAIGN = FROZEN
```

This directory implements only the machine-checkable identity / source / role
mechanisms that the June 2026 white paper specified as engineering constraints.
It does not implement subjectivity, first-person experience, ethical informed
consent, or pause/resume as lived continuity (ID-09 remains NOT_VERIFIED).

Passing these tests proves at most PROGRAM_RUNS plus selected SPEC_CONFORMANT
checks inside this pilot. It does not promote the white paper onto main, and it
does not create a second canonical identity authority.

## Tests

```
PYTHONPATH=src python -m pytest -q
```
