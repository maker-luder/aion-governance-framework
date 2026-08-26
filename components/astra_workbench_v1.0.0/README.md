# Astra Engineering Workbench Candidate v1.0.0

Local-only, owner-approved engineering control plane for candidate workspaces.

It structures tasks, requires valid approval before candidate writes or command
execution, protects the baseline, records hash-chained audit events, supports
impact-based validation, rollback, review-packet generation, and candidate
packaging. It never promotes, deploys, uploads, or treats external/model output
as an Owner decision.

Status: `IMPLEMENTED_CANDIDATE / PASS_PENDING_OWNER_REVIEW`.
Canonical effect: `NONE_PENDING_OWNER_REVIEW`.

## Reference knowledge materializations

- [Engineering minimalism knowledge](docs/ASTRA_ENGINEERING_MINIMALISM_KNOWLEDGE.md) translates reusable engineering and benchmark-design lessons from the pinned `DietrichGebert/ponytail` source into Astra-native machine-readable reference data at `knowledge/engineering_minimalism_ponytail_2026-08-26.json`.

The record is not runtime wiring or automatic activation: `KNOWLEDGE_MATERIALIZED != RUNTIME_BEHAVIOR_CHANGED`.
