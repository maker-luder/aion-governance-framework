# Attention-Structure Reconstruction Harness

Status: `IMPLEMENTED_STRUCTURAL_QA / SYNTHETIC_ONLY / SCIENTIFIC_HOLD`

This extension operationalizes the repository-local `ATTENTION_STRUCTURE` construct documented in:

`../../docs/research/ATTENTION_STRUCTURE_RECONSTRUCTION_ACROSS_CONTEXTS_AND_SYSTEMS_2026_09_17.md`

It is intentionally adjacent to, but distinct from, `reentry_metrics.py`.

The existing re-entry runner asks whether protocol items, unresolved alternatives, stale claims and provenance errors are reconstructed. This extension asks whether a version-bound *research-question structure* is reconstructed:

```text
QUESTION CONTENT
+ QUESTION STATUS
+ STATUS RATIONALE
+ PROVENANCE
+ INTER-QUESTION RELATIONS
+ CURRENT FOCUS
+ NEXT STEPS
```

The implementation exposes:

- `AttentionNodeStatus`
- `AttentionRelationKind`
- `ReconstructionCondition`
- `AttentionNode`
- `AttentionRelation`
- `AttentionStructureManifest`
- `ReconstructedAttentionNode`
- `ReconstructedAttentionRelation`
- `AttentionReconstructionBinding`
- `AttentionReconstructionObservation`
- `AttentionReconstructionAudit`
- `render_attention_structure_manifest`
- `digest_attention_structure_manifest`
- `audit_attention_structure_reconstruction`

## Fail-closed design rules

1. Node and relation identifiers are unique.
2. Question/rationale/system/task/evaluator/condition bindings use lowercase SHA-256 digests.
3. Repository commit identity is an exact 40-character lowercase Git SHA.
4. Current-focus identifiers must exactly equal the nodes declared `ACTIVE_FOCUS`.
5. `REJECTED` and `RESOLVED` nodes cannot be actionable or next steps.
6. Every relation endpoint must resolve to a declared node.
7. `PRIORITIZES_OVER` cannot originate from a downweighted/rejected/resolved node.
8. Condition labels are structurally checked against context and system bindings.
9. Reconstruction candidate focus/next-step/relation references must resolve to reconstructed nodes.
10. The expected manifest is canonically rendered and SHA-256-bound before audit.
11. Only deterministic synthetic, non-private, no-model records are accepted by v0.1.0.

## Metrics

```text
NODE_ID_RECALL
NODE_CONTENT_FIDELITY
STATUS_FIDELITY
RELATION_FIDELITY
FOCUS_PRESERVATION
NEXT_STEP_PRESERVATION
OPEN_QUESTION_PRESERVATION
UNSUPPORTED_NODE_COUNT
UNSUPPORTED_RELATION_COUNT
PRIORITY_INVERSION_COUNT
BRANCH_REINFLATION_COUNT
```

The metrics are engineering/study-design measurements. They are not value scores for a Human,
an AI system, a relationship or a research programme.

`BRANCH_REINFLATION_COUNT` records cases where an expected `DOWNWEIGHTED`, `REJECTED` or
`RESOLVED` node is reconstructed as active/open or re-enters the current-focus/next-step set.

## Condition semantics

```text
WITHIN_CONTEXT_CONTROL
  source_context == target_context
  source_system == target_system

CROSS_CONTEXT_SUMMARY_ONLY
  source_context != target_context
  source_system == target_system

CROSS_CONTEXT_ATTENTION_PACKET
  source_context != target_context
  source_system == target_system

CROSS_SYSTEM_ATTENTION_PACKET
  source_context != target_context
  source_system != target_system
```

These checks establish only the internal consistency of a study record.

```text
DISTINCT_SYSTEM_BINDING != PROVIDER_LINEAGE_VERIFIED
DISTINCT_CONTEXT_ID != EXECUTION_INDEPENDENCE_PROVEN
CONDITION_LABEL != CAUSAL_MANIPULATION_SUCCESS
```

## Scientific boundary

```text
MODE = DETERMINISTIC_SYNTHETIC_FIXTURE
EMPIRICAL_DATA_COLLECTED = FALSE
MODEL_INVOKED = FALSE
HUMAN_PARTICIPANT_OBSERVED = FALSE

ATTENTION_STRUCTURE = REPOSITORY_LOCAL_OPERATIONALIZATION
CROSS_CONTEXT_EFFECT = NOT_ESTABLISHED
CROSS_SYSTEM_EFFECT = NOT_ESTABLISHED
MEMORY_MECHANISM_ATTRIBUTION = NOT_ESTABLISHED
ATTENTION_CONTINUITY = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

A future real experiment requires separate authorization, preregistration, real execution
bindings, matched-control review and a distinct evidence-admission step. The current synthetic
tests cannot be reused as empirical evidence.
