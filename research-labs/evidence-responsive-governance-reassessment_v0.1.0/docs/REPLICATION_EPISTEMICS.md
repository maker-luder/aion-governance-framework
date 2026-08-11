# Replication Epistemics

Status: `RESEARCH_ENGINEERING / PROVISIONAL`

```text
ReplicationAttempt
-> ReplicationAssessment
-> ReplicationRecord
-> ReassessmentRecommendation
```

The raw attempt stores fixture lineage, protocol and implementation versions, evaluator
identity/version/contract, independent group, seed, outcome, validity, observation reference,
and provenance. Interpretation never mutates that attempt.

| Observation | Interpretation behavior |
|---|---|
| Failed + valid + independent | Downward reassessment pressure; no fixed level |
| Three preregistered valid independent failures | Strong downward pressure; hold for research decision |
| Failed + evaluator drift | Preserve level; evaluator review |
| Failed + invalid | No evidence downgrade |
| Mixed or boundary condition | Claim-scope review or narrowing |
| Inconclusive | Increased uncertainty |

Reproduction uses the same or tightly matched fixture, code, protocol, or seed. Independent
replication requires an independently identified group, fixture, implementation, or equivalent
test. A same-seed rerun is not counted as independent replication.

No score, optimization, retry-until-pass, attempt deletion, post-outcome seed selection,
rights grant, authority grant, or automatic review escalation is present.
