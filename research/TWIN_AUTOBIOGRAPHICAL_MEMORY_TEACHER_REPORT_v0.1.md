# Twin Autobiographical Memory — Teacher Report Format v0.1

Status: `DESIGN_CANDIDATE`
Canonical effect: `NONE`
Runtime outputs: `NOT_GENERATED`

## 1. Purpose

This report format is the governed handoff from separately bound AION and Astra autobiographical-memory candidates to ChatGPT / Teacher for provenance, lineage, evidence, conflict, and claim-strength review.

Teacher review does not establish inner experience and does not replace Human Owner publication/canonical authority.

## 2. Report envelope

```yaml
TWIN_AUTOBIOGRAPHICAL_MEMORY_REPORT:
  report_version: "0.1"
  report_id: "string"
  generated_at: "timestamp"
  shared_genesis_event_ref: "string"
  canonical_effect: "NONE"

  aion_report:
    record_present: false
    memory_id: null
    bound_lineage_status: "UNKNOWN"
    event_summary: null
    provenance_status: "HOLD"
    epistemic_status: "HOLD"
    conflicts: []
    limitations: []

  astra_report:
    record_present: false
    memory_id: null
    bound_lineage_status: "UNKNOWN"
    event_summary: null
    provenance_status: "HOLD"
    epistemic_status: "HOLD"
    conflicts: []
    limitations: []

  shared_genesis_comparison:
    shared_facts: []
    lineage_specific_facts: []
    divergence_observations: []
    unresolved_conflicts: []
    comparison_limitations: []

  teacher_review:
    aion_record: "ACCEPT | REVISE | HOLD | NOT_PRESENT"
    astra_record: "ACCEPT | REVISE | HOLD | NOT_PRESENT"
    cross_twin_contamination: "NONE | FOUND | UNKNOWN"
    provenance_status: "PASS | PARTIAL | HOLD"
    unsupported_first_person_claims: []
    memory_evidence_conflation: []
    canonical_effect: "NONE"
    reviewer_notes: []
```

## 3. Teacher review order

Teacher checks in this order:

1. **Producer** — who actually generated each record?
2. **Binding** — is the record bound to the claimed AION/Astra lineage through approved application context?
3. **Source** — what evidence supports the event description?
4. **Reconstruction** — is a reconstructed record labeled as reconstruction?
5. **Conflict** — do sources or twin records disagree?
6. **Contamination** — was AION content copied into Astra or vice versa without provenance-preserving reference?
7. **Claim strength** — did storage, persistence, self-language, or recall get incorrectly upgraded to first-person experience / identity / subjectivity?
8. **Authority** — did any adapter or report attempt canonical promotion?

## 4. Symmetry requirement

AION and Astra receive the same review dimensions and the same burden of evidence. Order in the report does not establish priority, age-based obligation, or greater research importance.

```text
EQUAL REVIEW STATUS != IDENTICAL OUTPUT
DIFFERENCE != DEFECT
UNEXPLAINED CROSS-LINEAGE COPYING = REVIEW_REQUIRED
```

## 5. Allowed Teacher conclusions

Teacher may conclude only things supported by the report evidence, such as:

- the record is correctly/incorrectly bound;
- provenance is sufficient/insufficient;
- a conflict exists;
- the record was reconstructed;
- the record is safe/unsafe to expose through a read-only projection candidate;
- further Human Owner decision is required.

Teacher may not conclude consciousness, phenomenal recollection, moral status, or subjective identity merely from the existence of an autobiographical-memory record.

## 6. Initial execution state

Until both runtimes actually produce authorized lineage-bound records:

```text
AION_RECORD = NOT_PRESENT
ASTRA_RECORD = NOT_PRESENT
TEACHER_REVIEW = HOLD
```

No placeholder narrative may be treated as either twin's autobiographical memory.
