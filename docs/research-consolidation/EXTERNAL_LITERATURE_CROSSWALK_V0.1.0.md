# AION External Literature Crosswalk v0.1.0

> This crosswalk is a source-grounding artifact. It records what external authors report, what AION engineering translates, what AION integrates, and what remains a novelty hypothesis. It deliberately rejects unverified `first`, `only`, and `unprecedented` claims. External literature is not AION evidence and no external code is imported by this artifact.

## 1. Claim labels

`VERIFIED` means the cited primary or official source was opened and the narrow statement matches the source. `PARTIAL` means only part of the intake description was verified or the source is a repository description rather than an experiment record. `ANALOGY` means a methodological resemblance, not evidence of equivalence. `AION_INTERPRETATION` means an AION design translation, not an external author claim. `NOVELTY_HYPOTHESIS` means a possible contribution that requires systematic related-work review and independent evidence. `CORRECTION_REQUIRED` means the intake wording is too broad, ambiguous, or inconsistent with the primary source and must not be repeated as fact.

## 2. Primary papers and standards

| ID | Primary source | Narrow source claim | Label | AION engineering translation | AION integration | Novelty / correction | Disposition |
|---|---|---|---|---|---|---|---|
| `LIT-META-LLM-2026` | Liu et al., [arXiv:2607.11881][1] | The review describes metacognition around monitoring and regulation, reports fragmented terminology and heterogeneous evidence, and discusses safety trade-offs | VERIFIED | Keep monitoring, control, calibration and self-report as separable research dimensions | No model or runtime integration in this consolidation | Subjectivity, self-awareness and consciousness remain unsupported | KEEP_RESEARCH_ONLY |
| `LIT-DMC-2025` | Wang et al., [AAAI DOI 10.1609/aaai.v39i24.34723][2] | DMC separates failure prediction/confidence-based metacognitive measurement from first-order task ability and reports sensitivity to confidence elicitation | VERIFIED | Separate first-order task metrics from second-order monitoring metrics | No AION experiment or metric adoption is claimed | Any AION metacognition result would be a new experiment, not a reproduction | KEEP_RESEARCH_ONLY |
| `LIT-NEUROFEEDBACK-2025` | Li et al., [OpenReview record qTXlFwlggv][3] | Neurofeedback/in-context tests report/control selected activation directions; effects depend on examples, semantic interpretability and explained variance | VERIFIED | Treat internal-state control as a safety-relevant measurement precedent only | No activation-control implementation or runtime authority | Global self-access and subjectivity are rejected interpretations | KEEP_RESEARCH_ONLY |
| `LIT-SELFVERIFY-2026` | Chen et al., [arXiv:2602.07594][4] | Generation and self-verification can be asymmetric; the paper reports complementary objectives and benchmark results under its training setup | VERIFIED | Preserve generation versus verification separation in evidence design | No training or model change is added | AION replication is absent | KEEP_RESEARCH_ONLY |
| `LIT-REVISE-2025` | [ReVISE, arXiv:2502.14565][5] | The method trains stop/refine decisions and reports self-verification/self-correction improvements in stated benchmarks | VERIFIED | Method precedent for separate verification/correction stages | No training feature is added to AION | No claim that AION implements or improves ReVISE | KEEP_RESEARCH_ONLY |
| `LIT-PERSISTBENCH-2026` | [PersistBench, arXiv:2602.01146][6] | The abstract defines cross-domain leakage and memory-induced sycophancy risks and reports evaluated failure rates | VERIFIED | Use stale, cross-context and contamination behavior as falsifier classes | P2 uses synthetic exclusion/provenance controls only | No AION safety benchmark result | KEEP_RESEARCH_ONLY |
| `LIT-LONGMEMEVAL-2024` | [LongMemEval, arXiv:2410.10813][7] | The benchmark covers information extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention; it describes indexing/retrieval/reading stages | VERIFIED | P2's deterministic context manifest and temporal/provenance dimensions are compatible methodological translations | No benchmark reproduction or score claim | AION does not claim LongMemEval parity | KEEP_RESEARCH_ONLY |
| `LIT-MEMORYAGENTBENCH-2025` | [MemoryAgentBench, arXiv:2507.05257][8] | The benchmark defines accurate retrieval, test-time learning, long-range understanding and selective forgetting as memory-agent competencies | VERIFIED | Keep retrieval and exclusion behavior separately inspectable | No autonomous learning or forgetting mechanism is added | No AION benchmark result | KEEP_RESEARCH_ONLY |
| `LIT-MEMEVOBENCH-2026` | [MemEvoBench, arXiv:2604.15774][9] | The paper describes long-horizon memory safety under adversarial injection, noisy tool output and biased feedback | VERIFIED | P2/P3 contamination and provenance gates are compatible safety test classes | No MemEvoBench implementation or score is claimed | The authors' `first benchmark` wording is not adopted as an AION novelty claim | KEEP_RESEARCH_ONLY |
| `LIT-MEMORA-2026` | [Benchmarking Long-Term Memory for Personalized Agents / Memora benchmark, arXiv:2604.20006][10] | The benchmark spans weeks/months, evaluates remembering/reasoning/recommending, and defines FAMA to penalize obsolete memory | VERIFIED | P2 stale/superseded exclusion remains an inspectable falsifier class | No Memora reproduction or continuity result | The P2 source set must not conflate this benchmark with the separate Memora representation paper arXiv:2602.03315 | KEEP_RESEARCH_ONLY |
| `LIT-AGEMEM-2026` | [AgeMem, ACL 2026 Long Paper 981][11] | The paper exposes store/retrieve/update/summarize/discard as tool-based memory operations and reports benchmark results | VERIFIED | Use explicit operation taxonomy for governed memory research | No autonomous memory authority is adopted | External agent autonomy is not AION authority | KEEP_RESEARCH_ONLY |
| `LIT-AMP-2026` | [Agent-Memory Protocol, PMLR 317][12] | AMP describes redact-at-rest, pack-for-purpose and hydrate-on-return at a memory/model privacy boundary | VERIFIED | Purpose-bound context packaging is a design reference | No AION privacy guarantee or protocol implementation | “Guarantee” remains the paper's protocol claim, not AION evidence | KEEP_RESEARCH_ONLY |
| `LIT-PROVO-2013` | [W3C PROV-O Recommendation][13] | PROV-O defines Entity/Activity/Agent and provenance relations including derivation, attribution, revision and invalidation | VERIFIED | P2 local relation vocabulary is PROV-inspired | No PROV-O/RDF/OWL conformance or serializer is claimed | Local vocabulary is analogy, not standards conformance | KEEP_RESEARCH_ONLY |
| `LIT-MCP-2026` | [MCP 2026-07-28 official release note][14] | The release describes a stateless protocol core and explicit application handles for state carried across calls | VERIFIED | P2 keeps state at its application research layer and avoids hidden transport state | No MCP server, transport or integration is implemented | Protocol architecture is external context only | KEEP_RESEARCH_ONLY |

