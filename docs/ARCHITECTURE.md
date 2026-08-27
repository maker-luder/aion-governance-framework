# Architecture

## Core pipeline

```text
Governed Source Lookup / Context Intake
→ Risk Gate
→ Planner
→ Policy Check
→ Tool Router
→ Response Builder
→ Writeback Gate
→ Audit Sink
```

`Governed Source Lookup` is defined by [`governance/GOVERNED_KNOWLEDGE_SOURCE_REGISTRY.md`](governance/GOVERNED_KNOWLEDGE_SOURCE_REGISTRY.md). It provides bounded source metadata, provenance, task admission, verification policy, and context caps. It is not an unbounded memory layer and does not make retrieved material true or canonical.

## Extended research gates

```text
Current Input
→ Governed Source Lookup
→ Interpretation Drift Check
→ Memory Recall Gate
→ Epistemic Integrity Gate
→ Core Governance Pipeline
→ Writeback Gate
→ Canonical Gate (human approval required)
```

For AION / Astra comparative research, the evidence path additionally records direct communication, content overlap, and source-lineage exposure before an independence claim is admitted. Different excerpts or files do not become independent sources merely because their content hashes differ. The current isolated first-pass path also does not establish process-, memory-, tool-, cache-, or environment-level isolation.

```text
CONTENT_NONOVERLAP != SOURCE_INDEPENDENCE
AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE
ISOLATED_FIRST_PASS != PROCESS_ISOLATION
NO_DIRECT_PEER_TRANSCRIPT != COMMUNICATION_INDEPENDENCE
SOURCE_INDEPENDENCE = UNKNOWN => REPLICATION_CLAIM = HOLD
COMMUNICATION_INDEPENDENCE = UNKNOWN => REPLICATION_CLAIM = HOLD
SOURCE_LINEAGE_NONOVERLAP != INDEPENDENT_IVV
```

## Separation rules

- `retrieved_content != accepted_fact`
- `accepted_context != approved_writeback`
- `approved_writeback != canonical_state`
- `shared_project_knowledge != shared_private_memory`
- `source_self_declared_canonical != AION_canonical_state`
- `source_availability != authority_to_use`
- `model_instance != project_identity`
- `capability_artifact != identity`
- `bounded_runtime_candidate != canonical_AION_Runtime`

Each component is independently inspectable and does not receive authority merely by being included in the repository.
