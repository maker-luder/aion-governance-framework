# External Runtime Baseline Comparison — v0.1.0

Status: `RESEARCH_ONLY / STATIC_BASELINE_MATERIALIZED / EMPIRICAL_RUNS_NOT_STARTED`

This module provides a stable research-branch home for comparing downloadable external agent/memory runtimes against existing AION whitepaper and governance distinctions.

It does **not** import, vendor, wrap, install, or execute any third-party runtime.

## Research object

```text
QUESTION:
Which observed behaviors arise from ordinary engineering mechanisms such as
persistent storage, profile cloning, shared memory, model/provider substitution,
scheduler state, checkpoint restoration, and sandbox boundaries?

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

Detailed Hermes crosswalk:

- `research-workbench/four-domain-materialization/2026-08-12/HERMES_AGENT_EXTERNAL_RUNTIME_BASELINE_2026-08-12.md`

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
SANDBOX != SUBJECTIVITY_EVIDENCE
```

## Hermes clone boundary correction

Current official Hermes documentation states that `--clone-all` copies broad profile state such as config, memories, skills, cron jobs and plugins, but excludes per-profile history including sessions, `state.db`, backups, state snapshots and checkpoints.

Therefore the research module now uses:

```text
HERMES_CLONE_ALL = SHARED_CONTROLLED_STATE OPPORTUNITY
HERMES_CLONE_ALL != FULL_HISTORICAL_DUPLICATION
SESSION_HISTORY_INHERITANCE = FALSE BY CURRENT UPSTREAM DOCUMENTATION
FULL_HISTORICAL_EQUIVALENCE = NOT_ASSUMED
```

The initial overbroad wording was corrected before empirical execution. The prior commits remain visible as audit history rather than being rewritten.

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

## Current status

```text
STATIC_REVIEW = COMPLETE
BASELINE_REGISTRY = MATERIALIZED
BASELINE_REGISTRY_SCHEMA = v0.1.1
HERMES_DETAILED_CROSSWALK = MATERIALIZED
HERMES_CLONE_BOUNDARY_CORRECTION = APPLIED
EXPERIMENT_MATRIX = MATERIALIZED
EMPIRICAL_RUN_COUNT = 0
LOCAL_INSTALLATION = NONE
VENDORED_CODE = NONE
SCIENTIFIC_RESULT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Provenance

The Human Research Owner authorized the external-runtime comparison direction and the research-branch update. ChatGPT research review performed the current source comparison and formalization, then corrected the Hermes `--clone-all` boundary after fresh primary-source verification. Upstream projects remain independently attributed. Codex did not implement this module in the current update.