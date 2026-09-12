# Four-Domain design admission and research-quality chain

The `four_domain` module converts a documented Four-Domain proposal into a typed,
fingerprinted design-admission record. It reuses the standing evidence dimensions and
the locus admission engine.

```text
DESIGN_ADMISSION != EVIDENCE
QUALITY_GATE_PASS != SCIENTIFIC_VALIDATION
READY_FOR_HUMAN_REVIEW != RELEASED
READY_FOR_HUMAN_REVIEW != HUMAN_APPROVAL
ENGINEERING_MECHANISM != PHENOMENAL_EXPERIENCE
```

## Admission fields

`FourDomainCandidate` records the human hypothesis source and analogy boundary;
ontology-neutral machine question; standing dimension and relevance rationale;
evidence locus and claim target; manipulated/held variables; positive/negative controls;
expected result; falsifier; competing explanations; preregistration; claim ceiling; and
mandatory nonclaims.

`source_refs` and `source_classes` are structurally recorded and fingerprint-bound. The
admission engine checks that both groups are non-empty, contain no blank values, and have
matching cardinality. It does not look up a governed-source registry, resolve a locator,
or authenticate the referent. Source-reference presence is therefore not source
authentication.

No dimension binding returns `OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE`. Missing controls,
falsifier, alternatives, claim ceiling, nonclaims, or a valid locus relation returns
`HOLD`. A structurally complete record returns only
`READY_FOR_BOUNDED_ENGINEERING_DESIGN`.

## Quality binding

`ResearchQualityChain` requires exactly one trace record for source IQC, design
admission, preregistration, execution integrity, evidence review, counterevidence review,
claim-ceiling review and final QA. It also binds non-empty exact source/runtime reference
fields and the candidate fingerprint.

The checkpoint enum ends at `FINAL_QA`. `HUMAN_REVIEW` is an external authority boundary,
not an automated `QualityCheckpoint` and not an action performed by
`ResearchQualityChainEngine`. A successful structural assessment emits
`READY_FOR_HUMAN_REVIEW`; that disposition is neither Human approval nor release or merge
authority.

`exact_source_state_ref` and `exact_runtime_ref` are required non-empty structural fields.
This engine does not independently resolve a Git object, interrogate a runtime, or verify
model/scaffold/environment identity. Recording an exact reference is not independent
resolution of its referent.

A defect routes to NCR/CAPA. `CapaRecord` requires root cause, corrective action,
preventive action, an effectiveness test and verification references before a closed
record is accepted. The strongest output is `READY_FOR_HUMAN_REVIEW`; the adapter has
no release authority.

External checks remain separate: `scripts/check_source_state_binding.py` compares a
declared head to the actual Git head/tree and working-tree state;
`scripts/fetch_quality_method_sources.py` offline-validates quality-card digests, manifest
and governed-record structure, while its explicit `--download-cache` mode additionally
retrieves or rechecks repository-external payload bytes against the recorded size and
SHA-256. None of these checks is automatically invoked merely because an opaque reference
string was accepted by either engine.

The full rationale, PR cross-read, external-source crosswalk and residuals are in
`docs/research/FOUR_DOMAIN_SUBJECTIVITY_QUALITY_CHAIN_2026_09_13.md`.
