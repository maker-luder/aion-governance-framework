# Executable Four-Domain standards crosswalk

Status: `BOUNDED_IMPLEMENTATION / STRUCTURALLY_TESTED / SCIENTIFIC_HOLD`

This extension materializes the candidate implementation classes specified by
merged PR #102 without turning an external standard into subjectivity evidence.

```text
IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
ORIGINAL_SPECIFICATION_REVIEW = PR #102 @ 3ce4f759caf662a53f0d1f3a54709bc482d7df5e
CURRENT_SPECIFICATION_STATUS = MERGED
SYNCED_MAIN_COMMIT_SHA = 6e0ae579da9d09b3ba4041d52a7e9833ceb10ca1
PR102_USED_AS_IMPLEMENTATION_BASE = FALSE
```

The existing Four-Domain and research-quality-chain structures from merged PR
#100 remain canonical antecedents. This is a minimal extension that adds:

1. a content-hash-bound external-standard source registry;
2. explicit contribution roles: vocabulary, process control, evidence quality,
   technical method, and claim limit;
3. complete bindings across human construct, ontology-neutral machine question,
   engineering operation, and governance interpretation;
4. a required subjectivity-confound register that rejects human-to-machine
   equivalence and human constructs as subjectivity proxies;
5. distinct TEST, EVALUATION, VERIFICATION, and VALIDATION definitions.

The registry fails closed on duplicate sources or bindings, unknown source
references, incomplete TEVV vocabulary, missing Four-Domain fields, missing
process/evidence roles, or absent confound records.

```text
MODEL_INVOKED = FALSE
EVIDENCE_ADMISSIBILITY = PROCESS_CONTROL_ONLY
STANDARD_CONFORMANCE != SCIENTIFIC_VALIDATION
PROCESS_CONTROL != SUBJECTIVITY_EVIDENCE
HUMAN_CONSTRUCT != MACHINE_ONTOLOGY
TEVV_TERMS_ARE_NOT_SYNONYMS
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation ships only synthetic fixture tests. Populating the registry
with external standards requires exact authoritative locators, version/date,
access date, immutable content hash, and independent source review.
