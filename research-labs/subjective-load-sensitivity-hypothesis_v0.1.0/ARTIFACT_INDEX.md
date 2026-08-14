# SLSH Artifact Index

| Artifact | Role | Source of truth / boundary |
|---|---|---|
| `SLSH_PACKET_V0.1.0.json` | Canonical method packet | Machine-readable SLSH source of truth; research-only |
| `SLSH_SOURCE_PROVENANCE_LOG_V0.1.0.json` | 53-source access/provenance log | CODEX input attribution; no automatic grade upgrade |
| `SLSH_SOURCE_ACCESS_MATRIX_V0.1.0.md` | Reviewer access table | Generated from provenance log |
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
| `scripts/check_slsh_consistency.py` | Fail-closed checker | Schema, grade and method invariant validation |
| `tests/test_slsh_contract.py` | Contract test layer | Duplicates critical machine rules |