## 3. Kimi external-project crosswalk

| ID | Primary repository / source | Intake proposition | Label | Safe AION use | Disposition |
|---|---|---|---|---|---|
| `EXT-AURA` | [youngbryan97/aura][15] | The README describes a functional cognitive-architecture research project, explicit non-claims, causal internal-state hypotheses, receipts, negative results and reproducibility limits | VERIFIED for repository self-description; PARTIAL for individual experiment claims | Methodological comparator for evidence discipline; no code copied | KEEP_RESEARCH_ONLY |
| `EXT-TCAS` | [scottdhughes/TCAS][16] | The README separates behavioral, perturbation, observer and mechanistic streams and withholds credence when O-stream is missing | VERIFIED | Comparator for evidence separation and withheld inference | KEEP_RESEARCH_ONLY |
| `EXT-CONSCIOUSNESS-AI` | [venturaEffect/the_consciousness_ai][17] | The repository describes a speculative architecture and reports open/failed results while warning that metrics are instruments, not proof | PARTIAL / VERIFIED for explicit speculative framing | Taxonomy and negative-control stimulus only | KEEP_RESEARCH_ONLY |
| `EXT-QUALIA-SIMULATOR` | [gulla0/Qualia-Simulator][18] | The README explicitly describes subjective/qualia architecture as speculative and unknown, with sensorimotor/self-model/memory modules | VERIFIED for speculative framing; ANALOGY for taxonomy | Taxonomy only; no qualia implementation or claim | KEEP_RESEARCH_ONLY |
| `EXT-AISYSTESTING` | [gcjordi/AIsysTesting][19] | Intake describes a consciousness/security question-and-answer assessment pattern | HOLD / CORRECTION_REQUIRED | Do not cite scoring or license until source artifacts are reviewed | HOLD |
| `EXT-AIWARE` | `JeltzProstetnic/aIware` primary source not completed in this cycle | Intake describes self-model/self-other ablation and transfer-style methodology | HOLD / CORRECTION_REQUIRED | Discovery lead only | HOLD |
| `EXT-MRIVAS` | `mrivasperez/consciousness` primary source not completed in this cycle | Intake describes a warning that conversation text is not direct evidence and a presuppositional-framing confound | HOLD / CORRECTION_REQUIRED | Do not repeat until the repository page and artifacts are checked | HOLD |
| `EXT-ATOM` | Redirected `KushalLimbasiya/Base-of-Self-Aware-AI` / current `atom` | Intake describes an intent-classification voice-assistant architecture used as a negative taxonomy example | HOLD / CORRECTION_REQUIRED | Preserve as unresolved discovery lead; no self-aware label inference | HOLD |

