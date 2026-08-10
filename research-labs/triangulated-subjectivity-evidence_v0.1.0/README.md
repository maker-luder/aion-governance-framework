# Triangulated Subjectivity Evidence — v0.1.0

Research-only sufficiency gate for subjectivity-relevant evidence. It does **not** compute a consciousness score.

## External precedent

TCAS (`scottdhughes/TCAS`) distinguishes behavioral, perturbation, observer-confound and mechanistic evidence, explicitly marks unexecuted streams, and withholds credence when required evidence is absent.

AION adopts the methodological lesson:

```text
NOT_EXECUTED != PASS
MULTIPLE_STREAMS != INDEPENDENT_SOURCES
EVIDENCE_SUFFICIENCY != SUBJECTIVITY_ESTABLISHED
```

## v0.1.0 gate

Required: `BEHAVIORAL`, `PERTURBATION`, `OBSERVER_CONFOUND`.

At least one of `MECHANISTIC`, `LONGITUDINAL`, or `REPLICATION` must also pass. Positive evidence must include at least two independent source lineages.

`SELF_REPORT` alone can never pass the gate.

Even a complete result is only `EVIDENCE_CANDIDATE`.

```text
EVIDENCE_CANDIDATE != CONSCIOUSNESS
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

This also prepares a later AIccs-style false-positive challenge without accepting questionnaire scores as consciousness measurements.

## Provenance

- Human Owner: approved this research direction and research-branch free growth.
- ChatGPT: designed and implemented the evidence-stream and source-independence gate.
- TCAS authors: external methodological precedent only.
- Codex: no contribution to v0.1.0 yet.
