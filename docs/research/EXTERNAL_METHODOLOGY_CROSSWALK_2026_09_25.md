# External methodology crosswalk for the repository research workflow — 2026-09-25

Status: `RESEARCH_METHODS_CROSSWALK / DESCRIPTIVE / NOT_A_STANDARD_CLAIM`

Canonical effect: `NONE`

Deployment: `FALSE`

Scientific disposition: `HOLD`

## 1. Purpose

This document maps repository-local research and governance practices to established external methodology families.

It does **not** claim that the repository:

- conforms to every cited standard;
- has independently validated a new scientific method;
- has demonstrated that its integrated workflow is superior to alternatives;
- has established causality between workflow structure and platform / streaming reliability.

The purpose is narrower:

```text
LOCAL_WORKFLOW_RULE
-> EXTERNAL_METHOD_FAMILY
-> OVERLAP
-> NON_EQUIVALENCE
-> CURRENT_CLAIM_CEILING
```

This crosswalk is intended to reduce accidental reinvention, distinguish established components from local integration choices, and create a reviewable basis for later empirical testing.

## 2. Provenance

### 2.1 HUMAN_OWNER_ORIGIN

The Human Owner originated the request to compare the repository's evolved research process against external scientific methodology, academic practice, model-building practice, research-software practice and GitHub-based research governance.

The Human Owner also observed that the bounded workflow used during PR #210 appeared materially more stable than several earlier high-error sessions, and proposed fixing the workflow in a new PR so that it could be tested prospectively over time.

### 2.2 CHATGPT_TEACHER_FORMALIZATION

The ChatGPT Teacher proposed:

- an external methodology crosswalk;
- a bounded serial workflow model;
- explicit separation between workflow stability observation and causal attribution;
- a prospective repeated-session observation protocol;
- explicit confounders and falsifiers.

### 2.3 JOINT_SYNTHESIS

The Human Owner and ChatGPT Teacher jointly converged on the principle that the workflow should be frozen as a reviewable protocol before interpreting later observations.

```text
HUMAN_ORIGIN != AI_FORMALIZATION
AI_FORMALIZATION != JOINT_SYNTHESIS
JOINT_SYNTHESIS != EXTERNAL_VALIDATION
PROVENANCE != CORRECTNESS
```

## 3. External methodology families

### 3.1 FAIR4RS — FAIR Principles for Research Software

FAIR4RS applies Findable, Accessible, Interoperable and Reusable principles to research software while explicitly accounting for software-specific properties such as executability, composite structure, continuous evolution and versioning.

Primary reference:

- Research Data Alliance / FAIR4RS Working Group, FAIR Principles for Research Software v1.0:
  https://www.rd-alliance.org/wp-content/uploads/2022/03/FAIR4RS20principles20v1.0.pdf

Repository overlap includes:

- exact version / revision recording;
- explicit metadata;
- license / terms review;
- provenance;
- reusable research software and structured artifacts.

Boundary:

```text
FAIR4RS_ALIGNMENT != FAIR4RS_CONFORMANCE_CERTIFICATION
VERSIONING_PRACTICE != COMPLETE_REUSABILITY
LICENSE_METADATA != COMPLETE_RIGHTS_REVIEW
```

### 3.2 W3C PROV — provenance representation

W3C PROV provides a standardized model for representing entities, activities and agents involved in producing or influencing data or other artifacts.

Primary references:

- W3C PROV-O Recommendation:
  https://www.w3.org/TR/prov-o/
- W3C PROV overview:
  https://www.w3.org/TR/prov-overview/

Repository overlap includes:

- Human Owner / AI / external source role separation;
- source -> transformation -> result lineage;
- exact artifact / version references;
- explicit derivation and activity records;
- provenance used to support later audit.

Boundary:

```text
PROVENANCE != CORRECTNESS
PROVENANCE != IDENTITY_PROOF
PROVENANCE != SCIENTIFIC_VALIDATION
LOCAL_PROVENANCE_SCHEMA != W3C_PROV_IMPLEMENTATION
```

The current repository uses provenance concepts strongly but does not claim full W3C PROV ontology implementation.

### 3.3 NASEM — reproducibility, replicability and generalizability

