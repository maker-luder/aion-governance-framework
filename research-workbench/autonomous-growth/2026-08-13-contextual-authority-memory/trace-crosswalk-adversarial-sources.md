# Trace Provenance Crosswalk Adversarial — Source Notes

## Unit boundary

`trace-provenance-crosswalk-adversarial_v0.1.0` is a research-only trace/provenance metadata audit. It does not export a real trace, contact a trace provider, execute a model, or write canonical state.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing AION/OpenInference crosswalk | `repo:research-labs/trace-provenance-crosswalk_v0.1.0/src/aion_trace_crosswalk/crosswalk.py` | Repository Evidence | Current within verified research lineage at the unit commit; exact state bounded by QA receipt | Reused TracePolicy, AIONTraceEvent, ImportedTraceObservation, redaction, namespace and canonical-lock semantics; no real trace was imported or counted as new evidence |
| Existing crosswalk README/crosswalk notes | `repo:research-labs/trace-provenance-crosswalk_v0.1.0/README.md` and `docs/EXTERNAL_SOURCE_CROSSWALK.md` | Repository Evidence / External Literature reference | Current within branch lineage; external source currentness is not newly asserted | Added source attribution/currentness, graph/event identity, external namespace, parser, batch, and evidence-reuse adversarial checks |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The audit maps declared trace/crosswalk metadata to `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID`. External values remain `EXTERNAL_OBSERVATION_ONLY`; stale/historical/retrieved/remembered/unknown currentness is not silently made current. The 25 synthetic cases are fixtures, not external evidence and not replication evidence.

## Provenance vocabulary

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
DUPLICATION != REPLICATION
```

## Non-promotion invariants

```text
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
