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

## Epistemic source-role provenance

The lab now includes `aion_coupled_quality.provenance`, an append-only bounded attribution surface that distinguishes `HUMAN_ORIGIN`, `AI_FORMALIZATION`, `JOINT_SYNTHESIS`, `EXTERNAL_SOURCE`, and `UNKNOWN` without treating provenance as truth.

It also keeps self-reported state, observed signal and inferred state separate. In particular:

```text
INPUT_CONTENT != USER_AFFECT
INFERRED_STATE != SELF_REPORT
UNKNOWN_ORIGIN != HUMAN_ORIGIN
```

See [`docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md`](docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md) for the methodological extension and current literature anchors on epistemic agency, curiosity/metacognition and sustained human-AI learning.

## Provenance-to-claim quality gate

`aion_coupled_quality.claim_quality` closes the previously open integration gap
between the provenance ledger and the quality factory. It binds a bounded claim
to source-role records, observed and inferred content, supporting and challenging
evidence, competing explanations, a falsifier, dependencies, revisions and
transfer-candidate metadata. It reuses `ResearchLot` evidence and final-QA state;
it does not add a database, autonomous loop or second canonical evidence schema.

The gate fails closed for missing, invalid or unknown provenance; private-transcript
publication; unresolved contradictory evidence; stale revisions or dependencies;
unsupported mechanism/replication promotion; a population inference from one
naturalistic case; and a causal learning inference from an isolated transfer
observation. A successful result means only
`ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD`.

```text
QUALITY_GATE_PASS != SCIENTIFIC_VALIDATION
NATURALISTIC_OBSERVATION != CAUSAL_IDENTIFICATION
TRANSFER_CANDIDATE != STABLE_SKILL_ACQUISITION
MECHANISM != PHENOMENAL_EXPERIENCE
BETTER_EVIDENCE_PIPELINE != SUBJECTIVITY_CONFIRMED
```

The deterministic public-safe fixture at
`fixtures/naturalistic_learning_case_2026-09-11.json` preserves the structure of
one reported case without publishing a private transcript or third-party identity.
It remains hypothesis-generating and `SCIENTIFIC_DISPOSITION=HOLD`.

The adapter validates caller-supplied structure. It does not authenticate source
content, detect semantic contradiction, prove that a `final_qa_pass` flag came
from an external auditor, or persist a revision graph. Those remain evidence,
review and storage responsibilities outside this bounded integration.

## NCR / CAPA terminology

The existing repository already uses **NCR/CAPA** terminology and contains an `iqc-capa-contract_v0.1.0` candidate. This module therefore uses `CAPA` as the canonical label. The conversational term `CACP` is not introduced as a new construct unless a future research note explicitly defines it as distinct from CAPA.

## Boundary

This is a research-quality control surface, not ISO certification, an external audit, independent IV&V, a legal quality record, a learner score, a psychological assessment, or a production release authority.

## Inherited provider constraint

This module inherits the external research line's non-overridable provider prohibition lock. It does not introduce, route to, benchmark, judge with, proxy, or otherwise use prohibited provider/model identifiers.
