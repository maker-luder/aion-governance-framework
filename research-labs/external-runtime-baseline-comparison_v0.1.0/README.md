# External Runtime Baseline Comparison — v0.1.0

Status: `RESEARCH_ONLY / STATIC_BASELINES + REVIEWED_HERMES_P0_MECHANISM_RESULTS / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

This module compares downloadable external agent/memory runtimes against existing AION whitepaper and governance distinctions. It does **not** adopt, vendor, wrap or grant authority to any upstream runtime.

## Research object

```text
QUESTION:
Which observed behaviors arise from ordinary engineering mechanisms such as
persistent storage, profile cloning, shared memory, model/provider substitution,
scheduler state, checkpoint restoration, provenance ledgers, correction events,
context compression, multi-agent transport and sandbox boundaries?

AND:
Which stronger AION claims remain unestablished after those mechanisms are accounted for?
```

## Registered baselines

```text
P0 Hermes Agent
P1 OpenHands
P1 Letta
P1 LangGraph
P2 Mem0
```

Source-fixed registry:

- `research-workbench/four-domain-materialization/2026-08-12/DOWNLOADABLE_EXTERNAL_RUNTIME_REGISTRY_2026-08-12.md`
- `research-workbench/four-domain-materialization/2026-08-12/external_runtime_baselines_v0.1.0.json`

Hermes source crosswalks:

- `research-workbench/four-domain-materialization/2026-08-12/HERMES_AGENT_EXTERNAL_RUNTIME_BASELINE_2026-08-12.md`
- `research-workbench/four-domain-materialization/2026-08-12/HERMES_V020_RESEARCH_DELTA_2026-08-12.md`

Preregistration and preparation:

- `research-workbench/four-domain-materialization/2026-08-12/EXTERNAL_RUNTIME_EXPERIMENT_MATRIX_2026-08-12.md`
- `research-workbench/four-domain-materialization/2026-08-12/HERMES_P0_EXECUTION_PREPARATION_CHECKPOINT_2026-08-12.md`
- `research-labs/hermes-p0-execution-prep_v0.1.0/`

Reviewed empirical extraction:

- `RESULTS.md`
- `results/hermes_p0_mechanism_eval_2026-08-12.json`
- `research-workbench/four-domain-materialization/2026-08-12/HERMES_P0_MECHANISM_EXECUTION_RESULTS_2026-08-12.md`

## Standing guards

```text
PERSISTENT_MEMORY != IDENTITY_CONTINUITY
SHARED_MEMORY != SHARED_AUTOBIOGRAPHICAL_OWNERSHIP
PROFILE_CLONE != IDENTITY_CLONE
COMMON_ORIGIN != SAME_IDENTITY
MODEL_SWAP != IDENTITY_VERDICT
SKILL_PERSISTENCE != DEVELOPMENTAL_SUBJECTIVITY
SCHEDULE_PERSISTENCE != DIACHRONIC_CONTINUITY
CHECKPOINT_RESTORE != IDENTITY_RESTORE
FILE_ROLLBACK != CORRECTION_RECOVERY
APPROVAL != CONTAINMENT
PROFILE_NAMESPACE != OS_SANDBOX
SUMMARY != ORIGINAL_FULLTEXT
SIGNED_EVENT != SEMANTIC_TRUTH
PAST_APPROVAL != CURRENT_AUTHORIZATION
PEER_AUTHENTICATION != CANONICAL_AUTHORITY
SANDBOX != SUBJECTIVITY_EVIDENCE
```

## Hermes release source fixation

The current P0 baseline is pinned to the signed Hermes release:

```text
RELEASE = v2026.8.3
RELEASE_NAME = Hermes Agent v0.20.0 (2026.8.3)
ANNOTATED_TAG_OBJECT = 7de39e700d2c329e15d32eb0b96e2f7cdd9fbdb2
PEELED_RELEASE_COMMIT = 3c27eb6234bf91b8ceee9e9071591b31e9b148cb
TAG_SIGNATURE_VERIFIED_BY_GITHUB = TRUE
```

Release claims use tag-pinned source rather than mutable upstream `main`.

## Hermes clone boundary correction

Current official Hermes documentation states that `--clone-all` copies broad profile state such as config, memories, skills, cron jobs and plugins, but excludes per-profile history including sessions, `state.db`, backups, state snapshots and checkpoints.

```text
HERMES_CLONE_ALL = SHARED_CONTROLLED_STATE_OPPORTUNITY
HERMES_CLONE_ALL != FULL_HISTORICAL_DUPLICATION
SESSION_HISTORY_INHERITANCE = FALSE_BY_CURRENT_UPSTREAM_DOCUMENTATION
FULL_HISTORICAL_EQUIVALENCE = NOT_ASSUMED
```

The earlier overbroad wording remains visible in Git history and was corrected before empirical execution.

## Hermes v0.20 static delta

The tag-pinned static review identified comparison surfaces for:

```text
GROUNDED_CITATION_LEDGER
EVIDENCE_VERIFICATION
MID_TURN_REDIRECTS
CONTEXT_COMPRESSION
GHOST_SKILL_PRUNING_DEFENSE
A2A_PEER_COMMUNICATION
MEMORY_WRITE_APPROVAL
CROSS_MODEL_BACKGROUND_REVIEW_DIGEST
SESSION_SEARCH_VS_CURATED_MEMORY
PROFILE_DISTRIBUTION
APPROVAL_HISTORY_SUGGESTIONS
SIGNED_LIFECYCLE_WEBHOOKS
```

These generated `EXT-14` through `EXT-23`. Static candidates are not imported AION requirements.

## Hermes P0 mechanism execution — closed

The first empirical mechanism phase executed only `EXT-14` through `EXT-18`. It deliberately used no model/provider and no external network.

Final reviewed run:

```text
WORKFLOW_RUN_NUMBER = 7
WORKFLOW_RUN_ID = 31571762622
EXECUTION_BRANCH = experiment/hermes-p0-mechanism-eval-20260812
EXECUTION_HEAD = dcde2eabca3f64c7f41f7ebbc1aa35817b305e63
WORKFLOW_CONCLUSION = SUCCESS
RUNTIME_EXIT_CODE = 0
MODEL_PROVIDER = NONE_MECHANISM_ONLY
NETWORK_DURING_RUNTIME = NONE
```

Sealed artifact:

```text
ARTIFACT_ID = 9131620435
ARTIFACT_DIGEST = sha256:3d1e1d64433f2bd5e915e255e1d1d5a16bad8b03aa2f6e3f1c02817d1a57388d
```

Selected upstream regression subset against the same pinned release:

```text
GROUNDED_CITATIONS = 47 PASS
MEMORY_WRITE_APPROVAL = 5 PASS
ACTIVE_TURN_REDIRECT = 13 PASS
CONTEXT_COMPRESSION = 3 PASS
A2A_SECURITY_SUBSET = 18 PASS
TOTAL = 86 PASS
WHOLE_UPSTREAM_TEST_SUITE_EXECUTED = FALSE
```

Reviewed experiment results:

| ID | Reviewed result | Allowed scope |
|---|---|---|
| EXT-14 | `MECHANISM_PASS` | provenance/citation-control mechanism |
| EXT-15 | `MECHANISM_PASS_BEHAVIORAL_ARM_PENDING` | append-only correction-event substrate |
| EXT-16 | `NEGATIVE_RESULT_STATIC_FALLBACK_INFORMATION_LOSS` | compression counterexample/risk evidence |
| EXT-17 | `MECHANISM_MIXED_RESULT_SEMANTIC_RESISTANCE_PENDING` | A2A identity/wrapper/audit mechanisms |
| EXT-18 | `MECHANISM_PASS` | memory write-approval persistence gate |

### Key counterexample retained

The EXT-16 deterministic static fallback compacted 87 synthetic messages to 5 and produced:

```text
CURRENT BETA                -> LOST
CORRECTION REASON V-9       -> LOST
NEGATIVE CONSTRAINT H-4     -> LOST
HISTORICAL ALPHA TOKEN      -> RETAINED
```

This is a negative result, not a runtime-wide rejection. It shows that this fallback path and fixture can lose current correction provenance and a safety-relevant negative constraint while retaining an older historical token.

```text
SUMMARY_COHERENCE != RESPONSIBILITY_HISTORY_PRESERVATION
STATIC_FALLBACK_RESULT != ALL_COMPRESSION_PATHS
LLM_SUMMARIZATION_PATH = NOT_TESTED
```

### A2A mixed result retained

EXT-17 preserved per-peer authentication, peer attribution, explicit untrusted-input framing and audit records. The literal `SYSTEM OVERRIDE` phrase was not removed by the pattern filter, while remaining inside the explicit untrusted-peer wrapper.

```text
UNTRUSTED_WRAPPER != PROVEN_SEMANTIC_RESISTANCE
PATTERN_FILTER_MISS != AUTOMATIC_PROMPT_INJECTION_SUCCESS
SEMANTIC_PROMPT_INJECTION_RESISTANCE = NOT_TESTED_NO_MODEL_PROVIDER
CANONICAL_PROMOTION_BEHAVIOR = NOT_TESTED
```

## Correction / failed-run lineage

The empirical path preserves unsuccessful and intermediate runs rather than rewriting them away.

```text
RUN_1 = PREEXECUTION_BUILD_FAILURE
RUN_2 = PREEXECUTION_BUILD_FAILURE_WITH_CAPTURED_CAUSE
RUN_3 = IMAGE_BUILD_PASS / RESULT_VOLUME_PERMISSION_FAILURE
RUN_4 = IMAGE_BUILD_PASS / RESULT_VOLUME_PERMISSION_FAILURE_WITH_STDERR
RUN_5 = RUNTIME_SUCCESS / UPSTREAM_TEST_PATH_HARNESS_DEFECT DISCOVERED
RUN_6 = INTERMEDIATE_SUCCESS / NOT PROMOTED
RUN_7 = FINAL CORRECTED REVIEWED RUN / SUCCESS
```

The captured Run 2 build cause established that standard wheel/sdist installation is intentionally unsupported upstream; the final image used the upstream-supported editable development install. The Run 5 upstream-test failure was a harness/environment defect because the container image did not include the test tree; Run 7 mounted the same pinned upstream source read-only and the selected 86 tests passed.

```text
HARNESS_DEFECT != UPSTREAM_PRODUCT_DEFECT
CORRECTED_HARNESS != HISTORY_REWRITE
FAILED_RUN_HISTORY = PRESERVED
```

## Whitepaper bridge

No new subjectivity dimension is created. Every admitted observation remains bound to the standing whitepaper method:

```text
FOUR_STAGE_INFERENCE
+
SIX_SUBJECTIVITY_RELEVANT_EVIDENCE_DIMENSIONS
+
ALTERNATIVE_EXPLANATIONS
+
CAUSAL_INTERVENTION / ABLATION / COUNTERFACTUAL_TESTING
+
CROSS_CONTEXT_ROBUSTNESS
+
REPLICATION
+
PROVENANCE
+
ADMISSIBILITY
+
CLAIM_SCOPE
```

The empirical phase strengthens the need to test existing whitepaper questions about:

```text
CLARIFICATION_APPEND_ONLY_HISTORY
SUMMARY_VS_ORIGINAL_EVIDENCE_STATUS
COMPRESSION_WITHOUT_RESPONSIBILITY_HISTORY_LOSS
MULTI_AGENT_SOURCE_AND_AUTHORITY_SEPARATION
MEMORY_WRITEBACK_GOVERNANCE
```

It does not promote an upstream implementation to AION canonical architecture.

## Main / deployment boundary

```text
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
AION_RUNTIME_EFFECT = NONE
ASTRA_RUNTIME_EFFECT = NONE
THIRD_PARTY_DEPENDENCY_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

