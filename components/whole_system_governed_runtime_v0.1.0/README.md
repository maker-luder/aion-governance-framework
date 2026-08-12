# Whole-System Governed Runtime v0.1.0 — Review v2 Candidate

Status: `IMPLEMENTED_CANDIDATE / OWNER_TEACHER_REVIEW_REQUIRED`

This component is a local, in-process AION/Astra integration candidate. It is replayed from the superseded review artifact and transformed to the authoritative v2 memory and repository package contracts. It does not deploy, promote canonical state, or establish ontological claims.

## Governed end-to-end flow

```text
INPUT
 -> CONTEXT_INTAKE
 -> IDENTITY / NAMESPACE BINDING
 -> RECALL REQUEST
 -> NAMESPACE + ACCESS + PROVENANCE + STATE FILTERS
 -> AUTHORIZED SEMANTIC MEMORY CONTEXT (bounded payload)
 -> TRUSTED PROVENANCE VERIFICATION
 -> TOOL APPROVAL REGISTRY (when requested)
 -> KILLABLE PROVIDER / TOOL EXECUTION WITH GLOBAL DEADLINE
 -> RESPONSE BUILD
 -> WRITEBACK AUTHORIZATION
 -> WRITE-AHEAD MEMORY INTENT
 -> MEMORY WRITE
 -> APPEND-ONLY AUDIT + CHECKPOINT
 -> INTENT COMMIT OR RESTART RECONCILIATION
 -> OUTPUT
```

## Semantic memory contract

The Language Core receives a bounded structured representation containing the authorized memory identifier, content, namespace, authority, confidence, revision, timestamp, provenance source, and supersession status. The runtime excludes other namespaces, unauthorized scope, unverified provenance, tombstoned records, superseded records, and conflict-flagged records. Tests use a sentinel secret and inspect the adapter input rather than checking only recalled IDs.

The repository's upstream memory component currently exposes content and provenance/state flags but does not expose an independent confidence/revision authority model. The whole-system layer therefore records bounded derived review metadata explicitly as a candidate representation; it does not claim those derived values are canonical truth.

## Trust boundaries

`ToolInvocation.approved`, `approval_id`, `WholeSystemRequest.owner_approved`, and `WholeSystemRequest.provenance_verified` are untrusted caller claims. A tool runs only when an independently registered `TrustedApprovalRecord` matches the requester, approver distinction, authority, exact tool, namespace, scopes, and validity window. Provenance runs only when an independently registered `TrustedProvenanceRecord` matches source identity, kind, locator, digest, branch and validity. A caller cannot promote a claim to verified proof by setting a boolean.

## Bounded execution

Generation and tool execution run in a child process. The parent enforces the global request deadline, observes mid-flight cancellation, terminates the child on the boundary, and performs no writeback after timeout or cancellation. This is a demonstrated hard boundary for the local Python candidate process model, not a claim about arbitrary external provider cancellation semantics.

## Durability semantics

Memory and whole-system state remain separate SQLite stores. The component does **not** claim cross-database atomicity. Instead, it writes a durable write-ahead intent before memory mutation, commits the intent only after audit/checkpoint persistence succeeds, and exposes `PENDING_RECONCILIATION` if required persistence fails. On restart, the runtime compares the stored memory content digest with the pending intent and deterministically marks the intent reconciled or aborted. No response is `COMPLETED` when required governance/audit persistence failed.

## Boundaries

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
NETWORK_MCP = NOT_IMPLEMENTED
FOUNDATION_MODEL_TRAINED = NOT_CLAIMED
SUBJECTIVITY_PROVEN = FALSE
IDENTITY_PROVEN = FALSE
PHENOMENAL_MEMORY_PROVEN = FALSE
```

A passing test demonstrates candidate implementation behavior only; it does not prove subjectivity, consciousness, selfhood, personal identity, phenomenal memory, trained-model quality, production readiness, or canonical truth.

## Test entrypoint

```bash
PYTHONPATH=src:../memory_recall_governance_v0.1.0/src pytest -q
```
