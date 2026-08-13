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

## 2026-08-13 main-merge authority reconciliation — corrective

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

See `docs/MAIN_AUTHORITY_RECONCILIATION_2026-08-13.md` and its machine-readable JSON companion for the incident evidence and corrective rule.

## Source package boundary

Source-derived components preserve their original candidate status. Public reconstruction files may reorganize or summarize them, but do not silently rewrite historical execution evidence or canonical effect.
