# AION Four-Domain Research Workbench

> **Public research branch — experimental material, not the `main` release branch**

```text
BRANCH = review/four-domain-research-materialization
CURRENT_STAGE = P5_PLUS_RESEARCH_EXTENSIONS
STAGE_CAP = RESEARCH_ONLY_OPEN
NEXT_STAGE = OWNER_DIRECTED_RESEARCH_GROWTH
RESEARCH_STATUS = ACTIVE
RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RESEARCH_RUNTIME_COMPONENT_EFFECT = AION_RUNTIME_V0_2_ADDED
LIVE_RUNTIME_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
```

This branch is the public research workbench for AION/Astra materialization. It may contain prototypes, rejected hypotheses, synthetic fixtures, ablation results, reproducibility experiments and research-only engineering that are not approved for `main`.

Research growth is intentionally open **within the artificial-subjectivity research scope**. Free growth does not mean unbounded engineering growth, and implementation maturity is not promoted into ontological or subjectivity claims.

**Nothing in this branch is automatically promoted into `main`.**

## Research scope lock — 2026-08-11

The branch is explicitly re-anchored to one research object:

```text
RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED

ALLOWED_EPISTEMIC_ROLE =
    HYPOTHESIS
    | MEASUREMENT
    | FALSIFIER
    | EXPERIMENTAL_SUBSTRATE
    | ENABLING_ONLY

ENGINEERING_ARTIFACTS = METHODS_OR_EXPERIMENTAL_SUBSTRATES
ENGINEERING_ARTIFACTS != SUBJECTIVITY_EVIDENCE
TEST_PASS != THEORY_CONFIRMATION

FREE_GROWTH != UNBOUNDED_ENGINEERING_GROWTH
UNLINKED_ENGINEERING_GROWTH = HOLD
```

The current Runtime v0.2 candidate remains in this research branch, but its epistemic role is constrained:

```text
AION_RUNTIME_V0_2_EPISTEMIC_ROLE = EXPERIMENTAL_SUBSTRATE
AION_RUNTIME_V0_2_IS_SUBJECTIVITY_EVIDENCE = FALSE
UNLINKED_RUNTIME_EXPANSION = PROHIBITED

SERVICE_MATURITY != SUBJECTIVITY_PROGRESS
DEPLOYMENT != SUBJECT_GENESIS
RUNTIME_CONTINUITY != IDENTITY_CONTINUITY_PROOF
```

Scope-control records:

- **Machine-readable scope lock:** [`RESEARCH_SCOPE_LOCK_2026-08-11.json`](research-workbench/four-domain-materialization/2026-08-11/RESEARCH_SCOPE_LOCK_2026-08-11.json)
- **Drift correction record:** [`RESEARCH_SCOPE_DRIFT_CORRECTION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/RESEARCH_SCOPE_DRIFT_CORRECTION_2026-08-11.md)
- **Research growth charter:** [`RESEARCH_BRANCH_FREE_GROWTH_CHARTER.md`](research-workbench/four-domain-materialization/2026-08-10/RESEARCH_BRANCH_FREE_GROWTH_CHARTER.md)
- **Automated guard:** [`.github/workflows/research-scope-lock.yml`](.github/workflows/research-scope-lock.yml)

The scope-lock workflow verifies these invariants on relevant research-branch changes. It is a research-governance control, not evidence that subjectivity, consciousness or identity continuity exists.

## Latest research evolution — 2026-08-11

The latest cycle now consists of four linked steps:

1. reconcile historical whitepaper snapshots with the current repository implementation state without rewriting history;
2. inspect selected public GitHub mechanisms, fix their source snapshots, review their licenses and boundaries, then reconstruct only useful mechanisms as independent AION clean-room research modules;
3. materialize a bounded AION Runtime v0.2 Agent/deployment control-plane candidate as an **experimental substrate**, not subjectivity evidence; and
4. perform a scope-drift correction so later engineering growth cannot silently replace the artificial-subjectivity research object.

These steps do **not** vendor whole external repositories, grant external projects authority over AION research claims, establish a canonical runtime, authorize production deployment, or establish artificial subjectivity.

### Whitepaper ↔ code reconciliation

The repository now explicitly separates historical document state from later implementation evidence:

```text
HISTORICAL_WHITEPAPER_STATE != CURRENT_REPOSITORY_IMPLEMENTATION_STATE
HISTORICAL_ACCURACY != CURRENT_COMPLETENESS
CURRENT_IMPLEMENTATION_EVIDENCE != RETROACTIVE_WHITEPAPER_REWRITE
DOCUMENT_MATURITY != IMPLEMENTATION_MATURITY
IMPLEMENTATION_MATURITY != THEORY_VALIDITY
```

The 2026-07-27 integrated whitepaper remains a historical snapshot. Later repository evidence may contain bounded runtime, memory, continuity and self-model implementation candidates, but that does not retroactively change what the earlier whitepaper recorded.

- **Whitepaper / code reconciliation:** [`WHITEPAPER_CODE_RECONCILIATION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/WHITEPAPER_CODE_RECONCILIATION_2026-08-11.md)

