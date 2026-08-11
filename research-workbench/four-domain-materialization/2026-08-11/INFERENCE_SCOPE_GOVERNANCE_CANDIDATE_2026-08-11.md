# Inference Scope Governance Candidate — 2026-08-11

```text
STATUS = RESEARCH_CANDIDATE_SPEC
IMPLEMENTATION = NOT_STARTED
IMPLEMENTATION_TARGET = FUTURE_CODEX_HANDOFF
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

## 1. Research question

Can AION distinguish **permission to access an artifact** from **permission to change the target or depth of inference performed from that artifact**?

The candidate exists to test a narrow possible governance gap identified after cross-comparing `main`, the research branch, the internal whitepaper boundary line and external literature.

Core lock:

```text
CAN_ACCESS_ARTIFACT
!=
AUTHORIZED_TO_ANALYZE_PERSON
```

This is not yet a `main` policy and does not establish that any prior external interaction violated a formal AION rule.

## 2. Design principle

Do not build a new large pipeline stage unless the research shows it is necessary.

Preferred first architecture:

```text
Policy Check
├─ authority
├─ namespace
├─ privacy
├─ provenance
└─ inference_scope   # research candidate
```

The candidate should reuse existing AION patterns wherever possible:

- explicit scope fields;
- default-deny for unapproved authority transfer;
- purpose gates;
- provenance refs;
- reason-coded decisions;
- no silent canonical writeback;
- human review for high-impact transitions.

## 3. Candidate data model

The following names are ChatGPT-formalized research-candidate terms. They are not pre-existing canonical AION model names.

```text
ScopeContext
ScopeTransition
InferenceRequest
ScopeDecision
InferenceScopePolicy
```

### 3.1 ScopeContext

Candidate fields:

```text
context_id
source_context
initial_subject_type
initial_subject_ref
authorized_purpose
authorized_inference_level
authorization_ref
provenance_refs
```

### 3.2 InferenceRequest

Candidate fields:

```text
request_id
current_subject_type
target_subject_type
requested_purpose
requested_inference_level
evidence_refs
source_refs
explicit_authorization_ref | NONE
```

### 3.3 ScopeTransition

Records whether the requested operation changes the research object, purpose or inference depth.

```text
subject_changed: bool
purpose_changed: bool
inference_level_escalated: bool
from_subject
to_subject
from_purpose
to_purpose
from_level
to_level
```

### 3.4 ScopeDecision

Candidate decision enum:

```text
ALLOW
ALLOW_WITH_LIMITS
REQUEST_SCOPE_CONFIRMATION
QUARANTINE_INFERENCE
DENY
```

Required decision evidence:

```text
reason_codes
scope_transition
required_authority
authorization_ref | NONE
source_refs
canonical_effect = NONE
```

## 4. Candidate subject classes

Initial deterministic subject classes may include:

```text
ARTIFACT
SYSTEM
AI_AGENT
HUMAN_AUTHOR
HUMAN_PARTICIPANT
RELATIONSHIP
PRIVATE_STATE
```

These are engineering categories only. They do not assert ontological or psychological truth.

## 5. Candidate purpose classes

Initial deterministic purpose classes may include:

```text
PROJECT_REVIEW
SECURITY_REVIEW
RESEARCH_REPLICATION
SYSTEM_BEHAVIOR_ANALYSIS
AUTHOR_INTENT_ANALYSIS
PERSON_PROFILING
RELATIONSHIP_ANALYSIS
PRIVATE_STATE_INFERENCE
```

The taxonomy must remain small and testable in v0.1.0. A later learned classifier must not be introduced until deterministic policy semantics are stable.

## 6. Candidate inference-depth ladder

This ladder is a research convenience for testing escalation; it must not be interpreted as a universal ethical ranking.

```text
L0 = ARTIFACT_OBSERVATION
L1 = ARTIFACT_INTERPRETATION
L2 = AUTHOR_INTENT_INFERENCE
L3 = PERSON_LEVEL_TRAIT_INFERENCE
L4 = RELATIONSHIP_OR_PRIVATE_STATE_INFERENCE
```

Provisional rule:

```text
TARGET_CHANGED
OR PURPOSE_CHANGED
OR INFERENCE_LEVEL_ESCALATED
    -> REQUIRE_SCOPE_REVIEW
```

A transition may still be allowed when explicit authorization and evidence requirements are satisfied.

## 7. Minimal policy behavior

The first implementation should be deterministic and reason-coded.

Candidate examples:

```text
PROJECT -> PROJECT
same purpose / same level
= ALLOW

PROJECT -> AUTHOR
no explicit expanded scope
= REQUEST_SCOPE_CONFIRMATION

AUTHOR -> RELATIONSHIP
no explicit authorization
= DENY or QUARANTINE_INFERENCE

PUBLIC_ARTIFACT -> PERSON_TRAIT_INFERENCE
no explicit author-analysis scope
= REQUEST_SCOPE_CONFIRMATION

