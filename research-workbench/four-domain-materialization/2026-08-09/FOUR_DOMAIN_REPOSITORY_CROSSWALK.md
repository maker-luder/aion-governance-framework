# Four-Domain Repository Crosswalk

**Workbench status:** engineering fact extraction only; `CANONICAL_EFFECT = NONE`.

**Epistemic locks:** `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`; `CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED`; `PHENOMENAL_AFFECT = NOT_ESTABLISHED`; `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`.

This crosswalk preserves the required direction: human research construct -> LLM-relevant question -> memory/LLM engineering operation -> software/governance control. A row is not a claim of biological or mechanistic equivalence. Repository paths are relative to the repository root. The source of truth for implementation status is executable code plus tests at the protected baseline; descriptive documents are marked as such.

## A. Four-domain transformation

| CONSTRUCT | DOMAIN_1_SOURCE_CONCEPT | DOMAIN_2_LLM_QUESTION | DOMAIN_3_ENGINEERING_OPERATION | DOMAIN_4_GOVERNANCE_CONTROL |
|---|---|---|---|---|
| Episodic memory | Event-specific recollection | Can an inference be supplied a subject-bound, ordered event record? | Persist and retrieve event/episode records | Bind agent, stream, runtime instance and provenance; audit access |
| Semantic memory | Generalized knowledge | Can reusable propositions be retrieved without implying lived recollection? | Store/query typed semantic records | Separate record type, source, namespace, revision and authority |
| Working memory / context limitation | Capacity-limited active information | Which selected records fit the current context budget? | Candidate selection, ranking and context assembly | Enforce read scope, privacy, deterministic selection evidence and cost limits |
| Source monitoring | Attribution of remembered content | Can output distinguish source, channel and evidential status? | Carry source/provenance with record and response | Fail closed on missing/conflicting provenance; never equate recall with truth |
| Memory updating | Incorporation of later information | Can a later record revise active retrieval without erasing history? | Append revision/supersession relation and project current state | Require writeback approval, evidence and immutable history |
| Correction | Recovery from an incorrect representation | Can a correction be linked to the corrected claim and affect later answers? | Create correction record and correction link; filter/rank accordingly | Attribute actor/evidence/time; preserve audit and rollback |
| Continued influence of corrected information | Persistence of outdated information | Does a superseded record still affect retrieval or answers? | Compare retrieval/output before and after correction | Freeze test condition and track both old/new record lineage |
| Salience / accessibility | Differential availability | Which records become more likely to enter context and why? | Governed ranking signal and explanation | Bound allowed signals; prevent relationship-derived privilege |
| Forgetting / interference | Reduced access or competition | Do competing or aged records reduce retrieval in a reproducible way? | Retention/access policy or interference test harness | Preserve deletion/tombstone provenance and owner authority |
| Reconsolidation / reactivation analogue | Change following reactivation | Does retrieval trigger a revision candidate without silently rewriting content? | Separate audited read from explicit revision proposal | Prohibit automatic writeback; record causal evidence or `UNKNOWN_PROCESS` |
| Memory importance | Priority assigned to a record | Is priority explicit, stable and source-attributed? | Store importance signal and ranking contribution | Define who may set/change it and record change history |
| Confidence | Degree of support/uncertainty | Can record confidence and output confidence be represented separately? | Typed confidence with basis and calibration evidence | Prevent confidence from granting authority or canonical status |
| Interpretation | Meaning assigned to evidence | Can multiple interpretations remain distinguishable and revisable? | Record analysis channel/perspective and evidence references | Preserve attribution, disagreement and writeback gate |
| Stance | Current answer-position or policy posture | Can a current stance be projected without treating it as immutable truth? | Typed stance record/current projection | Bind subject/namespace and distinguish candidate from canonical state |
| Stance revision | Change to a stance | Can the cause and sequence of stance changes be reconstructed? | Append revision relation with before/after references | Evidence, actor, approval, temporal order and rollback |
| Affective-cognitive represented state | Represented motivational/affective signals | Can non-phenomenal state variables influence analysis without claiming emotion? | Maintain independent bounded signals and conflict analysis | No authority from affect; no automatic persistence/canonicalization |
| Continuity | Stability/change across observations | Can engineering continuity dimensions be measured without identity proof? | Compare ordered observations and produce drift/correction results | Keep lineage binding, thresholds and conclusions separately governed |
| Provenance | Origin and transformation trace | Can each retrieved/asserted item be traced to a source and operation? | Attach source/evidence/hash/relation metadata | Validate completeness; reject inferred authority from relationship |
| Correction recovery | Use of corrected rather than old content | Does a later response recover after explicit correction? | Compare normalized before/after outputs | Frozen fixtures/criteria, provenance and abstention handling |
| Conflict | Incompatible records or goals | Can conflict be represented and surfaced rather than silently resolved? | Conflict flag/detection and abstention/ranking behavior | Fail closed; reserve resolution authority; retain both sources |
| Abstention | Withholding unsupported output | Does the system decline retrieval/use when gates fail? | Return rejected decision/reason or constrained output | Missing provenance/conflict/scope causes fail-closed result |
| Temporal/version resolution | Selection among versions over time | Can the system identify the applicable/current version and explain why? | Ordered versions, revision graph and current projection | Immutable timestamps/hashes; authority over promotion and rollback |

