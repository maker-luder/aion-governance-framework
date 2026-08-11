# External Module Intake — OpenInference Semantics — 2026-08-11

Status: `RESEARCH_INTAKE / SOURCE_FIXED / CLEAN_ROOM_SELECTED / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

## Source

```text
REPOSITORY = Arize-ai/openinference
COMMIT = 44cdf7996e05a5f16b2e38d0cbb500b1403fbaf1
COMMIT_TIME = 2026-08-11T05:37:41Z
LICENSE = Apache-2.0
TARGET_SURFACE = python semantic conventions / trace attributes
WHOLE_REPOSITORY_VENDORING = NO
```

## IQC disposition

AION already owns provenance, authority, identity, memory, encounter, and Audit Sink semantics. The useful external contribution is a mature public trace vocabulary that can make execution evidence easier to export or compare with external observability tooling.

```text
PUBLIC_TRACE_VOCABULARY = USEFUL
AION_PROVENANCE_REPLACEMENT = REJECTED
EXTERNAL_AUTHORITY_IMPORT = PROHIBITED
RAW_CONTENT_EXPORT_DEFAULT = OFF
CLEAN_ROOM_CROSSWALK = SELECTED
```

## Materialized output

`research-labs/trace-provenance-crosswalk_v0.1.0/`

The module maps a deliberately small vocabulary and adds AION-specific redaction and authority locks. It does not claim OpenInference compliance certification and does not import the OpenInference package.

## Local validation

```text
pytest = 12 passed
compileall = PASS
demo = PASS
```
