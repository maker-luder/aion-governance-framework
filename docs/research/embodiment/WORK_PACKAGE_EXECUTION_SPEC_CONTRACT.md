# Work Package Execution Spec Contract

Status: `DISPATCH CONTRACT / DRAFT`  
Canonical effect: `NONE`

## Purpose

The master registry is a long-lived navigation map. It must not freeze future implementation details that depend on then-current repository state, upstream model revisions, licenses, interfaces or CI.

Therefore:

```text
REGISTRY_ENTRY
!= EXECUTION_SPEC
!= IMPLEMENTATION_AUTHORIZATION
```

A worker such as Teacher, Work or Codex receives a **pinned execution spec**, not only a registry summary.

## Dispatch flow

```text
MASTER BLUEPRINT IN MAIN
↓
SELECT ONE WP
↓
REVERIFY LIVE MAIN
↓
REVERIFY REQUIRED EXTERNAL SOURCES
↓
CREATE PINNED EXECUTION SPEC
↓
REVIEW EXECUTION SPEC
↓
AUTHORIZE BOUNDED IMPLEMENTATION
↓
IMPLEMENT ON ISOLATED BRANCH / DRAFT PR
↓
VERIFY
↓
FRESH EXACT-HEAD MERGE AUTHORIZATION
```

## Execution spec location

Recommended path:

```text
docs/research/embodiment/work-packages/
WP-XX_<scope>_EXECUTION_SPEC_<YYYY_MM_DD>.md
```

The exact path may follow later repository conventions, but the execution spec must be a standalone, reviewable artifact.

## Required fields

Every execution spec must contain all of the following.

### Identity

- `WORK_PACKAGE_ID`
- `TITLE`
- `SPEC_VERSION`
- `CREATED_AT`
- `BASE_MAIN_SHA`
- `TARGET_BRANCH`
- `CORE_RESEARCH_LINK`

### Scope

- `PURPOSE`
- `DEPENDENCIES`
- `ALLOWED_PATHS`
- `FORBIDDEN_SCOPE`
- `DO_NOT_EXECUTE`

### Inputs

- repository artifacts and exact refs;
- external model/dataset/software IDs;
- exact upstream revisions / DOI / release IDs;
- licenses / terms;
- source hashes where available;
- required prior work-package receipts.

### Outputs

- exact expected artifacts;
- schemas / code / docs / evidence records;
- expected provenance records;
- expected rollback artifact when material.

### Tool routing

For each tool used, state:

- purpose;
- permitted output;
- authority boundary;
- fail-closed behavior if unavailable.

### Verification

- tests;
- static checks;
- deterministic checks;
- hashes;
- schema validation;
- source-to-derived traceability;
- CI requirements.

### Scientific gates

- acceptance criteria;
- falsification criteria;
- competing explanations;
- claim ceiling;
- explicit nonclaims.

### Governance

```text
MAIN_WRITE = NO
MERGE_TO_MAIN = NO
AUTOMATIC_SCOPE_EXPANSION = NO
CANONICAL_EFFECT = NONE
```

`MERGE_TO_MAIN = NO` means the execution spec does not self-authorize merge. A later fresh exact-head Human Owner authorization may approve the reviewed implementation candidate.

## Core research link

Every work package must state exactly how it serves the repository core.

Acceptable pattern:

```text
CORE_RESEARCH_LINK =
tests whether <embodiment variable / interface / reduction>
changes <bounded functional phenomenon>
relevant to AI_SUBJECTIVITY_POSSIBILITY
without treating the result as subjectivity evidence
```

A package with no defensible link to the core returns `HOLD / SCOPE_REVIEW`.

## Upstream pinning

External dependencies must be reverified at execution time.

The blueprint's named candidates are discovery/navigation references, not permanent pins.

```text
BLUEPRINT_SOURCE_NAME
!= EXECUTION_TIME_VERIFIED_DEPENDENCY
```

The execution spec must record the then-current exact source and explicitly decide whether to retain that version.

## Scope-expansion rule

If implementation discovers that the registered package cannot succeed without work outside its defined boundary:

```text
STOP
↓
RECORD BLOCKER
↓
RETURN HOLD
↓
PROPOSE BLUEPRINT / WP AMENDMENT
```

The worker must not silently absorb the next package or rewrite the master architecture.

```text
DISCOVERED_DEPENDENCY
!= AUTHORIZATION_TO_IMPLEMENT_DEPENDENCY
```

## Blueprint amendment rule

A work package may discover evidence that invalidates part of the master blueprint.

That is an allowed research outcome.

The correct route is:

1. preserve implementation evidence;
2. stop the affected package;
3. open a bounded blueprint-amendment PR;
4. record what evidence changed the design;
5. review the amended dependency graph;
6. resume through a new pinned execution spec.

Implementation PRs should not silently rewrite architectural commitments unless the PR scope explicitly includes the blueprint amendment.

## Worker handoff rule

A worker prompt should reference:

- the exact execution-spec path;
- exact base SHA;
- exact allowed package;
- forbidden adjacent packages;
- expected outputs;
- verification commands/gates;
- no-main-write boundary.

Example structure:

```text
EXECUTE = WP-02
EXECUTION_SPEC = <exact reviewed spec>
BASE_MAIN = <exact SHA>

DO_NOT_EXECUTE = WP-03..WP-10
MAIN_WRITE = NO
MERGE_TO_MAIN = NO
```

## Completion semantics

```text
EXECUTION_SPEC_COMPLETE
!= IMPLEMENTATION_COMPLETE

IMPLEMENTATION_COMPLETE
!= SCIENTIFIC_VALIDATION

WP_N_PASS
!= WP_N+1_AUTHORIZED
```
