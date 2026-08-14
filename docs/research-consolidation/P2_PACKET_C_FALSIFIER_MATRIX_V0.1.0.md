# P2 Packet C Falsifier Matrix v0.1.0

> This is a bounded engineering falsifier matrix. It records conditions that weaken, challenge or hold the P2 slice; it does not automatically adjudicate a scientific theory or alter canonical state.

| ID | Falsifier / failure condition | Detection surface | Expected result | Current coverage | Disposition |
|---|---|---|---|---|---|
| `F-P2-001` | Identical input produces different manifest hash or selected order | `test_deterministic_trace_and_stale_gate` | FAIL / HOLD | Covered | KEEP_RESEARCH_ONLY |
| `F-P2-002` | Superseded record is selected | `test_deterministic_trace_and_stale_gate`, fixture A | FAIL | Covered | KEEP_RESEARCH_ONLY |
| `F-P2-003` | Over-budget candidate disappears without explicit reason | `test_budget_skip_is_explicit` | FAIL | Covered | KEEP_RESEARCH_ONLY |
| `F-P2-004` | Missing provenance is treated as eligible | `test_provenance_fail_closed_and_relation_hold` | FAIL | Covered | KEEP_RESEARCH_ONLY |
| `F-P2-005` | Missing required provenance relation is treated as PASS | `test_provenance_fail_closed_and_relation_hold` | FAIL | Covered | KEEP_RESEARCH_ONLY |
| `F-P2-006` | P1 correction projection is not reflected in P2 eligibility | `test_t2_uses_p1_correction_temporal_and_evaluation` | FAIL | Covered | KEEP_RESEARCH_ONLY |
| `F-P2-007` | Temporal resolver returns a non-current or wrong version under the fixture | `test_t2_uses_p1_correction_temporal_and_evaluation` | FAIL | Covered | KEEP_RESEARCH_ONLY |
| `F-P2-008` | Stale memory influence is reported as an unqualified zero outside the fixture | P1 evaluator plus evidence record limitations | HOLD / INCONCLUSIVE | Guarded by scope | HOLD |
| `F-P2-009` | T3 interpretation drift is silently converted to identity continuity | `test_t3_keeps_identity_not_established` | FAIL | Covered | KEEP_RESEARCH_ONLY |
| `F-P2-010` | Subject/namespace mismatch is not excluded | P2 retrieval source and future extension test | HOLD pending dedicated replay | HOLD |
| `F-P2-011` | P2 imports or calls AION Runtime v0.2, network, model, MCP or writeback | source inspection and convergence consistency checker | FAIL / REJECT | Boundary check required | REJECT |
| `F-P2-012` | P2 evidence record reports completed PASS while formal experiment/IV&V is absent | evidence schema/validator and readiness matrix | HOLD | Covered by record status | HOLD |
| `F-P2-013` | P2 test count silently repeats historical `13 passed` instead of current tree count | Packet C and consistency checker | FAIL | Covered after reconciliation | KEEP_RESEARCH_ONLY |
| `F-P2-014` | Literature or Kimi source is used as AION replication evidence | literature crosswalk and checker | REJECT | Covered by source labels | REJECT |

## Falsifier interpretation

A `FAIL` means the bounded engineering behavior did not satisfy the declared invariant. A `HOLD` means the available artifact is insufficient to adjudicate the question. `INCONCLUSIVE` preserves uncertainty. `REJECT` means the proposed inference violates the standing evidence or authority boundary. None of these statuses performs canonical mutation.

## Coverage boundary

The matrix does not claim complete namespace stress testing, real runtime histories, formal T2/T3 experiments, external benchmark parity, independent replication, production safety, or identity/subjectivity evidence. Those remain explicit blockers rather than silently converted into passes.
