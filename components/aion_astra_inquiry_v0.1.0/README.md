# AION / Astra Bounded Inquiry v0.1.0

Status: `IMPLEMENTED_CANDIDATE / OWNER_REVIEW_PENDING`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Inquiry network calls: `FALSE`  
Repository mutation: `FALSE`  
Scientific disposition: `HOLD`

This component materializes a bounded dual-agent research loop in which AION and Astra remain distinct peers, alternate turns, inspect read-only repository evidence, challenge each other's claims, derive follow-up questions, and stop either by mutual vote or a hard budget.

```text
repository / optional owner seed question
    -> bounded question discovery
    -> AION evidence-driven reasoning
    -> read-only repository evidence retrieval
    -> ASTRA sees prior public contribution + new evidence
    -> ASTRA critical reasoning / counterexample search
    -> next bounded round
    -> derived follow-up question when useful
    -> mutual stop OR hard question/round budget
    -> HOLD campaign report + hash-chained dialogue evidence
```

## Implemented behavior

`BoundedInquiryLoop` enforces AION-first / Astra-second alternating turns. Each peer receives:

- the research question;
- current round index;
- its own and the peer's distinct `AgentId`;
- the complete prior public dialogue transcript;
- repository evidence accumulated so far.

A peer returns a `PeerContribution` containing a claim, challenge, repository evidence query, bounded probe proposal, and stop vote. Evidence found by AION during a turn is visible to Astra on the immediately following turn.

`RepositoryTextEvidenceSource` performs local read-only keyword retrieval over a bounded set of UTF-8 text/code file types. It skips `.git`, virtual environments, caches, `node_modules`, symlinks, oversized files, and anything resolving outside the configured repository root. Evidence records contain only a repository-relative ref, bounded excerpt, and SHA-256 of the complete source text.

Dialogue events form an append-style SHA-256 chain. `verify_transcript_chain(...)` detects transcript mutation after the report is produced.

## Independent reasoning providers

`ReasoningProvider` is the provider boundary. A provider is bound to exactly one `AgentId`; cross-agent use fails closed.

v0.1.0 includes `EvidenceDrivenReasoningProvider`, an offline deterministic provider that can actually drive the inquiry without scripted contributions. It:

- forms a provisional evidence-oriented interpretation;
- identifies an epistemic gap;
- chooses a repository evidence query;
- challenges the other peer's latest public claim;
- proposes observation, ablation, or counterexample probes;
- votes to stop only after the configured evidence/round condition is reached.

AION and Astra use separate provider-backed peer instances and separate bounded private engineering notes. Those notes are not copied into the shared dialogue context and are not represented as hidden-chain-of-thought evidence.

```text
AION_PROVIDER != ASTRA_PROVIDER
AION_PRIVATE_STATE != ASTRA_PRIVATE_STATE
SHARED_PUBLIC_TRANSCRIPT = YES
SHARED_REPOSITORY_EVIDENCE = YES
PRIVATE_ENGINEERING_STATE != IDENTITY_EVIDENCE
```

The default provider uses no external model, API key, network request, shell command, or commercial service. `ReasoningProvider` remains replaceable so a separately governed provider adapter can be added later without changing the inquiry protocol or collapsing AION/Astra identities.

## Autonomous research campaign

`RepositoryQuestionGenerator` discovers bounded candidate questions from explicit repository questions and unresolved surfaces such as `HOLD`, `NOT_ESTABLISHED`, falsifier, and open-question markers.

`AutonomousInquiryCampaign` then:

1. accepts optional owner-seeded questions or discovers a repository agenda;
2. runs AION/Astra dialogue for each question;
3. preserves distinct AION/Astra provider state;
4. derives a bounded follow-up question from the strongest remaining public challenge when useful;
5. stops at a hard question budget;
6. returns a `HOLD` campaign report with no canonical effect.

Campaign reports can be serialized to JSON and Markdown. The CLI refuses output paths inside the repository root so ordinary automated runs cannot turn inquiry output into repository writeback.

## Repository automation

`.github/workflows/aion-astra-inquiry.yml` provides the repository automation surface.

It runs:

- automatically after a push to `main`;
- manually through `workflow_dispatch`, optionally with an owner-seeded question.

The workflow has only `contents: read`, checks out without persisted credentials, runs the local provider, writes reports only under the runner temporary directory, appends the Markdown report to the GitHub Job Summary, and fails if the repository working tree changed.

