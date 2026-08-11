# External Module Intake — OpenLineage + in-toto — 2026-08-11

Status: `RESEARCH_INTAKE / SOURCES_FIXED / CLEAN_ROOM_SELECTED / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

## Sources

```text
OpenLineage/OpenLineage
  commit = c54b98bd6666dfd8a7087f4f9793538357a677b9
  license = Apache-2.0
  target = website/docs/spec/object-model.md

in-toto/in-toto
  commit = a8ce9ee2125ae5a4b041a4e37cc1cf10eed0da6b
  license = Apache-2.0
  target = in_toto/models/link.py

WHOLE_REPOSITORY_VENDORING = NO
```

## IQC disposition

AION already has source attribution, event lineage, QMS and audit concepts. The useful gap is a small machine-readable model for the transformation *of external research material itself*.

```text
DESIGN_TIME_VS_RUN_TIME_LINEAGE = USEFUL
MATERIAL_PRODUCT_HASH_CHAIN = USEFUL
COMMAND_ENVIRONMENT_EVIDENCE = USEFUL
EXTERNAL_RUNTIME_DEPENDENCY = NOT_REQUIRED
CLEAN_ROOM_RECONSTRUCTION = SELECTED
```

## Materialized output

`research-labs/artifact-transformation-lineage_v0.1.0/`

This module does not execute commands or sign artifacts. It records and verifies a bounded transformation evidence chain and preserves `CANONICAL_EFFECT=NONE`.

## Local validation

```text
pytest = 14 passed
compileall = PASS
demo = PASS
```
