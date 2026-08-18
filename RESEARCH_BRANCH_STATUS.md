# AION Research Branch Status

> **Current standing for `review/four-domain-research-materialization`.** This file supersedes earlier branch-standing fields that described the research workbench as actively growing. Earlier records remain preserved in Git history and dated research artifacts.

```text
BRANCH = review/four-domain-research-materialization
RESEARCH_STATE = FROZEN_CHECKPOINT
ACTIVE_RESEARCH_MATERIALIZATION = NO
AUTONOMOUS_RESEARCH_GROWTH = STOPPED
NEW_RESEARCH_TOPIC = NONE
NEW_FEATURE = NONE
NEW_RUNTIME_WORK = NONE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
AION_ASTRA_IDENTITY_EQUIVALENCE = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
FINAL_BRANCH_MODEL_TARGET = MAIN_PLUS_RESEARCH_ONLY
PHASE0_VISIBLE_BRANCH_REF_COUNT = 16
PR42_PREMERGE_VISIBLE_BRANCH_REF_COUNT = 17_AT_PR42_R1_R5_FRESH_INVENTORY
PR42_PREMERGE_SUPPORT_BRANCH_RETIREMENT = PENDING_OWNER_EXACT_TARGET_CONFIRMATION
PR42_PREMERGE_CONVERGENCE_STATE = IN_PROGRESS_PHASE_0_5
```

## 2026-08-15 lineage convergence

The research branch has been converged without force-push, history rewriting, squash of research ancestry, or merge into `main`.

The following research lineages are contained in the branch history:

- Four-Domain research materialization lineage;
- research-consolidation / literature-grounding metadata through `345649297fcfd0fe0a04642b701e411354714617`;
- CSOMI source lineage through `87405c1877c6f016c303971da13923a1ab690aae`;
- terminal SLSH semantic/provenance reconciliation through `893d8dc0c1c9d8f9a4188860520143c8d1d3977b`;
- CSOMI × SLSH read-only integration through `30897042608581a39f307edcdfc777f5bc59fef7`;
- research-only convergence PR #21 and PR #22.

`bad722c6c8ef75a233020453b0e3b436c56f87ca` is the lineage-closure snapshot before branch-facing freeze documentation and final branch retirement. The current/future exact research head is GitHub transition evidence and is intentionally not self-embedded as a permanent final-head claim.

## Historical QA / process-deviation record

PR #21 and PR #22 were merged into the research-only closure branch before their generic `Quality` workflows had completed. Their historical red checks are valid and are intentionally preserved.

- PR #21 merged at `2026-08-15T13:02:39Z`; Quality run #377 completed afterward with Python 3.11 and Python 3.12 failing at `Run component test suites`.
- PR #22 merged at `2026-08-15T13:03:11Z`; Quality run #378 completed afterward with Python 3.11 and Python 3.12 failing at `Run component test suites`.
- The defect was subsequently remediated on the surviving research branch by aligning the unified component-test execution environment with repository-root imports and aligning coverage execution to the same environment.
- The frozen research head `24de00c1fc8eaf09cdcef393f651f1cf3685bb57` later passed Quality run #390.

The later PASS establishes only that the surviving research branch no longer carries the QA defect exposed by PR #21/#22. It does **not** retroactively make those historical PR checks green or erase the fact that they were merged before generic Quality completion.

```text
PR21_PROCESS_DEVIATION = MERGED_BEFORE_QUALITY_COMPLETION
PR22_PROCESS_DEVIATION = MERGED_BEFORE_QUALITY_COMPLETION
HISTORICAL_RED_CHECKS = PRESERVED
HISTORICAL_RESEARCH_QUALITY_SNAPSHOT = PASS_AT_24de00c1fc8eaf09cdcef393f651f1cf3685bb57
RETROACTIVE_GREENWASH = FORBIDDEN
```

## Final branch retirement and archive conversion

The final five support branches were retired only after exact-head verification and creation of non-release archive tags. The tags preserve the exact candidate/authority commits without keeping them as active branches.

| Retired role | Archive tag | Exact commit | Standing |
|---|---|---|---|
| Native-language non-executable engineering candidate | `archive/engineering-native-language-feasibility-20260814` | `3dfc21463502e1c32189ae167d92f163ca1a55e8` | `ARCHIVED_CANDIDATE / NOT_PROMOTED` |
| CSOMI named research source checkpoint | `archive/research-csomi-source-20260814` | `87405c1877c6f016c303971da13923a1ab690aae` | `ARCHIVED_RESEARCH_AUTHORITY_CHECKPOINT` |
| terminal SLSH reconciliation checkpoint | `archive/research-slsh-terminal-20260814` | `893d8dc0c1c9d8f9a4188860520143c8d1d3977b` | `ARCHIVED_RESEARCH_AUTHORITY_CHECKPOINT` |
| deferred CSOMI selective canonical-promotion candidate | `archive/promotion-csomi-selective-canonical-deferred-20260814` | `7c48c0de87514088c3fd1410218ae92231be0887` | `ARCHIVED_DEFERRED_PROMOTION / NOT_ADOPTED` |
| deferred CSOMI×SLSH selective integration-promotion candidate | `archive/promotion-csomi-slsh-integration-deferred-20260815` | `ce0fa4899a9498d7795d4da9b5f96ba3570c3ead` | `ARCHIVED_DEFERRED_PROMOTION / NOT_ADOPTED` |