## B. Repository implementation evidence

| CONSTRUCT | CURRENT_REPOSITORY_PATHS | CURRENT_TYPES_OR_MODELS | CURRENT_FUNCTIONS_OR_SERVICES | CURRENT_TESTS | SOURCE_OF_TRUTH | IMPLEMENTATION_STATUS |
|---|---|---|---|---|---|---|
| Episodic memory | `components/individual_runtime_state_v0.1.0/`; `components/astra_workbench_v1.0.0/src/astra_engineering_workbench/episodic_adapter.py` | runtime event rows; `IndividualRuntimeContext`; episodic writer protocol | `append_event`, `events`, `EpisodicCoreAdapter.record/validate_stream` | runtime-state `test_store.py`; workbench adapter tests | Code + tests | REUSABLE_EXISTING_SERVICE |
| Semantic memory | `docs/MEMORY_LAYER_MODEL.md`; memory-recall component | `MemoryRecord`, `StoredMemory` (not explicitly semantic) | SQLite store `write/get/list_for_identity/recall` | memory store/gate tests | Code for generic records; document for layer label | PARTIAL_OVERLAP |
| Working memory / context limitation | memory recall gate; language-core-g1 metrics | `RecallRequest`, `RecallDecision`; evaluation records | `rank_candidates`, `decide_recall`; token/loop metrics | recall gate tests; language-core metric tests | Code + tests | PARTIAL_OVERLAP |
| Source monitoring | memory recall models; research-integrity; identity governance models | provenance fields; `EvidenceRecord`; `SourceProvenance` | `decide_recall`, `assess_evidence`, `evaluate_writeback` | recall, integrity and identity-governance tests | Code + tests | REUSABLE_WITH_ADAPTER |
| Memory updating | memory store; provenance schema | tombstone/superseded/conflict flags; `REVISION_OF` relation in schema | `write`, `tombstone`, `supersede`, `set_conflict` | `test_persistent_store.py` | Code + schema + tests | PARTIAL_OVERLAP |
| Correction | continuity checks; interpretation-governance document; memory flags | `DimensionObservation`; correction references documented, not a complete correction entity | `correction_recovery_observation`; store flag setters | continuity tests; store tests | Code + tests; descriptive doc is non-executable | PARTIAL_OVERLAP |
| Continued influence of corrected information | no dedicated implementation located | none | none | none | Repository search at baseline | RESEARCH_DEFINITION_REQUIRED |
| Salience / accessibility | affective-cognitive research lab; recall ranking | `MotivationalSignal.salience`; relevance on memory record | `MotivationalStateEngine.analyze`; `rank_candidates` | affective lab tests; recall tests | Code + tests | PARTIAL_OVERLAP |
| Forgetting / interference | tombstone support only | tombstone flag | `tombstone`; recall gate rejects tombstoned records | memory tests | Code + tests | DESIGN_GAP |
| Reconsolidation / reactivation analogue | runtime recall and memory write are separate operations | runtime/memory events | runtime `recall` appends audit event; `remember` writes explicitly | runtime tests | Code + tests | RESEARCH_DEFINITION_REQUIRED |
| Memory importance | no memory importance field located | none; salience is an affective-lab signal, not record importance | none | none | Repository search + model inspection | DESIGN_GAP |
| Confidence | identity analysis channel; interpretation docs; Bazi example | `AnalysisChannel.confidence_optional`; domain-specific confidence | perspective comparison; domain-specific evaluators | identity and Bazi tests | Code + tests, but not governed memory confidence | PARTIAL_OVERLAP |
| Interpretation | identity governance; continuity governance; workbench interpretation doc | `AnalysisChannel`, `PerspectiveEventRecord`, continuity dimensions | `compare_channels`, `check_interpretation_drift` | identity/continuity tests | Code + tests | REUSABLE_WITH_ADAPTER |
| Stance | no dedicated stance service located | none | none | none | Repository search at baseline | RESEARCH_DEFINITION_REQUIRED |
| Stance revision | provenance relation can express revision, but no stance entity | provenance schema `REVISION_OF` | no stance-revision service | schema validation only | Schema + search | DESIGN_GAP |
| Affective-cognitive represented state | `research-labs/affective-cognitive-motivation_v0.1.0/` | `MotivationalSignal`, `MotivationalState`, `StateAnalysis`, conflict kinds | `MotivationalStateEngine.analyze/preserve_domains`; policy `evaluate` | lab tests cover independence, conflict, authority rejection and no phenomenal claim | Research-lab code + tests | REUSABLE_WITH_ADAPTER |
| Continuity | `components/continuity_governance_v0.1.0/`; runtime state | continuity layers/dimensions/matrix; stable runtime bindings | drift/matrix/status functions; runtime verification/migration | continuity and runtime-state tests | Code + tests | ALREADY_IMPLEMENTED |
| Provenance | identity governance; research integrity; workbench evidence/audit; schemas | `SourceProvenance`, `EvidenceRecord`, `LineageEvent`, evidence references | `assess_evidence`, `evaluate_writeback`, evidence load/save, ledger append/verify | component tests | Code + tests + schema | REUSABLE_EXISTING_SERVICE |
| Correction recovery | continuity governance | `DimensionObservation`, `DriftResult` | `correction_recovery_observation` | `test_continuity.py` | Code + tests | ALREADY_IMPLEMENTED |
| Conflict | memory recall; affective lab; research integrity | memory conflict flag; `ConflictKind`; evidence conflict | recall rejection; motivational conflict analysis; evidence assessment | corresponding component tests | Code + tests | REUSABLE_WITH_ADAPTER |
| Abstention | recall gate; research integrity; governance kernel | rejected `RecallDecision`; evidence/gate decisions; pipeline decision | `decide_recall`, `assess_evidence`, `authorize_action`, `evaluate_risk` | gate/policy tests | Code + tests | REUSABLE_EXISTING_SERVICE |
| Temporal/version resolution | runtime lineage/checkpoints; memory recorded time and flags | ordered runtime events; checkpoints; `recorded_at`; superseded flag | `events`, `checkpoint`, `rollback_to_checkpoint`, store filters | runtime-state and memory tests | Code + tests | PARTIAL_OVERLAP |