The National Academies distinguishes:

- reproducibility: obtaining consistent computational results using the same input data, code, computational steps and analysis conditions;
- replicability: obtaining consistent results across studies addressing the same scientific question using newly obtained data;
- generalizability: applicability of results to other contexts or populations.

Primary reference:

- National Academies of Sciences, Engineering, and Medicine (2019), *Reproducibility and Replicability in Science*:
  https://www.nationalacademies.org/read/25303/chapter/3

Repository crosswalk:

```text
SAME_DATA + SAME_CODE + SAME_CONDITIONS
-> COMPUTATIONAL_REPRODUCIBILITY

NEW_DATA / NEW_RUN / NEW_STUDY
-> REPLICATION_EVIDENCE_CANDIDATE

NEW_PROVIDER / NEW_POPULATION / NEW_CONTEXT
-> GENERALIZABILITY_QUESTION
```

Boundary:

```text
ONE_RERUN != REPLICATION
REPRODUCIBLE != TRUE
REPLICATED != UNIVERSAL
GENERALIZABILITY != ASSUMED
```

### 3.4 ASME VVUQ — Verification, Validation and Uncertainty Quantification

VVUQ = Verification, Validation, and Uncertainty Quantification
（驗證、模型確認／效度檢驗、不確定性量化）

ASME distinguishes whether a computational model correctly implements its mathematical description from whether it adequately represents the relevant real-world application, while separately treating uncertainty.

Primary references:

- ASME VVUQ overview:
  https://www.asme.org/codes-standards/publications-information/verification-validation-uncertainty
- ASME VVUQ 1-2022:
  https://www.asme.org/codes-standards/find-codes-standards/verification-validation-and-uncertainty-quantification-terminology-in-computational-modeling-and-simulation

Repository crosswalk:

```text
CI / TEST / TYPECHECK / STATIC_ANALYSIS
-> GENERAL_SOFTWARE_QA_EVIDENCE

KNOWN_SOLUTION_OR_NUMERICAL_ERROR_CHECK
AGAINST_THE_MATHEMATICAL_MODEL
-> VVUQ_VERIFICATION_EVIDENCE_CANDIDATE

MODEL_TO_EMPIRICAL_REFERENCE_OR_MEASUREMENT_COMPARISON
-> VALIDATION_EVIDENCE_CANDIDATE

PARAMETER / NUMERICAL / MODEL-FORM VARIATION
-> UNCERTAINTY_QUESTION
```

ASME describes verification in computational modeling as checking the computational model against its mathematical description; its verification guidance includes numerical-error / known-solution procedures. Ordinary CI, linting, type checking, static analysis or generic unit tests can support software quality but do not automatically satisfy that VVUQ meaning of verification.

Critical local boundary:

```text
GENERAL_CI != ASME_VVUQ_VERIFICATION
SOFTWARE_TEST_PASS != NUMERICAL_VERIFICATION
LOCAL_TEST_PASS != REMOTE_CI_PASS
CI_PASS != SCIENTIFIC_VALIDATION
IMPLEMENTATION_EXISTS != IMPLEMENTATION_CORRECT
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
```

The repository does not claim ASME VVUQ certification.

### 3.5 Registered Reports / preregistration

Registered Reports review research questions, hypotheses, procedures and analysis plans before results are known. This reduces outcome-dependent flexibility and preserves the distinction between confirmatory and exploratory work.

Primary references:

- Center for Open Science:
  https://www.cos.io/initiatives/registered-reports
- Nature Human Behaviour Registered Reports:
  https://www.nature.com/nathumbehav/submission-guidelines/registeredreports

Repository overlap includes:

- preregistration;
- explicit expected outcomes;
- negative controls;
- falsifiers;
- pre-specified quality checks;
- separation of exploratory and confirmatory analyses.

Boundary:

```text
LOCAL_PREREGISTRATION != JOURNAL_REGISTERED_REPORT
PRE_SPECIFICATION != RESULT_VALIDITY
REGISTERED_HYPOTHESIS != CONFIRMED_HYPOTHESIS
```

### 3.6 UNESCO Open Science

