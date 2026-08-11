# External Module Transformation Status — 2026-08-11

Status: `RESEARCH_ONLY / SEQUENTIAL_INTAKE_MATERIALIZED / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

The Human Research Owner approved sequential retrieval and transformation of suitable public GitHub mechanisms. This file tracks the current conversion queue without granting automatic promotion authority.

| Order | External source | Fixed source | AION materialization | Validation status | Promotion |
|---|---|---|---|---|---|
| 1 | `pydantic/pydantic-ai` / Pydantic Evals | `d995cfee9f…` / MIT | `research-evaluation-harness_v0.1.0` | 11 tests + compileall + demo PASS; CI #25 SUCCESS | NONE |
| 2 | `Arize-ai/openinference` | `44cdf7996e…` / Apache-2.0 | `trace-provenance-crosswalk_v0.1.0` | 12 tests + compileall + demo PASS; CI #26 SUCCESS | NONE |
| 3 | `UKGovernmentBEIS/inspect_ai` | `6c5b888f95…` / MIT | `governed-tool-approval_v0.1.0` | 12 tests + compileall + demo PASS; CI #27 SUCCESS | NONE |
| 4 | `OpenLineage/OpenLineage` + `in-toto/in-toto` | `c54b98bd66…` + `a8ce9ee212…` / Apache-2.0 | `artifact-transformation-lineage_v0.1.0` | 14 tests + compileall + demo PASS; CI #28 SUCCESS | NONE |
| 5 | `confident-ai/deepeval` | `f97964445c…` / Apache-2.0 | `trajectory-evaluation_v0.1.0` | 14 tests + compileall + demo PASS; CI pending | NONE |

Standing rule:

```text
DOWNLOAD != ADOPT
PUBLIC_LICENSE != PROJECT_AUTHORITY
MECHANISM_EXTRACTION != SOURCE_COPY
LOCAL_TEST_PASS != CANONICAL_PROMOTION
APPROVED != EXECUTED
RECORDED_LINEAGE != SOURCE_AUTHORITY
SAME_OUTPUT != SAME_RECORDED_PATH
RECORDED_PATH != CAUSAL_MECHANISM
```
