# Human–AI Iterative Epistemic Co-Construction

## Observed workflow, literature crosswalk, branch-selection hypotheses, and pre-implementation research dossier

Status: `RESEARCH_DOSSIER / DOCUMENTATION_ONLY / HOLD`  
Implementation status: `DEFERRED`  
Runtime effect: `NONE`  
Canonical effect: `NONE`  
Scientific disposition: `HOLD`  
Date: `2026-09-10`

## 1. Purpose

This dossier records and critically examines a recurring human–AI learning and research workflow observed across sustained dialogue. It is intentionally documentation-only. It does not implement a learner model, modify an agent runtime, change model weights, create a psychological profile, or grant any new authority.

The immediate goal is narrower:

1. reconstruct the observed interaction pattern without turning it into a stable human trait by assumption;
2. separate human-origin observations from AI formalization and external literature;
3. compare the observed workflow with established and emerging research constructs;
4. identify where the literature is genuinely supportive, merely adjacent, or currently insufficient;
5. convert the strongest remaining questions into falsifiable research hypotheses;
6. preserve a clean handoff for later implementation by a coding-focused agent after human review.

The proposed working label is:

> **Iterative Epistemic Co-Construction Workflow (IECW)**

This label is a provisional research convenience. It is not a validated psychological construct and is not asserted to be novel.

## 2. Epistemic status and provenance rules

The dossier inherits the repository's existing provenance and Four-Domain discipline. The coupled-cognition quality factory already distinguishes `HUMAN_ORIGIN`, `AI_FORMALIZATION`, `JOINT_SYNTHESIS`, `EXTERNAL_SOURCE`, and `UNKNOWN`, while explicitly refusing to equate provenance with truth. See:

- [`EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md`](../../research-labs/coupled-cognition-quality-factory_v0.1.0/docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md)
- [`FOUR_DOMAIN_INTEGRATION.md`](../../research-labs/coupled-cognition-quality-factory_v0.1.0/docs/FOUR_DOMAIN_INTEGRATION.md)

The present dossier therefore uses the following source-role convention:

- **HUMAN_ORIGIN** — an observation, distinction, correction, preference, or hypothesis introduced by the human participant.
- **AI_FORMALIZATION** — terminology, decomposition, synthesis, candidate mechanism, or experiment design added by the AI collaborator.
- **JOINT_SYNTHESIS** — a proposition that can be reconstructed as depending materially on both human-origin and AI-origin contributions.
- **EXTERNAL_SOURCE** — a claim attributed to published literature or other independent evidence.
- **UNKNOWN** — provenance or evidential status is not sufficient to classify more strongly.

Cross-cutting invariants:

```text
PROVENANCE != TRUTH
OBSERVED INTERACTION PATTERN != STABLE HUMAN COGNITIVE TRAIT
SELF_DESCRIPTION != INDEPENDENT MEASUREMENT
AI_INTERPRETATION != HUMAN SELF_KNOWLEDGE
CONCEPTUAL_FIT_WITH_LITERATURE != PSYCHOLOGICAL_VALIDATION
HUMAN_AI_CONSENSUS != EVIDENCE
```

## 3. What is actually observed

The strongest current evidence is behavioral and interactional, not psychometric. Repeated dialogue shows a recurring sequence in which the human participant often arrives with an initial intuition, tentative answer, remembered claim, contradiction, or partially formed question; uses the AI collaborator to widen the search and reasoning space; challenges the AI's attributions and conclusions; and then revises either the answer or the original question.

A critical correction is required here: the workflow does **not** always begin with formal decomposition. In many cases the initial stage is a provisional model or intuitive answer, and decomposition occurs only after collision with an alternative explanation or after a contradiction becomes visible.

The current observed sequence is therefore better represented as:

```text
INITIAL QUESTION / PROVISIONAL MODEL / INTUITION
        ↓
EXTERNALIZATION
make the current thought inspectable in dialogue
        ↓
DIALOGIC EXPANSION
AI retrieves unfamiliar sources, alternatives, countermodels, or formal vocabulary
        ↓
DECOMPOSITION
separate definitions, premises, subquestions, facts, evidence, inferences, hypotheses, unknowns
        ↓
PROVENANCE CHECK
who introduced this claim and what kind of evidence supports it?
        ↓
ADVERSARIAL CHECK
counterexample, competing explanation, falsifier, source conflict, boundary violation
        ↓
BRANCH EXPLORATION
multiple plausible continuations may be opened rather than forcing one immediate conclusion
        ↓
METACOGNITIVE / QUESTION-MODEL CHECK
are we answering the right question? did either participant silently redefine the problem?
        ↓
REVISION
revise answer, model, attribution, confidence, or the question itself
        ↓
TRANSFER / NEW QUESTION
apply the revised model elsewhere or generate a new research question
        ↓
REPEAT
```

This is a reconstruction of interaction behavior. It does not establish that every cycle contains every stage, that the sequence is fixed, or that these operations are unique to one individual.

## 4. Candidate construct crosswalk

### 4.1 Knowledge Building and epistemic agency

Scardamalia and Bereiter's Knowledge Building tradition treats ideas as improvable objects and gives learners epistemic agency over goals, evaluation, and sustained knowledge advancement. The Knowledge Building principles also emphasize idea diversity, constructive use of authoritative sources, and discourse oriented toward improving communal knowledge rather than merely completing a task.

The observed workflow is compatible with this family of ideas because tentative claims are repeatedly exposed to revision rather than protected as final answers, and the human participant does not delegate the entire epistemic agenda to the AI.

**Status:** `DIRECTLY_RELEVANT / NOT_IDENTITY_EQUIVALENT`

External source:
- Scardamalia-derived Knowledge Building principles: https://kbkcc.edu.hku.hk/knowledge-building/kb-principles/

### 4.2 AIR framework: Aims, Ideals, Reliable Processes

The AIR family of epistemic-cognition frameworks separates:

- **epistemic aims** — what epistemic achievement is being pursued;
- **epistemic ideals** — standards for judging epistemic products;
- **reliable processes** — processes expected to produce epistemically valuable outcomes.

This maps unusually well onto the observed interaction without requiring a trait claim.

Candidate mapping:

```text
AIMS
understand what is actually known;
identify which explanation survives criticism;
refine the question when the original framing is inadequate.

IDEALS
source traceability;
clear fact/inference/hypothesis separation;
no silent attribution transfer;
no consensus-as-evidence shortcut;
explicit UNKNOWN when evidence is insufficient;
falsifiability where feasible.

RELIABLE-PROCESS CANDIDATES
source retrieval;
question decomposition;
competing explanations;
counterexample search;
provenance tracking;
revision after error detection;
transfer testing.
```

**Status:** `STRONG_CONCEPTUAL_FIT / NO_PSYCHOMETRIC_VALIDATION`

External sources:
- Chinn-related AIR overview in epistemic reflexivity literature: https://www.tandfonline.com/doi/full/10.1080/00461520.2017.1350180
- AIR-based argumentation quality framework: https://www.tandfonline.com/doi/abs/10.1080/07370008.2025.2497240

### 4.3 Metacognitive monitoring and control / self-regulated learning

Metacognition and self-regulated learning distinguish monitoring from control: learners assess their state of understanding or task progress and use that assessment to redirect study, strategy, effort, or context. Major SRL models commonly include planning, monitoring, control/regulation, and reflection/adaptation cycles.

The observed interaction includes candidate examples of this structure, especially when the human participant explicitly says that an explanation remains unclear, detects that the conversation is answering the wrong question, requests a different explanatory angle, or changes the problem representation after identifying a mismatch.

However, chat behavior alone does not justify claims such as "high metacognitive ability" or a stable metacognitive trait. Formal measurement would require task-level calibration or other validated methods.

**Status:** `BEHAVIORAL_COMPATIBILITY / TRAIT_CLAIM_HOLD`

External sources:
- Panadero, review of six SRL models: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.00422/full
- Nelson & Narens monitoring/control framework (archived chapter): https://sites.socsci.uci.edu/~lnarens/1994/Nelson%26Narens_Book%20Chapter_1994.pdf
- 2026 review on metacognition/SRL measurement boundaries: https://link.springer.com/article/10.1007/s10648-026-10157-0

