# Four-Domain design admission and research-quality chain

The `four_domain` module converts a documented Four-Domain proposal into a typed,
fingerprinted design-admission record. It reuses the standing evidence dimensions and
the locus admission engine.

```text
DESIGN_ADMISSION != EVIDENCE
QUALITY_GATE_PASS != SCIENTIFIC_VALIDATION
READY_FOR_HUMAN_REVIEW != RELEASED
ENGINEERING_MECHANISM != PHENOMENAL_EXPERIENCE
```

## Admission fields

`FourDomainCandidate` records the human hypothesis source and analogy boundary;
ontology-neutral machine question; standing dimension and relevance rationale;
evidence locus and claim target; manipulated/held variables; positive/negative controls;
expected result; falsifier; competing explanations; preregistration; claim ceiling; and
mandatory nonclaims.

No dimension binding returns `OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE`. Missing controls,
falsifier, alternatives, claim ceiling, nonclaims, or a valid locus relation returns
`HOLD`. A structurally complete record returns only
`READY_FOR_BOUNDED_ENGINEERING_DESIGN`.

## Quality binding

`ResearchQualityChain` requires exactly one trace record for source IQC, design
admission, preregistration, execution integrity, evidence review, counterevidence review,
claim-ceiling review and final QA. It also binds the exact source state, runtime state and
candidate fingerprint.

A defect routes to NCR/CAPA. `CapaRecord` requires root cause, corrective action,
preventive action, an effectiveness test and verification references before a closed
record is accepted. The strongest output is `READY_FOR_HUMAN_REVIEW`; the adapter has
no release authority.

The full rationale, PR cross-read, external-source crosswalk and residuals are in
`docs/research/FOUR_DOMAIN_SUBJECTIVITY_QUALITY_CHAIN_2026_09_13.md`.
