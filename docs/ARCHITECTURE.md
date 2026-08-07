# Architecture

## Core pipeline

```text
Context Intake
→ Risk Gate
→ Planner
→ Policy Check
→ Tool Router
→ Response Builder
→ Writeback Gate
→ Audit Sink
```

## Extended research gates

```text
Current Input
→ Interpretation Drift Check
→ Memory Recall Gate
→ Epistemic Integrity Gate
→ Core Governance Pipeline
→ Writeback Gate
→ Canonical Gate (human approval required)
```

## Separation rules

- `retrieved_content != accepted_fact`
- `accepted_context != approved_writeback`
- `approved_writeback != canonical_state`
- `shared_project_knowledge != shared_private_memory`
- `model_instance != project_identity`
- `capability_artifact != identity`
- `bounded_runtime_candidate != canonical_AION_Runtime`

Each component is independently inspectable and does not receive authority merely by being included in the repository.
