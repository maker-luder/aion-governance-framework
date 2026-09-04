# Inquiry-run provenance gap

```text
SOURCE_TREE_REF = 092f2a2ab46e746a6f93a61ef1c11e79dfdcd59d
CAMPAIGN_JSON_COMPLETENESS = PARTIAL
BYTE_FAITHFUL_EXECUTED_TRANSCRIPT = NOT_PRESERVED
EVENT_LEVEL_RECOMPUTATION = NOT_AVAILABLE
PRESERVED_EXECUTION_CHAIN_DIGEST = 609604a5626bf3a5454f77b95f48a808d8737bf5968a4f6db86745c23435e0b2
RUN_NOTE_RECORDED_CAMPAIGN_HASH = e7f65c9647dc298f5c4bf6e3ecfff1434834b7037a582aa221d7462acf816731
CHECKED_IN_PARTIAL_CAMPAIGN_HASH = 9fb03fd21b458799c9b5c21db8d0630e50f23364c3d429c56a8e8f6a58a7c3e6
CAMPAIGN_HASH_EQUIVALENCE = FALSE
```

The execution receipt may preserve the historical chain digest. It cannot
reconstruct missing exact claim bytes and is not an event-level hash authority.

Observed:
- Runner and receipt bind `repository_ref` to `092f2a2...`.
- Checked-in `campaign.json` stores abbreviated claim/challenge strings.
- Those strings are not a byte-faithful copy of the executed claims.

```text
CHECKED_IN_PARTIAL_CAMPAIGN_HASH = 9fb03fd21b458799c9b5c21db8d0630e50f23364c3d429c56a8e8f6a58a7c3e6
RUNNER_DECLARED_REF == REPORT_REF == SOURCE_TREE_REF
SOURCE_TREE_REF != ARTIFACT_COMMIT
```

`INQUIRY_RUN.md` retains a different run-note campaign hash (`e7f65c96...`).
Because the exact executed claim bytes are unavailable, neither hash is
silently upgraded into a byte-faithful event-level authority. The
`9fb03fd2...` value identifies the checked-in partial campaign representation;
the `e7f65c96...` value remains a historical run-note record.
