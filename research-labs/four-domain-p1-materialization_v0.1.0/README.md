# Four-Domain P1 Materialization v0.1.0

## Status

```text
MODULE_STATUS = RESEARCH_CANDIDATE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
NETWORK_ACCESS = NONE
PERSISTENT_STORAGE = NONE
AUTOMATIC_WRITEBACK = NO
MODEL_WEIGHT_CHANGE = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_AFFECT = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

This isolated lab implements the first three engineering-ready gaps identified by the four-domain materialization workbench:

1. **Temporal / Version Resolution** — append-only version records, historical `as_was` projection, later `current_as_of` projection, revision lineage, and separate retrospective annotations.
2. **Correction / Conflict Transition Ledger** — immutable claims plus evidence-bound transition events for conflict, correction proposal/review, supersession, resolution, and withdrawal.
3. **Memory Evaluation Harness** — deterministic fixture metrics for retrieval, source attribution, temporal resolution, correction recovery, abstention, provenance completeness, unsupported inference, and stale-memory influence.

## Package surface

- `TemporalVersionResolver`
  - prevents later records from leaking backward into historical `as_was` views;
  - keeps `recorded_at`, `valid_from`, `observed_at`, `event_time`, and later retrospective interpretation distinct;
  - exposes explicit `revision_of` transition lineage.
- `CorrectionConflictLedger`
  - preserves claims and transitions separately;
  - requires actor, role, time, and evidence on transitions;
  - requires explicit correction approval before a `SUPERSEDED` transition;
  - keeps unresolved conflicts visible until explicitly resolved.
- `EvaluationHarness`
  - produces metric values with explicit numerator/denominator;
  - preserves undefined metrics as `None` when a fixture lacks ground truth;
  - is model-independent and uses no network or private conversation source.

## Validation

```powershell
python -m pytest research-labs/four-domain-p1-materialization_v0.1.0/tests -q
```

The included tests cover anti-back-projection, namespace/subject binding, revision lineage, evidence-required correction transitions, approval-before-supersession, conflict persistence, undefined metric handling, stale-memory detection, unsupported inference, and aggregate metric behavior.

## Research relationship to existing workbench

This lab is a materialization of gaps already named by:

- `research-workbench/four-domain-materialization/2026-08-09/FOUR_DOMAIN_REPOSITORY_CROSSWALK.md`
- `research-workbench/four-domain-materialization/2026-08-09/T0_T4_EXPERIMENT_HARNESS_READINESS.md`
- `research-workbench/four-domain-materialization/2026-08-09/APPLICATION_SERVICE_CONTRACT_GAP_MAP.md`
- `research-labs/core-meaning-commitments_v0.1.0/docs/CORE22_MATERIALIZATION_BRIDGE_PACKET_A.md`

No existing component imports this package. Nothing in this module authorizes production storage, runtime integration, MCP exposure, canonical promotion, Teacher binding, or identity/subjectivity conclusions.

## Attribution

- **Human Owner:** authorized this current P1 materialization inside the isolated research branch.
- **Codex:** authored the earlier repository fact-extraction workbench and gap maps that supplied the starting engineering evidence.
- **ChatGPT:** designed and implemented this P1 research package and its synthetic validation fixtures in response to the current authorization.
- **External research:** informs the broader research questions; this package does not claim conformance to any external benchmark or ontology.
