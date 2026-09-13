# Current research navigation marker — 2026-09-13

Status: `NAVIGATION_NOTE / DOCUMENTATION_ONLY / DRAFT`
Canonical effect: `NONE`
Deployment: `FALSE`
Merge authorization: `NONE`
Main-write authorization: `NONE`

## Purpose

This note records the current preferred **research navigation order** for Codex / ChatGPT Work and later reviewers. It is a navigation aid, not a replacement for live repository discovery and not a grant of authority.

## Current navigation rule

As of the live state checked on 2026-09-13:

```text
PR #102
= PREFERRED_FIRST_RESEARCH_NAVIGATION_ENTRY

PR #102 FIRST-READ
!= PR #102 CANONICAL
!= PR #102 FIRST-MERGE
!= PR #102 COMPLETE_REPOSITORY_STATE
```

PR #102 is currently a useful first research navigation entry because it aggregates the newest draft work on repository-first handoff, reciprocal epistemic collaboration, external research memory, role separation, habit transfer, quality-line design, Four-Domain crosswalks, recursive inquiry, multi-agent coordination quality, digital continuity, and cross-dyad collaboration-regime research.

However, `main` remains the canonical baseline. PR #102 is an unmerged Draft overlay.

## Read order

Future Codex / ChatGPT Work should normally use the following order unless a narrower task clearly justifies less reading:

```text
1. LIVE_REPOSITORY_STATE
   -> current default branch
   -> exact main HEAD
   -> current open / draft / merged PR state
   -> current CI / authority state

2. CURRENT_MAIN
   -> canonical repository baseline

3. PR #102
   -> preferred current research / method navigation overlay
   -> current task specifications and bounded authorizations where applicable

4. TASK-RELEVANT SIBLING / HISTORICAL MATERIAL
   -> PR #101 when personality / memory / self-model / continuity is relevant
   -> merged PR #93 when longitudinal Human-AI grounding / study-harness ancestry is relevant
   -> other merged or open PRs only when the task requires them

5. EXISTING IMPLEMENTATION / HARNESS
   -> inspect before creating new infrastructure

6. MINIMAL AUTHORIZED ACTION
   -> implement, review, or return NO_IMPLEMENTATION_NEEDED
```

## Current related PR roles

### PR #102 — preferred first research navigation entry

Current role:

```text
PR_102
= CURRENT_DRAFT_RESEARCH_METHOD_OVERLAY
+ NAVIGATION_ENTRY
+ SPECIFICATION_SOURCE_FOR_AUTHORIZED_BOUNDED_EXPERIMENTS
```

It is not canonical until independently reviewed and merged under fresh Human Owner authority.

### PR #101 — specialized sibling research hypothesis

Current role:

```text
PR_101
= PERSONALITY / MEMORY / SELF_MODEL / CONTINUITY SPECIALIZED DRAFT
```

It should be cross-read when those constructs are relevant. It is not subordinate to PR #102.

### PR #93 — merged canonical antecedent

Current role:

```text
PR_93
= MERGED_LONGITUDINAL_HUMAN_AI_GROUNDING_AND_STUDY_HARNESS_ANTECEDENT
```

PR #93 is merged and therefore part of the canonical ancestry on `main`. It should be cross-read when a new experiment reuses or extends the longitudinal Human-AI study harness or related methodology.

## Dependency rule

An implementation agent must not silently treat PR #102 as a code base merely because it is the first navigation entry.

```text
FIRST_NAVIGATION_ENTRY
!= IMPLEMENTATION_BASE_BRANCH
```

Default implementation behavior:

```text
LIVE MAIN
-> READ PR #102 AS SPECIFICATION
-> READ TASK-RELEVANT PRs / MERGED HISTORY
-> INSPECT EXISTING HARNESS
-> CREATE SEPARATE IMPLEMENTATION BRANCH / DRAFT PR IF AUTHORIZED
```

If implementation truly depends on unmerged content from PR #102 or PR #101, the agent must report that dependency explicitly rather than silently inheriting it.

```text
UNMERGED_DEPENDENCY
-> EXPLICIT_REPORT_REQUIRED
```

## Dynamic-state warning

This file is a dated navigation marker. PR states, SHAs, CI results and merge status are dynamic and must be re-read live.

```text
NAVIGATION_MARKER
!= LIVE_STATE

DATED_PR_ROLE
!= PERMANENT_AUTHORITY
```

If a future live state conflicts with this note, live state wins for factual repository status, while any new authority still requires valid Human Owner authorization.

## Provenance

```text
HUMAN_OWNER_ORIGINAL
= request to record PR #102 as the current first research navigation entry,
  followed by task-dependent reading of main, PR #101, merged PR #93, and other relevant material

CHATGPT_TEACHER_FORMALIZATION
= separation of navigation priority from canonical authority,
  merge order, implementation base, and live-state truth
```

## Authority boundary

```text
PR_102_FIRST_READ != PR_102_FIRST_MERGE
PR_102_FIRST_READ != MAIN_REPLACEMENT
PR_102_FIRST_READ != COMPLETE_REPOSITORY_INGESTION
MAIN_CANONICAL != MAIN_WRITE_AUTHORIZED
REPOSITORY_DOCUMENTATION != MERGE_AUTHORIZATION
READ_ORDER != AUTHORITY_ORDER
CAPABILITY != AUTHORITY
```

This note does not authorize merge, main write, deployment, or autonomous scope expansion.
