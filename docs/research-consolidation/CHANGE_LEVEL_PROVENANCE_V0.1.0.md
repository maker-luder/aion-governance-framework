# AION Change-Level Provenance v0.1.0

> This artifact records only the provenance of the current convergence-branch final-review corrections. It does **not** rewrite the authorship or provenance of the historical P2 source material.

## 1. Role separation

| Role | Actor | Status | Authority effect | Scope |
|---|---|---|---|---|
| Human Owner proposal and authority boundary | `HUMAN_OWNER` | `OWNER_APPROVAL_PENDING` | `NONE` | Proposed the final-review corrections and retains authority over canonical, settings, merge, release and deployment actions |
| Architecture and review input | `CHATGPT` | `REVIEW_INPUT` | `NONE` | Supplied architecture/review framing and constraints; did not grant authority or canonical status |
| Convergence implementation and validation | `MANUS` | `IMPLEMENTED_ON_CONVERGENCE_BRANCH` | `NONE` | Implemented only the requested literature, provenance, taxonomy-invariant, schema, checker, test and handoff corrections |
| Owner approval gate | `HUMAN_OWNER` | `PENDING` | `NONE` | No approval is recorded for Topics application, canonical promotion, merge, release or deployment |

## 2. Historical P2 preservation

The original P2 provenance block and historical source references remain unchanged in their historical meaning. The current convergence provenance is a distinct change-level record. It does not replace the original P2 authors, does not attribute the historical P2 implementation to Manus, and does not rewrite the P2 historical test-count statement.

The current evidence-admission implementation now carries this separate change-level provenance reference. Its `provenance` field remains the P2 source/evidence provenance, while `change_level_provenance` identifies the actors and authority boundary for this convergence correction.

## 3. Current change surfaces

The change-level record covers the current External Literature Crosswalk, Research Index, P2 evidence-admission record, Public Discoverability Taxonomy and Cross-Branch Index. It is not a claim of authorship over historical research sources, external papers, repositories or Owner decisions.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
TOPICS_APPLIED = FALSE
MAIN_MERGE = PROHIBITED
OWNER_APPROVAL = PENDING
```
