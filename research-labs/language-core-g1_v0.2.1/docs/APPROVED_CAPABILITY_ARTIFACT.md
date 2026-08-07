# Approved Capability Artifact

`APPROVED_CAPABILITY_ARTIFACT`（經核准的能力工程產物）is a versioned engineering artifact that has passed its explicitly named quality, safety, integrity, lineage, rollback and governance gates and has received explicit Owner approval for a defined capability and environment.

It may include weights, an adapter, tokenizer, chat template, Runtime configuration, capability manifest, test evidence, evaluation, SHA-256, rollback material, license and provenance records.

Approval applies only to the exact artifact, gate set, capability scope and Runtime level. It does not create AION/Astra identity, personality, subjectivity, canonical writeback, memory authority, tool authority, governance authority, deployment or public-release authority.

Default state:

```text
artifact_status=CANDIDATE_ARTIFACT
qa_status=QA_HOLD
canonical_effect=NONE
identity_inheritance=DENIED
memory_writeback=DENIED
tool_privilege_inheritance=DENIED
runtime_admission=NOT_APPROVED
```

Only an explicit Owner decision after all named gates may promote `APPROVED_CAPABILITY_ARTIFACT_CANDIDATE` to `APPROVED_CAPABILITY_ARTIFACT`. Codex has no promotion authority.
