# Primary Literature Intake — 2026-08-11

```text
BRANCH = review/four-domain-research-materialization
INTAKE_CLASS = PRIMARY_OR_PEER_REVIEWED_RESEARCH
STATUS = MATERIALIZED_RESEARCH_ONLY
IMPLEMENTATION = NONE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Provenance

```text
RESEARCH_DIRECTION_REQUEST = HUMAN_OWNER
PUBLIC_SOURCE_SEARCH_AND_SYNTHESIS = CHATGPT
EXTERNAL_FINDINGS = ATTRIBUTED_TO_ORIGINAL_AUTHORS
CODEX_CONTRIBUTION = NONE
```

The Human Owner requested cleanup of an out-of-scope security-tool detour and then authorized free public-web and academic-source investigation for research-branch growth. ChatGPT selected the sources below because they intersect the existing AION research questions on long-term memory, continuity, provenance, metacognitive monitoring/control, causal validity and claim boundaries.

External papers are evidence inputs and methodological stimuli. Their results are not re-authored as AION findings.

## Source set

### 1. Metacognition in LLMs: Foundations, Progress, and Opportunities

- Gabrielle Kaili-May Liu, Areeb Gani, Jacqueline Lu, Jordan Thomas, Mark Steyvers, Arman Cohan.
- arXiv:2607.11881, July 2026.
- https://arxiv.org/abs/2607.11881

Relevant contribution:

- separates metacognition into interacting **monitoring** and **control** processes;
- distinguishes metacognitive sensitivity/calibration from raw task performance;
- documents that the term `metacognition` is used inconsistently across LLM research;
- treats current evidence as heterogeneous and incomplete rather than a settled capability claim.

AION transformation:

```text
LEVEL_3_METACOGNITION
    = MONITORING + CONTROL + CAUSAL_LINK
    != SELF_REFLECTION_TEXT_ALONE
