# Artifact Transformation Lineage Adversarial — Source Notes

## Unit boundary

`artifact-transformation-lineage-adversarial_v0.1.0` is a research-only metadata audit extension. It does not execute transformations, inspect private data, publish artifacts, modify canonical state, deploy, or establish scientific validity.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing artifact transformation lineage model | `repo:research-labs/artifact-transformation-lineage_v0.1.0/src/aion_artifact_lineage/lineage.py` | Repository Evidence | Current within the verified research lineage at the unit commit; exact state is bounded by QA receipt | Reused ArtifactRef/SHA-256, run-state, design/run separation, environment redaction, record-only and canonical-effect boundary concepts; no existing fixture was counted as new evidence |
| Existing artifact lineage source crosswalk | `repo:research-labs/artifact-transformation-lineage_v0.1.0/docs/EXTERNAL_SOURCE_CROSSWALK.md` | Repository Evidence | Current within branch lineage; not independently re-dated in this extension | Used as methodological context only; no external source code or runtime dependency was imported |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority was changed |

## Synthetic experiment transformation

The new audit maps declared event metadata into `VALID`, `HOLD`, or `INVALID` reason codes. A matching digest means only that supplied bytes equal a declared SHA-256 digest. It does not establish provenance truth, scientific validity, transformation correctness, release status, or canonical artifact status. The 15 fixtures are synthetic inputs and are not replication evidence.

The first `state-order-invalid` fixture reused `event:1` and therefore triggered duplicate-ID validation. This construction failure is retained in `artifact-lineage-adversarial-initial-failure.md`; the corrected fixture uses unique IDs and contiguous indexes and reaches the intended state-order branch.

## Provenance vocabulary

```text
Repository Evidence != External Literature
Tool Output != Scientific Evidence
Synthetic Fixture != Replication
DIGEST_MATCH != SCIENTIFIC_VALIDITY
LINEAGE_VALID != REPLICATION
RESEARCH_RESULT != CANONICAL_CONCLUSION
```

## Non-promotion invariants

```text
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```