Archive tags are provenance/checkpoint refs. They are **not releases**, do not create canonical effect, do not reactivate the candidate, and do not imply that a deferred promotion was approved.

The final branch model target after separately authorized exact-head retirement is intentionally limited to:

```text
main
review/four-domain-research-materialization
```

This is a target/end-state, not a claim that all transitional refs have already been deleted. During the current PHASE 0–5 convergence cycle, fresh GitHub inventory remains the authority for observed refs; branch deletion is not performed in this phase and requires Human Owner exact-target confirmation.

## Workflow standing after freeze

CSOMI, SLSH, and CSOMI×SLSH research-specific workflows are retained only as manual revalidation surfaces (`workflow_dispatch`). They no longer represent an active branch-development queue.

The integration revalidation workflow resolves the archived CSOMI/SLSH authority checkpoints through the archive tags and exact commit SHAs rather than requiring the retired branch refs. Historical artifacts may still record the branch names that were correct when those artifacts were authored; those historical strings are provenance, not current branch inventory.

## Whitepaper and evidence boundary

The standing research method preserves the whitepaper distinctions:

```text
LOWER_LAYER_PASS != HIGHER_LAYER_VALIDATION
TEST_PASS != THEORY_CONFIRMATION
CI_SUCCESS != SCIENTIFIC_VALIDATION
TRANSFORMABILITY != IDENTITY_CONTINUITY
COPY != IDENTITY
SIMILARITY != IDENTITY_CONTINUITY
COMMON_ORIGIN != SAME_IDENTITY
MEMORY_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
```

The retained whitepaper lineage treats `v0.14.23` as the stable/frozen integration baseline and `v0.14.24` as a later internal research candidate. A newer candidate does not automatically supersede a stable baseline or promote itself to canonical authority.

Repository consolidation, branch absorption, archive-tag conversion, data transformation, reproducibility, provenance preservation, CI success, or external-literature alignment therefore do **not** establish subjectivity, consciousness, identity continuity, moral status, canonical runtime authority, or deployment authority.

## Historical convergence package

`docs/research-consolidation/` and its associated v0.1.0 checker/workflow are preserved as the **2026-08-14 convergence snapshot** that produced source-of-truth, supersession, literature, promotion-readiness, discoverability, and provenance crosswalks.

Those artifacts may contain exact branch names and heads that were correct for that historical convergence cycle. They are no longer the authority for the current branch inventory after the 2026-08-15 closure. They must not be mechanically rewritten to pretend they were authored after the closure.

For current branch standing, this file is authoritative. For historical questions, use the dated artifact itself and its Git provenance. For implemented behavior, use the relevant source and tests. For external claims, re-check the current primary/official source before treating a time-sensitive version or status as current.

## Main / promotion boundary

No research lineage was wholesale merged into `main` during this convergence, and archive conversion does not revive a deferred promotion.

```text
RESEARCH_BRANCH != MAIN
RESEARCH_RESULT != CANONICAL_CONCLUSION
RESEARCH_CONVERGENCE != CANONICAL_PROMOTION
ARCHIVE_TAG != RELEASE
ARCHIVE_TAG != APPROVAL
ARCHIVE_TAG != CANONICAL_PROMOTION
RESEARCH_CONVERGENCE != DEPLOYMENT
MAIN_PROMOTION_AUTHORIZATION = NOT_GRANTED_BY_THIS_STATUS
```

The two deferred promotion histories are now preserved by archive tags and their PR/history evidence rather than active promotion branches.

## Stop condition

The branch is intentionally left as a preserved research workbench checkpoint rather than an active development queue. Every `PR42_PREMERGE_*` field below is a bounded pre-merge snapshot, not a permanent current fact; after any merge or retirement transition, fresh GitHub inventory must replace the snapshot before current status is stated.

```text
PR42_PREMERGE_RESEARCH_LINEAGE_CONVERGENCE = TARGETED / PHASE_0_5_IN_PROGRESS
PR42_PREMERGE_SUPPORT_BRANCH_RETIREMENT = PENDING_OWNER_EXACT_TARGET_CONFIRMATION
PHASE0_VISIBLE_BRANCH_REF_COUNT = 16
PR42_PREMERGE_VISIBLE_BRANCH_REF_COUNT_SOURCE = FRESH_GITHUB_INVENTORY_ONLY
FINAL_BRANCH_COUNT_TARGET = 2
HISTORICAL_PROVENANCE = PRESERVED
PR42_PREMERGE_BRANCH_STANDING = FROZEN_CHECKPOINT / CONVERGENCE_IN_PROGRESS
PR42_PREMERGE_FUTURE_WORK = PHASE_0_5_ONLY_UNDER_CURRENT_DIRECTIVE
```
