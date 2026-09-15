# Conversational and multi-agent coordination quality

Status: `IMPLEMENTED_EXPERIMENTAL_HARNESS / SCIENTIFIC_HOLD`

This module reuses the merged PR #91 coupled-cognition quality factory. It
represents speaker, context and monitor policies with a content-bound
`CoordinationCondition`, and the exact condition is now a required input to the
audit and is retained in the audit result. A condition object that exists beside
the event stream but is not bound into adjudication is not treated as sufficient.

The audit uses immutable event sequences for turn concentration, required-role
coverage, unresolved requests, repeated turn content and explicit stop/handoff
quality. Generic turn-request latency and topic-switch latency are reported as
separate metrics rather than being collapsed into one field; both remain subject
to the declared request-latency requirement.

An NCR reason is emitted only when a stated process requirement is violated.
Unequal participation by itself is measured but is not classified as suppression
or nonconformance. The harness performs no networking, agent orchestration,
psychometric inference or autonomous action. Its output is admissible only as
process-quality evidence, not as subjectivity or consciousness evidence.

```text
DECLARED_CONDITION != BOUND_AUDIT_CONDITION
TURN_REQUEST_LATENCY != TOPIC_SWITCH_LATENCY
MODEL_INVOKED = FALSE
EVIDENCE_ADMISSIBILITY = PROCESS_QUALITY_ONLY
TURN_CONCENTRATION != INTENTIONAL_SUPPRESSION
ROLE_COVERAGE != CONTENT_CORRECTNESS
ORCHESTRATION != EPISTEMIC_AUTHORITY
COORDINATED_BEHAVIOR != SHARED_MIND
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