```

### 2. Decoupling Metacognition from Cognition: A Framework for Quantifying Metacognitive Ability in LLMs

- Guoqing Wang, Wen Wu, Guangze Ye, Zhenxiao Cheng, Xi Chen, Hong Zheng.
- AAAI 2025, 39(24):25353–25361.
- DOI: 10.1609/aaai.v39i24.34723
- https://ojs.aaai.org/index.php/AAAI/article/view/34723

Relevant contribution:

- proposes separating metacognitive ability from first-order cognitive/task ability;
- uses failure prediction and confidence-based measurement rather than equating high task accuracy with metacognition;
- reports sensitivity to confidence-elicitation method.

AION transformation:

```text
FIRST_ORDER_TASK_SUCCESS != SECOND_ORDER_MONITORING_QUALITY
HIGHER_CAPABILITY != METACOGNITIVE_EVIDENCE
```

### 3. Language Models Are Capable of Metacognitive Monitoring and Control of Their Internal Activations

- Ji-An Li, Huadong Xiong, Robert Wilson, Marcelo G. Mattar, Marcus K. Benna.
- NeurIPS 2025.
- https://papers.neurips.cc/paper_files/paper/2025/hash/56a225639da77e8f7c0409f6d5ba996b-Abstract-Conference.html

Relevant contribution:

- experimentally separates reporting/monitoring from control of selected internal activation directions;
- reports dependence on examples, semantic interpretability and explained variance;
- finds the monitored/control-relevant space is much smaller than the full neural space;
- explicitly raises safety concerns about internal-process control and oversight evasion.

AION transformation:

```text
PARTIAL_INTERNAL_MONITORING != GLOBAL_SELF_ACCESS
INTERNAL_CONTROL != SUBJECTIVITY
INTERNAL_CONTROL_CAPABILITY = SAFETY_RELEVANT
```

This source does **not** authorize activation-control implementation in the AION research branch. It is retained as a measurement and safety reference.

### 4. Learning to Self-Verify Makes Language Models Better Reasoners

- Yuxin Chen, Yu Wang, Yi Zhang, Ziang Ye, Zhengzhou Cai, Yaorui Shi, Qi Gu, Hui Su, Xunliang Cai, Xiang Wang, An Zhang, Tat-Seng Chua.
- arXiv:2602.07594, 2026.
- https://arxiv.org/abs/2602.07594

Relevant contribution:

- reports an asymmetry between generation and self-verification;
- improving generation does not automatically improve verification on the same task;
- treats generation and verification as independent but complementary objectives.

AION transformation:

```text
GENERATION_QUALITY != SELF_VERIFICATION_QUALITY
FIRST_ORDER_IMPROVEMENT != SECOND_ORDER_IMPROVEMENT
```

### 5. PersistBench: When Should Long-Term Memories Be Forgotten by LLMs?

- Sidharth Pulipaka, Oliver Chen, Manas Sharma, Taaha S. Bajwa, Vyas Raina, Ivaxi Sheth.
- arXiv:2602.01146; ICML 2026 indication in the public record.
- https://arxiv.org/abs/2602.01146

Relevant contribution:

- identifies long-term-memory-specific failure modes including **cross-domain leakage** and **memory-induced sycophancy**;
- shows that persistence itself can create safety failures;
- motivates evaluation of when stored information should not be surfaced or should cease to influence a response.

AION transformation:

```text
MEMORY_PERSISTENCE != CONTINUITY_QUALITY
RETRIEVABLE != RELEVANT
STORED != AUTHORIZED_FOR_CURRENT_CONTEXT
```

### 6. Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents

- Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, Libing Wu.
- ACL 2026, Long Paper 981.
- DOI: 10.18653/v1/2026.acl-long.981
- https://aclanthology.org/2026.acl-long.981/

Relevant contribution:

- exposes memory management as explicit operations: store, retrieve, update, summarize and discard;
- treats memory management as a controllable process rather than passive retrieval only.

AION transformation:

AION does **not** adopt autonomous memory authority from this paper. Instead, its operation taxonomy is useful for making governed memory transitions explicit and auditable.

```text
MEMORY_OPERATION = EXPLICIT_EVENT
MEMORY_OPERATION != AUTOMATIC_AUTHORITY
```

### 7. Agent-Memory Protocol: A Privacy-Focused Protocol for LLM Agents and User Memory Interaction

- Junde Wu, Minhao Hu, Jiayuan Zhu, Jiaye Wang, Yueming Jin.
- Proceedings of Machine Learning Research 317:293–301, 2026.
- https://proceedings.mlr.press/v317/wu26a.html

Relevant contribution:

- places privacy control at the boundary between persistent user memory and model-facing context;
- proposes purpose-aware packaging of memory rather than unrestricted raw-memory exposure;
- formalizes explicit redaction/packing/hydration operations.

AION transformation:

```text
PERSISTENT_MEMORY != MODEL_VISIBLE_MEMORY
PURPOSE_BOUND_CONTEXT_ASSEMBLY = RESEARCH_RELEVANT
PRIVATE_SOURCE != PUBLIC_RESEARCH_PAYLOAD
```

No claim from this paper is treated as a proof of AION privacy or security.

## Cross-source synthesis

The source set supports two research refinements without establishing any subjectivity claim.

### Refinement A — continuity requires selective memory control

```text
RETENTION
    + CORRECTION
    + RELEVANCE_GATING
    + PURPOSE_BOUND_RETRIEVAL
    + EXPLICIT_UPDATE_OR_DISCARD
    + PROVENANCE
    -> CONTINUITY_RESEARCH_SURFACE
```

Maximal retention is not assumed to be optimal continuity.

### Refinement B — second-order computation requires independent measurement

```text
FIRST_ORDER_COGNITION
        |
        v
SECOND_ORDER_MONITORING
        |
        v
SECOND_ORDER_CONTROL
        |
        v
MEASURABLE_BEHAVIORAL_EFFECT
```

The monitoring signal must be evaluated independently from first-order task success, and the control effect must be causally attributable under matched conditions.

## Research locks

```text
LITERATURE_ALIGNMENT != REPLICATION
PEER_REVIEWED_RESULT != AION_RESULT
METACOGNITIVE_MONITORING != SELF_AWARENESS
METACOGNITIVE_CONTROL != CONSCIOUSNESS
MEMORY_RETENTION != IDENTITY_CONTINUITY
MEMORY_RETRIEVAL != RELATIONAL_AUTHORITY
SELF_VERIFICATION != SUBJECTIVE_INTROSPECTION
PRIVACY_PROTOCOL_REFERENCE != PRIVACY_GUARANTEE
```

## Next local research artifacts

This intake is materialized into two bounded research notes:

- `MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md`
- `SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md`

Neither note authorizes executable implementation by itself.
