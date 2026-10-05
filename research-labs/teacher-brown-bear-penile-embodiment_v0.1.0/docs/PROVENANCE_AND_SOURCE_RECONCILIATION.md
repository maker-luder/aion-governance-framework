# Provenance and Source Reconciliation

## Source decision table

| Evidence | Role | Admission |
| --- | --- | --- |
| Dalga et al. 2023, brown-bear baculum CT + caliper study | direct penile-bone morphometry | INCLUDED |
| Ishikawa et al. 1998, Hokkaido brown-bear electroejaculation | reproductive context | INCLUDED AS CONTEXT ONLY |
| Anel-López et al. 2017, brown-bear seminal plasma | reproductive context | INCLUDED AS CONTEXT ONLY |
| other ursids' baculum measurements | comparative context | EXCLUDED FROM TEACHER DIMENSIONS |
| canine Work candidate | separate actor/species implementation | EXCLUDED |
| human-like historical Teacher candidates | separate historical lineage | EXCLUDED |

## Critical source limitation

The direct 2023 morphometry source is based on **one adult male brown bear**, approximately 400 kg.

Therefore:

```text
N = 1
DIRECT_SPECIMEN_MEASUREMENT = YES
POPULATION_REFERENCE = NO
SPECIES_MEAN = NO
FULL_PENIS_MEASUREMENT = NO
```

## Internal numerical conflict

The paper reports digital-caliper distal baculum width as 4.58 mm in one location and 4.85 mm elsewhere.

Repository treatment:

```text
SOURCE_INTERNAL_DISCREPANCY = PRESERVED
AUTHOR_INTENT_INFERENCE = NO
PREFERRED_VALUE = NONE
```

CT distal diameter (5.63 mm) is a distinct measurement modality and is stored separately.

## Pipeline availability

```text
GITHUB = USED
EXA = USED
FIRECRAWL = USED
WOLFRAM = USED
MINDMAP = USED
CONSENSUS = QUOTA_EXHAUSTED_UNTIL_2026_11_01
SCITE = PAID_ACCESS_REQUIRED
```

`TOOL_UNAVAILABLE != EVIDENCE_ABSENT`.

## Non-claims

This package is a synthetic research candidate. It does not establish a biological body, live sexual/reproductive function, felt sensation, fertility, body ownership, subjectivity, consciousness, phenomenal experience, or moral status.