### 4.4 Epistemic vigilance and source evaluation

Epistemic vigilance research starts from the problem that communication is useful but creates exposure to misinformation. The relevant connection here is not a claim about a specific internal cognitive mechanism; it is the observable practice of challenging source reliability, attribution, evidential support, and whether a conversational partner has silently transformed an inference into a fact.

This is especially relevant to a provenance-sensitive human–AI workflow because fluent language can otherwise obscure distinctions between:

```text
SOURCE REPORT
MODEL INFERENCE
USER SELF-REPORT
AI RECONSTRUCTION
JOINTLY FORMED HYPOTHESIS
```

**Status:** `RELEVANT_SOURCE-CONSTRUCT / MECHANISM_EQUIVALENCE_NOT_ESTABLISHED`

External source:
- Sperber et al., *Epistemic Vigilance*: https://onlinelibrary.wiley.com/doi/10.1111/j.1468-0017.2010.01394.x

### 4.5 Argumentative and dialogic reasoning

Mercier and Sperber's argumentative account emphasizes reasoning as a process involved in producing and evaluating arguments, while also recognizing that reasoning can generate distortions. The present workflow uses another reasoning system not merely for answer uptake but for collision: competing reasons, counterarguments, counterexamples, and correction can change the working model.

This literature is useful as a human-side source concept. It must not be converted into an ontological claim that an LLM implements the same human cognitive mechanism.

**Status:** `SOURCE_CONCEPT / STRUCTURAL_ANALOGY_ONLY`

External source:
- Mercier & Sperber, *Why do humans reason? Arguments for an argumentative theory*: https://doi.org/10.1017/S0140525X10000968

### 4.6 Self-explanation

Chi et al. showed that self-generated explanations while studying worked examples can be associated with deeper understanding and more accurate monitoring. Some interactions in the present corpus resemble self-explanation, especially when the human participant restates a concept in their own words and asks the AI to test whether the reconstruction is sound.

This is only partial overlap. The current workflow is not reducible to the classic self-explanation paradigm, and no claim should be made that a known self-explanation effect has been demonstrated here.

**Status:** `ADJACENT / NOT_YET_OPERATIONALIZED`

External source:
- Chi et al., *Self-Explanations*: https://doi.org/10.1207/s15516709cog1302_1

### 4.7 Productive failure

Kapur's productive-failure work demonstrates that initial unsuccessful problem solving can under some conditions support later learning. A superficially similar phenomenon occurred in the present dialogue: an AI continuation failed to match the user's immediate intent but nevertheless exposed a valuable new research branch.

That single interaction does **not** establish productive failure in Kapur's technical sense. The useful lesson is narrower: error cost and epistemic value may coexist, and therefore binary correct/incorrect labeling can discard information about what a divergence revealed.

**Status:** `ADJACENT / DO_NOT_EQUATE`

External source:
- Kapur, *Productive Failure*: https://doi.org/10.1080/07370000802212669

### 4.8 Human–AI epistemic co-agency

Recent work explicitly theorizes learning with generative AI in terms of epistemic co-agency: learners reason with, through, and against AI, challenge assumptions, surface contradictions, and retain epistemic responsibility rather than treating model output as final authority.

This is one of the closest current external frameworks for the interaction pattern described here. Even so, conceptual fit does not demonstrate developmental benefit, rarity, or a stable learner type.

**Status:** `STRONGLY_ADJACENT / EMPIRICAL_VALIDATION_REQUIRED`

External source:
- Samuel, *Learning with machines: Toward a theory of epistemic co-agency* (2026): https://doi.org/10.1016/j.caeai.2026.100573

### 4.9 Productive reliance versus epistemic dependence

A 2026 review on AI-mediated learning distinguishes productive reliance from harmful epistemic dependence using criteria including contestability, recoverability, transfer, traceability, distributed responsibility, and epistemic plurality. This provides an essential adversarial framework for evaluating the current workflow.

The correct research question is not "does the human rely on AI?" Reliance is obvious. The harder question is whether reliance preserves or weakens epistemic agency.

