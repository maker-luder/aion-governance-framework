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

## Source package boundary

Source-derived components preserve their original candidate status. Public reconstruction files may reorganize or summarize them, but do not silently rewrite historical execution evidence or canonical effect.
