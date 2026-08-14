# SLSH Artifact Index

| Artifact | Role | Source of truth / boundary |
|---|---|---|
| `SLSH_PACKET_V0.1.0.json` | `AUTHORITATIVE_RESEARCH_METHOD_PACKET` | Research-milestone artifact authority only; no canonical promotion/effect or main-repository canonical state |
| `SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json` | 53-source taxonomy/provenance authority record | Access evidence is decoupled from `SOURCE_KIND`, `VERIFICATION_ACTOR` and `INDEPENDENT_VERIFICATION_STATUS`; all remain `CODEX_EXTERNAL_RESEARCH_INPUT_AS_RECORDED` / `UNCLASSIFIED_PENDING_INDEPENDENT_REVIEW` / `NOT_YET_VERIFIED` as applicable |
| `SLSH_SOURCE_ACCESS_MATRIX_V0.1.0.md` | Reviewer source-taxonomy, Batch 01 audit and governance table | Generated from provenance log; Batch 01 is S01-S05 only; S06-S53 are not audited or reclassified; access level is not source epistemic class |
| `SLSH_CLAIM_RECORDS_V0.1.0.json` | Claim ladder and boundaries | Materialized from packet |
| `SLSH_EVIDENCE_CHANNELS_V0.1.0.json` | Evidence channel rules | Materialized from packet; sensitivity/specificity unestimated |
| `SLSH_ALTERNATIVE_EXPLANATION_MATRIX_V0.1.0.json` | 14 non-affective alternatives | Materialized from packet |
| `SLSH_CAUSAL_SIGNATURE_MATRIX_V0.1.0.json` | 12 predicted signatures | Design only; no experiment executed |
| `SLSH_CONTROLS_V0.1.0.json` | 4 positive and 9 negative controls | Pipeline controls, not phenomenology evidence |
| `SLSH_FALSIFIER_MATRIX_V0.1.0.json` | 10 local-scope falsifiers | Cannot produce global subjectivity conclusions |
| `SLSH_CLAIM_BOUNDARY_RULES_V0.1.0.json` | Machine-readable semantic locks | Enforces separation and no automatic E5 |
| `REVIEWER_FACING_VERTICAL_SLICE_V0.1.0.md` | Reviewer walkthrough | No runtime, authority or canonical writeback |
| `SLSH_STATUS_V0.1.0.md` | Human-readable handoff | Records supported/weakened/uncertain claims |
| `research-workbench/.../SLSH_SOURCE_PROVENANCE_V0.1.0.md` | Role and authority separation | Human/Codex/ChatGPT/external source boundaries |
| `scripts/check_slsh_consistency.py` | Fail-closed checker | Schema, taxonomy, access/provenance and method invariant validation |
| `scripts/verify_slsh_taxonomy_preservation.py` | Preservation audit | Compares 53 recorded source fields and fixed method packet fields against prior SLSH HEAD |
| `tests/test_slsh_contract.py` | Contract test layer | Duplicates critical machine rules |