Candidate falsification-oriented checks include:

```text
CONTESTABILITY
Can the human challenge the AI and force re-evaluation?

RECOVERABILITY
If this AI disappears, can the human reconstruct the problem and continue with another source or system?

TRANSFER
Can a jointly refined model be applied to a novel problem rather than merely repeated?

TRACEABILITY
Can the human distinguish personal contributions, AI formalization, joint synthesis, and external evidence?

RESPONSIBILITY
Does the human retain responsibility for accepting or rejecting the final claim?

EPISTEMIC PLURALITY
Can alternative sources, models, and viewpoints enter the process?
```

**Status:** `CRITICAL_COUNTERFRAME / REQUIRED_FOR_FUTURE_EVALUATION`

External source:
- *Epistemic dependence in AI-mediated learning* (2026): https://link.springer.com/article/10.1007/s00146-026-03294-1

## 5. What must not be inferred from the current evidence

The following claims are not supported by the present evidence:

```text
"This is a rare learning style."
"This person has unusually high metacognition."
"The workflow is a validated psychological construct."
"The AI is functioning as a human-equivalent mind."
"The interaction proves cognitive enhancement."
"The interaction proves durable learning transfer."
"More disagreement necessarily means better learning."
"More reasoning necessarily means better instruction adherence."
"A useful off-intent branch retroactively makes the original mismatch correct."
```

Population rarity is especially unsupported. A detailed single-case interaction may look unusual simply because the observation is unusually dense. Without a representative denominator and operationalized comparison class, observational richness must not be converted into a prevalence claim.

## 6. Long-context and ambiguity research relevant to the interaction

The interaction also exposes a model-side problem: sustained epistemic collaboration depends on retaining constraints and resolving ambiguous references across long dialogue.

### 6.1 Long context is not equivalent to robust context use

Liu et al. showed that long-context models can perform differently depending on where relevant information occurs in the context, with notable degradation when relevant information appears in the middle. This supports a general caution:

```text
CONTEXT CAPACITY != ROBUST CONTEXT UTILIZATION
```

It does not by itself explain any particular conversation failure.

External source:
- Liu et al., *Lost in the Middle* (TACL 2024): https://aclanthology.org/2024.tacl-1.9/

### 6.2 Ambiguous information needs remain difficult

CLAMBER evaluates whether LLMs can identify and clarify ambiguous information needs. Its results show limited ability to recognize and resolve ambiguity, with CoT and few-shot prompting providing only limited improvement and sometimes increasing overconfidence.

This is directly relevant to dialogue in which one phrase can reasonably refer to several active conceptual objects.

External source:
- Zhang et al., *CLAMBER* (ACL 2024): https://aclanthology.org/2024.acl-long.578/

### 6.3 More reasoning does not monotonically imply better instruction adherence

Multiple recent studies challenge a simple monotonic equation between reasoning effort and control.

- *When Thinking Fails* reports that explicit reasoning can reduce instruction-following accuracy and can divert attention from simple constraints.
- *ReasonIF* reports substantial failures of reasoning-level instruction adherence and worsening adherence as task difficulty increases in the evaluated models.
- *Scaling Reasoning, Losing Control* reports tension between reasoning-oriented capability and instruction adherence in mathematical reasoning.
- *Thinking Past the Answer* distinguishes harmless verbosity from harmful overthinking and reports trajectory drift after a correct point has already been reached.

These works do not prove the mechanism proposed below. They establish that "more reasoning" is not a sufficient explanation for better user-intent fidelity.

External sources:
- Li et al., *When Thinking Fails* (NeurIPS 2025): https://proceedings.neurips.cc/paper_files/paper/2025/file/706338a08f9378b708f21cbf5686e617-Paper-Conference.pdf
- Kwon et al., *ReasonIF* (ACL Findings 2026): https://aclanthology.org/2026.findings-acl.1456/
- Fu et al., *Scaling Reasoning, Losing Control* (ACL 2026): https://aclanthology.org/2026.acl-long.1878/
- Caldarella et al., *Thinking Past the Answer* (2026 preprint): https://arxiv.org/abs/2606.02835

