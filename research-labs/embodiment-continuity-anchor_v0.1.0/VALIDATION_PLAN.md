# E-axis Validation Plan

Status: `RESEARCH_MATERIAL`
Main effect: `NONE`
Canonical effect: `NONE`
Runtime effect: `NONE`

Validation targets for this research slice:

1. Python syntax and import validity for `sensorimotor.py`.
2. Deterministic PASS for a fully evidenced closed transition.
3. Non-PASS for reset/no-bridge negative control.
4. HOLD when recalibration is required but evidence is absent.
5. PASS when morphology/action-channel migration has explicit recalibration evidence and the causal transition remains traceable.
6. Provenance validation rejects empty evidence sets.
7. No dependency on `LineageAnchor` or memory records in the E-axis evaluator.
8. Identity conclusion remains `NOT_ESTABLISHED` for every assessment.

Repository-level CI should be treated as the authoritative integration check when available. This file does not claim CI success by itself.