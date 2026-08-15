# Documentation Path Migration

This ledger records the physical documentation convergence. It is a path migration, not a content rewrite. Historical records retain their event-time meaning. `CONTENT_CHANGED = NO` for moved sources; only repository-relative link repair and navigation/index metadata are allowed. No file is deleted by this migration.

## Migration policy

| Field | Rule |
|---|---|
| `MOVE_ONLY` | A source file is relocated with `git mv`; its substantive content remains unchanged. |
| `LINK_FIX` | Only repository-relative links are corrected to resolve after relocation; external URLs and historical event claims are not rewritten. |
| `INDEX_UPDATE` | Navigation indexes and README layout descriptions are updated to reflect the physical tree. |
| `ACTUAL_TEXT_CHANGE` | Not planned for moved historical sources; any exception must be separately listed and justified. |
| `FILES_DELETED` | `0`; deletion candidates remain review-only. |

## Complete move mapping

| OLD_PATH | NEW_PATH | CLASSIFICATION | CONTENT_CHANGED | MOVE_TYPE | REASON |
|---|---|---|---|---|---|
| `docs/AFFECTIVE_COGNITIVE_RESEARCH_DIRECTION.md` | `docs/research/AFFECTIVE_COGNITIVE_RESEARCH_DIRECTION.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Research question and candidate operational chain; not current authority or core reader entry. |
| `docs/AIR_LEGACY_CROSSWALK.md` | `docs/research/AIR_LEGACY_CROSSWALK.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Legacy research crosswalk; preserve status and source semantics. |
| `docs/AI_COLLABORATION_DISCLOSURE.md` | `docs/governance/AI_COLLABORATION_DISCLOSURE.md` | `GOVERNANCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Current attribution and authority-boundary policy. |
| `docs/AUTHORITATIVE_METHODS_CROSSWALK.md` | `docs/evidence/standards/AUTHORITATIVE_METHODS_CROSSWALK.md` | `SUPPORTING_EVIDENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Methods/standards crosswalk; not certification or core claim. |
| `docs/BOUNDED_RUNTIME_CANDIDATE.md` | `docs/research/BOUNDED_RUNTIME_CANDIDATE.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Candidate runtime description; explicitly non-canonical. |
| `docs/C0_ACCEPTANCE_EVIDENCE_INDEX_RECOVERABILITY_ADDENDUM_2026-08-08.md` | `docs/history/c0/C0_ACCEPTANCE_EVIDENCE_INDEX_RECOVERABILITY_ADDENDUM_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated C0 addendum; preserve historical candidate status. |
| `docs/C0_FINAL_CONSISTENCY_REVIEW_2026-08-08.md` | `docs/history/c0/C0_FINAL_CONSISTENCY_REVIEW_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated C0 review record. |
| `docs/C0_OWNER_ACCEPTANCE_CRITERIA_DRAFT_2026-08-08.md` | `docs/history/c0/C0_OWNER_ACCEPTANCE_CRITERIA_DRAFT_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated draft acceptance record. |
| `docs/C0_OWNER_ACCEPTANCE_CRITERIA_FINAL_CANDIDATE_2026-08-08.md` | `docs/history/c0/C0_OWNER_ACCEPTANCE_CRITERIA_FINAL_CANDIDATE_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated final-candidate acceptance record. |
| `docs/C0_RECOVERABILITY_DEEP_REVIEW_2026-08-08.md` | `docs/history/c0/C0_RECOVERABILITY_DEEP_REVIEW_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated C0 recoverability review. |
| `docs/C0_REMAINING_HOLD_REGISTER_2026-08-08.md` | `docs/history/c0/C0_REMAINING_HOLD_REGISTER_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated HOLD register; preserve all HOLD semantics. |
| `docs/CHANGE_PROVENANCE_RULES_v0.1.md` | `docs/governance/CHANGE_PROVENANCE_RULES_v0.1.md` | `GOVERNANCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Current provenance rule candidate; governance rather than reader core. |
| `docs/CONTINUITY_LAYER_MODEL.md` | `docs/research/CONTINUITY_LAYER_MODEL.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Research model of continuity layers; not a current status entry point. |
| `docs/CROSS_CONVERSATION_EXTRACTION_REGISTER.md` | `docs/research/CROSS_CONVERSATION_EXTRACTION_REGISTER.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Research reconstruction register; preserve provenance. |
| `docs/DEVELOPER_LOCAL_RESEARCH_DISTRIBUTION.md` | `docs/research/DEVELOPER_LOCAL_RESEARCH_DISTRIBUTION.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Developer research distribution design; not public core. |
| `docs/DEVELOPER_RESEARCH_USE_AND_POLICY.md` | `docs/research/DEVELOPER_RESEARCH_USE_AND_POLICY.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Developer research-use policy and scope. |
| `docs/DIGITAL_INDIVIDUAL_SUBJECTIVITY_SYNTHESIS.md` | `docs/research/DIGITAL_INDIVIDUAL_SUBJECTIVITY_SYNTHESIS.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Research synthesis with explicit non-claim boundary. |
| `docs/FINAL_BRANCH_DISPOSITION_2026-08-15.json` | `docs/history/branch-and-release/FINAL_BRANCH_DISPOSITION_2026-08-15.json` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Historical branch inventory snapshot; exact event-time data must remain. |
| `docs/FINAL_BRANCH_DISPOSITION_2026-08-15.md` | `docs/history/branch-and-release/FINAL_BRANCH_DISPOSITION_2026-08-15.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Historical branch disposition snapshot. |
| `docs/FINAL_REPOSITORY_FREEZE_2026-08-15.json` | `docs/history/branch-and-release/FINAL_REPOSITORY_FREEZE_2026-08-15.json` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Historical freeze payload; preserve exact provenance. |
| `docs/FINAL_REPOSITORY_FREEZE_2026-08-15.md` | `docs/history/branch-and-release/FINAL_REPOSITORY_FREEZE_2026-08-15.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Historical freeze-preparation snapshot. |
| `docs/GOVERNANCE_MODEL.md` | `docs/governance/GOVERNANCE_MODEL.md` | `GOVERNANCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Current human-authority and state-class model. |
| `docs/IVV_READINESS_PACKET.md` | `docs/evidence/verification/IVV_READINESS_PACKET.md` | `SUPPORTING_EVIDENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Evidence/readiness packet; explicitly does not claim IV&V. |
| `docs/MAIN_AUTHORITY_RECONCILIATION_2026-08-13.json` | `docs/history/incidents/MAIN_AUTHORITY_RECONCILIATION_2026-08-13.json` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | PR/authority incident record. |
| `docs/MAIN_AUTHORITY_RECONCILIATION_2026-08-13.md` | `docs/history/incidents/MAIN_AUTHORITY_RECONCILIATION_2026-08-13.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | PR/authority incident record. |
| `docs/MAIN_TRANSITION_AUTHORITY_GATE.md` | `docs/governance/MAIN_TRANSITION_AUTHORITY_GATE.md` | `GOVERNANCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Current merge-authority control specification. |
| `docs/MEMORY_LAYER_MODEL.md` | `docs/research/MEMORY_LAYER_MODEL.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Research model; not evidence of memory truth. |
| `docs/MIGRATION_EVIDENCE_REUSE_IMPLEMENTATION_REPORT_2026-08-08.md` | `docs/history/reconciliation/MIGRATION_EVIDENCE_REUSE_IMPLEMENTATION_REPORT_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated implementation/reconciliation report. |
| `docs/MODEL_HANDOFF_AND_RELATIONAL_CONTINUITY.md` | `docs/research/MODEL_HANDOFF_AND_RELATIONAL_CONTINUITY.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Research/role-boundary model. |
| `docs/MULTI_PARTY_ENCOUNTER_PROTOCOL.md` | `docs/research/MULTI_PARTY_ENCOUNTER_PROTOCOL.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Research protocol candidate; explicitly non-executable. |
| `docs/P0_RUNTIME_BINDING_IMPLEMENTATION_REPORT_2026-08-08.md` | `docs/history/reconciliation/P0_RUNTIME_BINDING_IMPLEMENTATION_REPORT_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated implementation candidate report. |
| `docs/P1_P2_RUNTIME_LINEAGE_LIFECYCLE_IMPLEMENTATION_REPORT_2026-08-08.md` | `docs/history/reconciliation/P1_P2_RUNTIME_LINEAGE_LIFECYCLE_IMPLEMENTATION_REPORT_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated implementation candidate report. |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001.md` | `docs/governance/POL_UPSTREAM_SUPPLIER_TRUST_001.md` | `GOVERNANCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Current policy candidate and governance scope. |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_CROSSWALK_2026-08-08.md` | `docs/evidence/standards/POL_UPSTREAM_SUPPLIER_TRUST_001_CROSSWALK_2026-08-08.md` | `SUPPORTING_EVIDENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated standards crosswalk. |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_FREEZE_AND_CHANGE_CONTROL_2026-08-08.md` | `docs/history/reconciliation/POL_UPSTREAM_SUPPLIER_TRUST_001_FREEZE_AND_CHANGE_CONTROL_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated policy-cycle freeze/change record. |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_IMPLEMENTATION_ACCEPTANCE_v0.1_FROZEN_2026-08-08.md` | `docs/history/reconciliation/POL_UPSTREAM_SUPPLIER_TRUST_001_IMPLEMENTATION_ACCEPTANCE_v0.1_FROZEN_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated future-implementation acceptance baseline. |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_POLICY_ACCEPTANCE_2026-08-08.md` | `docs/history/reconciliation/POL_UPSTREAM_SUPPLIER_TRUST_001_POLICY_ACCEPTANCE_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated policy canonicalization acceptance record. |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_VALIDATION_RECORD_2026-08-08.md` | `docs/evidence/verification/POL_UPSTREAM_SUPPLIER_TRUST_001_VALIDATION_RECORD_2026-08-08.md` | `SUPPORTING_EVIDENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated named validation evidence, not normative policy. |
| `docs/PR16_POST_MERGE_RECONCILIATION_2026-08-13.json` | `docs/history/incidents/PR16_POST_MERGE_RECONCILIATION_2026-08-13.json` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | PR-specific reconciliation receipt. |
| `docs/PR16_POST_MERGE_RECONCILIATION_2026-08-13.md` | `docs/history/incidents/PR16_POST_MERGE_RECONCILIATION_2026-08-13.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | PR-specific reconciliation record. |
| `docs/PR19_FINAL_DISPOSITION_2026-08-15.md` | `docs/history/incidents/PR19_FINAL_DISPOSITION_2026-08-15.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | PR-specific final disposition record. |
| `docs/PUBLIC_CLOSURE_CHECKLIST_2026-08-09.md` | `docs/history/incidents/PUBLIC_CLOSURE_CHECKLIST_2026-08-09.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated closure/event record. |
| `docs/PUBLIC_DEPLOYMENT_DIRECTION.md` | `docs/history/other/PUBLIC_DEPLOYMENT_DIRECTION.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Superseded owner direction; preserve historical meaning. |
| `docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md` | `docs/evidence/verification/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md` | `SUPPORTING_EVIDENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Reader-usability verification protocol. |
| `docs/RESEARCH_CHECKPOINT_2026-08-07.md` | `docs/history/other/RESEARCH_CHECKPOINT_2026-08-07.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated research convergence checkpoint. |
| `docs/RISK_MODEL.md` | `docs/governance/RISK_MODEL.md` | `GOVERNANCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Current risk and control model. |
| `docs/ROADMAP_AFTER_PUBLIC_RC.md` | `docs/history/other/ROADMAP_AFTER_PUBLIC_RC.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Superseded historical owner direction. |
| `docs/RUNTIME_REALITY_MATRIX_2026-08-08.md` | `docs/history/reconciliation/RUNTIME_REALITY_MATRIX_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated pre-current runtime candidate view. |
| `docs/RUNTIME_REALITY_MATRIX_C0_CLOSING_2026-08-08.md` | `docs/history/c0/RUNTIME_REALITY_MATRIX_C0_CLOSING_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated C0 closing view. |
| `docs/RUNTIME_TWIN_PROVENANCE_ALIGNMENT_2026-08-08.md` | `docs/history/reconciliation/RUNTIME_TWIN_PROVENANCE_ALIGNMENT_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated runtime/research alignment candidate. |
| `docs/STABILIZATION_A_B_REPORT_2026-08-08.md` | `docs/history/reconciliation/STABILIZATION_A_B_REPORT_2026-08-08.md` | `HISTORICAL` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Dated stabilization report; preserve scope lock. |
| `docs/SUBJECTIVITY_RESEARCH_THREAT_MODEL.md` | `docs/research/SUBJECTIVITY_RESEARCH_THREAT_MODEL.md` | `RESEARCH_REFERENCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Research-specific threat model; distinct from core public threat model. |
| `docs/SUPPLY_CHAIN_ATTESTATION_PLAN.md` | `docs/governance/SUPPLY_CHAIN_ATTESTATION_PLAN.md` | `GOVERNANCE` | `NO` | `MOVE_ONLY + LINK_FIX_IF_NEEDED` | Current preparation-only supply-chain governance plan. |

## Stable path exceptions

The following files remain at their existing paths because current workflows, validators, tests, or the existing reader path depend on them. They are not accidental omissions.

| PATH | CLASSIFICATION | DECISION | REASON |
|---|---|---|---|
| `docs/ARCHITECTURE.md` | `CORE` | `KEEP_ROOT` | Existing core architecture entry point. |
| `docs/C0_ACCEPTANCE_EVIDENCE_INDEX_2026-08-08.md` | `SUPPORTING_EVIDENCE` | `KEEP_STABLE` | Hardcoded by traceability generator and its tests; current QA contract depends on exact path. |
| `docs/C0_EXTERNAL_STANDARDS_CROSSWALK_2026-08-08.md` | `SUPPORTING_EVIDENCE` | `KEEP_STABLE` | Required at exact path by the IQC inspector and strict QA controls. |
| `docs/NON_CLAIMS.md` | `CORE` | `KEEP_ROOT` | Existing core epistemic boundary entry point. |
| `docs/POSITION_PAPER_PROVENANCE_FIRST.md` | `CORE` | `KEEP_ROOT` | Existing core reader path names this position paper. |
| `docs/PROJECT_PURPOSE_ANCHOR.md` | `CORE` | `KEEP_ROOT` | Foundational purpose and claim-boundary anchor; retain as a root reader entry. |
| `docs/PROVENANCE.md` | `CORE` | `KEEP_ROOT` | Existing core attribution and authority entry point. |
| `docs/PUBLIC_PRIVATE_BOUNDARY.md` | `CORE` | `KEEP_ROOT` | Existing core boundary entry point. |
| `docs/QUALITY_ASSURANCE.md` | `CURRENT` | `KEEP_ROOT` | Current QA policy and evidence interpretation; keep as operational entry point. |
| `docs/README.md` | `CURRENT` | `KEEP_ROOT` | Authoritative navigation layer. |
| `docs/RELEASE_STATUS.md` | `CURRENT` | `KEEP_ROOT` | Authoritative current repository/release status. |
| `docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md` | `CORE` | `KEEP_ROOT` | Existing first-hop research contribution entry point. |
| `docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md` | `CORE` | `KEEP_ROOT` | Existing reviewer entry point and active evidence-boundary specification. |
| `docs/RUNTIME_REALITY_MATRIX_CURRENT_2026-08-08.md` | `CURRENT` | `KEEP_ROOT` | Workflow and QA exact-path dependency; current implementation candidate view. |
| `docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md` | `RESEARCH_REFERENCE` | `KEEP_STABLE` | Referenced by evidence schema/validator tests at an exact repository-local path. |
| `docs/THREAT_MODEL.md` | `CORE` | `KEEP_ROOT` | Existing core public threat-model entry point. |
| `docs/governance/PR23_CONTROL_CLOSURE_2026-08-15.json` | `GOVERNANCE` | `KEEP_STABLE` | Current PR23 closure provenance; task explicitly requires stable location. |
| `docs/governance/PR23_CONTROL_CLOSURE_2026-08-15.md` | `GOVERNANCE` | `KEEP_STABLE` | Current PR23 closure provenance; task explicitly requires stable location. |

## Deletion candidates

`FILES_DELETED = 0`. Any duplicate, superseded, or potentially removable record remains present and is `DELETION_CANDIDATE = REVIEW_REQUIRED`; this migration does not decide deletion.
