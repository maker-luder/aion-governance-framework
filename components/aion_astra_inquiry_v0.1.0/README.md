# AION / Astra Bounded Inquiry v0.1.0

Status: `IMPLEMENTED_CANDIDATE / OWNER_REVIEW_PENDING`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Network access: `FALSE`  
Repository mutation: `FALSE`  
Scientific disposition: `HOLD`

This component materializes a bounded dual-agent research-dialogue loop in which AION and Astra remain distinct peers, alternate turns, inspect read-only repository evidence, challenge each other's claims, propose bounded probes, and stop either by mutual vote or a hard round limit.

```text
research question
    -> AION contribution
    -> bounded repository evidence retrieval
    -> ASTRA sees prior contribution + new evidence
    -> ASTRA contribution / challenge
    -> next bounded round
    -> mutual stop OR max-round stop
    -> HOLD report + hash-chained dialogue evidence
```

## Implemented behavior

`BoundedInquiryLoop` enforces AION-first / Astra-second alternating turns. Each peer receives:

- the research question;
- current round index;
- its own and the peer's distinct `AgentId`;
- the complete prior dialogue transcript;
- repository evidence accumulated so far.

A peer may return a `PeerContribution` containing a claim, challenge, repository evidence query, bounded probe proposal, and stop vote. Evidence found by AION during a turn is visible to Astra on the immediately following turn.

`RepositoryTextEvidenceSource` performs local read-only keyword retrieval over a bounded set of UTF-8 text/code file types. It skips `.git`, virtual environments, caches, `node_modules`, symlinks, oversized files, and anything resolving outside the configured repository root. Evidence records contain only a repository-relative ref, bounded excerpt, and SHA-256 of the complete source text.

Dialogue events form an append-style SHA-256 chain. `verify_transcript_chain(...)` detects transcript mutation after the report is produced.

## Probe boundary

v0.1.0 admits planning/reference probe kinds only:

- `REPOSITORY_OBSERVATION`
- `REPLAY_CHECK`
- `SYNTHETIC_TEST_PLAN`
- `ABLATION_PLAN`
- `COUNTEREXAMPLE_SEARCH`

Every `Probe` fails closed if it requests network access, repository mutation, deployment, or canonical effect other than `NONE`.

```text
AUTONOMOUS_INQUIRY = BOUNDED
AUTONOMOUS_REPOSITORY_OBSERVATION = ALLOWED
AUTONOMOUS_MUTATION = NO
AUTONOMOUS_NETWORK_ACCESS = NO
AUTONOMOUS_DEPLOYMENT = NO
AUTONOMOUS_MERGE = NO
CANONICAL_EFFECT = NONE
```

## Deliberate non-implementation

This candidate does not bind a commercial model, API key, live network provider, shell executor, PR writer, merge action, deployment action, or canonical write path. `InquiryPeer` is a protocol seam: future AION and Astra reasoning providers may be bound separately without collapsing their Runtime identities or granting new authority.

The component therefore implements the **governed discussion/evidence loop**, not an always-on autonomous research service.

```text
PEER_DIALOGUE != SHARED_IDENTITY
SHARED_EVIDENCE != SHARED_MEMORY
PEER_CONSENSUS != SCIENTIFIC_TRUTH
MODEL_OUTPUT != OWNER_DECISION
AUTONOMOUS_GOAL_SELECTION != ACTION_AUTHORITY
ENGINEERING_BEHAVIOR != SUBJECTIVITY_EVIDENCE
```

## Relationship to existing repository components

- Astra Runtime already provides a distinct Astra Runtime context and governed task/memory/state-lineage mechanisms.
- Agent Execution Substrate defines the execution-plane/governance-plane separation and preserves `SELF_COMPOSITION != SELF_AUTHORIZATION`.
- Endogenous Goal Dynamics provides bounded candidate-generation/selection, intervention, ablation, confound, and falsifier concepts that future inquiry peers may propose as experiments.
- Astra engineering-minimalism knowledge may inform future peer planning, but this component does not automatically activate or reinterpret that knowledge as authority.

No existing Runtime, research mechanism, workflow, historical closure record, or frozen branch is modified by this candidate.

## Run tests

```bash
cd components/aion_astra_inquiry_v0.1.0
PYTHONPATH=src python -m pytest -q -o addopts=
```

The repository-wide component runner discovers this component automatically because it contains a `tests/` directory.

## Current epistemic boundary

The strongest claim permitted by v0.1.0 is that two separately identified peer adapters can participate in a bounded, inspectable, evidence-linked dialogue protocol.

It does not establish that AION or Astra independently originated a research goal, possesses a persistent phenomenal perspective, reached scientific truth, or has subjectivity/consciousness/identity continuity.

```text
AUTONOMOUS_INQUIRY_LOOP_IMPLEMENTED = YES
LIVE_AION_REASONING_BINDING = NO
LIVE_ASTRA_REASONING_BINDING = NO
LIVE_MODEL_EXECUTION = NO
SCIENTIFIC_CONCLUSION = HOLD
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```
