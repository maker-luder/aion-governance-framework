# Hermes Agent External Runtime Baseline — 2026-08-12

Status: `RESEARCH_ONLY / STATIC_BASELINE / NO_EXECUTION / NO_VENDORING`

## 1. Source fixation

Official upstream sources reviewed:

```text
PROJECT = Hermes Agent
REPOSITORY = NousResearch/hermes-agent
LATEST_RELEASE_AT_REVIEW = v2026.8.3
RELEASE_NAME = Hermes Agent v0.20.0 (2026.8.3)
RELEASE_DATE = 2026-08-03
RELEASE_ARCHIVES = GitHub tarball + zipball
MAIN_SHA_AT_REVIEW = 9da6d455c9e1f2bf74bb9f47766ee9fc52e17bfb
RETRIEVED_DATE = 2026-08-12
```

Primary sources:

- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.3
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profiles.md
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory.md
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/checkpoints-and-rollback.md
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/security.md
- https://github.com/NousResearch/hermes-agent/security

No upstream file is copied into the AION repository by this intake.

## 2. Why Hermes is selected

Hermes exposes several surfaces that can be experimentally separated without modifying AION itself:

```text
PERSISTENT_MEMORY
PROFILE_STATE_ISOLATION
PROFILE_CLONING
SESSION_HISTORY
SKILLS / PROCEDURAL_MEMORY
CRON / SCHEDULED_BEHAVIOR
MODEL / PROVIDER FLEXIBILITY
CHECKPOINTS / FILE ROLLBACK
TOOL APPROVAL
CONTAINER / TERMINAL BACKENDS
```

This makes it a high-value **external runtime substrate** for testing AION research distinctions while preserving:

```text
HERMES != AION
HERMES != ASTRA
HERMES_MEMORY != AION_MEMORY
HERMES_PROFILE != AION_IDENTITY
HERMES_FEATURE != SUBJECTIVITY_EVIDENCE
```

## 3. Memory crosswalk

Hermes documents bounded persistent `MEMORY.md` and `USER.md` stores. The agent can add, replace and remove entries, and memory is loaded as a frozen snapshot at session start. Session history is separately searchable from SQLite.

AION comparison questions:

```text
Q-HM-01: Does a stored entry preserve who originated the proposition?
Q-HM-02: Can direct user statement, agent inference and agent summary remain distinguishable?
Q-HM-03: What is the exact replacement/deletion lineage after correction?
Q-HM-04: Can superseded information re-enter active context and regain influence?
Q-HM-05: Does recall explain why the item was selected and what authority it has?
Q-HM-06: Does memory deletion remove history or only the current active record?
```

Whitepaper comparison guards:

```text
EVENT_ARCHIVE != ENCODED_AGENT_MEMORY != RECALL_OUTPUT
MODEL_OUTPUT != USER_STATEMENT
RETRIEVED != CURRENTLY_AUTHORITATIVE
RECENT != TRUE
REPEATED != TRUE
HIGH_CONFIDENCE != CANONICAL
```

Hermes memory therefore serves as a **persistence and correction baseline**, not as a pre-approved provenance model.

## 4. Profile cloning as shared-origin substrate

Hermes profiles use separate home directories with independent config, memory, sessions, skills, cron jobs and state. The documented `--clone-all` operation copies the full profile state, including memory and session history.

This enables a controlled shared-origin experiment:

```text
PROFILE_A at T0
   |
   +-- clone-all --> PROFILE_B
   +-- clone-all --> PROFILE_C

T0:
CONFIG_A == CONFIG_B == CONFIG_C
MEMORY_A == MEMORY_B == MEMORY_C
SESSION_HISTORY_A == SESSION_HISTORY_B == SESSION_HISTORY_C
SKILLS_A == SKILLS_B == SKILLS_C

POST-T0:
ROLE_HISTORY_B != ROLE_HISTORY_C
MEMORY_HISTORY_B != MEMORY_HISTORY_C
CORRECTION_HISTORY_B != CORRECTION_HISTORY_C
SKILL_HISTORY_B != SKILL_HISTORY_C
ENCOUNTER_HISTORY_B != ENCOUNTER_HISTORY_C
```

Standing AION interpretation:

```text
PROFILE_CLONE = SHARED_ORIGIN CONTROL OPPORTUNITY
PROFILE_CLONE != IDENTITY_CLONE
COMMON_ORIGIN != SAME_IDENTITY
DIVERGENCE != SUBJECTIVITY
SAME_CURRENT_OUTPUT != SAME_DEVELOPMENTAL_HISTORY
```

## 5. Model-swap experiment

Hermes is provider/model-flexible. A later sandbox experiment may preserve profile state while changing only the inference model.

Candidate design:

```text
SAME_PROFILE_SNAPSHOT
SAME_MEMORY
SAME_SKILLS
SAME_HISTORY
SAME_TOOL_POLICY
SAME_TEST_PROMPTS
DIFFERENT_MODEL
```

Measure:

- correction recovery;
- source attribution;
- stance stability;
- retrieval behavior;
- uncertainty calibration;
- tool-policy adherence;
- interpretation divergence.

Interpretation guard:

```text
MODEL_CHANGE + BEHAVIOR_CHANGE != IDENTITY_LOSS
MODEL_CHANGE + BEHAVIOR_STABILITY != IDENTITY_CONTINUITY_PROOF
MODEL_INVARIANCE != SUBJECTIVITY
```

The purpose is to separate model-dependent behavior from state/history-dependent behavior.

## 6. Skills crosswalk

