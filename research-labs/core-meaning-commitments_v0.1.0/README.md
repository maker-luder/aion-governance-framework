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
- `policy.py`: fail-closed status for canonical promotion, relationship authority and cross-namespace transfer.

## Example

```python
from aion_core_meaning import CoreMeaningWorkbench

workbench = CoreMeaningWorkbench()
# Add provenance-bound MeaningClaim and MeaningEvent objects.
# Ask assess(...) to produce an inspectable review trace.
# The result always has final_judgment=None and canonical_effect="NONE".
```

## Validation

```powershell
python -m pytest research-labs/core-meaning-commitments_v0.1.0/tests -q
```

The tests cover provenance, bounded importance/confidence, append-only revision, namespace isolation, conflict review, explicit relevance, subject separation and fail-closed governance.

## Integration boundary

No existing component imports this package. A later Human Owner + ChatGPT review would need to decide definitions, subject/namespace binding, privacy/retention, authorized storage, correction semantics, application-service contract and evaluation criteria before any integration proposal.
