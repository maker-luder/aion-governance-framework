# CSOMI Artifact Index v0.1.0

This index is branch-local and research-only. The Four-Domain source branch remains read-only and authoritative for the inherited research baseline. The canonical machine-readable method packet is `research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_PACKET_V0.1.0.json`.

| Artifact | Role | Machine check |
|---|---|---|
| `research-workbench/cross-substrate-other-minds-inference-2026-08-14/PRIMARY_SOURCE_FINDINGS.md` | Primary-source verification log and access limitations | Reviewed by source IDs in packet |
| `research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_PACKET_V0.1.0.json` | Canonical framework packet containing claims, channels, matrices, falsifiers and vertical slice | `schemas/aion_csomi_packet_v0.1.0.schema.json` |
| `schemas/aion_csomi_packet_v0.1.0.schema.json` | Draft 2020-12 packet schema | `scripts/check_csomi_consistency.py` |
| `schemas/aion_csomi_controls_v0.1.0.schema.json` | Draft 2020-12 controls fixture schema | `scripts/check_csomi_consistency.py` |
| `research-labs/cross-substrate-other-minds-inference_v0.1.0/artifacts/CSOMI_CLAIM_RECORD_V0.1.0.json` | Materialized claim records | Rebuilt by `scripts/build_csomi_artifacts.py` |
| `research-labs/cross-substrate-other-minds-inference_v0.1.0/artifacts/CSOMI_EVIDENCE_MATRIX_V0.1.0.json` | Materialized evidence channels and evidence matrix | Rebuilt by `scripts/build_csomi_artifacts.py` |
| `research-labs/cross-substrate-other-minds-inference_v0.1.0/artifacts/CSOMI_DISANALOGY_MATRIX_V0.1.0.json` | Materialized cross-substrate disanalogies | Rebuilt by `scripts/build_csomi_artifacts.py` |
| `research-labs/cross-substrate-other-minds-inference_v0.1.0/artifacts/CSOMI_FALSIFIER_MATRIX_V0.1.0.json` | Materialized falsifiers and failure conditions | Rebuilt by `scripts/build_csomi_artifacts.py` |
| `research-labs/cross-substrate-other-minds-inference_v0.1.0/artifacts/CSOMI_VERTICAL_SLICE_V0.1.0.json` | Materialized reviewer-facing vertical-slice contract | Rebuilt by `scripts/build_csomi_artifacts.py` |
| `research-labs/cross-substrate-other-minds-inference_v0.1.0/fixtures/csomi_positive_negative_controls_v0.1.0.json` | Synthetic positive/negative controls only; no model calls or runtime | `schemas/aion_csomi_controls_v0.1.0.schema.json` |
| `research-labs/cross-substrate-other-minds-inference_v0.1.0/REVIEWER_FACING_VERTICAL_SLICE_V0.1.0.md` | Human-readable slice walkthrough | Contract test and checker |
| `research-labs/cross-substrate-other-minds-inference_v0.1.0/tests/test_csomi_contract.py` | Contract tests | `pytest` |
| `scripts/check_csomi_consistency.py` | Cross-file consistency and boundary checker | CI entrypoint |
| `scripts/build_csomi_artifacts.py` | Deterministic materializer for reviewer-facing JSON subsets | CI rebuild step |
| `research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_STATUS_V0.1.0.md` | Status, supported/weak/uncertain claims and Owner-only decisions | Reviewer handoff |
| `.github/workflows/cross-substrate-other-minds-inference.yml` | Branch-scoped CI | Push/dispatch on milestone branch |

The package has no runtime authority, no model modification, no live-system data collection, no canonical manifest registration and no repository-setting operation. Its final subjectivity, consciousness and identity-continuity states remain `NOT_ESTABLISHED`.