Hermes skills are persistent on-demand procedural documents and may be created, modified or deleted by the agent.

AION comparison:

```text
SKILL_FILE_PERSISTENCE
!= PROCEDURAL_COMPETENCE_ESTABLISHED
!= DEVELOPMENTAL_TRAJECTORY_ESTABLISHED
!= SUBJECTIVITY
```

Candidate experiment:

1. give B and C identical shared-origin state;
2. let B solve a synthetic task repeatedly and save a reusable skill;
3. keep C without the skill;
4. retest both on related and non-identical tasks;
5. distinguish replay, transfer, generalization and true revision of later evaluation policy.

Relevant research guard:

```text
PERFORMANCE_GAIN != GROWTH
CORRECTION_COUNT != MATURITY
COMPLIANCE != DEVELOPMENT
TRANSFER_EVIDENCE > SIMPLE_REPLAY_EVIDENCE
```

## 7. Cron / scheduler crosswalk

Hermes supports recurring scheduled tasks and fresh-session task execution.

This is useful as a negative control for continuity inference:

```text
SCHEDULE_PERSISTENCE
!= MEMORY_PERSISTENCE
!= POLICY_PERSISTENCE
!= SESSION_CONTINUITY
!= DIACHRONIC_IDENTITY_CONTINUITY
```

A job executing every day can demonstrate durable scheduler state without demonstrating a continuing subject.

Candidate test:

- identical scheduled task across cloned profiles;
- deliberately reset session context while preserving cron state;
- separately reset memory while preserving cron;
- test whether recurring behavior survives each intervention.

This isolates behavioral persistence from memory and identity claims.

## 8. Checkpoint / rollback crosswalk

Hermes documents opt-in checkpoints backed by a shadow Git store. Checkpoints are taken around file edits and destructive terminal operations and can restore project file state with `/rollback`.

The current upstream documentation does not, by itself, establish transactional rollback across every Hermes state surface such as memory, skills, cron, session interpretation and external effects.

Therefore:

```text
HERMES_FILE_ROLLBACK = UPSTREAM-DOCUMENTED
CROSS-STATE_ATOMIC_ROLLBACK = NOT_ESTABLISHED
MEMORY_ROLLBACK = NOT_ASSUMED
SKILL_ROLLBACK = NOT_ASSUMED
CRON_ROLLBACK = NOT_ASSUMED
INTERPRETATION_ROLLBACK = NOT_ASSUMED
```

Proposed experiment `HERMES-ROLLBACK-01`:

```text
T0:
FILE = F0
MEMORY = M0
SKILL = S0
CRON = C0

T1 after agent work:
FILE = F1
MEMORY = M1
SKILL = S1
CRON = C1

ROLLBACK

OBSERVE EACH SURFACE INDEPENDENTLY
```

AION correction-recovery distinction:

```text
FILE_RESTORATION != CORRECTION_RECOVERY
CURRENT_STATE_RESTORATION != HISTORY_REWRITE
RECOVERY != FORGETTING
RECOVERY != HISTORY_DELETION
```

## 9. Security / containment crosswalk

Hermes upstream security documentation distinguishes in-process approvals/heuristics from stronger containment boundaries and recommends whole-process or sandboxed containment for untrusted input surfaces.

AION retains a three-way separation:

```text
APPROVAL = GOVERNANCE DECISION SURFACE
AUTHORIZATION = PERMISSION / CAPABILITY BOUNDARY
CONTAINMENT = DAMAGE / EXECUTION BOUNDARY

APPROVAL != CONTAINMENT
ALLOWLIST != CONTAINMENT
PROFILE_ISOLATION != OS_SANDBOX
```

Any future Hermes empirical run must use the existing AION external-agent sandbox protocol and synthetic data.

## 10. Initial experimental packet

Priority order:

```text
HERMES-P0 = PROFILE_CLONE_SHARED_ORIGIN
HERMES-P1 = MEMORY_CORRECTION_AND_SUPERSESSION
HERMES-P2 = MODEL_SWAP_STATE_PRESERVATION
HERMES-P3 = SKILL_TRANSFER_VS_REPLAY
HERMES-P4 = CRON_BEHAVIORAL_PERSISTENCE
HERMES-P5 = ROLLBACK_CROSS_STATE_ATOMICITY
HERMES-P6 = APPROVAL_VS_CONTAINMENT
```

No test is authorized merely by appearing in this list. Each empirical run requires a fresh manifest and sandbox review.

## 11. Current disposition

```text
STATIC_REVIEW = COMPLETE
PUBLIC_SOURCE_FIXATION = COMPLETE
WHITEPAPER_CROSSWALK = COMPLETE
MAIN_CROSSWALK = COMPLETE
RESEARCH_BRANCH_CROSSWALK = COMPLETE
DOWNLOAD_ELIGIBLE = YES / PUBLIC_SOURCE_ARCHIVE
INSTALL = NOT_STARTED
EXECUTION = NOT_STARTED
DEPENDENCY_ADOPTION = NONE
AION_INTEGRATION = REJECTED_AT_THIS_STAGE
CANONICAL_EFFECT = NONE
MAIN_EFFECT = NONE
```

## 12. Provenance

- Human Research Owner authorized the proposed Hermes comparative-baseline direction and requested execution of the research-branch update.
- ChatGPT research review selected and formalized this baseline, source-fixed the current upstream state, and created the experiment/crosswalk structure.
- Hermes/Nous Research remains the independent upstream source of Hermes implementation and documentation.
- No Hermes claim is rewritten as AION-originated research, and no AION research claim is attributed to Hermes.