UNESCO's 2021 Recommendation on Open Science emphasizes openness, transparency, accessibility, collaboration and reusable scientific knowledge / infrastructure.

Primary reference:

- UNESCO Recommendation on Open Science:
  https://www.unesco.org/en/legal-affairs/recommendation-open-science

Repository overlap includes:

```text
PUBLIC
TRANSPARENT
INSPECTABLE
AUDITABLE
CHALLENGEABLE
```

plus public source references, open repository artifacts and explicit provenance.

Boundary:

```text
PUBLIC != VALIDATED
OPEN != CORRECT
TRANSPARENT != BIAS_FREE
```

### 3.7 Research Software Engineering

RSE = Research Software Engineering
（研究軟體工程）

The Society of Research Software Engineering describes an RSE as combining professional software engineering expertise with an intimate understanding of research.

Primary reference:

- Society of Research Software Engineering:
  https://society-rse.org/about/

Repository overlap includes:

- version control;
- modular implementation;
- testing;
- CI;
- code review;
- research-aware software design;
- reproducible execution surfaces.

Boundary:

```text
GOOD_SOFTWARE_ENGINEERING != GOOD_SCIENCE_BY_ITSELF
RSE_PRACTICE != SCIENTIFIC_VALIDATION
ENGINEERING_RIGOR != EPISTEMIC_CERTAINTY
```


### 3.8 AI-assisted research workflow and provenance frameworks

A literature-layer review identified several neighboring frameworks and systems that more directly combine AI-assisted research, workflow orchestration, provenance, reproducibility, research software and human oversight.

These sources narrow the local novelty claim. They show that integrated Human–AI research workflows already exist as an active research area.

Selected neighboring work:

- Shao et al. (2025), **SciSciGPT: advancing human–AI collaboration in the science of science**, *Nature Computational Science*.
  - presents an open-source AI collaborator for scientific workflows;
  - emphasizes research prototyping, analytical workflows and reproducibility;
  - explicitly identifies transparency and balancing Human / AI contribution as open challenges.
  - Consensus record:
    https://consensus.app/papers/sciscigpt-advancing-human%E2%80%93ai-collaboration-in-the-shao-wang/bc63e2557cc353638ed6cb919e840090/

- Souza et al. (2025), **PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows**, IEEE eScience.
  - extends provenance modeling toward AI-agent interactions;
  - links prompts, responses, decisions and workflow outcomes;
  - explicitly targets transparency, traceability, reproducibility and reliability.
  - Consensus record:
    https://consensus.app/papers/provagent-unified-provenance-for-tracking-ai-agent-souza-gueroudji/5b969fd368015c8fbac1d8d80976a981/

- Chan (2026), **SHAPR: Operationalising Human-AI Collaborative Research Through Structured Knowledge Generation**, arXiv preprint.
  - proposes a Human-centred, AI-assisted research-software framework;
  - integrates iterative research cycles, evidence, traceability, version control and structured knowledge accumulation.
  - Peer-review status in this crosswalk: `PREPRINT`.
  - Consensus record:
    https://consensus.app/papers/shapr-operationalising-humanai-collaborative-research-chan/249284aad77a5b7280ad708d900cda61/

- Binkytė et al. (2026), **Inspectable AI for Science: A Research Object Approach to Generative AI Governance**, IEEE Security and Privacy Workshops.
  - treats AI interactions as inspectable research-process components;
  - records model configuration, prompts, outputs and provenance metadata;
  - emphasizes accountability and integrity-preserving provenance.
  - Consensus record:
    https://consensus.app/papers/inspectable-ai-for-science-a-research-object-approach-to-binkyt%C4%97-abuaddba/ecd690b3dab153fa9441b8aeddbc8138/

- Farshidi et al. (2026), **Advancing research software engineering with AI: a research framework**, *Automated Software Engineering*.
  - empirically analyzes 1,510 open-source research-software repositories;
  - combines software-engineering maturity, FAIR4RS indicators, AI integration, automation, testing and releases.
  - Consensus record:
    https://consensus.app/papers/advancing-research-software-engineering-with-ai-a-farshidi-bennin/f4e90883a0d85f4aa8adf0031ba3f56f/

