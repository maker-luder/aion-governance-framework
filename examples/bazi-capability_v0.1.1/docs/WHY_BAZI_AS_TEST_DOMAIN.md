# Why Bazi Is Used as a Test Domain

The Bazi capability example is a **deterministic, bounded domain fixture** for testing engineering properties. It is not included as scientific evidence for astrology, as a subjectivity mechanism, or as authority for real-world decisions.

```text
ROLE = DETERMINISTIC_DOMAIN_EXAMPLE
SCIENTIFIC_VALIDATION_OF_BAZI = NOT_CLAIMED
SUBJECTIVITY_EVIDENCE = NONE
REAL_PERSON_DATA = EXCLUDED
AUTOMATIC_DECISION_AUTHORITY = NONE
```

## Why useful as an engineering fixture

1. Explicit structured synthetic inputs.
2. Rule-bound transformations that can be compared against specifications.
3. Traceable intermediate states.
4. Practical revision/supersession/rollback cases.
5. No requirement for hidden personal data.
6. Clean separation between computation and decision authority.

## Intended tests

- storage integrity;
- deterministic transformation consistency;
- provenance and correction lineage;
- schema validation;
- current-vs-superseded state handling;
- reproducibility;
- public/private data separation.

## Not tested or claimed

- empirical truth of astrological claims;
- psychological validity;
- subjectivity, consciousness or identity continuity;
- autonomous authority;
- suitability for consequential decisions.

A reviewer should be able to replace this domain with another bounded deterministic fixture and still evaluate the same engineering controls.

```text
DOMAIN_CHOICE != RESEARCH_CONCLUSION
DETERMINISM != SCIENTIFIC_VALIDATION
SUCCESSFUL_TEST != BAZI_TRUTH_CLAIM
```
