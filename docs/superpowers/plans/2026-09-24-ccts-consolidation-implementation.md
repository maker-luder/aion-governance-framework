# CCTS current-main consolidation — implementation plan

**Goal:** Implement the approved PR #205 Option-C evidence lane and the still-missing, CCTS-compatible Human epistemic-agency retention structural audit without changing core CCTS admission, longitudinal required fields, or the canonical epistemic-revision module.

**Architecture:** Add two focused modules inside the existing `aion_human_ai_longitudinal` package. The first is a claim-local relational-continuity review surface that crosswalks existing continuity dimensions and reuses the current matched-information ancestry without making continuity a core admission gate. The second is a synthetic structural Human-retention matrix that reuses the current CCTS manifest, metacognitive task classes, exact-enum conventions, content digests, and fail-closed study errors. Neither module computes a scalar score or serializes scientific, causal, learning, identity, or subjectivity conclusions.

**Baseline:** `f5629ee06fef0a40efe19042c2731c6acf080ddc`; baseline targeted suites: `99 passed`.

---

## Task 1: Relational-continuity claim-local negative tests

**Files**
- Add: `research-labs/human-ai-longitudinal-study_v0.1.0/tests/test_ccts_relational_continuity.py`

1. Add synthetic fixtures for claim-not-asserted, evidence-required, supported-candidate, matched-null, and unresolved-confound paths.
2. Add negative tests proving style, memory, same-role, and data-only proxy evidence cannot satisfy the relational claim.
3. Add negative tests proving raw strings do not bypass exact enum checks, unknown contribution IDs fail closed, source-role provenance binding must match the admitted CCTS provenance digest, and identity/subjectivity promotion is rejected.
4. Add compatibility tests proving existing core and longitudinal CCTS fixtures remain valid without any relational-continuity field.
5. Run the new file and record the expected import/collection failure before implementation.

## Task 2: Relational-continuity evidence lane and path-dependence bridge

**Files**
- Add: `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/ccts_relational_continuity.py`
- Modify: `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/__init__.py`

1. Define exact enums for claim-local disposition, continuity evidence locus, proxy signal, path-dependence outcome, and matched-information confound.
2. Define content-addressed evidence bindings tied to existing `ContributionRole` provenance and known CCTS contribution IDs.
3. Define a matched-information comparison that binds information content, order/position, context length, leakage, model/version, relevance, and budget/access for both conditions.
4. Implement fail-closed structural review:
   - no assertion → `NOT_ASSERTED`;
   - assertion without admissible relational evidence → `EVIDENCE_REQUIRED`;
   - unresolved matching/confounds → `UNRESOLVED`;
   - adequately matched null → `WEAKENED`;
   - adequately matched material difference plus admissible relational evidence → `SUPPORTED_CANDIDATE`.
5. Preserve explicit `NOT_ESTABLISHED` ceilings for AI identity, subjectivity, held relationship experience, causal path dependence, learning, and scientific validation.
6. Export the public surface and run the focused tests to green.

## Task 3: Human epistemic-agency retention negative tests

**Files**
- Add: `research-labs/human-ai-longitudinal-study_v0.1.0/tests/test_ccts_human_epistemic_agency.py`

1. Add a synthetic trajectory containing baseline AI-withheld judgement, CCTS/AI-available interaction, same-task AI-withheld judgement, and distinct held-out AI-withheld judgement.
2. Add failures for same-label/different-manifest snapshots, cross-task contamination, held-out exact-content reuse, broken source-role bindings, unmatched controls, invalid phase order, raw enum strings, and stale historical-pass receipts.
3. Assert that assisted output never satisfies independent-Human-retention criteria and that structural PASS keeps independent Human gain and learning `NOT_ESTABLISHED`.
4. Run the new file and record the expected import/collection failure before implementation.

## Task 4: CCTS-compatible Human retention audit

**Files**
- Add: `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/ccts_human_epistemic_agency.py`
- Modify: `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/__init__.py`

1. Reuse `CoConstructedThinkingSpaceManifest`, `MetacognitiveTaskClass`, `PolicyAccessCondition`, `ContributionRole`, `AdmissionDisposition`, and `StudyError`.
2. Bind the complete admitted CCTS manifest snapshot with deterministic canonical SHA-256 rather than trusting `space_id`, task labels, or role labels.
3. Enforce phase/access flags, source-role provenance-digest binding, explicit same-domain transfer binding, matched evaluator/rubric/control bindings, condition-manifest digests recomputed from actual condition content, and exact held-out content separation.
4. Produce structural observations only; retain explicit residuals for matched-practice comparator, semantic answer equivalence, actual exposure/access, delayed retention, baseline ability, causal identification, evidence independence, and incomplete conversation retrieval.
5. Export the surface and run the focused tests to green.

## Task 5: Minimal integration documentation

**Files**
- Modify: `research-labs/human-ai-longitudinal-study_v0.1.0/README.md`
- Modify: `docs/INDEX.md`

1. Link the two executable surfaces to the already-approved #205 design and canonical CCTS ancestry.
2. State that core CCTS and longitudinal required fields are unchanged.
3. State that #199 revision code remains superseded by `epistemic_revision.py` and no obsolete module was restored.
4. Preserve claim ceilings and synthetic/privacy boundaries.

## Task 6: Verification, reversible delivery, and Draft PR

1. Run both new focused test files.
2. Run all directly affected CCTS, revision, robustness, metacognitive, and continuity suites.
3. Run the full human-AI longitudinal component pytest suite.
4. Run strict mypy, Ruff, repository-prescribed Quality checks that cover the changed surface, and `git diff --check`.
5. Generate a binary-safe patch, a verification record containing exact commands/literal outputs/exit statuses, and a runnable rollback script; execute the patch and rollback checks in disposable copies/worktrees.
6. Commit only CCTS-scoped files, push the single branch, create one Draft PR against `main`, attach it to this task, and verify Quality/CodeQL/other required workflows against the exact pushed head. The in-module validation binding proves declared-head equality only; actual Git-head identity remains an external GitHub/CI verification fact.
7. Stop without merging and report all residual scientific and method gaps separately.
