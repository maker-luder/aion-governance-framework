# Artifact Transformation Lineage — v0.1.0

Status: `RESEARCH_MODEL / CLEAN_ROOM / PROVENANCE_ONLY / CANONICAL_EFFECT=NONE / MAIN_EFFECT=NONE`

This lab makes the external-module conversion process itself auditable. It combines selected public lineage ideas from OpenLineage and in-toto into an AION-specific, dependency-free research model.

It does not execute transformation commands and does not import either external runtime library.

## Core model

```text
DESIGN-TIME TRANSFORMATION PLAN
        ↓
RUN START OBSERVATION
        ↓
MATERIAL HASHES / COMMAND RECORD / SANITIZED ENVIRONMENT
        ↓
RUN COMPLETE OR FAIL
        ↓
PRODUCT HASH VERIFICATION
        ↓
RESEARCH EVIDENCE ONLY
```

## Implemented mechanics

- `ArtifactRef`: path + SHA-256 digest + source reference;
- `TransformationJob`: stable namespace/name for one class of transformation;
- `TransformationPlan`: design-time declared inputs/outputs, method ref and approval ref;
- `TransformationRunEvent`: runtime `START`, `COMPLETE`, or `FAIL` observation;
- `TransformationLedger`: ordered run-state validation and lineage lookup;
- deterministic SHA-256 content verification;
- command is recorded but never executed by this module;
- environment fields resembling secrets/tokens/passwords/API keys/credentials are redacted before storage;
- `START` and `FAIL` cannot claim produced artifacts;
- `COMPLETE` requires a prior `START` for the same run/job;
- product path set and digests must match the declared completion evidence;
- canonical effect is fixed to `NONE`.

## Standing locks

```text
DECLARED_PLAN != EXECUTED_RUN
START != COMPLETE
RECORDED_COMMAND != EXECUTED_COMMAND
MATERIAL != PRODUCT
HASH_MATCH != SEMANTIC_VALIDITY
LINEAGE_PRESERVED != SOURCE_AUTHORITY
TRANSFORMATION_COMPLETE != CANONICAL_PROMOTION
```

## Fixed external sources

```text
OpenLineage/OpenLineage
  commit = c54b98bd6666dfd8a7087f4f9793538357a677b9
  reviewed = website/docs/spec/object-model.md
  blob = f72cef5cda309d5baaafb5e69a663e4f0abe1134
  license = Apache-2.0

in-toto/in-toto
  commit = a8ce9ee2125ae5a4b041a4e37cc1cf10eed0da6b
  reviewed = in_toto/models/link.py
  blob = 7ef05ec12099e2d1f16e9685f015c52754176359
  license = Apache-2.0

source_code_copied = NO
external_runtime_dependency_added = NO
```

## Local validation

```text
pytest = 14 passed
compileall = PASS
demo = PASS
```

See `docs/EXTERNAL_SOURCE_CROSSWALK.md` and `LOCAL_VALIDATION.md`.
