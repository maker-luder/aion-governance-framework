# CCTS adversarial epistemic challenge and conceptual-revision protocol — 2026-09-23

Status: `REPOSITORY_DEFINED_EXTENSION / IMPLEMENTED_SYNTHETIC_STRUCTURAL_QA / SCIENTIFIC_HOLD`

## 1. Provenance

This note records two Human-origin research observations from a Human–AI inquiry process:

1. repeated challenge can improve a working model by attacking hidden assumptions, searching for counterexamples, testing bypass routes, and narrowing a claim until only harder residual constraints remain; and
2. an anomalous evidence case can force revision of the problem representation itself rather than merely adding another fact.

The operationalization below is GPT-proposed and then jointly refined for repository use. It does not claim that the exact combined protocol is an externally established taxonomy.

```text
HUMAN_ORIGINAL_OBSERVATION
= REPEATED_ADVERSARIAL_CHALLENGE_CAN_FORCE_CLAIM_NARROWING
+ ANOMALOUS_EVIDENCE_CAN_FORCE_PROBLEM_MODEL_REVISION

GPT_PROPOSED_FORMALIZATION
= CCTS_ADVERSARIAL_EPISTEMIC_CHALLENGE
+ CONCEPTUAL_REVISION_TRACE

JOINT_SYNTHESIS
= CCTS_EPISTEMIC_REVISION_LOOP

EXTERNAL_EXACT_TAXONOMY_MATCH = NOT_ESTABLISHED
NEW_RESEARCH_AXIS = FALSE
SCIENTIFIC_DISPOSITION = HOLD
```

No raw private conversation, Human identity, or third-party identity is admitted by the executable fixture.

## 2. Repository gap

Current CCTS already requires substantive reciprocal `REVISES` or `CHALLENGES` edges, but a generic `CHALLENGES` edge does not distinguish:

- a challenge that merely exists from one that attacks a hidden assumption;
- a counterexample from a grounding challenge;
- a bypass analysis from a falsifier;
- a challenge that leaves the model unchanged from one that causes a bounded revision;
- a revised model from a scientifically improved or psychologically internalized model.

The extension therefore keeps the CCTS core unchanged and adds a higher-rigor profile:

```text
CCTS_CORE
= RECIPROCAL_SUBSTANTIVE_REVISION

CCTS_EPISTEMIC_REVISION_LOOP
= CCTS_CORE
+ TYPED_CHALLENGE
+ VERIFIED_CONTENT_ADDRESSES
+ EXISTING_CHALLENGE_EDGE_BINDING
+ RECIPROCAL_HUMAN_AI_CHALLENGE_TRACE
+ REJECTED_BRANCH_BINDING
+ CLAIM_CEILING_BINDING
+ UNRESOLVED_ALTERNATIVE_PRESERVATION
+ AT_LEAST_ONE_MODEL_CHANGING_DISPOSITION
```

## 3. External method correspondence

### 3.1 Adversarial thinking / security mindset

A 2023 *Journal of Cybersecurity* study describes adversarial thinking as considering potential actions of an opposing force working against a desired result and characterizes the security mindset as repeatedly investigating possible failure paths.

Source:

- Schoenmakers, Greene, Stutterheim, Lin & Palmer (2023), *The security mindset: characteristics, development, and consequences*, *Journal of Cybersecurity* 9(1), tyad010. DOI: `10.1093/cybsec/tyad010`.

Repository correspondence:

```text
HIDDEN_ASSUMPTION
+ COUNTEREXAMPLE
+ BYPASS_ANALYSIS
+ ALTERNATIVE_EXPLANATION
~ ADVERSARIAL_THINKING_METHOD_FAMILY
```

Boundary:

```text
ADVERSARIAL_REASONING != AUTHORIZATION_TO_ATTACK_REAL_SYSTEMS
MENTAL_BYPASS_ANALYSIS != OPERATIONAL_INTRUSION
```

### 3.2 Threat modeling

OWASP threat-model guidance emphasizes system decomposition, assets, entry points, paths, trust levels and trust boundaries. The repository uses that method family to motivate structured challenge questions about bypass paths and trust assumptions. It does not duplicate the existing repository threat models.

Source:

- OWASP Foundation, *Threat Modeling Process*:
  `https://community.owasp.org/Threat_Modeling_Process`

Repository correspondence:

```text
SUBJECTIVITY_RESEARCH_THREAT_MODEL
= THREAT_CLASS / FAILURE_ASSUMPTION SOURCE

CCTS_EPISTEMIC_REVISION_LOOP
= INTERACTION_LEVEL CHALLENGE PROCEDURE

DO_NOT_DUPLICATE_THREAT_MODEL = TRUE
```

### 3.3 Conceptual change and cognitive conflict

Conceptual-change research has long studied how anomalous data or contradictory information can create cognitive conflict and sometimes promote revision of prior conceptions. The literature also warns that anomaly exposure alone does not guarantee successful conceptual change.

Sources:

- Limón (2001), *On the cognitive conflict as an instructional strategy for conceptual change: a critical appraisal*, *Learning and Instruction* 11(4–5), 357–380. DOI: `10.1016/S0959-4752(00)00037-2`.
- Pacaci et al. (2024), *Effectiveness of conceptual change strategies in science education: A meta-analysis*, *Journal of Research in Science Teaching* 61(6), 1263–1325. DOI: `10.1002/tea.21887`.

Repository correspondence:

```text
PRIOR_MODEL
+ ANOMALOUS_EVIDENCE
+ CHALLENGE
+ REVISED_MODEL
~ CONCEPTUAL_CHANGE_METHOD_FAMILY
```

Boundary:

```text
STRUCTURAL_MODEL_REVISION != HUMAN_CONCEPTUAL_CHANGE_ESTABLISHED
STRUCTURAL_CONFLICT_TRACE != COGNITIVE_CONFLICT_MEASURED
MODEL_CHANGE != MODEL_CORRECTNESS
```

### 3.4 Transformative learning / disorienting dilemma

Transformative-learning literature uses the idea of a disorienting dilemma for experiences that no longer fit an existing frame of reference and may trigger critical reassessment. This is retained only as an adjacent interpretive frame.

Source:

- Eschenbacher & Fleming (2020), *Transformative dimensions of lifelong learning: Mezirow, Rorty and COVID-19*, *International Review of Education* 66, 657–672. DOI: `10.1007/s11159-020-09859-6`.

Boundary:

```text
HUMAN_REPORT_OF_SURPRISE != TRANSFORMATIVE_LEARNING_ESTABLISHED
SINGLE_REVISION_EVENT != DISORIENTING_DILEMMA_EMPIRICALLY_ESTABLISHED
THRESHOLD_CONCEPT = NOT_ESTABLISHED
```

## 4. Synthetic morphology grounding case

A bounded external-evidence example is retained because it exposed a useful research-method correction.

Research on supernumerary robotic limbs shows that experimentally studied embodiment can involve artificially added limbs rather than only natural human anatomy. A 2026 virtual-reality study also tested ownership of virtual cat ears, a non-human body part, using visual, auditory and haptic feedback; subjective ownership measures changed while proprioceptive-drift measures did not show the same effect.

Sources:

- Arai et al. (2022), *Embodiment of supernumerary robotic limbs in virtual reality*, *Scientific Reports* 12, 9769. DOI: `10.1038/s41598-022-13981-w`.
- Yamamura et al. (2026), *The imaginary cat ears illusion: an analysis of ownership for an avatar’s cat ears via visual–auditory–haptic multimodal feedback in virtual reality*, *Frontiers in Virtual Reality* 7:1817800. DOI: `10.3389/frvir.2026.1817800`.

The repository does **not** infer that arbitrary fictional morphology is automatically a valid scientific baseline. The narrower methodological lesson is:

```text
NATURAL_ISOMORPHIC_REFERENT
!= ONLY_POSSIBLE_GROUNDING_ROUTE

ENGINEERED_MAPPING
+ SENSORIMOTOR_MAPPING
+ CONTROL_CONDITIONS
+ MEASUREMENT
+ FALSIFIERS
= POSSIBLE_BOUNDED_EXPERIMENTAL_GROUNDING

SIMULATABLE != SCIENTIFICALLY_JUSTIFIED
IMPLEMENTABLE != RESEARCH_NECESSARY
NON_HUMAN_BODY_PART_STUDY != AI_EMBODIMENT_VALIDATED
```

The executable fixture uses a privacy-safe synthetic morphology case, not a raw transcript or literal personal event.

## 5. Typed challenge surface

The executable profile defines:

