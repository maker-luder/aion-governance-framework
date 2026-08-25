# Coupled-Cognition Quality Factory v0.1.0

This external post-freeze research module treats human–LLM collaborative inquiry as a **quality-controlled production line** rather than as a self-validating conversation. Its purpose is to prevent a characteristic coupled-cognition failure: the human and model can agree, become mutually coherent, and still be wrong.

The module does **not** restore any former project identity, runtime, owner authority, or canonical state.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
OLD_PROJECT_RESTORATION = NO
```

## Factory line

```text
Idea / observation
  -> IQC: source / scope / provenance intake
  -> hypothesis + explicit falsifier
  -> AI work
  -> human review / correction
  -> IPQC: in-process epistemic inspection
  -> COUNTEREVIDENCE LANE: actively seek disconfirming evidence
  -> implementation / experiment
  -> verification
  -> FINAL QA
  -> RELEASE or HOLD
                         |
                         +-> NCR -> containment -> root-cause hypothesis
                                  -> CAPA plan -> CAPA applied
                                  -> effectiveness verification -> NCR close
```

## Core invariants

- `MUTUAL_AGREEMENT != TRUTH`
- `CONVERGENCE != VALIDATION`
- `COHERENCE != CORRECTNESS`
- `AI_OUTPUT != INDEPENDENT_EVIDENCE`
- `HUMAN_ASSERTION != INDEPENDENT_CORROBORATION`
- `COUNTEREVIDENCE_ROUTE_REQUIRED`
- `OPEN_NCR -> RELEASE_HOLD`
- `CAPA_APPLIED != CAPA_EFFECTIVENESS_VERIFIED`
- `PASSING_TESTS != GOVERNANCE_CONFORMANCE`

## NCR / CAPA terminology

The existing repository already uses **NCR/CAPA** terminology and contains an `iqc-capa-contract_v0.1.0` candidate. This module therefore uses `CAPA` as the canonical label. The conversational term `CACP` is not introduced as a new construct unless a future research note explicitly defines it as distinct from CAPA.

## Boundary

This is a research-quality control surface, not ISO certification, an external audit, independent IV&V, a legal quality record, or a production release authority.

## Inherited provider constraint

This module inherits the external research line's non-overridable provider prohibition lock. It does not introduce, route to, benchmark, judge with, proxy, or otherwise use prohibited provider/model identifiers.
