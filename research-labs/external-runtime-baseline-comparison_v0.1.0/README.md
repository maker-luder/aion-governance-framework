# External Runtime Baseline Comparison — v0.1.0

Status: `RESEARCH_ONLY / STATIC_BASELINE_MATERIALIZED / EMPIRICAL_RUNS_NOT_STARTED`

This module provides a stable research-branch home for comparing downloadable external agent/memory runtimes against existing AION whitepaper and governance distinctions.

It does **not** import, vendor, wrap, install, or execute any third-party runtime.

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

## Baselines currently registered

```text
P0 Hermes Agent
P1 OpenHands
P1 Letta
P1 LangGraph
P2 Mem0
```

Source-fixed details are recorded in:

- `research-workbench/four-domain-materialization/2026-08-12/DOWNLOADABLE_EXTERNAL_RUNTIME_REGISTRY_2026-08-12.md`
- `research-workbench/four-domain-materialization/2026-08-12/external_runtime_baselines_v0.1.0.json`

Detailed Hermes crosswalks:

- `research-workbench/four-domain-materialization/2026-08-12/HERMES_AGENT_EXTERNAL_RUNTIME_BASELINE_2026-08-12.md`
- `research-workbench/four-domain-materialization/2026-08-12/HERMES_V020_RESEARCH_DELTA_2026-08-12.md`

Experiment preregistration scaffold:

- `research-workbench/four-domain-materialization/2026-08-12/EXTERNAL_RUNTIME_EXPERIMENT_MATRIX_2026-08-12.md`

Supervised reconciliation:

- `research-workbench/four-domain-materialization/2026-08-12/EXTERNAL_AGENT_RUNTIME_BASELINE_RECONCILIATION_2026-08-12.md`

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

The current P0 static baseline is pinned to the signed Hermes release:

```text
RELEASE = v2026.8.3
ANNOTATED_TAG_OBJECT = 7de39e700d2c329e15d32eb0b96e2f7cdd9fbdb2
PEELED_RELEASE_COMMIT = 3c27eb6234bf91b8ceee9e9071591b31e9b148cb
TAG_SIGNATURE_VERIFIED_BY_GITHUB = TRUE
```

The review uses tag-pinned documentation/source specimens rather than mutable `main` for release claims. Current upstream `main` may be consulted only as a separately recorded moving reference.

## Hermes clone boundary correction

Current official Hermes documentation states that `--clone-all` copies broad profile state such as config, memories, skills, cron jobs and plugins, but excludes per-profile history including sessions, `state.db`, backups, state snapshots and checkpoints.

Therefore the research module uses:

```text
HERMES_CLONE_ALL = SHARED_CONTROLLED_STATE_OPPORTUNITY
HERMES_CLONE_ALL != FULL_HISTORICAL_DUPLICATION
SESSION_HISTORY_INHERITANCE = FALSE_BY_CURRENT_UPSTREAM_DOCUMENTATION
FULL_HISTORICAL_EQUIVALENCE = NOT_ASSUMED
```

The initial overbroad wording was corrected before empirical execution. The prior commits remain visible as audit history rather than being rewritten.

## Hermes v0.20 research delta

The tag-pinned v0.20 review adds comparison surfaces for:

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

These surfaces generated `EXT-14` through `EXT-23`. They are experiment candidates, not imported requirements or scientific conclusions.

## Whitepaper bridge

This module does not create new subjectivity dimensions. Any future observation must bind back to the standing whitepaper evidence architecture:

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

The v0.20 delta is especially relevant to existing whitepaper questions about:

```text
CLARIFICATION_APPEND_ONLY_HISTORY
MULTI_AGENT_SOCIALITY_AND_AUTHORITY
SUMMARY_VS_ORIGINAL_EVIDENCE_STATUS
COMPRESSION_WITHOUT_RESPONSIBILITY_HISTORY_LOSS
MEMORY_WRITEBACK_GOVERNANCE
```

## Main-branch boundary

The public `main` baseline remains independently governed and frozen with respect to this research module.

```text
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
THIRD_PARTY_DEPENDENCY_EFFECT = NONE
```

No result produced here may automatically change `main`.

## Execution boundary

Future empirical work must use `research-labs/external-agent-sandbox-protocol_v0.1.0`.

Minimum execution conditions:

- separate sandbox/environment;
- synthetic persona and memory;
- pinned upstream version or commit;
- no production secrets;
- no private AION memory;
- no direct write authority to `main` or the research integration branch;
- explicit network/tool policy;
- human-reviewed run manifest;
- reviewed extraction instead of raw authority import.

Additional v0.20-specific stop rules:

- no A2A exposure to real external peers;
- no real memory-profile mutation;
- no approval-history experiment that changes host permissions;
- no webhook receiver using production credentials;
- no context-compression experiment containing private conversation history.

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
HERMES_V020_DELTA_EXPERIMENTS = 10
EMPIRICAL_RUN_COUNT = 0
LOCAL_INSTALLATION = NONE
VENDORED_CODE = NONE
SCIENTIFIC_RESULT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Provenance

The Human Research Owner authorized continuation of the external-runtime research-branch update. ChatGPT performed the current tag-pinned source comparison, formalized the v0.20 crosswalk and experiment candidates, and preserved the earlier `--clone-all` correction lineage. Upstream projects remain independently attributed. Codex is not attributed as the implementer of this checkpoint.