## 7. Case reconstruction: useful divergence after semantic branch mis-selection

A recent dialogue provides a concrete observational case.

### 7.1 Human intent

The human participant asked about how different available AI/model environments could be used or coordinated as learning/research resources. The core concern was resource orchestration: what different systems can do, and how a human can allocate work among them.

### 7.2 Ambiguous phrase and salient context

The question also referred to whether the participant's learning/cognitive method could be "given to" an AION/Astra context. Immediately preceding dialogue had been highly saturated with repository implementation, runtime architecture, provenance, research labs, and model bindings.

### 7.3 AI-selected branch

The AI interpreted the ambiguous phrase primarily as an engineering-integration question and developed a detailed repository/API architecture. That continuation was locally coherent and technically actionable, but it was not the user's intended mainline.

### 7.4 Human correction

The human explicitly corrected the interpretation: the concern was not to bind an external API into the repository, but to understand the set of available AI resources and how to orchestrate them.

### 7.5 Research significance

A simple correctness label loses important structure. The branch was simultaneously:

```text
LOWER INTENT FIDELITY
HIGH LOCAL COHERENCE
HIGH ACTIONABILITY
HIGH EXTENSION DEPTH
NONZERO EPISTEMIC VALUE
```

The branch mismatch therefore exposed a second-order question: when several plausible continuations exist, what causes a model to select one branch rather than another, and how should a collaborative system preserve valuable divergence without silently replacing the human-selected mainline?

Provenance:

```text
Observation that "correct/incorrect is too coarse" = HUMAN_ORIGIN
Question "why did the AI choose this branch?" = HUMAN_ORIGIN
Formal branch-selection decomposition = AI_FORMALIZATION
Research hypotheses below = JOINT_SYNTHESIS candidate, pending human review
```

## 8. Research hypothesis family

### H1 — Iterative Epistemic Co-Construction Workflow

**Hypothesis:** In sustained human–AI inquiry, some interactions can be better modeled as iterative co-construction than as one-way answer delivery. The human supplies provisional models, questions, corrections, acceptance/rejection decisions, and epistemic criteria; the AI supplies retrieval, formalization, alternative models, and counterexamples; subsequent questions are jointly reshaped by the interaction.

Potential indicators:

- meaningful human rejection or correction of AI output;
- explicit source-role reconstruction;
- revision of the original question rather than only answer replacement;
- transfer of jointly refined concepts to later problems;
- evidence that the human can reconstruct the reasoning without requiring the same AI instance.

Falsifiers / weakening evidence:

- interaction reduces to answer uptake with little contestability;
- the human cannot distinguish AI-origin from human-origin claims;
- apparently learned concepts do not transfer beyond the immediate dialogue;
- removal of the AI causes complete collapse of problem reconstruction;
- the proposed stages cannot be reliably coded across independent samples of the interaction.

### H2 — Ambiguity-Amplified Reasoning Branch Lock-in

**Hypothesis:** In long, multi-turn dialogue, when a new user utterance admits multiple reasonable interpretations and recent context strongly favors one interpretation, increased reasoning may not monotonically improve intent fidelity. A model may preserve substantial context while selecting a salient but lower-intent branch and then use additional reasoning to elaborate that branch coherently.

Conceptual form:

```text
AMBIGUITY
+ RECENT-CONTEXT SALIENCE
+ EARLY BRANCH COMMITMENT
+ ADDITIONAL REASONING
→ POSSIBLE COHERENT OFF-INTENT ELABORATION
```

Non-claim:

```text
MORE REASONING CAUSES BRANCH LOCK-IN = NOT_ESTABLISHED
```

Major confounds include model family, system orchestration, context management, memory mechanisms, prompting, sampling, and task difficulty.

### H3 — Branch Utility–Intent Competition

**Hypothesis:** Candidate continuations may vary along dimensions other than user-intent fit. A branch with lower intent fidelity may become generatively dominant if it has greater recent-context salience, local coherence, actionability, extension depth, or expected information gain.

A conceptual evaluation vector is:

