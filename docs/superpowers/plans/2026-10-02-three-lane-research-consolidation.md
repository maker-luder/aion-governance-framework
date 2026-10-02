# Three Research Lines and Legacy Hold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Organize the repository's future work into an AI subjectivity possibility main line, a CCTS/Human–AI learning line, an independent embodiment line, and a temporary uncertainty hold, with no branch deletion or main merge in this round.

**Architecture:** All three new research/hold branch refs start from the same freshly verified main SHA. Each receives one bounded index rather than moving code or pretending old histories were merged. A separate navigation Draft PR proposes changes to main entry pages. The hold branch records unknown old refs without absorbing their unique Git histories.

**Tech Stack:** GitHub repository, Markdown, Git refs, local link/diff checks and remote CI observation.

**Spec:** `docs/superpowers/specs/2026-10-02-three-lane-research-consolidation-design.md` (design branch `design/three-lane-research-consolidation-20261002`).

## Global Constraints

- Main stays unchanged; no merge, ready transition, publication or subjectivity/learning validation claims.
- Ranking: AI subjectivity possibility has always been central, CCTS/Human–AI learning second, independent embodiment third. The fourth hold is temporary and not a scientific construct.
- CCTS release metadata and DOI stay at their existing main paths; draft manuscript stays distinct from the archived scholarly object.
- Preserve every old branch ref in this round. `SAFE_DELETE` is a candidate label only, never a deletion instruction.
- An index of old branch names and SHAs does not contain their unique Git commits; retain those original refs.
- Do not conflate implementation, provenance, publication, CI, or scientific establishment.
- Actor label and interaction surface do not verify model identity.
- Documentation work gets content/link/diff checks; remote CI status is reported separately. No implementation or experiment changes.

## Review Focus

- A branch changes while inventory is being built: reread exact ref and label the row unstable or `HOLD_UNKNOWN`.
- One old branch has unique commits: retain old ref; destination index records pointer, not false ancestry.
- A main entry link resolves into the wrong branch: use explicit GitHub URL for side branch entry.
- An unpublished CCTS draft is described as the archived scholarly object: check both source paths and fix wording.
- A historical embodiment candidate appears as merged or scientifically validated: check PR state and scope sentence.

---

### Task 1: Lock live state and preserve the new requirement

**Files:** Modify only the design spec on its design branch; create this plan alongside it.

**Interfaces:** Produces a frozen main SHA, ordered lane names, and a read-only source inventory for later tasks.

- [ ] Verify live main exact SHA, open PRs, recent merges, candidate branch-name availability, current entry files, CCTS metadata, and embodiment baseline.
- [ ] Update the approved spec with the fourth temporary hold lane and explicit no-deletion instruction.
- [ ] Commit the plan on the design branch and re-fetch both files.
- [ ] Check the design branch against main; expected only spec and plan files added, no main change.

### Task 2: Create the second and third research lanes

**Files:** Create `docs/research/ccts-human-ai-learning/README.md` on `research/ccts-human-ai-learning-lane`; create `docs/research/embodiment/README.md` on `research/embodiment-lane`.

**Interfaces:** Consumes exact main SHA from Task 1. Produces two exact heads and durable branch URLs for Task 4.

- [ ] Create both refs from that exact main SHA and verify merge-base/status.
- [ ] Read exact current source paths and relevant closed PR states before writing source matrix.
- [ ] Write bounded bilingual or Chinese-led indexes, provenance/source status, science/authority boundaries, and links to current main paths or historical exact heads.
- [ ] Verify each changed-files list contains only its own index, links resolve, source claims match live repository, and main remains unchanged.

### Task 3: Inventory unknown old branches in a temporary hold lane

**Files:** Create `docs/research/legacy-uncertainty/README.md` and `docs/research/legacy-uncertainty/BRANCH_DISPOSITION_MATRIX.md` on `research/legacy-uncertainty-hold`.

**Interfaces:** Consumes exact main SHA, current branch list, and Tasks 2 heads. Produces uncertainty inventory and retained-ref statement.

- [ ] Enumerate all live branch names and exact heads where the connector permits; compare to main where feasible. Record unavailable head/diff as `UNKNOWN`, never guess.
- [ ] Create hold ref from exact main SHA and write its purpose, exact provenance boundary, and a row for each legacy branch with observed head and preliminary disposition.
- [ ] Mark only evidenced main/lane coverage; everything else remains `HOLD_UNKNOWN`. Do not cherry-pick, merge, rebase, force-push, or delete any old ref.
- [ ] Re-enumerate branch count and verify hold index rows, exact head, and main SHA.

### Task 4: Propose main navigation without merging

**Files:** Modify `README.md`, `README.zh-TW.md`, and only necessary entry docs on `docs/three-line-research-navigation-20261002`.

**Interfaces:** Consumes exact branch URLs and science boundaries from Tasks 2–3. Produces one Draft PR.

- [ ] Create navigation ref from fresh exact main SHA, verify no intervening main change.
- [ ] Replace the misleading equal-status four-line presentation with one longstanding subjectivity core and two ranked work lines; link the temporary hold separately.
- [ ] Preserve CCTS publication/draft distinction and embodiment experimental status; maintain English/Traditional Chinese semantic alignment.
- [ ] Validate links, Markdown, changed-file list, diff and no accidental scientific claims.
- [ ] Open Draft PR against main; verify PR head/base/state and observe remote CI without equating local checks to CI.

### Task 5: Final reverse review and report

**Files:** No additional changes unless a specific documented defect requires a bounded correction.

**Interfaces:** Consumes all exact branch/PR heads and inventories. Produces reviewable report.

- [ ] Re-fetch live main, all new heads, PR, changed files, diff and CI.
- [ ] Check no old branch deleted, no old history was silently merged, no original CCTS DOI metadata path removed, and no unverified actor claim promoted.
- [ ] Provide branch matrix, unresolved questions and next Human review gate. No merge or deletion in this round.
