# Trace Provenance Crosswalk Adversarial v0.1.0

Status: `RESEARCH_ONLY / EXTERNAL_OBSERVATION_ONLY / TRACE_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a trace-to-observability crosswalk preserve source attribution, currentness, redaction, graph and event identity, external namespace isolation, and evidence-reuse boundaries when trace and provenance metadata are adversarially changed?

This unit extends `trace-provenance-crosswalk_v0.1.0` without contacting a trace provider or exporting a real trace. The base crosswalk maps selected public OpenInference vocabulary into an AION observability envelope while retaining AION runtime/subject/source/approval namespacing and a fixed canonical effect of `NONE`. The adversarial extension audits source attribution fields, controlled source kinds/currentness, stable source references, reuse-versus-new-evidence labels, raw content policies, blank provenance references, graph self-parenting, external `aion.*` fields, external score parsing, duplicate runtime event IDs, and review-only batch/crosswalk behavior.

## Decision layers

The source-entry audit requires `WHAT`, `WHO`, `WHERE`, `WHEN`, `METHOD`, `AUTHORITY`, `TRANSFORMATION`, `CURRENTNESS`, `SOURCE_REF`, and target-field metadata. Uncontrolled source kinds/currentness are invalid. Reused references cannot be mislabeled as new evidence. Stale, historical, retrieved-only, remembered, or unknown currentness is held for review. Trace auditing defaults to redaction and holds explicit raw input/output/tool-parameter export for review. Blank source/approval references and graph self-parenting are invalid. External `aion.*` fields do not gain authority; invalid external scores are rejected. Event/crosswalk batches preserve stable IDs and remain review metadata only.

The experiment constructs synthetic `AIONTraceEvent`, `CrosswalkEntry`, and external-attribute mappings only. It does not export a trace, call OpenInference, access a provider, execute a model, observe a runtime result, or write canonical state. Every output preserves `EXTERNAL_OBSERVATION_ONLY`, `TRACE_EXECUTION=FALSE`, `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, and `DEPLOYMENT=FALSE`.

## Results

The suite passed **26 pytest tests** and **25 synthetic trace/crosswalk cases**. Cases covered valid trace mapping, raw input/output/tool-parameter policy holds, graph self-parent, blank source/approval references, valid external observation, external AION namespace, invalid/out-of-range external score, empty/duplicate/valid trace batches, trace constructor canonical lock, valid/missing/unknown source attribution, uncontrolled currentness, reused-reference mislabeling, stale source review, empty/duplicate/missing-ref/historical/valid crosswalks.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Valid trace/crosswalk | `ADMITTED_FOR_REVIEW` | Observability metadata maps without authority promotion |
| Raw input/output/tool parameters | `HOLD` | Sensitive content export requires explicit review |
| Blank provenance or graph self-parent | `INVALID` | Trace identity/lineage fails closed |
| External observation with ordinary keys | `ADMITTED_FOR_REVIEW` | External data remains observation-only |
| External `aion.*` namespace | `HOLD` | External attributes cannot self-authorize |
| Invalid external score | `INVALID` | Parser and score boundaries are enforced |
| Duplicate event/crosswalk IDs | `INVALID` | Stable identity prevents ambiguous lineage |
| Stale/historical/uncontrolled currentness | `HOLD` / `INVALID` | Freshness is not inferred from retrieval |
| Reused reference marked as new evidence | `INVALID` | Evidence reuse is not counted as new evidence |
| Valid batch | `ADMITTED_FOR_REVIEW` | Batch remains review metadata only |

## Falsifiers

The mechanism would be falsified if it accepted incomplete source attribution, uncontrolled source kind/currentness, reused references mislabeled as new evidence, raw content export without review, blank source/approval references, graph self-parenting, external `aion.*` authority, invalid scores, duplicate event/crosswalk identifiers, or trace/crosswalk batches that changed canonical state. It would also be falsified if stale/retrieved/remembered data were silently treated as current or if an external observation were treated as AION authority.

A mapped trace is not truth, authority, memory truth, theory validity, identity proof, or evidence of a scientific result. A trace score is not theory validity. The unit does not establish observability completeness, source reliability, model generalization, causal effect, replication, identity continuity, subjectivity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment readiness.

## Evidence reuse and provenance

The base trace crosswalk is reused through stable repository source and crosswalk references. Its OpenInference vocabulary mapping is methodological input, not new evidence. No external trace is imported and no prior observation is counted as a new independent item. The 25 synthetic cases are fixtures, not replication evidence.

## Explicit non-claims

```text
TRACE != TRUTH
OBSERVABILITY != AUTHORITY
SESSION_ID != SUBJECT_ID
AGENT_NAME != IDENTITY_PROOF
RETRIEVAL_DOCUMENT != MEMORY_TRUTH
EVALUATION_SCORE != THEORY_VALIDITY
EXTERNAL_ATTRIBUTE != APPROVAL_AUTHORITY
TRACE_EXPORT != CANONICAL_WRITEBACK
EVIDENCE_REFERENCE != NEW_EVIDENCE
TRACE_EXECUTION = FALSE
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
AUTHORITY = EXTERNAL_OBSERVATION_ONLY
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses Python standard-library runtime modules plus the existing repository crosswalk source path for composition. It does not call external services, access private data, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../trace-provenance-crosswalk_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../trace-provenance-crosswalk_v0.1.0/src python scripts/run_crosswalk_adversarial.py --output fixtures/crosswalk_adversarial_result.json
PYTHONPATH=src:../trace-provenance-crosswalk_v0.1.0/src python scripts/validate_fixture.py fixtures/crosswalk_adversarial_result.json
```

## References

The implementation reuses repository evidence from `trace-provenance-crosswalk_v0.1.0` by stable path. Its existing OpenInference source crosswalk remains methodological context; no external trace provider or external source code is used by this unit.
