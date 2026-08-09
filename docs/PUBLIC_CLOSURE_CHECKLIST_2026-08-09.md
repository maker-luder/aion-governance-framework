# Public Closure Checklist — 2026-08-09

```text
MAIN_BASE = b2fb12c050a9c6f93240106929a282ae8cf88499
CLOSURE_BRANCH = review/public-closure-2026-08-09
RESEARCH_BRANCH = review/four-domain-research-materialization
DIRECT_RESEARCH_BRANCH_MERGE_TO_MAIN = NO
```

## Closure items

- [x] 30-second / 5-minute / deep-reference README orientation drafted.
- [x] Three-layer public positioning: AION / Astra / Executable Runtime.
- [x] Public threat model added.
- [x] Bazi methodological rationale added.
- [x] Twin embodiment ethics boundary and future opt-in/opt-out requirements added.
- [x] Provenance-first position paper draft added.
- [x] Unfamiliar-reader usability protocol added.
- [x] Minimal Memory Recall Gate contrast experiment added.
- [x] Synthetic pre-commit experiment reconstruction produced expected 6-vs-1 result.
- [ ] Repository verifier run against final closure branch.
- [ ] Component test suite run against final closure branch.
- [ ] Public-tree secret/private-path scan run against final closure branch.
- [ ] Human Owner final review.
- [ ] Main merge / release decision.

## Branch policy

The research-materialization branch is intentionally not merged wholesale. Its workbench and isolated research labs require their own later disposition.

The public-closure branch is based directly on main and contains only public-facing closure material. Main remains a stable public baseline until this package is reviewed.

## Main merge gate

```text
VERIFY_RELEASE = PASS
COMPONENT_TESTS = PASS OR EXPLICITLY_DOCUMENTED_BLOCKER
PUBLIC_TREE_SCAN = PASS
PRIVATE_SECRET_FINDINGS = 0
OWNER_REVIEW = APPROVED
```

A merge does not authorize runtime deployment, canonical state, subjectivity conclusions, or automatic continuation of research.
