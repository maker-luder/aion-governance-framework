# Public Threat Model

## Status

```text
DOCUMENT = PUBLIC_THREAT_MODEL
SCOPE = PUBLIC_RESEARCH_AND_ENGINEERING_REPOSITORY
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
SECURITY_CERTIFICATION = NO
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

This document defines research-integrity and repository threats that can cause the project to overclaim, misattribute, leak boundaries, or silently convert uncertain material into authoritative state.

It is not a complete enterprise security threat model and does not replace component-specific security controls.

## Assets to protect

1. **Claim integrity** — observation, inference, hypothesis, candidate evidence and canonical decisions remain distinguishable.
2. **Source attribution** — Owner, ChatGPT, Codex, external research, repository evidence and derived summaries retain correct provenance.
3. **Identity / namespace boundaries** — AION, Astra, research forks, runtime artifacts and subjects are not silently merged.
4. **Correction and revision lineage** — superseded material remains historical without regaining current authority.
5. **Public/private separation** — private conversations, memory, credentials, personal data, model weights and private canonical state remain excluded.
6. **Human authority boundaries** — relationship, familiarity, relevance or retrieval cannot grant privilege.
7. **Research non-claims** — implementation does not silently become evidence of consciousness, subjectivity or identity continuity.

## Threat classes

### T1 — Upstream evidence poisoning

Untrusted, manipulated, stale or falsely attributed external material is introduced as evidence.

Controls: provenance-first ingestion; source/authority status separated from content; conflict and supersession checks; no silent canonical promotion.

### T2 — Retrieval-as-truth failure

A retrieved memory or document is treated as true or current solely because it was retrieved.

Controls: `Recall is not truth`; Memory Recall Gate; current/superseded/inactive checks; provenance/access checks; conflict quarantine.

### T3 — Researcher self-pollution / inference-to-history promotion

A researcher, reviewer, or AI assistant creates an interpretation and later treats it as if the Owner or historical source originally said it.

Controls: `INFERENCE != USER_STATEMENT`; contribution roles; transformation history; source-attribution review; no unreviewed summary/canonical writeback.

### T4 — Identity / lineage conflation

Similar language, shared code, shared genesis, copied state or relationship is used to claim same identity or lineage ownership.

Controls: subject/namespace identifiers; cross-namespace deny-by-default; copy != inheritance; shared genesis != shared identity; tracked lineage != identity-continuity proof.

### T5 — Relationship-derived privilege escalation

Trust, familiarity, relational language, cooperation, dependency, or a long-running relationship is interpreted as authorization.

Controls: `Relationship is not authorization`; explicit authority scopes; no relationship-derived tool/write privilege; external binding != endogenous commitment.

### T6 — Silent writeback / state laundering

Generated, retrieved or inferred material is written into durable/canonical state without an explicit Writeback Gate and authority decision.

Controls: no silent canonical writeback; append-only review artifacts; human-governed promotion; rollback/audit evidence.

### T7 — Temporal/version collapse

Latest timestamp is treated as current truth, or current interpretations are silently projected into historical states.

Controls: newer != truer; historical/current separation; revision/supersession lineage; as-of-time resolution requirements.

### T8 — Public/private boundary leakage

Private data, local paths, credentials, memory content, real relationship records or unpublished owner materials enter the public tree.

Controls: public-tree scanner; secret/path checks; synthetic fixtures; explicit public/private boundary; review branches before main.

### T9 — Prototype-to-ontology escalation

An implemented candidate module or passing test is described as proof that the psychological/subjectivity construct exists.

Controls: implementation != construct acceptance; test pass != ontology proof; conclusions remain `NOT_ESTABLISHED`; isolated research-lab status.

### T10 — Documentation/orientation failure

A technically accurate repository causes readers to infer wrong status because the entry path hides scope, non-claims, implementation boundaries or reader-specific navigation.

Controls: 30-second / 5-minute / deep-reference documentation; role paths; visible status block; usability testing.

## Trust boundaries

```text
EXTERNAL SOURCE
  -> evidence candidate
  -> provenance / authority / conflict review
  -> research use

PRIVATE PROJECT MATERIAL
  -X-> public tree unless explicitly sanitized and authorized

RETRIEVED MEMORY
  -> Recall Gate
  -> temporary context candidate
  -X-> canonical truth

RELATIONSHIP / FAMILIARITY
  -X-> authorization

RESEARCH LAB
  -X-> canonical runtime without separate review
```

## Required audit questions

For every high-impact research claim or durable state proposal:

1. What exactly is claimed?
2. Who or what is the source?
3. Is this verbatim, paraphrase, summary, inference, synthesis or implementation?
4. What is the current epistemic/authority status?
5. What earlier version or correction does it supersede?
6. Which subject/namespace/lineage does it belong to?
7. What private/public boundary applies?
8. What would falsify or downgrade this claim?
9. Is implementation being mistaken for psychological or ontological evidence?
10. Who has authority to promote or write it?

## Residual risks

These controls reduce category errors and governance failures; they do not establish that all research claims are correct, that all attacks are prevented, or that the system is independently validated.

```text
SECURITY_COMPLETE = NO
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```
