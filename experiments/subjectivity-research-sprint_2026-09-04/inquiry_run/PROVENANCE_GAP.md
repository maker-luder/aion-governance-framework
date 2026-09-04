# Inquiry-run provenance gap

```text
SOURCE_TREE_REF = 092f2a2ab46e746a6f93a61ef1c11e79dfdcd59d
CAMPAIGN_JSON_COMPLETENESS = PARTIAL
BYTE_FAITHFUL_EXECUTED_TRANSCRIPT = NOT_PRESERVED
EVENT_LEVEL_RECOMPUTATION = NOT_AVAILABLE
PRESERVED_EXECUTION_CHAIN_DIGEST = 609604a5626bf3a5454f77b95f48a808d8737bf5968a4f6db86745c23435e0b2
```

The execution receipt may preserve the historical chain digest. It cannot
reconstruct missing exact claim bytes and is not an event-level hash authority.

Observed:
- Runner and receipt bind `repository_ref` to `092f2a2...`.
- Checked-in `campaign.json` stores abbreviated claim/challenge strings.
- Those strings are not a byte-faithful copy of the executed claims.

```text
CAMPAIGN_HASH = 9fb03fd21b458799c9b5c21db8d0630e50f23364c3d429c56a8e8f6a58a7c3e6
RUNNER_DECLARED_REF == REPORT_REF == SOURCE_TREE_REF
SOURCE_TREE_REF != ARTIFACT_COMMIT
```
