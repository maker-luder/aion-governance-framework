# External Module Transformation Status — 2026-08-11

Status: `RESEARCH_ONLY / SEQUENTIAL_INTAKE_ACTIVE / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

The Human Research Owner approved sequential retrieval and transformation of suitable public GitHub mechanisms. This file tracks the current conversion queue without granting automatic promotion authority.

| Order | External source | Fixed source | AION materialization | Local status | Promotion |
|---|---|---|---|---|---|
| 1 | `pydantic/pydantic-ai` / Pydantic Evals | `d995cfee9f…` / MIT | `research-evaluation-harness_v0.1.0` | 11 tests + compileall + demo PASS | NONE |
| 2 | `Arize-ai/openinference` | `44cdf7996e…` / Apache-2.0 | `trace-provenance-crosswalk_v0.1.0` | 12 tests + compileall + demo PASS | NONE |
| 3 | `UKGovernmentBEIS/inspect_ai` | pending fixed snapshot | governed tool approval / sandbox evaluation candidate | NOT YET MATERIALIZED | NONE |
| 4 | `OpenLineage/OpenLineage` + `in-toto/in-toto` | pending fixed snapshots | artifact transformation lineage candidate | NOT YET MATERIALIZED | NONE |
| 5 | `confident-ai/deepeval` | pending fixed snapshot | trajectory evaluation candidate | NOT YET MATERIALIZED | NONE |

Standing rule:

```text
DOWNLOAD != ADOPT
PUBLIC_LICENSE != PROJECT_AUTHORITY
MECHANISM_EXTRACTION != SOURCE_COPY
LOCAL_TEST_PASS != CANONICAL_PROMOTION
```