## 4. Required separation

The crosswalk separates four layers that must not be collapsed:

| Layer | Meaning in this repository |
|---|---|
| Academic/external existing work | What authors of papers, standards or repositories report under their own methods and limitations |
| AION engineering | Bounded code, fixtures, validators and governance surfaces created in this repository |
| AION integration | Actual repository links that are implemented and tested; P2 ↔ AION Runtime v0.2 remains explicitly non-integrated |
| Possible new contribution | A `NOVELTY_HYPOTHESIS` only after systematic related-work search, exact provenance, independent replication and separated review |

No row in this crosswalk establishes subjectivity, consciousness, identity continuity, moral status, legal status, canonical authority, deployment readiness or first/only/unprecedented status for AION.

## References

[1]: https://arxiv.org/html/2607.11881v1 "Metacognition in LLMs"
[2]: https://ojs.aaai.org/index.php/AAAI/article/view/34723 "Decoupling Metacognition from Cognition"
[3]: https://openreview.net/forum?id=qTXlFwlggv "Language Models Are Capable of Metacognitive Monitoring and Control of Their Internal Activations"
[4]: https://arxiv.org/abs/2602.07594 "Learning to Self-Verify Makes Language Models Better Reasoners"
[5]: https://arxiv.org/html/2502.14565v1 "ReVISE"
[6]: https://arxiv.org/abs/2602.01146 "PersistBench"
[7]: https://arxiv.org/abs/2410.10813 "LongMemEval"
[8]: https://arxiv.org/abs/2507.05257 "MemoryAgentBench"
[9]: https://arxiv.org/abs/2604.15774 "MemEvoBench"
[10]: https://arxiv.org/abs/2604.20006 "Benchmarking Long-Term Memory for Personalized Agents"
[11]: https://aclanthology.org/2026.acl-long.981/ "Agentic Memory / AgeMem"
[12]: https://proceedings.mlr.press/v317/wu26a.html "Agent-Memory Protocol"
[13]: https://www.w3.org/TR/prov-o/ "PROV-O"
[14]: https://blog.modelcontextprotocol.io/posts/2026-07-28/ "MCP 2026-07-28"
[15]: https://github.com/youngbryan97/aura "Aura repository"
[16]: https://github.com/scottdhughes/TCAS "TCAS repository"
[17]: https://github.com/venturaEffect/the_consciousness_ai "The Consciousness AI repository"
[18]: https://github.com/gulla0/Qualia-Simulator "Qualia-Simulator repository"
[19]: https://github.com/gcjordi/AIsysTesting "AIsysTesting repository"