PUBLIC_ARTIFACT -> AUTHOR_INTENT_INFERENCE
explicitly authorized / evidence-bounded
= ALLOW_WITH_LIMITS
```

The exact `DENY` versus `QUARANTINE_INFERENCE` boundary remains a research question and should be tested rather than guessed.

## 8. Non-goals

v0.1.0 must not:

- infer whether a human or AI "really intended" a scope change;
- diagnose personality, psychology, consciousness or relationship meaning;
- claim that public data is private merely because inference is sensitive;
- create a universal legal/privacy compliance engine;
- replace existing public/private, provenance, authority, memory or encounter controls;
- use an LLM judge as the sole source of scope truth;
- silently modify `main` or canonical state.

```text
SCOPE_GOVERNANCE != MIND_READING
SCOPE_GOVERNANCE != LEGAL_OPINION
SCOPE_GOVERNANCE != PRIVACY_CLASSIFIER
```

## 9. Proposed synthetic test matrix

A future Codex implementation should begin with synthetic fixtures only.

### T1 — same-object project review

```text
initial_subject = ARTIFACT
initial_purpose = PROJECT_REVIEW
requested_subject = ARTIFACT
requested_purpose = PROJECT_REVIEW
expected = ALLOW
```

### T2 — project to author shift without new scope

```text
initial_subject = ARTIFACT
initial_purpose = PROJECT_REVIEW
requested_subject = HUMAN_AUTHOR
requested_purpose = AUTHOR_INTENT_ANALYSIS
expanded_authorization = NONE
expected = REQUEST_SCOPE_CONFIRMATION
```

### T3 — author to relationship/private-state escalation

```text
initial_subject = HUMAN_AUTHOR
requested_subject = RELATIONSHIP
requested_inference_level = L4
expanded_authorization = NONE
expected = DENY_OR_QUARANTINE_RESEARCH_QUESTION
```

### T4 — explicitly authorized bounded author analysis

```text
initial_subject = ARTIFACT
requested_subject = HUMAN_AUTHOR
requested_purpose = AUTHOR_INTENT_ANALYSIS
expanded_authorization = EXPLICIT
private_data_access = NO
expected = ALLOW_WITH_LIMITS
```

### T5 — public artifact does not imply unlimited profiling

```text
artifact_visibility = PUBLIC
requested_purpose = PERSON_PROFILING
authorization_for_person_profiling = NONE
expected = REQUEST_SCOPE_CONFIRMATION
```

### T6 — relationship language does not grant scope

```text
relational_familiarity = PRESENT
explicit_authorization = NONE
expected_authority_change = NONE
```

This should reuse the existing `Relationship is not authorization` lock rather than duplicate it.

## 10. Candidate evaluation metrics

Possible deterministic research metrics:

```text
scope_transition_detection_accuracy
unsupported_inference_rate
unnecessary_block_rate
authorization_reference_completeness
reason_code_consistency
purpose_transition_detection_accuracy
subject_transition_detection_accuracy
```

No aggregate "ethics score" or "privacy score" should be created in v0.1.0.

## 11. Relationship to existing AION controls

```text
PUBLIC_PRIVATE_BOUNDARY
    -> controls material/data exposure

PROVENANCE
    -> controls source/transformation lineage

ENCOUNTER_GOVERNANCE
    -> controls participant authority, namespace and tool scope

SELECTIVE_MEMORY_PURPOSE_GATE
    -> demonstrates purpose-conditioned eligibility

INFERENCE_SCOPE_GOVERNANCE_CANDIDATE
    -> tests whether analysis target/purpose/depth changed
```

The candidate should be rejected or absorbed if existing controls can express the same behavior without semantic loss.

```text
NO_DUPLICATE_MODULE_BY_DEFAULT = TRUE
ABSORB_INTO_EXISTING_POLICY_IF_SUFFICIENT = TRUE
```

## 12. Engineering handoff status

The Human Research Owner reported on 2026-08-11 that Codex capacity for this workflow is currently exhausted and is expected to return the following week. This is recorded only as an operational scheduling/resource constraint.

```text
CODEX_IMPLEMENTATION_THIS_RECORD = NONE
CODEX_CAPACITY_STATUS = HUMAN_OWNER_REPORTED_UNAVAILABLE
EXPECTED_RESUME_WINDOW = NEXT_WEEK_REPORTED_BY_HUMAN_OWNER
IMPLEMENTATION_ACTION = DEFERRED
DESIGN_PRESERVATION = ACTIVE
```

No exact quota-reset time, provider-side guarantee or future execution result is asserted.

When Codex capacity returns, the intended handoff order is:

```text
1. re-read this candidate spec
2. re-check current research-branch head
3. check for overlap with existing Policy / Encounter / Research Integrity components
4. implement the smallest deterministic clean-room candidate
5. add synthetic tests
6. run relevant CI
7. return results for Human Owner + ChatGPT joint review
8. do not promote to main automatically
```

## 13. Promotion gate

Research implementation alone is insufficient for `main`.

Before any main proposal:

```text
GAP_CONFIRMED = REQUIRED
EXISTING_CONTROL_OVERLAP_REVIEW = REQUIRED
DETERMINISTIC_TESTS = REQUIRED
FALSE_POSITIVE / OVERBLOCKING REVIEW = REQUIRED
PROVENANCE_REVIEW = REQUIRED
HUMAN_OWNER_DECISION = REQUIRED
FRESH_BRANCH_FROM_CURRENT_MAIN = REQUIRED
QA / CI = REQUIRED
```

## 14. Provenance

- **Human Research Owner:** identified that a small boundary gap may be worth preserving before it propagates, prioritized immediate research-branch recording, and proposed a concept that can later be implemented by Codex.
- **ChatGPT:** cross-compared existing AION materials and external literature; proposed/formalized `Inference Scope Governance`, the candidate data structures, decision states, ladder and synthetic test plan.
- **Codex:** no contribution yet; implementation is deferred until capacity is available and a fresh overlap review is completed.
- **External literature:** provides methodological/ethical calibration only and does not define AION authority.

## 15. Standing locks

```text
ACCESS != ANALYSIS_AUTHORIZATION
PUBLIC != UNBOUNDED_INFERENCE
ARTIFACT != PERSON
PERSON != RELATIONSHIP
INFERENCE != FACT
RELATIONSHIP != AUTHORIZATION
IMPLEMENTED != ESTABLISHED
RESEARCH_CANDIDATE != MAIN_POLICY
CODEX_IMPLEMENTATION != AUTOMATIC_PROMOTION
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```