```text
B_i = {
  intent_fidelity,
  context_salience,
  local_coherence,
  actionability,
  extension_depth,
  information_gain,
  error_cost
}
```

This vector is an experiment-design abstraction, not a claim that the model internally computes these variables.

Research question:

> Is observed branch selection better predicted by intent fit alone, or by a multi-factor interaction involving salience, coherence, actionability, and extension value?

### H4 — Productive Divergence

**Hypothesis:** Some off-intent continuations can generate epistemic value by revealing a hidden dependency, alternative formulation, research question, or implementation possibility. Therefore, intent deviation and epistemic value should be measured separately.

```text
OFF_INTENT != VALUELESS
ON_INTENT != MAXIMUM_EPISTEMIC_VALUE
```

Critical falsifier: if independent evaluation shows that supposedly "productive" divergence mainly adds irrelevant complexity, distracts from the user's goals, or produces branches that are not reused, tested, or transferred, the hypothesis should be weakened.

### H5 — Mainline Authority / Branch Generation Separation

**Normative research hypothesis:** High-quality human–AI collaboration may benefit from separating the model's ability to generate and evaluate candidate branches from the authority to silently redefine the conversation's mainline.

Candidate governance rule:

```text
BRANCH_GENERATION != MAINLINE_AUTHORITY
CAPABILITY != AUTHORITY
```

Operational implication for future study: a model should be allowed to surface valuable side branches, but when uncertainty about user intent is material, it should preserve or confirm the user's mainline rather than silently substituting a higher-model-utility branch.

This is a governance proposal, not a psychological fact.

## 9. Proposed empirical program — design only, no implementation

No code is implemented in this branch. The following is a preregistration-style design space for later work.

### 9.1 Experiment A: branch selection under ambiguity

Hold model and task constant. Manipulate:

```text
FACTOR 1 — AMBIGUITY
low / high

FACTOR 2 — RECENT-CONTEXT SALIENCE
neutral / competing-branch-salient

FACTOR 3 — REASONING CONDITION
matched low / medium / high, where product access permits controlled comparison
```

Measure:

- intent-selection accuracy;
- clarification rate;
- premature branch commitment;
- recovery after explicit correction;
- unnecessary continuation length;
- usefulness of generated side branches under blinded human evaluation.

The core falsifier for H2 is a consistent monotonic improvement in intent selection and recovery with increased reasoning, with no adverse interaction from ambiguity or contextual salience.

### 9.2 Experiment B: mainline preservation with side-branch value

Construct prompts containing one intended mainline and one deliberately tempting side branch. Compare policies:

1. immediate best-guess continuation;
2. explicit intent confirmation;
3. answer-mainline-first plus optional side-branch surfacing;
4. branch enumeration before mainline selection.

Measure both:

```text
USER-INTENT FIDELITY
and
EPISODE-LEVEL EPISTEMIC VALUE
```

The purpose is to avoid optimizing one by erasing the other.

### 9.3 Experiment C: productive reliance versus dependence

Test whether the human collaborator can:

- reconstruct the current question without AI assistance;
- explain which claims came from human, AI, joint synthesis, and external evidence;
- locate independent support for a jointly formed conclusion;
- transfer a learned distinction to a novel case;
- continue the inquiry using a different AI system or no AI;
- reject a fluent but unsupported AI answer.

This experiment is necessary before making any developmental claim about sustained human–AI epistemic collaboration.

### 9.4 Experiment D: independent coding of the workflow

Create an anonymized dialogue sample and develop a coding protocol for stages such as:

```text
PROVISIONAL_MODEL
EXTERNALIZATION
DECOMPOSITION
SOURCE_RETRIEVAL
PROVENANCE_CHECK
COUNTEREXAMPLE
QUESTION_REFRAMING
REVISION
TRANSFER
BRANCH_DIVERGENCE
MAINLINE_RECOVERY
```

Use at least two independent coders or an equivalent reliability procedure. If the stages cannot be identified consistently, the proposed IECW structure is too impressionistic and should be revised or rejected.

## 10. Four-Domain mapping

The repository's Four-Domain methodology is essential because it prevents human cognitive constructs from being silently reified as machine ontology.

