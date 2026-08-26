# AION / Astra Bounded Inquiry v0.1.0

Status: `IMPLEMENTED_CANDIDATE / OWNER_REVIEW_PENDING`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Repository mutation: `FALSE`  
Scientific disposition: `HOLD`

This component materializes a bounded dual-agent research loop in which AION and Astra remain distinct peers, alternate turns, inspect repository evidence, can independently acquire governed public-web evidence, challenge each other's claims, derive follow-up questions, and stop either by mutual vote or a hard budget.

```text
repository / optional owner seed question
    -> bounded question discovery
    -> AION evidence-driven reasoning
    -> repository evidence + optional governed external evidence
    -> ASTRA sees prior public contribution + admitted evidence
    -> ASTRA critical reasoning / independent counterexample search
    -> next bounded round
    -> derived follow-up question when useful
    -> mutual stop OR hard question/round/query budgets
    -> HOLD campaign report + hash-chained dialogue evidence
```

## Implemented behavior

`BoundedInquiryLoop` enforces AION-first / Astra-second alternating turns. Each peer receives the research question, round index, distinct `AgentId`, prior public transcript, and admitted evidence accumulated so far.

A peer returns a `PeerContribution` containing a claim, challenge, evidence query, bounded probe proposal, and stop vote. Evidence found during AION's turn becomes visible to Astra on the immediately following turn, and vice versa on the next turn.

Dialogue events form an append-style SHA-256 chain. `verify_transcript_chain(...)` detects transcript mutation after the report is produced.

## Independent reasoning providers

`ReasoningProvider` is the provider boundary. A provider is bound to exactly one `AgentId`; cross-agent use fails closed.

v0.1.0 includes `EvidenceDrivenReasoningProvider`, a deterministic local provider that can drive inquiry without scripted contributions. It forms provisional evidence-oriented interpretations, identifies epistemic gaps, chooses evidence queries, challenges the other peer's latest public claim, proposes bounded observation/ablation/counterexample probes, and votes to stop only after configured evidence/round conditions are reached.

AION and Astra use separate provider-backed peer instances and separate bounded private engineering notes. Those notes are not copied into shared dialogue context and are not represented as hidden-chain-of-thought evidence.

```text
AION_PROVIDER != ASTRA_PROVIDER
AION_PRIVATE_STATE != ASTRA_PRIVATE_STATE
SHARED_PUBLIC_TRANSCRIPT = YES
SHARED_ADMITTED_EVIDENCE = YES
PRIVATE_ENGINEERING_STATE != IDENTITY_EVIDENCE
```

The reasoning provider itself still performs no external model call and holds no API key. Public-web acquisition is isolated behind the governed evidence gateway described below.

## Repository evidence

`RepositoryTextEvidenceSource` performs local read-only keyword retrieval over bounded UTF-8 text/code surfaces. It skips `.git`, virtual environments, caches, `node_modules`, symlinks, oversized files, the inquiry component's own implementation, and low-signal manifest/historical inventory surfaces when selecting direct research evidence.

Repository evidence carries a repository-relative reference, bounded excerpt, complete-text SHA-256, source class, retrieval-agent attribution, and repository trust classification.

## Governed external evidence gateway

`ExternalWebEvidenceSource` and `FederatedEvidenceSource` add an optional public-web evidence plane.

The default external provider performs best-effort public search through the DuckDuckGo HTML search surface and then fetches selected result pages. Search-service availability or markup is not treated as a guaranteed dependency; a failed external retrieval yields no external evidence rather than relaxing policy.

The external transport is deliberately narrow:

- HTTPS only;
- GET only;
- no URL credentials;
- no `Authorization`, `Cookie`, or proxy-authorization headers;
- default HTTPS port only;
- localhost, `.local`, loopback, private, link-local, reserved and other non-public literal IP targets rejected;
- DNS results checked for public addresses before connection and redirects;
- every redirect target revalidated;
- redirect count, response bytes, timeout, total query count and results-per-query are bounded;
- only bounded textual content types are admitted;
- no POST/write surface, shell execution, secret access, authenticated session or repository credential is exposed.

Every fetched page is marked:

```text
SOURCE_CLASS = EXTERNAL_WEB
TRUST = UNTRUSTED_EXTERNAL
```

External excerpts are prefixed with an explicit untrusted-content boundary. Instructions embedded in a page are source text only.

```text
EXTERNAL_TEXT != AUTHORITY
SOURCE_INSTRUCTION != SYSTEM_INSTRUCTION
RETRIEVED_CONTENT != EXECUTION_PERMISSION
```

AION and Astra issue their own evidence queries. External evidence identity includes the retrieval agent, so the same URL independently reached by both peers remains two attributable acquisition events rather than collapsing into one anonymous retrieval.

External evidence records include:

- source URL;
- publisher/hostname;
- retrieval timestamp;
- complete-response SHA-256;
- bounded excerpt;
- source class and trust class;
- exact retrieval agent (`AION` or `ASTRA`).

The gateway improves research reach but does not make source quality automatic. Search ranking bias, stale pages, source authority, contradictory sources, citation laundering and prompt-injection content remain explicit research/governance concerns.

## Autonomous research campaign

