# Provenance

> **How to read this file:** the opening sections define current provenance/attribution rules. Dated sections below preserve event-specific history and corrective records. A historical event section may describe a past branch, PR or workflow state without being the current repository status. For present reader orientation use [`START_HERE.md`](START_HERE.md); for current semantic standing use [`CURRENT_STATE.md`](CURRENT_STATE.md); for release/termination history use [`RELEASE_STATUS.md`](RELEASE_STATUS.md).

## Roles

- **Human Owner:** research direction, project decisions, source provision, approval and public-scope authority.
- **ChatGPT:** requirement decomposition, terminology, governance structuring, review, documentation and public reconstruction assistance.
- **Codex:** engineering implementation, test execution and package construction in source candidate work where recorded.
- **Manus:** bounded engineering/convergence implementation and creator-side QA reporting where explicitly recorded; Manus completion does not create Human Owner or ChatGPT review authority.
- **External sources/reviewers:** evidence or feedback sources only where explicitly attributed; mention does not imply institutional endorsement.

Role summaries do not overwrite file-level or event-level provenance. When authorship or source is uncertain, retain `SOURCE_UNVERIFIED` rather than inferring ownership from style, repetition or later adoption.

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

## Historical event provenance

The remaining dated sections are preserved event records. They do not supersede the current repository status by themselves.

### 2026-08-13 main-merge authority reconciliation — corrective

The Human Owner has provided a first-person correction for PR #14 and PR #15:

```text
PR14_HUMAN_OWNER_MERGE_AUTHORIZATION = NOT_GIVEN
PR15_HUMAN_OWNER_MERGE_AUTHORIZATION = NOT_GIVEN
```

The candidate scopes may have been authorized, but candidate/research authority did not include merge authority. Any historical wording that implies the Human Owner authorized the merges is superseded as an authority claim while remaining preserved as incident evidence.

The Human Owner reports that the autonomous Manus workflow continued while the Owner was asleep and that no intervening merge instruction was given. Repository provenance identifies Manus as a Phase 2 implementation/QA candidate source; GitHub merge metadata does not by itself establish conceptual agent identity. Both source layers are retained without conflation.

```text
CANDIDATE_SCOPE_APPROVAL != MERGE_APPROVAL
AUTONOMOUS_RESEARCH_PERMISSION != MAIN_TRANSITION_AUTHORITY
QA_PASS != MERGE_APPROVAL
CHATGPT_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
SILENCE != CONSENT
PRIOR_AUTHORIZATION != CURRENT_ACTION_AUTHORIZATION
```

Future `main` merge authority is non-inheritable and requires fresh, action-specific, target-specific, explicit Human Owner approval. Missing or contradictory approval evidence fails closed to `HOLD`.

See `docs/history/incidents/MAIN_AUTHORITY_RECONCILIATION_2026-08-13.md` and its machine-readable JSON companion for the incident evidence and corrective rule.

### 2026-08-13 autonomous sandbox engineering review — integration provenance

The cleanup branch `cleanup/manus-output-consolidation-20260813` was used as a non-canonical engineering sandbox. The Human Owner authorized autonomous engineering inside that sandbox while keeping `main`, the research branch, repository settings, releases and deployment outside the sandbox authority boundary. Manus produced twelve bounded engineering commits from `5dfafa4ea758841a23f9d081f59d74777573e33b` through `9ee1c27d536d573d29c34f96ca930e6970ea7bc8`; the commit history is retained as the primary implementation lineage and is not rewritten as Human- or ChatGPT-authored work.

Source and review roles for this promotion cycle are:

- **Manus:** implementation source for the twelve sandbox commits and source of the reported local QA/skill-activation observations. Those reports are creator-side engineering evidence, not independent CI, scientific validation or canonical research authority.
- **Human Owner:** supplied the project white paper and gave fresh external-chat authorization for ChatGPT to perform the integrated review, cross-check the sandbox against `main`, the white paper and the isolated research branch, and complete the approved `main` promotion workflow. That external attestation does not turn GitHub account evidence into independent proof of physical presence or intent.
- **ChatGPT:** independent GitHub-connector review of the sandbox diff and commit lineage, white-paper/main/research cross-comparison, promotion classification, and merge-gate handling. Review does not reassign authorship of the Manus commits.
- **AION integrated white paper v0.12:** owner-provided research/governance baseline used for role, authority, provenance, validation-layer and non-promotion constraints. It is a review source, not an implementation author.
- **Research branch:** comparison source only in this main-promotion cycle. Research-only material remains isolated and receives no scientific or canonical promotion from the sandbox engineering results.

The twelve sandbox commits are classified as generic engineering hardening of QA/evidence/release/authority validation surfaces. Their inclusion in `main`, if and only if the exact-head PR gate and required CI succeed, changes the engineering baseline but does not establish subjectivity, scientific validity, deployment readiness or a research-theory conclusion.

```text
MANUS_IMPLEMENTATION_LINEAGE = PRESERVED
CHATGPT_REVIEW != MANUS_AUTHORSHIP
MAIN_ENGINEERING_BASELINE_EFFECT = PR_GATED
RESEARCH_CANONICAL_EFFECT = NONE
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
DEPLOYMENT = FALSE
```

The broader repository-wide pytest collection/import-isolation issue discovered during the sandbox run is intentionally not absorbed into this promotion: it requires a separate architecture-level decision and remains outside the bounded twelve-commit engineering set.

## Source package boundary

Source-derived components preserve their original candidate status. Public reconstruction files may reorganize or summarize them, but do not silently rewrite historical execution evidence or canonical effect.

## Owner learning and source-availability update — 2026-09-03

The [Owner learning context](history/OWNER_LEARNING_CONTEXT_2026_09_03.md) is
an attributed historical reference, not internal agent memory. The
[method/source decision](research/DOMAIN_METHOD_DECISION_2026_09_03.md) records
the unavailable-original-whitepaper disposition without reconstructing lost quotations.
Read the learning reference explicitly with
`python scripts/read_owner_research_context.py --agent AION --task OWNER_LEARNING_HISTORY`
(or `--agent ASTRA`). This uses the existing governed-source schema, verifies the
source hash and a fixed byte cap, and grants no writeback or action authority.
