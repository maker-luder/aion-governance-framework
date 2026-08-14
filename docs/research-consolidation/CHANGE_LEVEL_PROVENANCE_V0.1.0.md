# AION Change-Level Provenance v0.1.0

> This artifact records only the provenance of the current convergence-branch final-review corrections. It does **not** rewrite the authorship or provenance of the historical P2 source material.

## 1. Role separation

| Role | Actor | Status | Authority effect | Scope |
|---|---|---|---|---|
| Human Owner task authorization and final authority | `HUMAN_OWNER` | `TASK_AUTHORIZED_OWNER_APPROVAL_PENDING` | `NONE` | Authorized this closure and retains final authority over public positioning, canonical, settings, merge, release and deployment actions |
| Final-review findings and architecture review | `CHATGPT` | `FINAL_REVIEW_FINDINGS_PROPOSED` | `NONE` | Proposed the final-review findings and architecture constraints; did not grant authority or canonical status |
| Convergence implementation and validation | `MANUS` | `IMPLEMENTED_ON_CONVERGENCE_BRANCH` | `NONE` | Implemented and validated only the requested literature, provenance, public-positioning, schema, checker, test and handoff corrections |
| Owner approval gate | `HUMAN_OWNER` | `PENDING` | `NONE` | No approval is recorded for Topics application, canonical promotion, merge, release or deployment |

## 2. Historical P2 preservation

The original P2 provenance block and historical source references remain unchanged in their historical meaning. The current convergence provenance is a distinct change-level record. It does not replace the original P2 authors, does not attribute the historical P2 implementation to Manus, and does not rewrite the P2 historical test-count statement.

The current evidence-admission implementation now carries this separate change-level provenance reference. Its `provenance` field remains the P2 source/evidence provenance, while `change_level_provenance` identifies ChatGPT as the final-review findings source, Human Owner as task authorizer/final authority, Manus as implementation actor and Owner approval as PENDING.

## 3. Current change surfaces

The change-level record covers the current External Literature Crosswalk, Research Index, P2 evidence-admission record, Public Discoverability Taxonomy and Cross-Branch Index. It is not a claim of authorship over historical research sources, external papers, repositories or Owner decisions.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
TOPICS_APPLIED = FALSE
MAIN_MERGE = PROHIBITED
OWNER_APPROVAL = PENDING
```
