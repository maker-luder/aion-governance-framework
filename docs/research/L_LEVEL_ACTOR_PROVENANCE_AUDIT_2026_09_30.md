# L-level actor provenance audit — 2026-09-30

Status: `DOCUMENTATION_ONLY / ACTOR_AUDIT_PARTIAL / REENTRY_HOLD`

This is a separate review record reconstructed from current `main` at `15ab7c5f5711bee20957cec6f1b9d8a351e5ca6e`. It preserves the bounded actor-attribution findings and distinguishes three L-level namespaces. It does not resolve the terminology or define a runtime.

```text
ANTECEDENT_HOLD = PR #229
ORIGINAL_HOLD_COMMIT = 5bc0ad43d4000b9a338ac148381568af7099e618
FOLLOWUP_AUDIT_COMMIT = f78ca3e4ae68ef91795f2fc74cd1d8037a8620c8
PR_229_STATE_AT_AUDIT = CLOSED / DRAFT / NOT_MERGED
NEW_RECORD_BASE = 15ab7c5f5711bee20957cec6f1b9d8a351e5ca6e
OLD_BRANCH_ROLE = AUDIT_EVIDENCE_SOURCE_ONLY
OLD_BRANCH_MERGED_OR_REBASED = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The follow-up audit was recorded on the historical #229 branch. This new file is an independent candidate on current-main ancestry, not a transplant of the original HOLD file or its Git history. PR #229 stays closed and unmerged. Neither this file nor a draft PR reopens it.

## Controls, method, and evidence register

Current-main [change provenance rules](../governance/CHANGE_PROVENANCE_RULES_v0.1.md), [epistemic provenance note](../../research-labs/coupled-cognition-quality-factory_v0.1.0/docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md), and [ledger implementation](../../research-labs/coupled-cognition-quality-factory_v0.1.0/src/aion_coupled_quality/provenance.py) were reread. Merged [PR #228](https://github.com/maker-luder/aion-governance-framework/pull/228) added a separate `ContributionActor` axis. Its code requires a specific supported AI actor before admitting a new `AI_FORMALIZATION` ledger entry. An unresolved historical description is an audit finding, not an admissible new ledger entry with a guessed actor.

```text
CONTRIBUTION_ORIGIN != CONTRIBUTOR_ACTOR
SOURCE != AUTHORSHIP != IMPLEMENTATION != REVIEW != APPROVAL
GENERIC_CHATGPT != CHATGPT_TEACHER
GENERIC_CHATGPT != CHATGPT_WORK
GENERIC_CHATGPT != CODEX
AI_FORMALIZATION != SPECIFIC_ACTOR
GIT_COMMITTER != CONCEPTUAL_AUTHOR
ACTOR_LABEL != VERIFIED_MODEL_IDENTITY
PROVENANCE != CORRECTNESS
```

Evidence keys below name the exact inspected records; a document's own attribution is evidence of what it reports, not independent authentication of model or person identity.

| Key | Inspected source | Scope |
|---|---|---|
| E1 | [PR #228](https://github.com/maker-luder/aion-governance-framework/pull/228), head `ddaf09a86ce94d400ae262a19e5e469af6c3b3a6`, merge `be585416032fd4712be4e36b240a9b54bbe543e7` | Human-origin correction; explicitly reported Teacher formalization and bounded implementation; scoped merge receipt |
| E2 | [PR #222](https://github.com/maker-luder/aion-governance-framework/pull/222), [§22 branch document at `8e1d1f1`](https://github.com/maker-luder/aion-governance-framework/blob/8e1d1f1c29f16984ebe70547a26af3f1db46009e/docs/research/HIERARCHICAL_PERSONALIZATION_POLICY_ARTIFACT_CCTS_PROBE_2026_09_27.md) | Human challenge; explicitly reported Teacher formalization; local policy hierarchy |
| E3 | [PR #229](https://github.com/maker-luder/aion-governance-framework/pull/229), original `5bc0ad43d4000b9a338ac148381568af7099e618`, follow-up `f78ca3e4ae68ef91795f2fc74cd1d8037a8620c8` | Historical HOLD and bounded audit; neither merged |
| E4 | [PR #230](https://github.com/maker-luder/aion-governance-framework/pull/230), [current-main drift record](INTERACTION_ROUTING_DRIFT_OBSERVATION_2026_09_30.md) §§7, 11, merge `15ab7c5f5711bee20957cec6f1b9d8a351e5ca6e` | Explicit origin/actor pairs in that record only |
| E5 | [Role separation note](HUMAN_AI_RESEARCH_ROLE_SEPARATION_2026_09_13.md) | Human-origin local role rule and Teacher formalization |
| E6 | [Change provenance rules](../governance/CHANGE_PROVENANCE_RULES_v0.1.md) | Legacy generic `CHATGPT`, candidate status and unresolved fine attribution |
| E7 | [Supplier-trust CAPA](../history/reconciliation/POL_UPSTREAM_SUPPLIER_TRUST_001_FREEZE_AND_CHANGE_CONTROL_2026-08-08.md) NCR-SUP-003 | Document roles separated from executable implementation; generic actor remains |
| E8 | [CCTS contrast record](CCTS_LEARNING_CONTRAST_STRENGTHENING_2026-09-28.md) §7 | `AI_FORMALIZATION` identifies a role, not a specific actor |
| E9 | [Longitudinal README](../../research-labs/human-ai-longitudinal-study_v0.1.0/README.md), introducing `e11d4c5d602f284f32d8651e3d73113cb8419a14`, parent `7065e850f2e0622509026aeda544eabceb289932` | Exact phrase occurrence; no proposal definition |
| E10 | [Current subjectivity evidence protocol](../SUBJECTIVITY_EVIDENCE_PROTOCOL.md) §Claim ladder | Present L0–L5 meanings; no inference of attainment |

Confidence values are limited to `CONFIRMED`, `SUPPORTED`, `SOURCE_UNVERIFIED`, and `CONFLICT_REQUIRES_REVIEW`. `ROLE_DISTINCTION_CONFIDENCE` concerns the bounded role or source claim; `SPECIFIC_ACTOR_CONFIDENCE` concerns a named collaborator for that same scoped claim. A `CONFIRMED` field means an explicit repository record, not independent identity verification. `UNKNOWN` in a role column means no adequate attribution was found; `NONE` is reserved for an explicit exclusion. Git author/committer metadata never fills an authorship column by itself.

## ACTOR_PROVENANCE_AUDIT_MATRIX

| RECORD / FILE | DATE | CLAIM OR CHANGE | CURRENT ATTRIBUTION | EVIDENCE | PROPOSED_BY | IMPLEMENTED_BY | REVIEWED_BY | APPROVED_BY | CONTRIBUTION_ORIGIN | CONTRIBUTOR_ACTOR | ROLE_DISTINCTION_CONFIDENCE | SPECIFIC_ACTOR_CONFIDENCE | DISPOSITION |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PR #228 / `provenance.py` | 2026-09-29 | Separate origin and actor axes | Human correction; Teacher formalization and bounded implementation, as PR reports | E1 | HUMAN_OWNER | CHATGPT_TEACHER, per PR | Exact-head review requested; completion not inferred | HUMAN_OWNER for merge per PR receipt; independent identity unknown | HUMAN_ORIGIN; AI_FORMALIZATION | HUMAN_OWNER; CHATGPT_TEACHER for scoped contributions | CONFIRMED | CONFIRMED | Preserve axes; merge approval proves neither every review step nor model identity. |
| PR #222 / policy §22 | 2026-09-28 | Add policy L-1 value/purpose | Human challenge; Teacher formalization | E2 | HUMAN_OWNER | File-edit operator unknown; Teacher formalization expressly reported | Adversarial review described; separate reviewer attestation unknown | No canonical/merge approval | HUMAN_ORIGIN; AI_FORMALIZATION; bounded JOINT_SYNTHESIS | HUMAN_OWNER; CHATGPT_TEACHER for stated roles | CONFIRMED | CONFIRMED | Local working policy only; no runtime inference. |
| PR #229 / historical HOLD | 2026-09-29 | Pause reconciliation | Human stop decision; Human and Teacher reported confusion | E3 | HUMAN_OWNER for HOLD | Exact document author/operator unknown | Formal review outcome unknown | HUMAN_OWNER for stop; no canonical approval | HUMAN_ORIGIN for stop; other role not assigned | HUMAN_OWNER; CHATGPT_TEACHER for reported observation only | CONFIRMED | SUPPORTED | Observer is not automatically implementer. PR stays closed. |
| PR #230 / drift record | 2026-09-30 | Bounded observation and mapping | Explicit Human origin/actor and Teacher origin/actor pairs | E4 | HUMAN_OWNER for observation | CHATGPT_TEACHER for record's explicitly reported drafting/formalization; Git operator unknown | Not inferred from merge | Approval actor not independently established here | HUMAN_ORIGIN; AI_FORMALIZATION | HUMAN_OWNER; CHATGPT_TEACHER | CONFIRMED | CONFIRMED | Applies to #230 only; does not resolve #229. |
| Role-separation note | 2026-09-13 | Distinct Teacher/Work/Codex assignments | Human rule; Teacher formalization | E5 | HUMAN_OWNER | CHATGPT_TEACHER for formalization; file operator unknown | UNKNOWN | UNKNOWN | HUMAN_ORIGIN; AI_FORMALIZATION | HUMAN_OWNER; CHATGPT_TEACHER for scoped statements | CONFIRMED | CONFIRMED | Role assignments do not attribute unrelated files to Work or Codex. |
| Change provenance rules | Historical; amended 2026-09-29 | `IMPLEMENTED_BY = CHATGPT` and generic example | Generic ChatGPT; Codex contribution to this rule expressly NONE | E6; E1 amendment | HUMAN_OWNER, expressly | Generic CHATGPT for candidate text; specific actor unknown | UNKNOWN | Candidate says OWNER_REVIEW=PENDING | AI_FORMALIZATION for stated document formatting | SOURCE_UNVERIFIED as specific AI actor | CONFIRMED | SOURCE_UNVERIFIED | Example's generic `confidence: CONFIRMED` cannot verify a specific actor. |
| Supplier-trust CAPA | 2026-08-08 | Correct document-work vs executable-work ambiguity | Generic CHATGPT policy formalization/crosswalk/QA; executable NONE; Codex NONE | E7 NCR-SUP-003 | HUMAN_OWNER for policy | Generic CHATGPT for documentation; executable NONE | Generic CHATGPT pre-promotion QA; specific actor unknown | HUMAN_OWNER accepted specified CAPAs, not blanket canonicalization | AI_FORMALIZATION for stated document work | SOURCE_UNVERIFIED as specific AI actor | CONFIRMED | SOURCE_UNVERIFIED | Role distinction confirmed; Teacher/Work identity unverified. |
| Legacy exact-pattern inventory | Current main 2026-09-30 | 21 files with `IMPLEMENTED_BY = CHATGPT` or `implemented_by: CHATGPT` | Generic CHATGPT; events not collectively adjudicated | E6, E7, inventory below | Per event unknown | Specific actor unknown | Per event unknown | Per event unknown | Per event unknown | SOURCE_UNVERIFIED | SOURCE_UNVERIFIED | SOURCE_UNVERIFIED | Queue only; no bulk rewrite or count of misattributions. |
| CCTS contrast record §7 | 2026-09-28 | Formalization, counterexamples, code correction | `AI_FORMALIZATION` only in scoped provenance field | E8 | HUMAN_OWNER for inspection request | Specific actor not established by origin field | UNKNOWN | UNKNOWN | AI_FORMALIZATION | SOURCE_UNVERIFIED from that field | CONFIRMED | SOURCE_UNVERIFIED | A historical audit finding, not a new admitted ledger record. |
| Longitudinal README / runtime phrase | 2026-09-28 | Lists held `L-1 runtime` | No runtime-proposal actor or definition | E9, child/parent text | UNKNOWN | UNKNOWN for underlying proposal | UNKNOWN | UNKNOWN | UNKNOWN | SOURCE_UNVERIFIED | CONFIRMED for occurrence only | SOURCE_UNVERIFIED | Commit identity is not conceptual proposal authorship. |

`CONFLICT_REQUIRES_REVIEW`: no contradictory *specific actor* attribution was established within these inspected records. This is not a repository-wide proof that no conflict exists. A later conflicting contemporaneous source must be recorded as `CONFLICT_REQUIRES_REVIEW`, without silently choosing one.

### LEGACY_ATTRIBUTION_AUDIT_QUEUE

An exact-pattern search of `docs`, `components`, and `research-labs` at the specified current-main SHA returned **21 files**. The two individually discussed files are E6 and E7. The other 19 paths are listed for later event-by-event review:

```text
components/aion_runtime_v0.1.0/README.md
components/astra_runtime_v0.1.0/README.md
components/individual_runtime_state_v0.1.0/README.md
docs/C0_ACCEPTANCE_EVIDENCE_INDEX_2026-08-08.md
docs/C0_EXTERNAL_STANDARDS_CROSSWALK_2026-08-08.md
docs/RUNTIME_REALITY_MATRIX_CURRENT_2026-08-08.md
docs/history/c0/C0_ACCEPTANCE_EVIDENCE_INDEX_RECOVERABILITY_ADDENDUM_2026-08-08.md
docs/history/c0/C0_FINAL_CONSISTENCY_REVIEW_2026-08-08.md
docs/history/c0/C0_OWNER_ACCEPTANCE_CRITERIA_DRAFT_2026-08-08.md
docs/history/c0/C0_OWNER_ACCEPTANCE_CRITERIA_FINAL_CANDIDATE_2026-08-08.md
docs/history/c0/C0_RECOVERABILITY_DEEP_REVIEW_2026-08-08.md
docs/history/c0/C0_REMAINING_HOLD_REGISTER_2026-08-08.md
docs/history/c0/RUNTIME_REALITY_MATRIX_C0_CLOSING_2026-08-08.md
docs/history/reconciliation/MIGRATION_EVIDENCE_REUSE_IMPLEMENTATION_REPORT_2026-08-08.md
docs/history/reconciliation/P0_RUNTIME_BINDING_IMPLEMENTATION_REPORT_2026-08-08.md
docs/history/reconciliation/P1_P2_RUNTIME_LINEAGE_LIFECYCLE_IMPLEMENTATION_REPORT_2026-08-08.md
docs/history/reconciliation/RUNTIME_REALITY_MATRIX_2026-08-08.md
docs/history/reconciliation/RUNTIME_TWIN_PROVENANCE_ALIGNMENT_2026-08-08.md
docs/history/reconciliation/STABILIZATION_A_B_REPORT_2026-08-08.md
```

```text
INVENTORY_ENTRY != PROVEN_MISATTRIBUTION
LEGACY_GENERIC_CHATGPT != VERIFIED_SPECIFIC_ACTOR
UNRECOVERABLE_SPECIFIC_ACTOR = SOURCE_UNVERIFIED
```

The queue is a bounded literal-pattern inventory, not a census of every generic narrative use of “ChatGPT” and not a claim that all 21 labels are wrong. No batch relabeling follows from it.

## L-1 runtime: verified mention, unresolved proposal

The exact phrase `L-1 runtime` occurs in the longitudinal README at introducing commit `e11d4c5d602f284f32d8651e3d73113cb8419a14` (line 156 at that commit). It does **not** occur in that path at parent `7065e850f2e0622509026aeda544eabceb289932`. On current main it remains a list item describing separate held/document-only questions; it is not a definition. This is the first verified repository-file occurrence in the bounded inspected lineage, not proof of the first occurrence anywhere or the original proposal source.

```text
L_MINUS_1_RUNTIME_FIRST_VERIFIED_REPOSITORY_MENTION = e11d4c5d602f284f32d8651e3d73113cb8419a14
FIRST_VERIFIED_MENTION != ORIGINAL_PROPOSAL_SOURCE
L_MINUS_1_RUNTIME_ORIGINAL_SOURCE = SOURCE_UNVERIFIED
L_MINUS_1_RUNTIME_PROPOSED_BY = SOURCE_UNVERIFIED
L_MINUS_1_RUNTIME_REVIEWED_BY = SOURCE_UNVERIFIED
L_MINUS_1_RUNTIME_DEFINITION = NOT_RECONSTRUCTED
L_MINUS_1_RUNTIME_CANONICAL_STATUS = NOT_ESTABLISHED
L_MINUS_1_RUNTIME_IMPLEMENTATION = NOT_ESTABLISHED
L_MINUS_1_RUNTIME_SUPERSESSION_OR_ABANDONMENT = UNKNOWN
```

## L_LEVEL_NAMESPACE_MATRIX

| NAMESPACE | LEVEL | DEFINITION | SOURCE | ACTOR | STATUS | CANONICAL? | SCOPE | COLLISION_RISK |
|---|---|---|---|---|---|---|---|---|
| POLICY | L-1 | Human value/purpose, why | E2 §22 | Human challenge; Teacher formalization | Local working / HOLD | No | Human-governed collaboration policy | Same label as runtime phrase |
| POLICY | L0 | Core objective, what | E2 §22 | Same scoped attribution | Local working / HOLD | No | Policy artifact | Same numeral as subjectivity L0 |
| POLICY | L1 | High-level policy | E2 §22 | Same scoped attribution | Local working / HOLD | No | Policy artifact | Same numeral as subjectivity L1 |
| POLICY | L2 | Sub-policy/decision rule | E2 §22 | Same scoped attribution | Local working / HOLD | No | Policy artifact | Same numeral as subjectivity L2 |
| POLICY | L3 | Operational rule | E2 §22 | Same scoped attribution | Local working / HOLD | No | Policy artifact | Same numeral as subjectivity L3 |
| POLICY | L4 | Case/example | E2 §22 | Same scoped attribution | Local working / HOLD | No | Policy artifact | Same numeral as subjectivity L4 |
| SUBJECTIVITY | L0 | `OBSERVATION` | E10 | Schema author not established here | Current operational claim ladder | Current protocol, not evidence of attainment | Claim-strength classification | Same numeral as policy L0 |
| SUBJECTIVITY | L1 | `REPEATABLE_BEHAVIOR` | E10 | Same attribution limit | Same | Same | Same | Same numeral as policy L1 |
| SUBJECTIVITY | L2 | `STATE_ASSOCIATION` | E10 | Same attribution limit | Same | Same | Same | Same numeral as policy L2 |
| SUBJECTIVITY | L3 | `INTERVENTION_SENSITIVE_MECHANISM` | E10 | Same attribution limit | Same | Same | Same | Same numeral as policy L3 |
| SUBJECTIVITY | L4 | `ROBUST_REPLICATION` | E10 | Same attribution limit | Same | Same | Same | Same numeral as policy L4 |
| SUBJECTIVITY | L5 | `SUBJECTIVITY_NOT_AUTOMATICALLY_ESTABLISHED` | E10 | Same attribution limit | Same | Same | Same | No automatic conclusion |
| RUNTIME | `L-1 runtime` | SOURCE_UNVERIFIED / NOT_RECONSTRUCTED | E9; E3 | SOURCE_UNVERIFIED | Held/document-only reference; proposal status unknown | NOT_ESTABLISHED | Unknown runtime proposal | Do not equate to either other namespace |

```text
POLICY_L_MINUS_1 != RUNTIME_L_MINUS_1
POLICY_L0 != SUBJECTIVITY_L0
POLICY_L1 != SUBJECTIVITY_L1
POLICY_L2 != SUBJECTIVITY_L2
POLICY_L3 != SUBJECTIVITY_L3
POLICY_L4 != SUBJECTIVITY_L4
CROSS_NAMESPACE_EQUIVALENCE = NOT_ESTABLISHED
```

Numerical similarity supplies no semantic mapping. The current protocol's claim levels are not findings that any level has been achieved.

## Reverse review, unresolved questions, and gate

- This new candidate does not make #229 merged, reopened, canonical, or current-main ancestry. The old `f78ca3e` is cited as evidence history, not made a parent of this new branch.
- Explicit actor attributions in E1/E2/E4/E5 are limited to the contribution each record names. Generic `CHATGPT` and `AI_FORMALIZATION` were not converted into Teacher, Work or Codex. No Git author was assigned conceptual authorship on that basis.
- The supplier-trust row separately marks the documented work/implementation distinction `CONFIRMED` and specific actor `SOURCE_UNVERIFIED`. Other matrix confidence pairs receive the same scoped reading.
- The README phrase does not supply an original source, definition, implementation, canonical status, or evidence of abandonment. Three namespaces remain separate; no crosswalk is asserted.
- The actor audit is partial and the runtime proposal remains unreconstructed. This document cannot satisfy the re-entry prerequisite.

```text
ACTOR_AUDIT_STATUS = BOUNDED / PARTIAL
L_MINUS_1_RUNTIME_SOURCE = SOURCE_UNVERIFIED
L_MINUS_1_RUNTIME_DEFINITION = NOT_RECONSTRUCTED
REENTRY_PREREQUISITE = NOT_SATISFIED
REENTRY = HOLD
TERMINOLOGY_RECONCILIATION = NOT_ADVANCED
IMPLEMENTATION = NONE
EXPERIMENT = NONE
WRITE_TO_MAIN = NO
MERGE = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

Unresolved: identify the original `L-1 runtime` proposal and contemporaneous actor-specific evidence; determine whether it was reviewed, implemented, superseded, or abandoned. Legacy generic records require individual source checks only if an actor-specific answer later matters. The next gate is source retrieval, followed by a fresh actor check; no terminology reconciliation starts from this document.
