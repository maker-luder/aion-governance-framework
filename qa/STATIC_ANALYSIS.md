# Static Analysis

## Current cleanup-sandbox evidence — 2026-08-14

The following results are **Manus-local QA evidence** from the existing `cleanup/manus-output-consolidation-20260813` branch. They are supplemental, non-canonical engineering evidence; they are not a GitHub Actions result, an independent IV&V result, a release decision, or scientific validation.

| Scope | Tool or gate | Result | Evidence boundary |
|---|---|---|---|
| Runtime components | `mypy` strict through `scripts/run_runtime_strong_qa.sh` | **PASS** for AION Runtime, Astra Runtime, twin AION/Astra Runtime, and Individual Runtime State | Type-check evidence only; does not establish canonical promotion or whole-system validation |
| Runtime components | Branch-aware coverage through `scripts/run_runtime_strong_qa.sh` | **PASS**, each changed Runtime component at or above the pre-established `80%` threshold | Test-path coverage only; does not establish performance, recoverability, or scientific validity |
| Runtime packages | Wheel build, clean virtual environment, cold `--no-index` wheelhouse install, and cold import smoke | **PASS** for the eight Strong-QA package builds | Local reproducibility evidence only; no package publication is performed |
| Main Language Core | `mypy` strict and Ruff | **PASS**; 17 mypy source files and configured source/test Ruff scope | Current sandbox result; not a main-branch result |
| G1 Language Core mirror | `mypy` strict, Ruff, compileall, and tests | **PASS**; 23 mypy source files, configured source/test scopes, and 67 tests | Research-lab mirror remains a sandbox derivative; no research promotion is implied |
| Identity Governance and Upstream Security | Ruff configured scopes | **PASS** | Lint evidence only |
| Language Core regression | Main and G1 test suites | **PASS**; 38 main tests and 67 G1 tests | Component regression evidence only |
| Repository hygiene | `git diff --check` on the current sandbox worktree | **PASS** | Worktree hygiene only |

The G1 offline tokenizer/telemetry fixture is deliberately recorded separately as `OFFLINE_CONTRACT_ONLY`. It pins the paired dataset hash, validates UTF-8 character-level sample provenance, checks the local non-streaming Ollama telemetry contract, and keeps token counts, model scores, benchmark execution, and streaming parity explicitly unexecuted.

## Historical and release-status boundaries

The current local results do not rewrite historical release evidence. In particular, `qa/CURRENT_RELEASE_STATUS_LOCK.json` and `qa/RELEASE_EVIDENCE.json` retain their earlier `NOT_EXECUTED_TOOL_UNAVAILABLE` fields for the locked release evidence set. That distinction is intentional: a later cleanup-sandbox run cannot retroactively change the exact-head release record, Owner decision, CI record, or independent verification status.

`compileall`, mypy, Ruff, tests, coverage, wheel builds, and offline installation remain **engineering QA**. They do not establish `WHOLE_SYSTEM_VALIDATION`, `INDEPENDENT_IVV`, `SUBJECTIVITY_CONCLUSION`, `CANONICAL_EFFECT`, `DEPLOYMENT`, or release-license selection. The current status remains subject to the existing Owner, release, C0, research, and canonical-promotion gates.

## Reproducibility references

- Runtime Strong QA method: `scripts/run_runtime_strong_qa.sh`
- Main Language Core package: `components/language_core_v0.1.0/`
- G1 mirror package: `research-labs/language-core-g1_v0.2.1/`
- G1 offline fixture: `research-labs/language-core-g1_v0.2.1/evaluation/OFFLINE_TOKENIZER_TELEMETRY_FIXTURE.json`
- G1 fixture builder and tests: `research-labs/language-core-g1_v0.2.1/evaluation/build_offline_tokenizer_fixture.py` and `research-labs/language-core-g1_v0.2.1/tests/test_offline_tokenizer_fixture.py`

No unavailable tool is reported as passed, and no local pass is represented as an independent or canonical result.