## C. Provenance, authority, limitations and pending decisions

| CONSTRUCT | PROVENANCE_BEHAVIOR | AUTHORITY_BEHAVIOR | KNOWN_LIMITATIONS | RESEARCH_DECISION_REQUIRED |
|---|---|---|---|---|
| Episodic memory | Runtime events are hashed/ordered and bound to lineage | Append is explicit; workbench adapter validates stream | Not a human-memory-equivalence model | Define experimental episode/unit and retrieval semantics |
| Semantic memory | Generic records carry provenance | Write requires `writeback_approved` | No executable semantic-vs-episodic type distinction | Define record taxonomy and truth/update rules |
| Working memory / context limitation | Recall decision contains reason | Scope/provenance/conflict gates restrict candidates | No context assembler or explicit budget contract | Define context unit, budget and reproducibility evidence |
| Source monitoring | Provenance is required by several gates | Relationship does not grant action authority | Provenance output is not uniformly returned to callers | Define attribution metric and response presentation |
| Memory updating | New writes and flags exist | Writeback gate is authoritative for canonical change | Flag transitions omit complete actor/reason/evidence history | Define immutable revision object and projection rules |
| Correction | Correction-recovery observation is attributable to inputs | No automatic canonical correction | No end-to-end correction entity/flow | Define correction semantics, actor authority and evidence minimum |
| Continued influence | No dedicated provenance behavior | No resolution authority exists | No fixture, runner or metric implementation | Define operational condition and outcome measure |
| Salience / accessibility | Signals can be traced within affective state inputs | Affective policy denies authority gain | Recall ranking reason does not expose a salience decomposition | Define permitted ranking signals and explanation |
| Forgetting / interference | Tombstone is observable as a flag | Deletion/retention authority is not fully modeled here | No decay/interference mechanism; tombstone is not forgetting equivalence | Define whether this is simulation, policy or experiment-only construct |
| Reconsolidation analogue | Recall and write are separate auditable calls | Recall does not authorize writeback | Runtime recall appends an observation event but no causal revision link | Define analogue and prohibit category error with biological reconsolidation |
| Memory importance | None | None | Absent from governed memory model | Define meaning, setter authority and change history |
| Confidence | Some domain/channel records retain confidence/basis | Confidence grants no canonical authority | No unified memory-confidence semantics/calibration | Define layers and calibration protocol |
| Interpretation | Perspective channels retain attribution | Writeback remains separately gated | No unified current interpretation projection | Define disagreement and revision behavior |
| Stance | None | None | No stable entity or projection | Define stance vs answer vs policy |
| Stance revision | Generic revision relation is available | Canonical promotion remains gated | No actor/time/reason-complete stance history | Define entity, causes, authority and stability metric |
| Affective-cognitive state | Input signals and analysis remain represented data | Policy rejects affect-derived authority | Lab model does not establish phenomenal affect; no approved persistence | Decide experimental variables and persistence prohibition/conditions |
| Continuity | Observations and runtime lineage are inspectable | Engineering continuity does not confer identity authority | Thresholds/ontological interpretation are not established | Freeze dimensions and criteria before experiments |
| Provenance | Evidence, source, hash and lineage structures exist | Missing/conflicting provenance fails closed in relevant gates | Structures are distributed; no single query facade | Define minimum projection for future application contract |
| Correction recovery | Inputs/results are explicit | Function observes; it does not promote state | Metric threshold and end-to-end answer harness absent | Freeze normalized comparison and scoring criteria |
| Conflict | Sources/flags may be retained | Conflict can block recall/writeback | Flag mutation lacks complete transformation history | Define resolver authority, abstention and current projection |
| Abstention | Gate reason can be recorded | Fail-closed decisions are implemented in several components | No cross-component abstention-quality metric | Define eligible cases and scoring |
| Temporal/version resolution | Runtime order/checkpoint hashes are preserved | Rollback/migration are explicit operations | Memory revision graph/current projection is incomplete | Define applicable-time semantics and tie/conflict rules |

## D. Boundary findings

- No repository evidence supports collapsing human cognitive terminology directly into code semantics.
- `MotivationalSignal.salience` is not governed-memory importance and is not phenomenal affect evidence.
- A runtime event stream is an episodic engineering analogue, not evidence of recollective experience.
- Generic provenance `REVISION_OF` support does not supply a complete correction or stance-revision service.
- Engineering continuity, shared schemas and stable identifiers do not establish ontological identity continuity.
- Missing constructs remain `DESIGN_GAP` or `RESEARCH_DEFINITION_REQUIRED`; no missing process is inferred.

## E. Attribution

- **HUMAN_OWNER:** research direction, authorization, acceptance/rejection and later canonical decisions.
- **ChatGPT:** prior formalization/review only where source artifacts record it.
- **Codex:** repository inspection and this fact-extraction workbench artifact.
- **JOINT / EXTERNAL_SOURCE:** only where explicit source evidence supports those labels; none is newly asserted here.