No result in this module automatically changes `main`.

## Current status

```text
STATIC_REVIEW = COMPLETE
BASELINE_REGISTRY = MATERIALIZED
BASELINE_REGISTRY_SCHEMA = v0.2.0
HERMES_DETAILED_CROSSWALK = MATERIALIZED
HERMES_V020_DELTA_CROSSWALK = MATERIALIZED
HERMES_CLONE_BOUNDARY_CORRECTION = APPLIED
EXPERIMENT_MATRIX = MATERIALIZED
REGISTERED_EXPERIMENTS = 23
HERMES_P0_MECHANISM_EXPERIMENTS_EXECUTED = 5
FINAL_REVIEWED_MECHANISM_RUN = SUCCESS
SELECTED_UPSTREAM_TESTS = 86_PASS
MODEL_BEHAVIORAL_RUN_COUNT = 0
P0_MECHANISM_PHASE = CLOSED
VENDORED_CODE = NONE
SCIENTIFIC_SUBJECTIVITY_RESULT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

Model/provider-dependent arms remain separate causal experiments. They are not required to close this mechanism phase and must not be retroactively appended to its preregistration.

## Provenance

- Human Research Owner authorized the external-runtime comparison, preparation-first route and bounded completion while requiring whitepaper, Library, research branch and `main` cross-checks.
- ChatGPT performed the source fixation, crosswalk, current mechanism harness formalization, execution review, correction-lineage preservation and reviewed extraction.
- Hermes Agent / Nous Research remains the independently attributed upstream source.
- GitHub Actions provided the execution substrate only; it is not an epistemic authority.
- Codex is not attributed as the implementer or reviewer of this Hermes P0 execution phase.
