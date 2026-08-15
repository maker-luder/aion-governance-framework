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
LIVE_BRANCH_MODEL = MAIN_PLUS_RESEARCH_ONLY
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

After this retirement, the repository's live branch model is intentionally limited to:

```text
main
review/four-domain-research-materialization
```

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

The branch is intentionally left as a preserved research workbench checkpoint rather than an active development queue.

```text
RESEARCH_LINEAGE_CONVERGENCE = COMPLETE
SUPPORT_BRANCH_RETIREMENT = COMPLETE
LIVE_BRANCH_COUNT = 2
HISTORICAL_PROVENANCE = PRESERVED
CURRENT_BRANCH_STANDING = FROZEN_CHECKPOINT
FUTURE_WORK = SEPARATELY_AUTHORIZED_ONLY
```
