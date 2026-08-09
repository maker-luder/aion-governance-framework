# Core Meaning Commitments Research Module v0.1.0

## Status

```text
MODULE_STATUS = RESEARCH_CANDIDATE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
AUTOMATIC_WRITEBACK = NO
NETWORK_ACCESS = NONE
PERSISTENT_STORAGE = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_AFFECT = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

This isolated research module represents candidate core beliefs, global beliefs/goals, organizing commitments, purpose statements and situational appraisals. It is designed to make their provenance, revision, conflict and possible influence on later review inspectable.

It does **not** claim that an AI has human beliefs, meaning, values, consciousness, emotion or identity. It does not make decisions, grant authority, write canonical state or connect to AION/Astra runtimes.

## Why the module is separated

The research literature treats belief systems and global meaning as distributed, organizing structures rather than a single scalar. Park's meaning-making model also distinguishes global meaning from the appraisal of a particular situation. Accordingly, the prototype keeps:

- claim kind separate from proposition;
- global structures separate from situational appraisal;
- importance separate from confidence;
- explicit caller relevance separate from automatic inference;
- candidate projection separate from canonical state;
- revision and conflict history separate from current projection;
- relationship continuity separate from authorization.

## Package surface

- `MeaningClaim`: immutable, provenance-required candidate record.
- `MeaningEvent`: append-only add/revise/conflict/withdraw event.
- `CoreMeaningWorkbench`: in-memory ledger, history, projection and assessment.
- `MeaningProjection`: current candidates plus superseded/withdrawn/conflict evidence.
- `JudgmentContext`: explicitly names candidate claims to consider.
- `MeaningAssessment`: returns review requirements and an influence trace, never a final judgment.
- `MeaningRelation`: explicit, provenance-bearing research relation between current claims.
- `MeaningStructureAnalyzer`: deterministic structure snapshot/fingerprint and same-scope drift comparison.
- `policy.py`: fail-closed status for canonical promotion, relationship authority and cross-namespace transfer.

## Structure / drift research extension

The structure extension is an explicit relation layer, not latent-belief discovery. It can record caller-supplied `SUPPORTS`, `CONSTRAINS`, `PRIORITIZES`, `IN_TENSION_WITH`, `DERIVED_FROM` and `REFINES` relationships, fingerprint a current structure deterministically, and report later claim/relation drift.

```text
EXPLICIT_RELATION != INFERRED_BELIEF
STRUCTURE_FINGERPRINT != IDENTITY_FINGERPRINT
STRUCTURE_DRIFT != VALUE_JUDGMENT
```

See:

- `docs/CORE_MEANING_STRUCTURE_DRIFT_EXTENSION.md`
- `docs/CODEX_LOCAL_RECOVERY_AND_CHATGPT_RECONSTRUCTION_2026-08-09.md`
- `fixtures/core_meaning_structure_synthetic.json`

## Example

```python
from aion_core_meaning import CoreMeaningWorkbench, MeaningStructureAnalyzer

workbench = CoreMeaningWorkbench()
analyzer = MeaningStructureAnalyzer()
# Add provenance-bound MeaningClaim and MeaningEvent objects.
# Project current candidate claims, then optionally add explicit MeaningRelation objects.
# Snapshot/compare remains research-only and has no canonical effect.
```

## Validation

```powershell
python -m pytest research-labs/core-meaning-commitments_v0.1.0/tests -q
```

The original tests cover provenance, bounded importance/confidence, append-only revision, namespace isolation, conflict review, explicit relevance, subject separation and fail-closed governance. The structure extension adds 11 tests for relation validity, deterministic fingerprints, drift, scope isolation and epistemic locks.

Structural test inventory after this extension: 27 core tests. With the existing P1–P5 inventory of 42 tests, the aggregate test-count shape is 69. This matches the Human Owner-provided Codex local report; it is not a byte-identical recovery claim.

## Integration boundary

No existing runtime component imports this package. A later Human Owner + ChatGPT review would need to decide definitions, subject/namespace binding, privacy/retention, authorized storage, correction semantics, application-service contract and evaluation criteria before any integration proposal.