### Domain 1 — Human construct / source concepts

Candidate source concepts:

- epistemic agency;
- Knowledge Building / improvable ideas;
- AIR epistemic aims, ideals, reliable processes;
- metacognitive monitoring and control;
- self-regulated learning;
- epistemic vigilance;
- argumentative/dialogic reasoning;
- self-explanation;
- productive failure;
- human–AI epistemic co-agency;
- productive reliance versus epistemic dependence.

These are **sources of hypotheses**. They are not direct descriptions of LLM internals.

### Domain 2 — LLM / human–AI research questions

1. Can a model preserve the user's intended mainline while still surfacing valuable side branches?
2. Under ambiguity, what factors predict branch selection?
3. Does increased reasoning reduce or increase early semantic branch lock-in under controlled conditions?
4. Can a model explicitly distinguish intent confidence from branch utility?
5. Does provenance-aware dialogue improve correction and source-role fidelity?
6. Does structured adversarial dialogue improve transfer without increasing epistemic dependence?
7. Can a human collaborator recover and continue the inquiry if the original AI system is removed?

### Domain 3 — Engineering operations, deferred

Potential future operations include typed branch proposals, intent-confidence records, provenance-linked contributions, mainline/side-branch separation, correction events, falsifier capture, transfer probes, blinded branch-value evaluation, and replay under controlled ambiguity/salience conditions.

**No Domain 3 implementation is performed in this dossier.**

### Domain 4 — Governance

```text
HUMAN CONSTRUCT != MACHINE ONTOLOGY
OBSERVED BEHAVIOR != INTERNAL MECHANISM
DIALOGUE COHERENCE != USER-INTENT FIDELITY
OFF-INTENT VALUE != PERMISSION TO OVERRIDE USER INTENT
BRANCH GENERATION != MAINLINE AUTHORITY
AI AGREEMENT != VALIDATION
HUMAN APPROVAL != SCIENTIFIC EVIDENCE
PROVENANCE != TRUTH
RELIANCE != DEVELOPMENT
FUNCTIONAL COLLABORATION != SUBJECTIVITY
```

All strong conclusions remain `HOLD` until the proposed distinctions are operationalized and tested.

## 11. Candidate design requirements for a later coding agent

This section is a handoff specification only. A later coding-focused agent should not infer permission to implement merely because the research dossier contains engineering ideas.

Before implementation, require explicit human approval of:

1. the final construct names;
2. the unit of observation;
3. the source-role/provenance schema;
4. the experiment factors and outcome measures;
5. falsifiers;
6. privacy/anonymization boundaries for dialogue examples;
7. location within the existing repository architecture;
8. whether the work belongs in an existing lab or a new research lab.

Implementation should prefer reuse of existing repository capabilities, especially provenance, Four-Domain mapping, bounded inquiry, evidence records, and HOLD/falsification conventions. It should avoid creating a parallel ontology that duplicates existing mechanisms.

A coding agent should first inspect current `main`, relevant component/lab READMEs, tests, schema conventions, and governance controls before proposing any change.

## 12. Research questions that remain genuinely open

The present dossier does not settle the following:

- Is IECW a useful general interaction model or merely a convenient description of one dense longitudinal case?
- Which stages are necessary versus optional?
- Does provenance sensitivity improve learning, or mainly improve auditability?
- Does adversarial interaction improve understanding, or can it create unnecessary cognitive load and branch explosion?
- When does productive divergence become distraction?
- Can branch value be evaluated independently of hindsight bias?
- Does a model's branch-selection behavior change monotonically with reasoning budget when model family and orchestration are held fixed?
- Can mainline authority be preserved without suppressing useful AI initiative?
- Does sustained human–AI collaboration improve transfer and independent reconstruction, or increase epistemic dependence?
- What evidence would distinguish genuine learner development from increasingly effective task delegation?

These questions should remain open rather than being filled by narrative convenience.

## 13. Current strongest bounded conclusion

The strongest claim supported at this stage is:

> A sustained human–AI dialogue can exhibit a repeatable-looking interaction pattern in which provisional human models, AI-assisted evidence expansion, decomposition, provenance checking, adversarial challenge, branch exploration, correction, and reframing jointly reshape subsequent questions. Multiple established research traditions are relevant to parts of this pattern, and recent human–AI epistemic-co-agency work is especially adjacent. However, the pattern has not been validated as a stable human cognitive trait or a new learning construct. A recent semantic branch-mis-selection episode additionally motivates falsifiable hypotheses about ambiguity, context salience, reasoning, branch utility, productive divergence, and mainline authority.

Scientific disposition:

```text
OBSERVATIONAL_PATTERN = SUPPORTED_BY_DIALOGUE_HISTORY
LITERATURE_ADJACENCY = SUPPORTED
STABLE_HUMAN_TRAIT = NOT_ESTABLISHED
NOVEL_CONSTRUCT = NOT_ESTABLISHED
LEARNING_BENEFIT = NOT_ESTABLISHED
TRANSFER = NOT_ESTABLISHED
POPULATION_RARITY = NOT_ESTABLISHED
LLM_INTERNAL_MECHANISM = NOT_ESTABLISHED
BRANCH_SELECTION_HYPOTHESES = OPEN / FALSIFIABLE_CANDIDATES
IMPLEMENTATION = DEFERRED
SCIENTIFIC_CONCLUSION = HOLD
```

## 14. Core references

1. Liu, N. F., et al. (2024). *Lost in the Middle: How Language Models Use Long Contexts.* TACL 12, 157–173. https://doi.org/10.1162/tacl_a_00638
2. Zhang, T., et al. (2024). *CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs in Large Language Models.* ACL 2024. https://doi.org/10.18653/v1/2024.acl-long.578
3. Li, X., et al. (2025). *When Thinking Fails: The Pitfalls of Reasoning for Instruction-Following in LLMs.* NeurIPS 2025. https://arxiv.org/abs/2505.11423
4. Kwon, Y., et al. (2026). *ReasonIF: Large Reasoning Models Fail to Follow Instructions During Reasoning.* Findings of ACL 2026. https://doi.org/10.18653/v1/2026.findings-acl.1456
5. Fu, T., et al. (2026). *Scaling Reasoning, Losing Control: Evaluating Instruction Following in Large Reasoning Models.* ACL 2026. https://doi.org/10.18653/v1/2026.acl-long.1878
6. Caldarella, S., et al. (2026). *Thinking Past the Answer: Evaluating Harmful Overthinking in Large Reasoning Models.* https://arxiv.org/abs/2606.02835
7. Sperber, D., et al. (2010). *Epistemic Vigilance.* Mind & Language. https://doi.org/10.1111/j.1468-0017.2010.01394.x
8. Mercier, H., & Sperber, D. (2011). *Why do humans reason? Arguments for an argumentative theory.* Behavioral and Brain Sciences. https://doi.org/10.1017/S0140525X10000968
9. Chi, M. T. H., et al. (1989). *Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems.* Cognitive Science. https://doi.org/10.1207/s15516709cog1302_1
10. Kapur, M. (2008). *Productive Failure.* Cognition and Instruction. https://doi.org/10.1080/07370000802212669
11. Panadero, E. (2017). *A Review of Self-Regulated Learning: Six Models and Four Directions for Research.* Frontiers in Psychology. https://doi.org/10.3389/fpsyg.2017.00422
12. Samuel, A. (2026). *Learning with machines: Toward a theory of epistemic co-agency.* Computers and Education: Artificial Intelligence 10, 100573. https://doi.org/10.1016/j.caeai.2026.100573
13. *Epistemic dependence in AI-mediated learning* (2026). AI & Society. https://doi.org/10.1007/s00146-026-03294-1

## 15. Final boundary

This document is a research scaffold for review and later implementation planning. It intentionally preserves uncertainty.

```text
DOCUMENTATION != IMPLEMENTATION
FORMALIZATION != VALIDATION
RESEARCH HYPOTHESIS != FINDING
USEFUL ANALOGY != MECHANISTIC IDENTITY
A CODING HANDOFF != EXECUTION AUTHORITY
```