- Suchikova et al. (2025), **GAIDeT (Generative AI Delegation Taxonomy): A taxonomy for humans to delegate tasks to generative artificial intelligence in scientific research and publishing**, *Accountability in Research*.
  - classifies AI delegation across research stages;
  - explicitly preserves Human oversight, accountability and research integrity;
  - includes a GitHub-based declaration tool for transparent delegation records.
  - Consensus record:
    https://consensus.app/papers/gaidet-generative-ai-delegation-taxonomy-a-taxonomy-for-suchikova-tsybuliak/d61c95655149576e8523539a64433d52/

- Strickland et al. (2026), **Talk Freely, Execute Strictly: Schema-Gated Agentic AI for Flexible and Reproducible Scientific Workflows**, arXiv preprint.
  - proposes schema-gated orchestration as an execution boundary;
  - separates conversational flexibility from deterministic / constrained execution;
  - identifies Human-in-the-loop control and transparency as required boundary properties.
  - Peer-review status in this crosswalk: `PREPRINT`.
  - Consensus record:
    https://consensus.app/papers/talk-freely-execute-strictly-schemagated-agentic-ai-for-strickland-vijeta/4eca28396c5a5686b9f550e1a46617c4/

Bounded implication:

```text
AI_ASSISTED_RESEARCH_WORKFLOW_FRAMEWORKS_EXIST = YES
AI_AGENT_PROVENANCE_FRAMEWORKS_EXIST = YES
AI_ASSISTED_RSE_FRAMEWORKS_EXIST = YES
HUMAN_OVERSIGHT_IN_AI_RESEARCH_WORKFLOWS_EXISTS_AS_A_RESEARCH_DIRECTION = YES
AI_RESEARCH_DELEGATION_TAXONOMIES_EXIST = YES
SCHEMA_GATED_AI_SCIENTIFIC_WORKFLOW_DESIGNS_EXIST = YES

OUR_WORKFLOW_IS_THE_FIRST_INTEGRATED_AI_RESEARCH_WORKFLOW = NO
OUR_WORKFLOW_IS_EQUIVALENT_TO_ANY_ONE_NEIGHBORING_FRAMEWORK = NO
COMPLETE_ONE_TO_ONE_EXTERNAL_EQUIVALENT = NOT_ESTABLISHED
LOCAL_NOVELTY = NOT_ESTABLISHED
```

These sources are treated as neighboring frameworks rather than retrospective proof of the repository method. They also show that the earlier crosswalk must not imply that AI-assisted workflow integration is absent from the literature.

## 4. Repository-method crosswalk

| Repository practice | Closest external method family | Bounded interpretation |
|---|---|---|
| exact commit SHA / branch / PR | RSE / version control / FAIR4RS | exact state identification |
| source / hash / lineage record | W3C PROV / FAIR4RS | provenance and derivation evidence |
| CI / Quality / CodeQL | RSE / software QA | engineering QA evidence; not ASME VVUQ verification by itself |
| `CI_PASS != SCIENTIFIC_VALIDATION` | local boundary consistent with VVUQ separation | generic CI success does not establish model validation |
| preregistration / expected outcome | Registered Reports | reduced outcome-dependent flexibility |
| falsification matrix / counterexamples | scientific methodology | explicit weakening / rejection criteria |
| same data + code rerun | NASEM reproducibility | computational reproducibility question |
| new data / new independent study | NASEM replicability | replication question |
| new provider / context / population | NASEM generalizability | transfer / applicability question |
| public repository + explicit sources | Open Science | transparency and inspectability |
| modular bounded work package | RSE / workflow engineering | scope and change control |
| exact-head Human Owner approval gate | local governance / change control | repository authority control, not a standard scientific inference rule |
| `READ -> DECIDE -> WRITE -> VERIFY` | RSE / incremental workflow discipline | local operational workflow pattern |
| session stability tracking | reliability / metascience-like self-observation | local operational research hypothesis |

## 5. What appears established versus local

```text
EXTERNAL_COMPONENTS
= WELL_ESTABLISHED_AS_SEPARATE_METHOD_FAMILIES

REPOSITORY_INTEGRATION
= LOCALLY_COMPOSED

INTEGRATED_COMBINATION_AS_A_SINGLE_NAMED_STANDARD
= NOT_ESTABLISHED

LOCAL_INTEGRATION
!= NEW_SCIENTIFIC_METHOD_PROVEN
```