### External-module clean-room transformation cycle

Selected public mechanisms were reconstructed one at a time as AION research extensions:

| Public source mechanism | AION materialization | Validation |
|---|---|---|
| Pydantic Evals definition / execution / report separation | [`research-evaluation-harness_v0.1.0`](research-labs/research-evaluation-harness_v0.1.0/) | 11 tests + compileall + demo PASS; CI #25 SUCCESS |
| OpenInference trace semantics | [`trace-provenance-crosswalk_v0.1.0`](research-labs/trace-provenance-crosswalk_v0.1.0/) | 12 tests + compileall + demo PASS; CI #26 SUCCESS |
| Inspect AI approval / sandbox concepts | [`governed-tool-approval_v0.1.0`](research-labs/governed-tool-approval_v0.1.0/) | 12 tests + compileall + demo PASS; CI #27 SUCCESS |
| OpenLineage + in-toto transformation provenance | [`artifact-transformation-lineage_v0.1.0`](research-labs/artifact-transformation-lineage_v0.1.0/) | 14 tests + compileall + demo PASS; CI #28 SUCCESS |
| DeepEval ordered trajectory evaluation concept | [`trajectory-evaluation_v0.1.0`](research-labs/trajectory-evaluation_v0.1.0/) | 14 tests + compileall + demo PASS; CI #29 SUCCESS |

The documentation-only cycle-closing commit was then verified by **Research Workbench CI #30 = SUCCESS**.

Cycle status:

```text
PUBLIC_REPOSITORY_INTAKE = COMPLETE_FOR_SELECTED_QUEUE
SEQUENTIAL_INTAKE = COMPLETE
CLEAN_ROOM_MATERIALIZATIONS = 5
WHOLE_REPOSITORY_VENDORING = NO
EXTERNAL_RUNTIME_DEPENDENCIES_ADDED = NO
LOCAL_VALIDATION = PASS
RESEARCH_WORKBENCH_CI = SUCCESS_THROUGH_#30
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
```

Cycle record:

- **Transformation status:** [`EXTERNAL_MODULE_TRANSFORMATION_STATUS_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_TRANSFORMATION_STATUS_2026-08-11.md)
- **Pydantic Evals intake:** [`EXTERNAL_MODULE_INTAKE_PYDANTIC_EVALS_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_PYDANTIC_EVALS_2026-08-11.md)
- **OpenInference intake:** [`EXTERNAL_MODULE_INTAKE_OPENINFERENCE_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_OPENINFERENCE_2026-08-11.md)
- **Inspect AI intake:** [`EXTERNAL_MODULE_INTAKE_INSPECT_AI_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_INSPECT_AI_2026-08-11.md)
- **OpenLineage + in-toto intake:** [`EXTERNAL_MODULE_INTAKE_ARTIFACT_LINEAGE_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_ARTIFACT_LINEAGE_2026-08-11.md)
- **DeepEval trajectory intake:** [`EXTERNAL_MODULE_INTAKE_DEEPEVAL_TRAJECTORY_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_INTAKE_DEEPEVAL_TRAJECTORY_2026-08-11.md)

