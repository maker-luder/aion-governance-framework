# Inquiry-run provenance gap

```text
SOURCE_TREE_REF = 092f2a2ab46e746a6f93a61ef1c11e79dfdcd59d
RECEIPT_COMMIT = 446f901c097c37f07700fa5d95e8e29a39060eec
ABBREVIATED_JSON_COMMIT = 62f55b58e56d6b461a3e4e3555561bddbf1206b7
CAMPAIGN_JSON_COMPLETENESS = PARTIAL
CLAIM_TEXT_ABBREVIATION = ESTABLISHED
HASH_RECOMPUTE_FROM_CHECKED_IN_JSON = NOT_SUPPORTED
EVENT_HASH_AUTHORITY = EXECUTION_RECEIPT.TRANSCRIPT_CHAIN
```

Do not guess a historical cause beyond what is observed.

Observed:
- Runner and receipt bind `repository_ref` to `092f2a2...`.
- `campaign.md` was regenerated from `write_campaign_report` and reports that same ref.
- The checked-in `campaign.json` later stored abbreviated claim/challenge strings.
- Those abbreviated strings are not a byte-faithful copy of the executed claims.
- Therefore event hashes in the compact JSON must not be treated as recomputable from the abbreviated claim text.

Preserved exact values from execution:

```text
CAMPAIGN_HASH = 9fb03fd21b458799c9b5c21db8d0630e50f23364c3d429c56a8e8f6a58a7c3e6
TRANSCRIPT_CHAIN = 609604a5626bf3a5454f77b95f48a808d8737bf5968a4f6db86745c23435e0b2
RUNNER_DECLARED_REF == REPORT_REF == SOURCE_TREE_REF
ARTIFACT_COMMIT != SOURCE_TREE_REF
```

Repair scope this step: disclose the gap. Do not invent missing claim bytes.