The inquiry process itself implements no network calls. GitHub Actions infrastructure still requires ordinary GitHub service connectivity for checkout/setup; that infrastructure connectivity is not inquiry-model network authority.

```text
AUTONOMOUS_INQUIRY = BOUNDED
AUTONOMOUS_REPOSITORY_OBSERVATION = ALLOWED
AUTONOMOUS_QUESTION_DISCOVERY = ALLOWED
AUTONOMOUS_PEER_CRITIQUE = ALLOWED
AUTONOMOUS_REPOSITORY_MUTATION = NO
AUTONOMOUS_NETWORK_MODEL_CALL = NO
AUTONOMOUS_DEPLOYMENT = NO
AUTONOMOUS_MERGE = NO
CANONICAL_EFFECT = NONE
```

## Probe boundary

v0.1.0 admits planning/reference probe kinds only:

- `REPOSITORY_OBSERVATION`
- `REPLAY_CHECK`
- `SYNTHETIC_TEST_PLAN`
- `ABLATION_PLAN`
- `COUNTEREXAMPLE_SEARCH`

Every `Probe` fails closed if it requests network access, repository mutation, deployment, or canonical effect other than `NONE`.

## What automation does not mean

The component does not bind a commercial model, hold an API key, run arbitrary shell experiments, write pull requests, merge changes, deploy software, or create canonical research conclusions.

```text
PEER_DIALOGUE != SHARED_IDENTITY
SHARED_EVIDENCE != SHARED_MEMORY
PEER_CONSENSUS != SCIENTIFIC_TRUTH
PROVIDER_OUTPUT != OWNER_DECISION
AUTONOMOUS_GOAL_SELECTION != ACTION_AUTHORITY
ENGINEERING_BEHAVIOR != SUBJECTIVITY_EVIDENCE
```

## Relationship to existing repository components

- Astra Runtime provides a distinct Astra Runtime context and governed task/memory/state-lineage mechanisms.
- Agent Execution Substrate defines the execution-plane/governance-plane separation and preserves `SELF_COMPOSITION != SELF_AUTHORIZATION`.
- Endogenous Goal Dynamics provides bounded candidate-generation/selection, intervention, ablation, confound, and falsifier concepts that inquiry peers can cite or propose as bounded tests.
- Astra engineering-minimalism knowledge informs the compatible design principle of searching/reusing existing evidence before constructing new mechanisms; this component does not reinterpret that knowledge as authority.

No historical closure record or frozen branch is modified by this candidate.

## Run locally

Tests:

```bash
cd components/aion_astra_inquiry_v0.1.0
PYTHONPATH=src python -m pytest -q -o addopts=
```

Autonomous repository inquiry with discovered questions:

```bash
PYTHONPATH=components/aion_astra_inquiry_v0.1.0/src \
python -m aion_astra_inquiry.cli \
  --root . \
  --max-questions 3 \
  --max-rounds 3
```

Owner-seeded question:

```bash
PYTHONPATH=components/aion_astra_inquiry_v0.1.0/src \
python -m aion_astra_inquiry.cli \
  --root . \
  --question "Which current evidence most strongly challenges the working mechanism?"
```

The repository-wide component runner discovers this component automatically because it contains a `tests/` directory.

## Current epistemic boundary

The strongest claim permitted by v0.1.0 is that two separately identified, independently stateful local reasoning providers can conduct a bounded, inspectable, evidence-linked repository inquiry and autonomously choose follow-up evidence queries/questions under hard authority and budget limits.

It does not establish that AION or Astra has a phenomenal perspective, reached scientific truth, independently possesses human-like intention, or has subjectivity/consciousness/identity continuity.

```text
AUTONOMOUS_INQUIRY_LOOP_IMPLEMENTED = YES
LOCAL_AION_REASONING_BINDING = YES
LOCAL_ASTRA_REASONING_BINDING = YES
AUTONOMOUS_REPOSITORY_AGENDA_DISCOVERY = YES
GITHUB_ACTIONS_INQUIRY_AUTOMATION = YES
EXTERNAL_LIVE_MODEL_BINDING = NO
INQUIRY_NETWORK_MODEL_EXECUTION = NO
SCIENTIFIC_CONCLUSION = HOLD
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```
