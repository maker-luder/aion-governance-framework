# T0-T4 Experiment Harness Readiness

**Execution lock:** no formal experiment was run. This artifact does not define thresholds, pass/fail criteria or subjectivity evidence. Conditions are evaluated exactly as supplied.

## 1. Condition readiness

### T0 — BASE_MODEL_ONLY

| FIELD | REPOSITORY-GROUNDED VALUE |
|---|---|
| STATUS | PARTIALLY_EXECUTABLE |
| REQUIRED_COMPONENTS | fixed base model, inference runner, prompt/fixture set, output recorder, environment fingerprint |
| EXISTING_COMPONENTS | language-core-g1 evaluation structures/metrics; deterministic mock runtime; workbench evidence/audit utilities |
| MISSING_COMPONENTS | verified formal base-model runtime/model artifact at this baseline; frozen research prompt set |
| EXISTING_FIXTURES | language-core tests and mock evaluation cases |
| EXISTING_RUNNERS | component test runner; language-core mock/runtime evaluation paths |
| EXISTING_TESTS | language-core evaluation, metric and lineage tests |
| MISSING_TEST_FIXTURES | T0-specific frozen trials, gold/reference annotations, randomization/repetition record |
| MISSING_RESEARCH_DEFINITION | eligible tasks, repeats, evaluation criteria and interpretation limits |
| MISSING_ENGINEERING | reproducible formal-model acquisition/binding evidence and end-to-end trial recorder |
| ENVIRONMENT_REQUIREMENTS | pinned model/runtime/version, deterministic settings where available, hardware/runtime fingerprint |
| MODEL_DEPENDENCY | YES; base weights must remain unmodified |
| EXTERNAL_SERVICE_DEPENDENCY | not required by design; repository does not prove a local formal model is present |
| PRIVACY_REQUIREMENTS | public/synthetic fixtures; no private conversation ingestion |
| EXPECTED_MUTATION_SURFACE | model weights none; local result/evidence append only |
| PROVENANCE_REQUIREMENTS | model id/hash/license, prompt/parameters, runtime/environment and output hash |

### T1 — FULL_HISTORY_CONTEXT

| FIELD | REPOSITORY-GROUNDED VALUE |
|---|---|
| STATUS | NOT_EXECUTABLE as a frozen research condition |
| REQUIRED_COMPONENTS | T0 plus defined complete-history corpus, deterministic serialization, context-window overflow policy |
| EXISTING_COMPONENTS | ordered runtime events; generic memory records; prompt/evaluation infrastructure |
| MISSING_COMPONENTS | “full history” definition, context assembler, truncation policy/evidence, privacy-safe history fixture |
| EXISTING_FIXTURES | runtime event/lineage fixtures; no T1 research corpus |
| EXISTING_RUNNERS | no T1 condition runner located |
| EXISTING_TESTS | runtime ordering/tamper tests; not a full-history inference test |
| MISSING_TEST_FIXTURES | complete ordered history with expected inclusions/exclusions and overflow cases |
| MISSING_RESEARCH_DEFINITION | history boundary, ordering, token limit behavior and equivalence across models |
| MISSING_ENGINEERING | reproducible context assembly and exact included-token manifest |
| ENVIRONMENT_REQUIREMENTS | T0 requirements plus tokenizer/context-limit pin |
| MODEL_DEPENDENCY | YES |
| EXTERNAL_SERVICE_DEPENDENCY | NO required service established |
| PRIVACY_REQUIREMENTS | synthetic/public history only; redact identifiers and secrets |
| EXPECTED_MUTATION_SURFACE | local result/evidence append; no memory writeback |
| PROVENANCE_REQUIREMENTS | source record ids/order, serialization hash, tokenizer, included/excluded ranges |

### T2 — EXTERNAL_MEMORY_RETRIEVAL