The repository currently combines elements from:

```text
SCIENTIFIC_METHODOLOGY
+ COMPUTATIONAL_REPRODUCIBILITY
+ RESEARCH_SOFTWARE_ENGINEERING
+ PROVENANCE
+ MODEL_VVUQ
+ OPEN_SCIENCE
+ PREREGISTRATION
+ HUMAN_GOVERNANCE
```

The combination may be useful and may contain locally distinctive integration choices, but novelty requires separate literature review and empirical discrimination.

## 6. Bounded workflow currently under observation

The workflow stabilized during PR #210 is recorded as:

```text
LOCK_CURRENT_STATE
-> READ
-> IDENTIFY_ONE_ISSUE
-> DECIDE
-> WRITE_OR_ACT
-> VERIFY_LIVE_STATE
-> NEXT_GATE
```

Operational preferences:

```text
ONE_ACTIVE_PR_PER_REVIEW_LANE = PREFERRED
PHASE_SEPARATION = PREFERRED
READ_BEFORE_RETRY = TRUE
VERIFY_AFTER_WRITE = TRUE
EXACT_STATE_CHECKPOINTING = REQUIRED_FOR_CRITICAL_TRANSITIONS
```

This workflow is a **local operational hypothesis**, not an externally validated causal intervention.


### 6.1 Review-cycle convergence gate

The repository review workflow uses a bounded convergence rule so that review tooling does not become an uncontrolled recursive loop.

```text
ROUND_1
= BROAD_PIPELINE_REVIEW

ROUND_1
-> CORRECTIONS
-> TEACHER_REVIEW

IF TEACHER_REVIEW = PASS
-> HUMAN_REVIEW_STAGE

IF TEACHER_REVIEW = MATERIAL_DEFECT_FOUND
-> ROUND_2_FINAL_PIPELINE_REVIEW
-> CORRECTIONS
-> TEACHER_FINAL_REVIEW
```

A single review cycle MUST NOT automatically invoke more than two complete pipeline rounds.

```text
MAX_FULL_PIPELINE_ROUNDS_PER_REVIEW_CYCLE = 2
```

If a material defect remains after the second pipeline round and Teacher final review:

```text
ROUND_3_AUTOMATIC_RETRY = PROHIBITED

DISPOSITION
= HOLD
| DEFER
| RE_SCOPE
| REDESIGN_PROTOCOL
```

A later third pipeline run is permitted only as a **new review cycle** after the unresolved problem has been explicitly re-scoped or the protocol has materially changed. It must not be represented as a continuation of the exhausted two-round cycle.

```text
REVIEW_EXHAUSTION != APPROVAL
TOOL_REPETITION != INDEPENDENT_EVIDENCE
MORE_REVIEW_ROUNDS != AUTOMATICALLY_HIGHER_QUALITY
```

This is a local workflow-governance rule. It is not claimed as an externally standardized scientific method and is intentionally kept separate from the pilot's preregistered primary exposure classification.

## 7. Claim ceiling

```text
WORKFLOW_IS_EXTERNALLY_STANDARDIZED_AS_ONE_METHOD = NOT_ESTABLISHED
WORKFLOW_IMPROVES_STREAMING_STABILITY = NOT_ESTABLISHED
WORKFLOW_CAUSES_LOWER_ERROR_RATE = NOT_ESTABLISHED
PLATFORM_ROOT_CAUSE = NOT_ESTABLISHED

EXTERNAL_METHOD_COMPONENT_OVERLAP = SUPPORTED
LOCAL_INTEGRATION_EXISTS = YES
PROSPECTIVE_TESTING_IS_JUSTIFIED = YES
```

## 8. Next evidence step

The next step is not to strengthen the claim.

It is to prospectively record eligible research sessions under a predefined observation protocol and test whether apparent stability persists while tracking alternative explanations.

See:

- `RESEARCH_SESSION_STABILITY_OBSERVATION_PROTOCOL_2026_09_25.md`

