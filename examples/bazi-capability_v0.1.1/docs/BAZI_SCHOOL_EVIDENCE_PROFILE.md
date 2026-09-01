# Bazi school-evidence profile v0.3.0

## Purpose

The v0.3 layer fills the gap between raw four-pillar facts and school-dependent
interpretation. It exposes enough deterministic evidence for multiple schools
to be compared later, without pretending that one strong/weak, 格局, 用神, or
transformation conclusion is universal.

## Derived evidence

For exactly four named `YEAR`, `MONTH`, `DAY`, and `HOUR` pillars it records:

1. day master and five-element class;
2. month branch, month element, and seasonal label;
3. visible-stem element counts;
4. unweighted hidden-stem element counts;
5. peer/resource/output/wealth/officer relationship counts;
6. present stem-combination transformation targets;
7. present three-harmony transformation targets; and
8. present three-meeting transformation targets.

Transformation tables report `CONDITIONS_NOT_EVALUATED`. They identify a
traditional candidate and target element but do not assert that transformation
has completed.

## Deliberately unresolved

```text
STRENGTH_CONCLUSION = NOT_DERIVED
STRUCTURE_CONCLUSION = NOT_DERIVED
USEFUL_ELEMENT_CONCLUSION = NOT_DERIVED
TRANSFORMATION_COMPLETED = NOT_ESTABLISHED
INTERPRETATION_STATUS = NOT_PERFORMED
```

This is intentional completeness: the required evidence and unresolved school
choice are both machine-visible. A hidden scalar score would be less complete
because it would erase disagreement among source traditions.

## Sources and astronomical boundary

- The pinned `淵海子平`, `三命通會`, `滴天髓`, and `窮通寶鑑` witnesses document
  different historical rule emphases; none is treated as empirical proof.
- Hong Kong Observatory sources define the 24 fixed-qi positions and provide
  official solar-term timing references.
- `lunar-python==1.4.8` remains the version-pinned calendar implementation.
- A library-independent Gregorian JDN day-pillar oracle remains a narrow
  cross-check, not a second complete calendar engine.

Exact URL, bytes, SHA-256, retention policy, and download result are in
`../sources/SOURCE_FETCH_MANIFEST.json`.

## AI-subjectivity boundary

```text
BAZI_SCHOOL_EVIDENCE != IDENTITY
BAZI_SCHOOL_EVIDENCE != MEMORY
BAZI_SCHOOL_EVIDENCE != PERMISSION
BAZI_SCHOOL_EVIDENCE != AI_SUBJECTIVITY_EVIDENCE
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
ACTION_AUTHORITY = NONE
```