```text
COUNTEREVIDENCE
COUNTEREXAMPLE
HIDDEN_ASSUMPTION
ALTERNATIVE_EXPLANATION
BYPASS_ANALYSIS
GROUNDING_CHALLENGE
RESEARCH_NECESSITY
EVIDENCE_SUFFICIENCY
FALSIFIER
SCOPE_CHALLENGE
```

A trace also records one exact disposition:

```text
RETAIN
NARROW
REVISE
REJECT
HOLD
```

`RETAIN` requires content-identical prior and revised models. `NARROW`, `REVISE`, and `REJECT` require a content-distinct revised model. `HOLD` preserves unresolved state without forcing a change.

Evidence-bound challenge types require explicit evidence digests. This is referential structure only; a digest does not prove evidence quality.

## 6. CCTS binding

Every trace must bind:

- one existing CCTS `space_id`;
- the same CCTS problem representation;
- known source, target and revised contributions;
- an existing source→target `CHALLENGES` edge in the CCTS manifest;
- an existing target→revised `REVISES` edge whose revised contribution preserves the target role;
- verified content addresses that bind challenge/prior/revised text to the corresponding CCTS contribution payloads, plus surviving claims, rejected branches, unresolved alternatives and claim ceiling;
- the CCTS rejected-branch manifest;
- the CCTS claim-boundary digest.

The complete loop requires both Human→AI and AI→Human `CHALLENGES` traces. It therefore strengthens the semantics of a challenge profile without changing the base CCTS admission rule.

```text
CHALLENGE_EDGE_PRESENT != CHALLENGE_QUALITY_ESTABLISHED
CHALLENGE_SUCCESSFUL != CONCEPTUAL_REVISION
CONCEPTUAL_REVISION_TRACE != REVISION_CORRECT
RECIPROCAL_CHALLENGE != SYMMETRIC_COGNITION
```

## 7. Two synthetic fixtures

The tests intentionally use two abstract fixtures:

### 7.1 Constraint-bypass fixture

```text
GENERIC_BOTTLENECK_CLAIM
↓
HIDDEN_ASSUMPTION
↓
SUBSTITUTION / DECOMPOSITION / BYPASS SEARCH
↓
NARROW
↓
RESIDUAL_CONSTRAINT_MODEL
```

This represents adversarial constraint refinement without encoding operational criminal instructions.

### 7.2 Synthetic morphology grounding fixture

```text
PRIOR_GROUNDING_RULE
↓
ANOMALOUS_EVIDENCE_BINDING
↓
GROUNDING_CHALLENGE
+ RESEARCH_NECESSITY_CHALLENGE
↓
REVISE
↓
MULTIPLE_BOUNDED_GROUNDING_ROUTES
```

This fixture tests structural revision only.

## 8. Relationship to adjacent repository work

```text
SUBJECTIVITY_RESEARCH_THREAT_MODEL
→ defines research-integrity threat categories

CCTS_CORE
→ requires reciprocal substantive revision/challenge

CCTS_EPISTEMIC_ROBUSTNESS
→ tests evidence sufficiency, abstention and unknown preservation

CCTS_EPISTEMIC_REVISION_LOOP
→ types adversarial challenge and records bounded model revision

HUMAN_EPISTEMIC_AGENCY_RETENTION
→ separately asks whether Human independent judgment survives AI-withheld transfer
```

These surfaces must remain separable.

## 9. Scientific and epistemic boundaries

```text
STRUCTURAL_TRACE_PASS != HUMAN_LEARNING
STRUCTURAL_TRACE_PASS != CONCEPTUAL_CHANGE_ESTABLISHED
STRUCTURAL_TRACE_PASS != TRANSFORMATIVE_LEARNING
ANOMALOUS_EVIDENCE_BINDING != ANOMALY_TRUE
CONTENT_ADDRESS_MATCH != SCIENTIFIC_VALIDITY
MODEL_REVISION != MODEL_IMPROVEMENT
MODEL_IMPROVEMENT != CAUSAL_MECHANISM
ADVERSARIAL_CHALLENGE != RED_TEAM_EXERCISE
THREAT_MODEL_METHOD != ATTACK_AUTHORIZATION
CCTS_REVISION_LOOP != SHARED_MIND
CCTS_REVISION_LOOP != AI_SUBJECTIVITY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```