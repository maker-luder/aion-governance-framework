# Provenance

## Roles

- **Human Owner:** research direction, project decisions, source provision, approval and public-scope authority.
- **ChatGPT:** requirement decomposition, terminology, governance structuring, review, documentation and public reconstruction assistance.
- **Codex:** engineering implementation, test execution and package construction in source candidate work where recorded.

## Confirmed attribution examples

- Topic-cued selective cross-session recall: core concept originated with the human Owner; `Topic-Cued Cross-Session Recall (TCCR)` and its gate structure were ChatGPT-assisted formalization; the resulting framework is jointly developed.
- Subjectivity research as an attack surface: core concern originated with the human Owner; threat categories and evidence gate were ChatGPT-assisted formalization; the resulting framework is jointly developed.
- Twin male embodiment request: explicit current request originated with the human Owner; requirements and governance boundaries were ChatGPT-assisted formalization.

Unknown historical attribution is marked `SOURCE_UNVERIFIED` rather than guessed.

## Imperceptible watermark policy — normative

The project distinguishes technical content markers, provenance records, authorship claims and identity claims. They are not interchangeable.

```text
MARKER != IDENTITY
PROVENANCE != IDENTITY
MARKER != AUTHORSHIP_PROOF
RESPECT != WATERMARK
TRANSPARENCY != IMPERCEPTIBLE_MARKING
```

The following requirements apply to project-owned output paths:

1. The project **MUST NOT** intentionally embed imperceptible, hidden or undisclosed machine-readable watermarks or content markers in user-facing text, images, files or other artifacts as a mechanism for identity, authorship, attribution, respect or provenance.
2. The presence or absence of a watermark or content marker **MUST NOT**, by itself, establish the identity of a user, author, model, agent or research subject, and **MUST NOT**, by itself, establish authorship.
3. When provenance is required, the project **SHOULD** use explicit, inspectable, documented and auditable records such as declared attribution, version history, commit lineage, manifests, checksums or other disclosed provenance mechanisms.
4. A marker discovered in an external artifact **MUST** remain an external technical signal. It **MUST NOT** be promoted into canonical identity, authorship or subjectivity evidence.
5. A dependency, provider or output path that requires non-disableable imperceptible watermarking in project-generated outputs **MUST** be treated as incompatible with that output path unless a later explicit governance revision authorizes a transparent alternative.

This policy rejects imperceptible marking as a project provenance or identity mechanism without rejecting provenance itself. Provenance remains a first-class governance requirement; it must remain distinguishable from identity and be represented through transparent, reviewable evidence.

## 2026-08-13 main / white-paper / research cross-review disposition

The Human Owner supplied the AION integrated white paper v0.12 as the governance/research comparison baseline and gave fresh external-chat authorization for ChatGPT to complete one integrated review operation covering the Manus sandbox result, `main`, and this isolated research branch.

The reviewed Manus sandbox engineering set was promoted through PR #18 at exact candidate head `230a321c77734da05f8e5c5bb556ed0ebbdd44ab` after independent GitHub Quality success and the fresh exact-head main-transition authority gate. The resulting `main` merge commit is `e079fb7dfe7a04be7dcb94b8a059951a003caa94`.

Attribution for that operation remains separated:

- **Manus:** implementation source for the twelve autonomous sandbox engineering commits. Its local QA and skill-activation reports remain creator-side observations.
- **ChatGPT:** integrated diff/lineage review, white-paper/main/research cross-comparison, CI failure diagnosis/correction, promotion classification, and transition-gate handling. This review does not reassign Manus authorship.
- **Human Owner:** source of the governing project decision and fresh authorization for this one operation. External chat attestation is not independent proof of physical presence or identity.
- **AION integrated white paper v0.12:** owner-provided governance/research baseline; not an implementation author and not a source of automatic engineering authority.

The post-merge cross-branch comparison shows `main` and this research branch remain deliberately divergent: the research branch retains hundreds of research-only commits while `main` contains newer generic governance/QA hardening. A whole-branch automatic synchronization was not performed because overlapping workflows, QA artifacts and research-specific semantics require conflict-by-conflict review; bulk synchronization would violate the white paper's scope/provenance/non-promotion boundaries.

No post-baseline research family was established as already absorbed into `main`, so no research family, experiment, historical evidence or provenance record is deleted as "already merged" in this operation. Absence of a safe deletion candidate is a preservation decision, not a claim that the research branch is fully reconciled.

The cleanup sandbox branch was fully absorbed by PR #18 and then fast-forwarded to the resulting `main` merge commit so it no longer carries unique repository state. Its commit lineage remains in Git history as Manus implementation provenance.

```text
MAIN_TO_RESEARCH_BULK_SYNC = HOLD_FOR_SEMANTIC_REVIEW
RESEARCH_TO_MAIN_PROMOTION = NONE
RESEARCH_FAMILY_DELETION = NONE_ESTABLISHED_SAFE
MANUS_IMPLEMENTATION_LINEAGE = PRESERVED
CHATGPT_REVIEW != MANUS_AUTHORSHIP
RESEARCH_CANONICAL_EFFECT = NONE
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
DEPLOYMENT = FALSE
```

## Source package boundary

Source-derived components preserve their original candidate status. Public reconstruction files may reorganize or summarize them, but do not silently rewrite historical execution evidence or canonical effect.
