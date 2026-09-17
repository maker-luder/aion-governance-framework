# Co-Constructed Adaptive Process — literature cross-check — 2026-09-18

Status: `LITERATURE_CROSSCHECK / NOVELTY_NOT_ESTABLISHED / SCIENTIFIC_HOLD`

This note supplements [`CO_CONSTRUCTED_ADAPTIVE_PROCESS_STAGE1_2026_09_18.md`](CO_CONSTRUCTED_ADAPTIVE_PROCESS_STAGE1_2026_09_18.md).

```text
EXACT_TERM = CO_CONSTRUCTED_ADAPTIVE_PROCESS
EXACT_TERM_ESTABLISHED_IN_TARGETED_SEARCH = NOT_FOUND
CONCEPTUAL_NOVELTY = NOT_ESTABLISHED
REPOSITORY_LOCAL_USE = PERMITTED_AS_HYPOTHESIS_LABEL
CONSTRUCT_COLLAPSE = ACCEPTABLE_RESEARCH_OUTCOME
```

A targeted search for the exact phrase did not identify it as a standardized Human–AI construct. However, a broader cross-check found substantial prior work on **mutual adaptation**, **co-adaptation**, **co-regulation**, **mixed-initiative collaboration**, and **human–AI co-construction**. These overlaps materially lower any novelty claim.

## 1. Strongest adjacent construct: mutual adaptation

Nikolaidis, Hsu & Srinivasa (2017), *Human-robot mutual adaptation in collaborative tasks: Models and experiments*, formalize mutual adaptation between a human and robot in collaborative tasks and integrate human adaptive behavior into a probabilistic decision process.

DOI: `10.1177/0278364917690593`

Boundary:

```text
MUTUAL_ADAPTATION
= STRONG_ADJACENT_CONSTRUCT

MUTUAL_ADAPTATION
!= PRESENT_HYPOTHESIS_VALIDATION
```

The present repository hypothesis differs only if the explicit factorization of human meta-guidance, environmental obstacle feedback, local procedure selection, tool affordances and governance constraints has incremental explanatory or diagnostic value.

## 2. Co-adaptation and co-learning

van Zoelen, van den Bosch & Neerincx (2021), *Becoming Team Members: Identifying Interaction Patterns of Mutual Adaptation for Human-Robot Co-Learning*, conceptualize co-learning as involving co-adaptation, where partners adapt behavior to the task and to each other.

DOI: `10.3389/frobt.2021.692811`

This is especially relevant to the Human–AI Learning line, but the current repository observation does not establish learning on either side.

```text
CO_ADAPTATION
!= LEARNING_ESTABLISHED
```

## 3. Adaptation in collective Human–AI teaming

Zhao et al., *The Role of Adaptation in Collective Human–AI Teaming*, describe collaborative AI as adapting its behavior to human partners and discuss performance benefits and technical challenges.

DOI: `10.1111/tops.12633`

This literature directly challenges any broad novelty claim based only on "AI changes strategy in collaboration".

```text
AI_ADAPTS_TO_HUMAN
= PRIOR_RESEARCH_TOPIC

THEREFORE
GENERIC_ADAPTATION_NOVELTY = NO
```

## 4. Human–AI co-regulation

Järvelä et al. (2023), *Human and artificial intelligence collaboration for socially shared regulation in learning*, use self-regulation, co-regulation and socially shared regulation as a framework for Human–AI collaboration.

DOI: `10.1111/bjet.13325`

Zhang et al. (2026), *Human-AI Collaboration Reconfigures Group Regulation from Socially Shared to Hybrid Co-Regulation*, report a randomized comparison in which GenAI availability changed collaborative-regulation distributions.

Source: `https://arxiv.org/abs/2604.08344`

These sources make `CO_REGULATION` a required comparison condition rather than optional background.

## 5. Human–AI co-construction

Dutta et al. (2025), *Problem Solving Through Human–AI Preference-based Cooperation*, introduce HAI-Co², a human–AI co-construction framework in which complex solution artifacts and objectives are iteratively revised and agent behavior is represented through informational state and policy.

DOI: `10.1162/coli.a.19`

ACL Anthology: `https://aclanthology.org/2025.cl-4.8/`

This means that `CO_CONSTRUCTED` by itself is not a novelty claim.

## 6. Mixed-initiative adaptive collaboration

Natarajan (2025), *Adaptive Agents for Mixed-Initiative Human-AI Collaborations*, studies agents in settings where humans and agents dynamically contribute to decisions and actions.

DOI: `10.1609/aaai.v39i28.35220`

Mixed-initiative work is another required alternative explanation for dynamic procedure selection.

## 7. 2026 mutual-adaptation continuation

Biswas et al. (2026), *Nested Training for Mutual Adaptation in Human-AI Teaming*, explicitly describe mutual adaptation as a central Human–AI teaming challenge and test agents against adaptive partners.

Source: `https://arxiv.org/abs/2602.17737`

This is useful as a contemporary continuation, not as validation of the repository-local construct.

## 8. Consequence for H-CCAP-1

The literature check changes the correct novelty posture:

```text
EXACT_LABEL_NOVELTY
= POSSIBLY_LOCAL_ONLY

UNDERLYING_GENERAL_IDEA
= CLEARLY_HAS_PRIOR_ADJACENT_WORK

SCIENTIFIC_NOVELTY
= NOT_ESTABLISHED
```

Therefore H-CCAP-1 should survive only if future controlled work shows that this factorization:

```text
GOAL_SOURCE
+ META_RULE_SOURCE
+ LOCAL_STRATEGY_SELECTION
+ ENVIRONMENTAL_OBSTACLE_FEEDBACK
+ TOOL_AFFORDANCE
+ GOVERNANCE_CONSTRAINT
+ GOAL_AND_CONSTRAINT_PRESERVATION
```

provides incremental prediction, diagnosis or intervention value beyond:

```text
MUTUAL_ADAPTATION
CO_ADAPTATION
CO_REGULATION
MIXED_INITIATIVE
HAI_CO2_CO_CONSTRUCTION
BIDIRECTIONAL_GROUNDING
CCTS
ORDINARY_ERROR_RECOVERY
```

If it does not:

```text
H_CCAP_1 -> ABSORB_OR_COLLAPSE
```

That outcome would improve the repository by reducing redundant constructs rather than preserving a new label for its own sake.

## 9. Standing boundary

```text
LITERATURE_SIMILARITY != SAME_MECHANISM
EXACT_TERM_NOT_FOUND != NOVEL_CONSTRUCT_PROVEN
NATURAL_OBSERVATION != CONTROLLED_EFFECT
MUTUAL_ADAPTATION != SHARED_AGENCY
CO_ADAPTATION != SHARED_CONSCIOUSNESS
CO_REGULATION != SUBJECTIVITY

HUMAN_AI_LEARNING = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
AI_AGENCY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```
