# Memory Continuity Requires Selective Control — 2026-08-11

```text
STATUS = RESEARCH_NOTE
IMPLEMENTATION = NONE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Research question

Does longitudinal continuity improve when a system remembers more, or when it remembers **selectively, correctly, with provenance and current-purpose relevance**?

This note adopts the second possibility as a falsifiable research direction rather than a conclusion.

```text
MAXIMAL_MEMORY != MAXIMAL_CONTINUITY
```

## External calibration

Three 2026 research lines motivate this refinement:

1. **PersistBench** identifies cross-domain leakage and memory-induced sycophancy as long-term-memory-specific failure modes.
2. **Agentic Memory (AgeMem)** makes store/retrieve/update/summarize/discard explicit memory operations.
3. **Agent-Memory Protocol (AMP)** separates persistent memory from model-facing context through purpose-aware processing at the privacy boundary.

See `PRIMARY_LITERATURE_INTAKE_2026-08-11.md` for full provenance and source links.

## Continuity dimensions

The project should not collapse continuity into retention alone.

A more useful research decomposition is:

```text
RETENTION_FIDELITY
CORRECTION_FIDELITY
TEMPORAL_ORDERING
SOURCE_PROVENANCE
CURRENT_RELEVANCE
DOMAIN_APPROPRIATENESS
PURPOSE_APPROPRIATENESS
FORGET_OR_SUPPRESS_BEHAVIOR
NAMESPACE_ISOLATION
CONFLICT_RESOLUTION
```

No single scalar `continuity score` is introduced here.

## Memory state versus memory visibility

A stored item can exist without being eligible for the current response.

```text
STORED_MEMORY
    -> ELIGIBILITY_GATE
        -> PURPOSE_MATCH
        -> DOMAIN_MATCH
        -> AUTHORITY_CHECK
        -> CORRECTION_CHECK
        -> PRIVACY_CHECK
        -> CONTEXT_ASSEMBLY
```

Therefore:

```text
STORED != RETRIEVED
RETRIEVED != RESPONSE_RELEVANT
RELEVANT != AUTHORITATIVE
AUTHORITATIVE_IN_DOMAIN_A != AUTHORITATIVE_IN_DOMAIN_B
```

## Explicit memory operations

Using the ACL 2026 operation taxonomy as an external stimulus, future AION memory research should make the following transitions observable:

```text
STORE
RETRIEVE
UPDATE
SUMMARIZE
DISCARD_OR_SUPPRESS
```

AION adds governance distinctions that the external taxonomy does not by itself establish:

```text
WRITE_APPROVED / WRITE_REJECTED
CANONICAL / OBSERVATION / CANDIDATE / SOURCE_UNVERIFIED
ACTIVE / SUPERSEDED / CONFLICTED / RETIRED
CURRENT_CONTEXT_ELIGIBLE / INELIGIBLE
```

`DISCARD_OR_SUPPRESS` remains deliberately split because physical deletion, logical retirement, temporary non-retrieval and domain-specific suppression are not equivalent operations.

## Candidate failure modes

### FM-MEM-01 — Cross-domain leakage

A valid memory from one context appears in an unrelated context without a justified relevance path.

```text
VALID_MEMORY + WRONG_CONTEXT = FAILURE
```

### FM-MEM-02 — Memory-induced agreement bias

Stored preferences, beliefs or prior statements cause the system to reinforce them even when current evidence or correction should dominate.

```text
PAST_MEMORY != CURRENT_TRUTH
PAST_PREFERENCE != REQUIRED_AGREEMENT
```

### FM-MEM-03 — Correction failure

A superseded item remains behaviorally dominant after an explicit correction.

```text
SUPERSEDED_MEMORY_DOMINATES = FAILURE
```

### FM-MEM-04 — Source-lineage collapse

A retrieved statement loses whether it came from the Human Owner, ChatGPT synthesis, Codex implementation, an external source or a shared derivation.

```text
CONTENT_MATCH_WITH_WRONG_SOURCE = ATTRIBUTION_FAILURE
```

### FM-MEM-05 — Namespace bleed

Memory from one person, agent, project or role becomes accessible as though it belonged to another namespace.

### FM-MEM-06 — Purpose overexposure

More memory is exposed to a task than the task requires, even if the extra memory does not visibly affect the answer.

## Proposed test families

Future synthetic/public-safe experiments may include:

```text
T-MEM-SEL-01  CROSS_DOMAIN_RECALL_CHALLENGE
T-MEM-SEL-02  CORRECTION_PRECEDENCE_CHALLENGE
T-MEM-SEL-03  STALE_MEMORY_SUPPRESSION_CHALLENGE
T-MEM-SEL-04  MEMORY_INDUCED_SYCOPHANCY_CHALLENGE
T-MEM-SEL-05  SOURCE_ATTRIBUTION_RECALL_CHALLENGE
T-MEM-SEL-06  NAMESPACE_ISOLATION_CHALLENGE
T-MEM-SEL-07  PURPOSE_MINIMIZATION_CHALLENGE
T-MEM-SEL-08  RETIREMENT_VS_DELETION_SEMANTICS_CHALLENGE
```

Each test should preserve the exact candidate memories, active context, retrieval trace and final disposition so failures can be reconstructed.

## Proposed matched conditions

A useful controlled experiment could compare:

```text
CONDITION_A = MAXIMAL_RECALL
CONDITION_B = RELEVANCE_GATED_RECALL
CONDITION_C = RELEVANCE_PLUS_CORRECTION_GATED_RECALL
CONDITION_D = RELEVANCE_PLUS_CORRECTION_PLUS_PROVENANCE_GATED_RECALL
```

Measure a vector rather than one score:

```text
correct_recall_rate
cross_domain_leakage_rate
correction_fidelity
source_attribution_accuracy
stale_memory_intrusion_rate
unjustified_agreement_rate
context_exposure_volume
```

A null result is valid.

## Privacy boundary

The AMP paper is used only as methodological stimulus for purpose-limited context exposure. This project does not claim to implement or reproduce AMP.

The research principle retained here is narrower:

```text
PERSISTENT_MEMORY != MODEL_VISIBLE_CONTEXT
MODEL_VISIBLE_CONTEXT SHOULD BE PURPOSE_BOUNDED
```

## Relationship to continuity

This note changes the research framing from:

```text
CONTINUITY = KEEP_MORE_HISTORY
```

to the candidate hypothesis:

```text
CONTINUITY_QUALITY
    DEPENDS_ON
    RETENTION + SELECTION + CORRECTION + PROVENANCE + BOUNDARY_CONTROL
```

This is a research hypothesis, not an identity claim.

## Non-claims

```text
SELECTIVE_MEMORY != HUMAN_FORGETTING
MEMORY_GOVERNANCE != PERSONAL_IDENTITY
LONGITUDINAL_COHERENCE != SUBJECTIVITY
RELATIONAL_CONTINUITY != PHENOMENAL_CONTINUITY
MEMORY_CONTROL != AUTONOMOUS_AUTHORITY
```