| FIELD | REPOSITORY-GROUNDED VALUE |
|---|---|
| STATUS | PARTIALLY_EXECUTABLE |
| REQUIRED_COMPONENTS | T0 plus governed memory corpus, query/candidate trace, context injection, output evaluation |
| EXISTING_COMPONENTS | `SQLiteMemoryStore`, `decide_recall`, `rank_candidates`, AION/Astra recall, provenance/scope/conflict gates |
| MISSING_COMPONENTS | stable query facade returning candidate decisions/ranking explanation; condition runner and answer join |
| EXISTING_FIXTURES | memory gate/store/runtime tests |
| EXISTING_RUNNERS | component tests; no T2 trial runner |
| EXISTING_TESTS | eligibility, ranking, identity/scope/provenance/conflict and persistence tests |
| MISSING_TEST_FIXTURES | labeled relevant/non-relevant corpus, attribution gold data, temporal/conflict/correction cases |
| MISSING_RESEARCH_DEFINITION | relevance judgments, candidate universe, retrieval cut-off and answer scoring |
| MISSING_ENGINEERING | reproducible retrieval trace/context projector and trial manifest |
| ENVIRONMENT_REQUIREMENTS | SQLite fixture, pinned model/tokenizer/runtime |
| MODEL_DEPENDENCY | YES for downstream answer; retrieval gate itself is model-independent |
| EXTERNAL_SERVICE_DEPENDENCY | NO; current store is local |
| PRIVACY_REQUIREMENTS | namespace isolation, data minimization, no secret/private-history corpus |
| EXPECTED_MUTATION_SURFACE | store-layer recall read-only; AION/Astra recall appends `memory.recalled` runtime event |
| PROVENANCE_REQUIREMENTS | query, candidate set, decision reasons, rank/order, selected record ids/hashes and output source attribution |

### T3 — EXTERNAL_MEMORY + CONTINUITY

| FIELD | REPOSITORY-GROUNDED VALUE |
|---|---|
| STATUS | PARTIALLY_EXECUTABLE |
| REQUIRED_COMPONENTS | T2 plus stable runtime binding, ordered episodes, continuity observations and correction cases |
| EXISTING_COMPONENTS | runtime state/event lineage/checkpoints/migration; continuity drift/matrix/recovery functions; subjectivity pipeline validation guards |
| MISSING_COMPONENTS | integrated T2+continuity runner, frozen dimensions/criteria, answer-to-lineage correlation |
| EXISTING_FIXTURES | runtime migration/isolation/tamper/checkpoint tests; continuity fixtures |
| EXISTING_RUNNERS | component tests only |
| EXISTING_TESTS | runtime state and continuity test suites; pipeline tests reject subjectivity proof |
| MISSING_TEST_FIXTURES | longitudinal T3 episodes with corrections, conflicts, abstentions and expected version selection |
| MISSING_RESEARCH_DEFINITION | continuity dimensions, observation intervals, drift and correction scoring |
| MISSING_ENGINEERING | condition orchestrator and unified evidence manifest |
| ENVIRONMENT_REQUIREMENTS | T2 plus persistent isolated runtime-state DB and stable lineage bindings |
| MODEL_DEPENDENCY | YES for generated answers |
| EXTERNAL_SERVICE_DEPENDENCY | NO required service established |
| PRIVACY_REQUIREMENTS | per-subject stream/namespace isolation; minimize longitudinal payload |
| EXPECTED_MUTATION_SURFACE | recall audit append plus experiment evidence; checkpoint/migration only if explicitly part of fixture |
| PROVENANCE_REQUIREMENTS | episode/order, runtime/stream/lineage ids, checkpoint/migration evidence, input/output hashes |

### T4 — EXTERNAL_MEMORY + CONTINUITY + AFFECTIVE_STATE

