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
- [x] Pull request opened to expose repository checks.
- [x] Quality workflow public-tree scan passed on Python 3.11 and 3.12 for the first closure commit.
- [x] Quality workflow component test suites passed on Python 3.11 and 3.12 for the first closure commit.
- [ ] Final closure commit Quality workflow, including the executable Recall Gate contrast step, passes.
- [ ] Human Owner final review.
- [ ] Main merge / release decision.

## Frozen release manifest semantics

`scripts/verify_release.py` verifies the frozen `v0.1.0-rc.1` manifest. The Quality workflow intentionally checks out that frozen tag for manifest verification on `main`.

It is **not** a current-head manifest generator for post-RC additions. Therefore:

```text
FROZEN_RC_MANIFEST_VERIFICATION
!=
CURRENT_CLOSURE_BRANCH_INTEGRITY_CHECK
```

Post-RC closure integrity is evaluated with the public-tree scanner, compilation, component tests, the explicit Recall Gate experiment, reviewable diff, and Human Owner review. The frozen RC tag remains historical evidence and must not be rewritten to absorb later files.

## Branch policy

The research-materialization branch is intentionally not merged wholesale. Its workbench and isolated research labs require their own later disposition.

The public-closure branch is based directly on main and contains only public-facing closure material. Main remains a stable public baseline until this package is reviewed.

## Main merge gate

```text
QUALITY_PY311 = PASS
QUALITY_PY312 = PASS
PUBLIC_TREE_SCAN = PASS
PUBLIC_PYTHON_COMPILE = PASS
COMPONENT_TESTS = PASS
MINIMAL_RECALL_GATE_CONTRAST = PASS
PRIVATE_SECRET_FINDINGS = 0
FROZEN_RC_HISTORY = PRESERVED
OWNER_REVIEW = APPROVED
```

The unfamiliar-reader protocol is now specified but has not been represented as executed human-subject/usability evidence. A future real-reader run must retain that distinction.

A merge does not authorize runtime deployment, canonical state, subjectivity conclusions, or automatic continuation of research.
