# Baseline and Branch Protection Evidence

This artifact is the seven-file workbench package manifest. It distinguishes the isolated research branch from the protected/public baseline.

## 1. Baseline bindings

```text
TASK_START_TIME = 2026-08-09T11:45:48.1304921+08:00
ORIGIN_MAIN_SHA_AT_START = b2fb12c050a9c6f93240106929a282ae8cf88499
P0_PR_NUMBER = 5
P0_BRANCH = review/p0-crosswalk-verifier-reconciliation
P0_HEAD_SHA = 43c937f72972556c4a28cb2399a754d11a3e062b
WORKBENCH_BRANCH = review/four-domain-research-materialization
WORKBENCH_BASE_SHA = b2fb12c050a9c6f93240106929a282ae8cf88499
FINAL_WORKBENCH_HEAD_SHA = RESOLVE_FROM_refs/heads/review/four-domain-research-materialization_AFTER_MANIFEST_COMMIT
```

The exact final commit id cannot be embedded in the content of the commit it identifies because a Git commit id hashes the tree containing this file. The authoritative exact value is therefore the branch ref resolved after this manifest commit; the completion handoff records the literal 40-character value and verifies the remote ref matches it.

## 2. Change inventory

```text
FILES_ADDED = 7
FILES_MODIFIED_EXISTING = 0
FILES_DELETED = 0

PRODUCTION_SOURCE_CHANGED = NO
TEST_CODE_CHANGED = NO
WORKFLOW_CHANGED = NO
CANONICAL_DOC_CHANGED = NO
FROZEN_MANIFEST_CHANGED = NO
P0_BRANCH_CHANGED = NO

CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
MCP_IMPLEMENTATION = NO
TEACHER_MEMORY_IMPLEMENTATION = NO
SUBJECTIVITY_STATUS_CHANGE = NO
```

## 3. Exact files added

1. `research-workbench/four-domain-materialization/2026-08-09/FOUR_DOMAIN_REPOSITORY_CROSSWALK.md`
2. `research-workbench/four-domain-materialization/2026-08-09/STATE_SIDE_EFFECT_SURFACE_MAP.md`
3. `research-workbench/four-domain-materialization/2026-08-09/CORRECTION_PROVENANCE_FLOW_MAP.md`
4. `research-workbench/four-domain-materialization/2026-08-09/LINEAGE_NAMESPACE_AUTHORITY_MAP.md`
5. `research-workbench/four-domain-materialization/2026-08-09/T0_T4_EXPERIMENT_HARNESS_READINESS.md`
6. `research-workbench/four-domain-materialization/2026-08-09/APPLICATION_SERVICE_CONTRACT_GAP_MAP.md`
7. `research-workbench/four-domain-materialization/2026-08-09/BASELINE_AND_BRANCH_PROTECTION_EVIDENCE.md`

No eighth workbench artifact is authorized or included.

## 4. Commit list

The branch contains these workbench commits after the protected base:

1. `research: materialize four-domain repository crosswalk`
2. `research: map state side effects and correction provenance`
3. `research: map lineage authority and experiment readiness`
4. `research: map application contract gaps and baseline protection`
5. `research: normalize workbench artifact formatting`
6. `research: finalize workbench protection manifest`

No history rewrite, amend, squash, force push, P0 merge or main merge is part of this branch.

## 5. Final verification commands and required literal outcomes

These commands are executed after the manifest commit; the exact head and remote comparison are recorded in the completion handoff.

```powershell
git status --short --branch
# ## review/four-domain-research-materialization

git diff --check origin/main...HEAD
# <no output>; exit status 0

git diff --name-status origin/main...HEAD
# seven lines, each status A, matching section 3 exactly

git rev-list --count origin/main..HEAD
# 6

git merge-base origin/main HEAD
# b2fb12c050a9c6f93240106929a282ae8cf88499

git diff --quiet origin/main -- components docs schemas scripts .github
# exit status 0 for tracked protected areas (the new research-workbench path is outside them)
```

Scanner command:

```powershell
python scripts/scan_public_tree.py
```

The completion handoff records its actual exit status/output. The scanner is not weakened or edited.

## 6. Branch comparison against origin/main

| PROPERTY | EXPECTED AND VERIFIED BOUNDARY |
|---|---|
| Merge base | protected `origin/main@b2fb12c050a9c6f93240106929a282ae8cf88499` |
| Ahead count | six workbench commits |
| Behind count | zero at verified task baseline |
| Changed path prefix | only `research-workbench/four-domain-materialization/2026-08-09/` |
| Existing tracked files modified | none |
| Production/runtime effect | none; Markdown evidence only |
| P0 ancestry | P0 head is not merged into this branch |
| Merge intent | none |

## 7. Rollback

```text
ROLLBACK_METHOD = Delete or abandon the isolated workbench branch after owner review; protected main remains unchanged.
```

The local transfer ZIP is produced outside the repository and is not part of this manifest tree.