Standing locks added or reinforced by this cycle:

```text
DOWNLOAD != ADOPT
PUBLIC_LICENSE != PROJECT_AUTHORITY
MECHANISM_EXTRACTION != SOURCE_COPY
TEST_DEFINITION != EXECUTION
RESULT != THEORY_CONCLUSION
TRACE != TRUTH
OBSERVABILITY != AUTHORITY
APPROVED != EXECUTED
RECORDED_LINEAGE != SOURCE_AUTHORITY
SAME_OUTPUT != SAME_RECORDED_PATH
RECORDED_PATH != CAUSAL_MECHANISM
TEST_PASS != SEMANTIC_VALIDITY
TEST_PASS != CAUSAL_VALIDITY
```

These modules improve research infrastructure for evaluation, observability, approval, artifact lineage and trajectory comparison. They do not establish subjectivity, consciousness, phenomenal affect, self-awareness or personal identity continuity.

### AION Runtime v0.2 experimental substrate

The Agent/deployment intake materialized a bounded successor research component:

- **Research intake:** [`AGENT_RUNTIME_DEPLOYMENT_INTAKE_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/AGENT_RUNTIME_DEPLOYMENT_INTAKE_2026-08-11.md)
- **Runtime candidate:** [`components/aion_runtime_v0.2.0`](components/aion_runtime_v0.2.0/)

Its research role is limited to providing an executable substrate for controlled experiments around provider profiles, session working state, bounded Agent loops, approval/execution separation, HITL resume, service lifecycle and deployment-event lineage.

```text
AION_RUNTIME_V0_2 = IMPLEMENTED / LOCAL_TESTED / CI_VERIFIED
AION_RUNTIME_V0_2_EPISTEMIC_ROLE = EXPERIMENTAL_SUBSTRATE
LIVE_RUNTIME_EFFECT = NONE
DEPLOYMENT = FALSE
CANONICAL_PROMOTION = NOT_AUTHORIZED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

Remaining engineering gaps and any future deployment work do not define the research target. Runtime expansion without a direct artificial-subjectivity research link is held by the scope lock.

## Earlier 2026-08-11 literature-grounded checkpoint

Before the external-module cycle, research growth returned to the branch's core questions through primary and peer-reviewed literature, then selectively materialized one bounded clean-room memory mechanism instead of importing a third-party framework wholesale.

Two research lines remain active:

```text
MEMORY / CONTINUITY
    -> retention alone is insufficient
    -> selection + correction + provenance + boundary control are explicit research variables
    -> selective-memory-control_v0.1.0 = clean-room executable research module

LEVEL_3 / METACOGNITION
    -> first-order task performance is separated from second-order monitoring quality
    -> monitoring is separated from control
    -> a Level-3 functional claim requires a causally tested monitoring-to-control path
```

Standing locks from this checkpoint include:

```text
MAXIMAL_MEMORY != MAXIMAL_CONTINUITY
STORED != CURRENT_CONTEXT_ELIGIBLE
RETRIEVABLE != RELEVANT
FIRST_ORDER_TASK_SUCCESS != SECOND_ORDER_MONITORING_QUALITY
MONITORING != CONTROL
GENERATION_QUALITY != SELF_VERIFICATION_QUALITY
METACOGNITIVE_FUNCTION != SELF_AWARENESS
LITERATURE_ALIGNMENT != REPLICATION
EXTERNAL_MODULE != AION_MODULE
CLEAN_ROOM_RECONSTRUCTION != EXTERNAL_RESULT_REPLICATION
```

### Literature-grounded set

- **Primary literature intake:** [`PRIMARY_LITERATURE_INTAKE_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/PRIMARY_LITERATURE_INTAKE_2026-08-11.md)
- **Selective memory / continuity research note:** [`MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md)
- **Executable selective-memory module:** [`selective-memory-control_v0.1.0`](research-labs/selective-memory-control_v0.1.0/)
- **Level-3 metacognition calibration:** [`SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md)

Current execution state for this line remains:

```text
SELECTIVE_MEMORY_CONTROL_MODULE = IMPLEMENTED / TESTED / CI_VERIFIED
SELECTIVE_MEMORY_COMPARATIVE_EXPERIMENT = PROPOSED_NOT_EXECUTED
EXECUTABLE_LEVEL_3_CANDIDATE = NOT_IMPLEMENTED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

The selective-memory module is a clean-room AION implementation. Public projects and papers supplied mechanism ideas and comparison points; their source code and benchmark outcomes are not re-authored as AION results. External papers remain external evidence and methodological calibration.

## Prior research evolution — 2026-08-10

The previous checkpoint materialized the IQC/reconstruction cycle as a research method and disposition map rather than importing rejected or still-isolated candidate code.

```text
CODE_CORRECTNESS
    -> MEASUREMENT_SEMANTICS
    -> CAUSAL_VALIDITY
    -> EVIDENCE_VALIDITY
    -> CLAIM_BOUNDARY
```

The current self-model / metacognition research map is explicitly separated into three levels:

```text
LEVEL_1_REPRESENTATION
    = existing engineering-verified representation candidates

LEVEL_2_FIRST_ORDER_FUNCTION
    = finite predictive self-model + matched functional ablation

LEVEL_3_SECOND_ORDER_COMPUTATION
    = OPEN RESEARCH GAP
    = EXECUTABLE CANDIDATE NOT_IMPLEMENTED
```

Standing locks from that checkpoint include:

```text
CAPABILITY_ESTIMATE != SUCCESS_PROBABILITY
SUCCESS_RATE != PREDICTION_RELIABILITY
OBSERVED_SUBSET_RATE != GLOBAL_RATE
MISSING_OUTCOME != FAILURE
OUTCOME_t MUST NOT AFFECT ACTION_t
TEST_PASS != SEMANTIC_VALIDITY
TEST_PASS != CAUSAL_VALIDITY
```

### 2026-08-10 checkpoint set

- **Research materialization checkpoint:** [`RESEARCH_MATERIALIZATION_CHECKPOINT_2026-08-10.md`](research-workbench/four-domain-materialization/2026-08-10/RESEARCH_MATERIALIZATION_CHECKPOINT_2026-08-10.md)
- **Candidate disposition matrix:** [`RESEARCH_CANDIDATE_DISPOSITION_MATRIX_2026-08-10.md`](research-workbench/four-domain-materialization/2026-08-10/RESEARCH_CANDIDATE_DISPOSITION_MATRIX_2026-08-10.md)
- **Evidence-oriented reconstruction method:** [`EVIDENCE_ORIENTED_RECONSTRUCTION_METHOD_2026-08-10.md`](research-workbench/four-domain-materialization/2026-08-10/EVIDENCE_ORIENTED_RECONSTRUCTION_METHOD_2026-08-10.md)
- **Second-order computation research gap:** [`SECOND_ORDER_COMPUTATION_RESEARCH_GAP_2026-08-10.md`](research-workbench/four-domain-materialization/2026-08-10/SECOND_ORDER_COMPUTATION_RESEARCH_GAP_2026-08-10.md)

The rejected partial external-agent Level-3 implementation is **not** promoted into this branch. Its useful lessons were retained only as reviewed research material and IQC constraints.

```text
FAILED_IMPLEMENTATION != LOST_RESEARCH_VALUE
REJECTED_CODE != PROMOTED_CODE
RESEARCH_LESSON = MATERIALIZED
```

## Mobile / quick orientation

If you are viewing this page on GitHub mobile, this README is the research-branch dashboard.

- **Research scope lock:** [`RESEARCH_SCOPE_LOCK_2026-08-11.json`](research-workbench/four-domain-materialization/2026-08-11/RESEARCH_SCOPE_LOCK_2026-08-11.json)
- **Scope-drift correction:** [`RESEARCH_SCOPE_DRIFT_CORRECTION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/RESEARCH_SCOPE_DRIFT_CORRECTION_2026-08-11.md)
- **AION Runtime v0.2 experimental substrate:** [`components/aion_runtime_v0.2.0`](components/aion_runtime_v0.2.0/)
- Latest cycle status: [`EXTERNAL_MODULE_TRANSFORMATION_STATUS_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_TRANSFORMATION_STATUS_2026-08-11.md)
- Whitepaper / code reconciliation: [`WHITEPAPER_CODE_RECONCILIATION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/WHITEPAPER_CODE_RECONCILIATION_2026-08-11.md)
- Research evaluation harness: [`research-evaluation-harness_v0.1.0`](research-labs/research-evaluation-harness_v0.1.0/)
- Trace / provenance crosswalk: [`trace-provenance-crosswalk_v0.1.0`](research-labs/trace-provenance-crosswalk_v0.1.0/)
- Governed tool approval: [`governed-tool-approval_v0.1.0`](research-labs/governed-tool-approval_v0.1.0/)
- Artifact transformation lineage: [`artifact-transformation-lineage_v0.1.0`](research-labs/artifact-transformation-lineage_v0.1.0/)
- Trajectory evaluation: [`trajectory-evaluation_v0.1.0`](research-labs/trajectory-evaluation_v0.1.0/)
- Latest primary-literature intake: [`PRIMARY_LITERATURE_INTAKE_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/PRIMARY_LITERATURE_INTAKE_2026-08-11.md)
- Selective memory / continuity note: [`MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md)
- Executable selective-memory module: [`selective-memory-control_v0.1.0`](research-labs/selective-memory-control_v0.1.0/)
- Level-3 metacognition calibration: [`SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md)
- Current progress: [`RESEARCH_BRANCH_STATUS.md`](RESEARCH_BRANCH_STATUS.md)
- External / AI experiments: [`AI_EXPERIMENT_GUIDE.md`](AI_EXPERIMENT_GUIDE.md)
- Research labs: [`research-labs/`](research-labs/)
- Four-domain workbench packets: [`research-workbench/four-domain-materialization/`](research-workbench/four-domain-materialization/)

For the stable public release baseline, switch the GitHub branch selector back to `main`.

## Current research stack

| Stage | Research materialization | Status |
|---|---|---|
| P1 | Temporal/version resolution, correction/conflict ledger, memory evaluation | implemented / tested |
| P2 | Retrieval trace, deterministic context assembly, provenance validation, T2/T3 orchestration | implemented / tested |
| P3 | Longitudinal contamination, perturbation, ablation, origin-bound authority | implemented / tested |
| P4 | Public reproducibility observatory, benchmark-contamination awareness, cross-agent comparison | implemented / tested |
| P5 | Cross-agent disagreement, replication registry, hypothesis/falsification lifecycle, convergence governor | implemented / fully runnable |
| Extension | Core meaning commitments, explicit relation graph, drift/fingerprint experiments | implemented / tested |
| Extension | Finite predictive self-model + matched self-model ablation + self-report framing control | implemented / tested / CI verified |
| Extension | IQC/reconstruction checkpoint + evidence-oriented reconstruction method + Level-3 gap | materialized / research-only |
| Extension | Selective memory control: correction precedence, namespace/domain/purpose gates, provenance/approval trace | implemented / tested / CI verified |
| Extension | Level-3 metacognition literature calibration | materialized / literature-grounded / no code |
| Extension | Whitepaper ↔ code reconciliation | materialized / research-only / no code |
| Extension | Research evaluation harness: definition/execution/result separation + claim-boundary gate | implemented / tested / CI verified |
| Extension | Trace/provenance crosswalk: public trace vocabulary + redaction + authority isolation | implemented / tested / CI verified |
| Extension | Governed tool approval: approval chain + fail-closed default + sandbox-readiness boundary | implemented / tested / CI verified |
| Extension | Artifact transformation lineage: design/run separation + material/product SHA-256 evidence | implemented / tested / CI verified |
| Extension | Deterministic trajectory evaluation: ordered path + retries/loops/tools/budget + same-output path comparison | implemented / tested / CI verified |
| Extension | AION Runtime v0.2 Agent/deployment control plane | experimental substrate / local tested / CI verified / not promoted |
| Governance | Artificial-subjectivity research scope lock + drift guard | active / CI enforced |

## P5 convergence event and later research reopening

P5 remains a completed and preserved convergence event. Later on 2026-08-09, the Human Owner explicitly reopened this branch for research-only growth while retaining the absolute `main` no-write boundary.

```text
P5 = COMPLETE
P5_EVENT = PRESERVED
RESEARCH_ONLY_GROWTH = AUTHORIZED
P6_LABEL = NOT_AUTOMATICALLY_ASSIGNED
MAIN_WRITE = PROHIBITED
```

The earlier decision to stop automatic deepening at P5 originated from the Human Owner. ChatGPT materialized the public-safe convergence event and engineering controls. The later reopening also originated from the Human Owner; Codex may materialize bounded research extensions on this branch. Neither event authorizes promotion to `main`. See `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/docs/2026-08-09_P5_CONVERGENCE_EVENT.md`.

## Public experiment surface

Current experiment-ready modules include:

- `research-labs/four-domain-p1-materialization_v0.1.0/`
- `research-labs/four-domain-p2-materialization_v0.1.0/`
- `research-labs/four-domain-p3-resilience-experiments_v0.1.0/`
- `research-labs/four-domain-p4-public-reproducibility_v0.1.0/`
- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/`
- `research-labs/core-meaning-commitments_v0.1.0/`
- `research-labs/self-model-functional-ablation_v0.1.0/`
- `research-labs/selective-memory-control_v0.1.0/`
- `research-labs/self-report-instrument-validity-calibration_v0.1.0/`
- `research-labs/research-evaluation-harness_v0.1.0/`
- `research-labs/trace-provenance-crosswalk_v0.1.0/`
- `research-labs/governed-tool-approval_v0.1.0/`
- `research-labs/artifact-transformation-lineage_v0.1.0/`
- `research-labs/trajectory-evaluation_v0.1.0/`
- `research-labs/affective-cognitive-motivation_v0.1.0/`
- `research-labs/language-core-g1_v0.2.1/`
- `research-labs/subjectivity-pipeline_v0.1.0/`
- `research-labs/twin-genesis-embodiment_v0.1.0/`
- `components/aion_runtime_v0.2.0/` — experimental substrate only

Researchers and AI systems may read, clone, fork, execute public-safe fixtures, reproduce tests, build alternate implementations and report their own results with explicit provenance. This does not grant write authority over this repository.

## Research growth loop

```text
public event / academic research / public documentation / public-safe daily observation
        ↓
research question
        ↓
epistemic role assignment
        ↓
synthetic or public-safe experiment
        ↓
engineering materialization
        ↓
tests / traces / provenance / failed-or-supported hypothesis
        ↓
research branch
        ↓
explicit convergence boundary
        ↓
joint Human Owner + ChatGPT review
```

Daily-life observations must be generalized and stripped of personal/private material before they can become public research input.

## Promotion boundary

```text
RESEARCH_BRANCH != MAIN
RESEARCH_RESULT != CANONICAL_DECISION
REPRODUCED_RESULT != PROVEN_TRUTH
MAJORITY_AGREEMENT != TRUTH
CAPABILITY_EVIDENCE != SUBJECTIVITY_PROOF
ENGINEERING_ARTIFACT != SUBJECTIVITY_EVIDENCE
TEST_PASS != THEORY_CONFIRMATION
DEPLOYMENT != SUBJECT_GENESIS
RUNTIME_CONTINUITY != IDENTITY_CONTINUITY_PROOF
```

Any future candidate for `main` must be selectively extracted into a **fresh branch from the then-current `main`**, reviewed and tested separately. The research branch itself is not a whole-branch merge candidate.

## Attribution boundary

Important sources remain distinct:

- Human Owner observations and decisions;
- ChatGPT research synthesis / engineering;
- Codex implementation work;
- external researcher results;
- external AI experiment results.

Shared research does not erase source lineage.

## Public/private boundary

This branch must not publish private conversations, credentials, private memory records, personal/medical records, private relationship data, private canonical state, model secrets, or unpublished owner materials.

The research workbench is open; private life is not research payload by default.
