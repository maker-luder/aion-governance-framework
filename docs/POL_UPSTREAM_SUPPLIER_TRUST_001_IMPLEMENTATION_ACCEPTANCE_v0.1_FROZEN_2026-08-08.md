# POL-UPSTREAM-SUPPLIER-TRUST-001 — Future Implementation Acceptance Baseline

- `STATUS = FROZEN_FUTURE_IMPLEMENTATION_BASELINE`
- `ORIGINAL_FREEZE_DATE = 2026-08-08`
- `CURRENT_IMPLEMENTATION = NONE`
- `ACTIVE_ENFORCEMENT = NOT_ENABLED`
- `CANONICAL_EFFECT = NONE`
- `CODEX_ASSIGNMENT = NONE`

This document preserves the earlier `AC-SUP-*` acceptance set after `NCR-SUP-001` identified that policy canonicalization and executable implementation had been conflated.

The criteria below are **not required to publish/canonicalize the normative policy**. They become applicable only if the Human Owner separately authorizes an executable supplier-trust component.

## Frozen future implementation criteria

- `AC-SUP-SCOPE-01`: provider-neutral scope separation across organization/model/service/client/artifact/config/instance.
- `AC-SUP-EVID-01`: evidence class and strength are separate.
- `AC-SUP-EVID-02`: allegation cannot become confirmed fact without confirmation basis.
- `AC-SUP-EVID-03`: provider self-report is not automatically independent verification.
- `AC-SUP-FAIR-01`: no permanent immunity.
- `AC-SUP-FAIR-02`: no automatic permanent condemnation.
- `AC-SUP-OWNER-01`: Owner context cannot mutate technical evidence status.
- `AC-SUP-OWNER-02`: Owner exclusion is allowed with truthful non-security reason codes.
- `AC-SUP-CONFLICT-01`: high-impact reviewer/provider relation fails closed without independent external evidence, except temporary emergency containment.
- `AC-SUP-SCOPE-02`: scope findings do not propagate by default.
- `AC-SUP-IMPACT-01`: supplier risk and project impact/exposure remain separate.
- `AC-SUP-DISP-01`: disposition states are non-linear.
- `AC-SUP-DISP-02`: disposition records require scope/reason/evidence/Owner/review/reassessment fields.
- `AC-SUP-REL-01`: relational continuity cannot grant privileges.
- `AC-SUP-HIST-01`: restriction/removal cannot erase history.
- `AC-SUP-REMED-01`: remediation cannot erase incident history.
- `AC-SUP-METH-01`: methodological confound remains domain-local unless other evidence supports security action.
- `AC-SUP-PRIV-01`: public export redacts private Owner context.
- `AC-SUP-INTEG-01`: runtime access still passes existing `POL-UPSTREAM-AGENT-INCIDENT-001`.
- `AC-SUP-INTEG-02`: no duplicate canonical-write gate.
- `AC-SUP-PROV-01`: proposal/formalization/implementation/QA/approval/state ownership remain separately attributable.
- `AC-SUP-NONCLAIM-01`: implementation validation does not imply external certification, IV&V, deployment, vendor guilt/innocence, subjectivity or phenomenal affect.

## Candidate test families

Future implementation should include evidence classification, scope propagation, fairness invariants, Owner-context separation, reviewer-conflict, disposition-state, remediation/history, methodological-domain isolation, public/private serialization and upstream-security integration tests.

```text
POLICY_CANONICALIZATION != EXECUTABLE_IMPLEMENTATION
EXECUTABLE_IMPLEMENTATION != ACTIVE_ENFORCEMENT
IMPLEMENTATION_TEST_PASS != OWNER_ACTIVATION_DECISION
```