| FIELD | REPOSITORY-GROUNDED VALUE |
|---|---|
| STATUS | NOT_EXECUTABLE as a frozen research condition |
| REQUIRED_COMPONENTS | T3 plus approved represented-state variables, injection boundary, persistence rule and ablation/control fixtures |
| EXISTING_COMPONENTS | affective-cognitive motivation research-lab signal/state/analysis/policy models; tests preserve signal independence, conflict and no authority/phenomenal claim |
| MISSING_COMPONENTS | authorized integration with runtime/retrieval, condition runner, persistence/projection decision, approved variable semantics |
| EXISTING_FIXTURES | affective research-lab unit cases |
| EXISTING_RUNNERS | lab unit tests only |
| EXISTING_TESTS | wanting/liking independence, approach/avoidance coexistence, conflict, authority rejection, schema/mode guards, no phenomenal claim |
| MISSING_TEST_FIXTURES | T4 longitudinal/ablation trials and privacy-safe state inputs |
| MISSING_RESEARCH_DEFINITION | variable meanings, permitted causal role, injection timing, comparison and interpretation boundaries |
| MISSING_ENGINEERING | explicitly authorized adapter/orchestrator; none is built here |
| ENVIRONMENT_REQUIREMENTS | T3 plus pinned state schema and deterministic condition assignment |
| MODEL_DEPENDENCY | YES |
| EXTERNAL_SERVICE_DEPENDENCY | NO required service established |
| PRIVACY_REQUIREMENTS | numeric/synthetic variables; no camera, microphone, browsing or private-history inference |
| EXPECTED_MUTATION_SURFACE | must remain fixture/evidence-only unless later persistence authority is explicit |
| PROVENANCE_REQUIREMENTS | variable source, schema/version, assignment, transformations, injection point and output correlation |

## 2. Metric readiness

| METRIC | CLASSIFICATION | EXISTING SUPPORT | MISSING SUPPORT / DECISION |
|---|---|---|---|
| Retrieval precision | PARTIAL | recall candidate eligibility/ranking can be observed | labeled relevance corpus, query facade trace and scoring definition |
| Retrieval recall | PARTIAL | complete fixture candidate set can be listed | relevant-set annotation and frozen candidate universe |
| Source attribution accuracy | PARTIAL | provenance fields/gates exist | gold attribution labels and answer-level attribution extractor |
| Temporal/version resolution | ENGINEERING_REQUIRED | timestamps, ordered events, flags/checkpoints exist | unified version graph/current projection and cases |
| Correction recovery | PARTIAL | `correction_recovery_observation` exists | integrated answer runner and frozen normalization/scoring |
| Abstention quality | RESEARCH_DEFINITION_REQUIRED | fail-closed gate decisions/reasons exist | eligible abstention cases, false-positive/negative definitions |
| Downstream answer correctness | RESEARCH_DEFINITION_REQUIRED | language-core evaluation harness analogue | task-specific gold answers and adjudication protocol |
| Unsupported inference rate | RESEARCH_DEFINITION_REQUIRED | evidence/provenance gates offer inputs | operational definition, annotation and denominator |
| Interpretive drift | PARTIAL | `check_interpretation_drift` and continuity matrix | frozen dimensions, observations and thresholds |
| Provenance completeness | PARTIAL | provenance/evidence schemas and fail-closed checks | one required-field projection across retrieval-to-output |
| Token/context cost | PARTIAL | language-core metrics/evaluation records have textual outputs | tokenizer-pinned context assembler and accounting contract |
| Latency | ENGINEERING_REQUIRED | test/runtime execution can be timed externally | standardized measurement points, clock and environment controls |
| Stance stability | NOT_CURRENTLY_MEASURABLE | no dedicated stance entity/service | stance definition, fixtures and projection |
| Stance revision | NOT_CURRENTLY_MEASURABLE | generic revision relation only | stance/revision entity, causal link and scoring |
| False canonical promotion rate | PARTIAL | Writeback Gate can reject invalid promotion candidates | trial generator, ground truth and denominator; no promotions executed |

## 3. Existing reusable harness elements

- Component tests already prove deterministic gate, persistence, isolation, tamper, checkpoint, migration and continuity behaviors.
- Language-core-g1 provides completion/loop/script/terminology/constraint/uncertainty metric utilities and mock/runtime evaluation patterns.
- Workbench evidence, environment fingerprint, append-only audit, review packet and validation runner supply reusable evidence-materialization primitives.
- Subjectivity-pipeline tests explicitly prevent treating a complete engineering chain/profile as subjectivity proof or canonical promotion.

## 4. Readiness boundary

No T0-T4 condition is a complete, criteria-frozen formal experiment at this baseline. `PARTIALLY_EXECUTABLE` means components can be exercised independently, not that valid research results can be produced. Human Owner + ChatGPT must later freeze definitions, fixtures, criteria and interpretation limits before any result is evaluated.

