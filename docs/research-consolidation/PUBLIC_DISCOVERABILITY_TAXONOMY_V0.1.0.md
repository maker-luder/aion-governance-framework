# AION Public Discoverability Taxonomy v0.1.0

> **Proposal only.** This taxonomy proposes repository Topics; it does not modify GitHub settings. The repository was public at inspection time and had no Topics configured. All candidate terms are lowercase GitHub-compatible slugs and are grounded in the repository's verified research/engineering surfaces, not in novelty or ontological claims.

## 1. Public positioning rule

The public description should make AION discoverable as a **research-engineering and governance framework for evidence, provenance, memory evaluation and bounded agent systems**. It should not market AION as conscious, sentient, self-aware, identity-bearing, unprecedented, or scientifically proven. The taxonomy therefore favors method, engineering surface and governance terms that are supported by current artifacts.

## 2. Recommended candidate Topics

| Rank | Topic slug | Taxonomy class | Source basis | Adoption readiness | Why it is safe |
|---:|---|---|---|---|---|
| 1 | `ai-research` | broad domain | Root research tree, Four-Domain materialization, G1 and runtime research labs | READY_CANDIDATE | Describes repository purpose without a scientific conclusion |
| 2 | `research-engineering` | engineering method | P1–P5 packages, component runner, convergence artifacts | READY_CANDIDATE | Names the actual code/document/test practice |
| 3 | `research-integrity` | governance method | Research Scope Lock, evidence validator, non-claim boundaries | READY_CANDIDATE | Matches explicit integrity and fail-closed controls |
| 4 | `evidence-provenance` | evidence method | P2 provenance validator, evidence record schema, source-of-truth map | READY_CANDIDATE | Describes implemented evidence/provenance work |
| 5 | `provenance-aware-ai` | engineering orientation | P2 provenance-gated retrieval and external PROV-O crosswalk | READY_CANDIDATE | Describes a bounded design orientation, not a guarantee |
| 6 | `memory-governance` | domain/control | Memory recall governance and P2 stale/superseded controls | READY_CANDIDATE | Supported by repository memory governance surfaces |
| 7 | `agent-memory` | research domain | P2 memory retrieval/provenance slice and verified MemoryAgentBench/AgeMem crosswalk | READY_CANDIDATE | Names the studied engineering domain without performance claims |
| 8 | `long-term-memory` | research domain | LongMemEval, MemoryAgentBench, Memora and P2 temporal/stale controls | OWNER_REVIEW_REQUIRED | Accurate but broad; Owner should confirm public scope |
| 9 | `metacognition` | research domain | Verified metacognition literature crosswalk and Four-Domain research questions | OWNER_REVIEW_REQUIRED | External literature term; does not imply AION has metacognition |
| 10 | `hypothesis-testing` | research method | P1–P5 hypotheses, fixtures, expected outcomes and evidence records | READY_CANDIDATE | Describes method rather than result |
| 11 | `falsification` | research method | P5 falsifier lifecycle and P2 falsifier matrix | READY_CANDIDATE | Names explicit challenge/failure handling |
| 12 | `reproducible-research` | research method | Deterministic fixtures, manifest hashes, component runner and exact-head CI | READY_CANDIDATE | Supported for engineering replay, not universal scientific replication |
| 13 | `ai-safety-evaluation` | governance/evaluation | Safety gates, adversarial research labs, P2/P3 falsifiers and verified safety literature | OWNER_REVIEW_REQUIRED | Accurate but public-facing scope should be Owner-confirmed |
| 14 | `language-model-evaluation` | evaluation domain | G1 QA gates, Four-Domain LLM questions and research evaluation harnesses | READY_CANDIDATE | Names evaluation scope without model superiority claims |
| 15 | `deterministic-retrieval` | implementation surface | P2 deterministic context assembler, explicit exclusion reasons and manifest hashes | READY_CANDIDATE | Directly implemented and reviewer-verifiable |
| 16 | `governance-kernel` | implementation surface | `components/governance_kernel_v0.4.0` and governance artifacts | OWNER_REVIEW_REQUIRED | Accurate component term, but public scope/branding should be confirmed |

## 3. Suggested initial candidate set

The smallest coherent initial set is:

```text
ai-research
research-engineering
research-integrity
evidence-provenance
memory-governance
agent-memory
hypothesis-testing
falsification
reproducible-research
language-model-evaluation
deterministic-retrieval
governance-kernel
```

This set is intentionally method- and implementation-oriented. `long-term-memory`, `metacognition` and `ai-safety-evaluation` are valid candidates but should receive explicit Owner review because they may shape public expectations beyond the narrowest repository description. `provenance-aware-ai` is safe as a technical orientation but should be reviewed if the Owner wants only noun-based domain Topics.

## 4. Explicitly rejected Topics

The following are not proposed because they are unsupported, misleading or too close to forbidden ontological/novelty claims:

| Rejected Topic | Reason |
|---|---|
| `consciousness` | Research question and external taxonomy only; not an established repository result |
| `artificial-consciousness` | Converts a research subject into a public capability claim |
| `self-aware-ai` | Label does not establish a self-model mechanism or subjectivity |
| `sentient-ai` | No evidence or authorized conclusion |
| `identity-continuity` | P2 explicitly keeps identity continuity `NOT_ESTABLISHED` |
| `first-of-its-kind` | Unverified novelty claim and invalid Topic style |
| `agi` | Overbroad positioning not supported by the current source-of-truth map |
| `production-ai` | Deployment is `FALSE`; research-only status would be contradicted |

## 5. Application boundary

No Topics were applied. Actual repository settings changes remain `OWNER_DECISION_REQUIRED`. If the Owner later approves a subset, the settings operation should apply only the approved lowercase slugs and then record the exact resulting metadata in a dated read-only audit. This branch does not perform that operation.

## 6. Source grounding

The candidate set is grounded in current repository artifacts: the Four-Domain crosswalk, P1–P5 research packages, P2 provenance/retrieval implementation, Scope Lock, evidence validator, G1 governance/QA gates, governance kernel code, and the primary-source literature crosswalk. External terminology is used descriptively; it is not evidence that AION reproduces or exceeds any cited work.
