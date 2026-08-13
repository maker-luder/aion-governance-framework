# Current Reconstruction Test Results

Execution date: 2026-08-14. Evidence source: `scripts/run_component_tests.py` on the existing cleanup sandbox branch.

| Target | Tests passed | Return code |
|---|---:|---:|
| `components/aion_runtime_v0.1.0` | 13 | 0 |
| `components/astra_runtime_v0.1.0` | 7 | 0 |
| `components/astra_workbench_v1.0.0` | 89 | 0 |
| `components/continuity_governance_v0.1.0` | 7 | 0 |
| `components/encounter_governance_v0.1.0` | 8 | 0 |
| `components/executable_runtime_v0.1.0` | 13 | 0 |
| `components/governance_kernel_v0.4.0` | 46 | 0 |
| `components/identity_governance_v0.1.0` | 35 | 0 |
| `components/individual_runtime_state_v0.1.0` | 15 | 0 |
| `components/iqc_quality_inspection_v0.1.0` | 15 | 0 |
| `components/language_core_v0.1.0` | 38 | 0 |
| `components/memory_recall_governance_v0.1.0` | 19 | 0 |
| `components/research_integrity_security_v0.1.0` | 9 | 0 |
| `components/upstream_security_v0.1.0` | 33 | 0 |
| `examples/bazi-capability_v0.1.1` | 82 | 0 |
| `research-labs/affective-cognitive-motivation_v0.1.0` | 7 | 0 |
| `research-labs/language-core-g1_v0.2.1` | 67 | 0 |
| `research-labs/subjectivity-pipeline_v0.1.0` | 6 | 0 |
| `research-labs/twin-genesis-embodiment_v0.1.0` | 17 | 0 |

**Total:** 526 passed across 19 targets; all listed targets returned code 0.

The root-level `pytest -q` command is not the supported aggregate method for this monorepo because multiple targets intentionally reuse test-module basenames and some targets require target-local import paths. The per-target runner isolates each target and records its `PYTHONPATH`, test output, and return code in `qa/CURRENT_TEST_RESULTS.json.

This current local test evidence is separate from the historical 2026-08-03 source-package record of 232 passing tests and from the locked release-status evidence. It is engineering QA only; it does not establish whole-system validation, independent IV&V, canonical promotion, deployment, subjectivity, identity continuity, or relational continuity.