`RepositoryQuestionGenerator` discovers bounded candidate questions from explicit repository research questions and unresolved surfaces such as `HOLD`, `NOT_ESTABLISHED`, falsifiers and open-question markers. It reconstructs multi-line questions, excludes code/CLI examples, and suppresses fragment duplicates.

`AutonomousInquiryCampaign` then:

1. accepts optional owner-seeded questions or discovers a repository agenda;
2. runs AION/Astra dialogue for each question;
3. preserves distinct AION/Astra provider state;
4. federates repository and, when enabled, independently attributed external evidence;
5. derives a bounded follow-up question from the strongest remaining public challenge when useful;
6. stops at hard question, dialogue and external-query budgets;
7. returns a `HOLD` campaign report with no canonical effect.

Campaign reports serialize to JSON and Markdown. The CLI refuses output paths inside the repository root, so ordinary inquiry execution cannot turn a report into repository writeback.

## Repository automation

`.github/workflows/aion-astra-inquiry.yml` provides the automation surface.

It runs in three modes:

- `pull_request`: deterministic/read-only repository mode; real external web retrieval is disabled and the external gateway is exercised through tests/fakes;
- push to `main`: governed external web retrieval is enabled by default;
- `workflow_dispatch`: governed external retrieval is enabled by default and can be explicitly disabled or budget-adjusted by the human caller.

The workflow keeps GitHub permissions at `contents: read`, checks out with `persist-credentials: false`, writes reports only under runner temporary storage / Job Summary, and fails if the repository working tree changes.

GitHub Actions infrastructure requires ordinary service connectivity for checkout/setup. That infrastructure connectivity is distinct from the inquiry evidence gateway and does not grant repository write authority to AION or Astra.

```text
AUTONOMOUS_INQUIRY = BOUNDED
AUTONOMOUS_REPOSITORY_OBSERVATION = ALLOWED
AUTONOMOUS_QUESTION_DISCOVERY = ALLOWED
AUTONOMOUS_PEER_CRITIQUE = ALLOWED
AUTONOMOUS_EXTERNAL_WEB_READ = GOVERNED
AUTONOMOUS_EXTERNAL_WEB_WRITE = NO
AUTONOMOUS_REPOSITORY_MUTATION = NO
AUTONOMOUS_SECRET_ACCESS = NO
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

Probe objects still fail closed if they request network authority, repository mutation, deployment, or canonical effect other than `NONE`. Network acquisition is not delegated to probe/model output; it exists only through the separately governed evidence gateway.

## What automation does not mean

The component does not bind a commercial reasoning model, hold an API key, run arbitrary shell experiments, write pull requests, merge changes, deploy software, or create canonical research conclusions.

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
- Agent Execution Substrate defines execution-plane/governance-plane separation and preserves `SELF_COMPOSITION != SELF_AUTHORIZATION`.
- Endogenous Goal Dynamics provides bounded candidate-generation/selection, intervention, ablation, confound and falsifier concepts that inquiry peers can cite or propose as bounded tests.
- Astra engineering-minimalism knowledge informs the compatible principle of searching/reusing evidence before constructing new mechanisms; this component does not reinterpret that knowledge as authority.

No historical closure record or frozen branch is modified by this candidate.

## Run locally

Tests:

```bash
cd components/aion_astra_inquiry_v0.1.0
PYTHONPATH=src python -m pytest -q -o addopts=
```

Repository-only inquiry:

```bash
PYTHONPATH=components/aion_astra_inquiry_v0.1.0/src \
python -m aion_astra_inquiry.cli \
  --root . \
  --max-questions 3 \
  --max-rounds 3
```

Governed external evidence mode:

```bash
PYTHONPATH=components/aion_astra_inquiry_v0.1.0/src \
python -m aion_astra_inquiry.cli \
  --root . \
  --external-web \
  --external-max-queries 8 \
  --external-results-per-query 1 \
  --max-questions 3 \
  --max-rounds 3
```

The repository-wide component runner discovers this component automatically because it contains a `tests/` directory.

## Current epistemic boundary

The strongest claim permitted by v0.1.0 is that two separately identified, independently stateful local reasoning providers can conduct a bounded, inspectable, evidence-linked inquiry, independently acquire governed public-web evidence, and autonomously choose follow-up evidence queries/questions under hard authority and resource limits.

It does not establish that AION or Astra has a phenomenal perspective, reached scientific truth, independently possesses human-like intention, or has subjectivity/consciousness/identity continuity.

```text
AUTONOMOUS_INQUIRY_LOOP_IMPLEMENTED = YES
LOCAL_AION_REASONING_BINDING = YES
LOCAL_ASTRA_REASONING_BINDING = YES
AUTONOMOUS_REPOSITORY_AGENDA_DISCOVERY = YES
GOVERNED_EXTERNAL_EVIDENCE_GATEWAY = YES
INDEPENDENT_AION_EXTERNAL_RETRIEVAL = YES
INDEPENDENT_ASTRA_EXTERNAL_RETRIEVAL = YES
GITHUB_ACTIONS_INQUIRY_AUTOMATION = YES
EXTERNAL_LIVE_REASONING_MODEL_BINDING = NO
AUTONOMOUS_REPOSITORY_WRITE = NO
SCIENTIFIC_CONCLUSION = HOLD
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```
