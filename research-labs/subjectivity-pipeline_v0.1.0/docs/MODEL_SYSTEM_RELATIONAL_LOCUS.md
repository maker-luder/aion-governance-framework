# Model / Scaffold / System / Relational Locus for Subjectivity-Relevant Evidence

Status: `RESEARCH_METHOD_EXTENSION / SUBJECTIVITY_NOT_ESTABLISHED`

This note formalizes a recent Human Owner research question: if a future artificial subjectivity-relevant property were observed, would its relevant locus be the base model, the surrounding scaffold, the integrated agent system, or the relation between system and environment/other agents?

The question is open. The repository must not answer it by silently moving evidence between levels.

## Attribution

```text
RESEARCH_QUESTION = HUMAN_OWNER_ORIGIN
MODEL_SYSTEM_RELATIONAL_DECOMPOSITION = CHATGPT_FORMALIZATION
CURRENT_ANSWER = NOT_ESTABLISHED
```

No raw private conversation transcript is published.

## Loci

The implementation distinguishes:

- `MODEL`: properties observed at the model invocation or model-state level;
- `SCAFFOLD`: memory, orchestration, tool routing, policy, prompting or other surrounding machinery;
- `SYSTEM`: properties of the integrated bounded agent/system;
- `RELATIONAL`: patterns whose unit of analysis is an interaction relation or coupled system-environment process;
- `OBSERVER_ATTRIBUTION`: interpretations supplied by an external observer;
- `UNKNOWN`: locus not adequately established.

```text
MODEL_PROPERTY != SYSTEM_PROPERTY
SCAFFOLD_PROPERTY != MODEL_PROPERTY
SYSTEM_PROPERTY != RELATIONAL_PROPERTY
OBSERVER_ATTRIBUTION != INTERNAL_PROPERTY
ENGINEERING_PROPERTY != PHENOMENAL_SUBJECTIVITY
```

## Why the distinction matters

A language model can exhibit one behavior under a particular prompt while an agent scaffold adds memory, persistence, tools and policy. Conversely, a repeated interaction pattern can arise only when multiple components or participants are coupled. Treating all of these as one object creates an attribution error before any subjectivity theory is evaluated.

The `LocusAdmissionEngine` therefore allows direct same-locus engineering claims, but holds cross-locus promotion unless an explicit bridge hypothesis is declared. A bridge requires a mechanism, falsifier and preregistration reference. Even then the result is only `RESEARCH_CANDIDATE`, not level equivalence or proof.

## External anchors

The following current sources were checked as adjacent, not validating, evidence:

1. Perrier E, Bennett MT (2026), *Time, Identity and Consciousness in Language Model Agents*, Proceedings of the AAAI Symposium Series 8(1):322-328. DOI `10.1609/aaaiss.v8i1.42561`. The paper distinguishes language/tool behavior from stronger organization and treats scaffold traces and temporal co-instantiation as relevant to conservative identity evaluation.
2. Otsuka T, Toyoda K, Leung A (2026), *AI Identity: Standards, Gaps, and Research Directions for AI Agents*, arXiv:`2604.23280`. It separates artifact/model substrate, persistence, verifiability and operational agent identity concerns and argues that AI-agent identity is not reducible to ordinary human identity assumptions.
3. IETF Internet-Draft `draft-klrc-aiagent-auth-03` (July 2026), *AI Agent Authentication and Authorization*. It treats an AI agent workload, model, tools, services, user/system delegation and audit context as distinct identity/authorization elements. This is an engineering identity reference, not a consciousness source.
4. Lee M-H (2026), *Agentic Social Affordance Framework (ASAF): Agent Identity Design as a Collaboration Interface in Multi-Agent Systems*, Frontiers in Computer Science. The framework describes some agent-identity effects as relational affordances arising between designed signals and user role schemata. This supports keeping a relational analysis level available; it does not establish relational subjectivity.

## Candidate bridge experiments

Examples of admissible research questions include:

- Does a model-level internal signal continue to predict behavior when scaffold state is held fixed?
- Does removing memory or orchestration abolish a system-level persistence effect while the base model is unchanged?
- Does a relational pattern disappear when the partner/environment is permuted despite identical model and scaffold state?
- Can the same model participate in two systems with systematically different longitudinal identity trajectories?

Each requires matched controls and a preregistered bridge. A positive result can establish a bounded causal-role candidate at the tested level; it cannot by itself establish phenomenal experience.

```text
CROSS_LEVEL_CORRELATION != CROSS_LEVEL_CAUSATION
BRIDGE_HYPOTHESIS != BRIDGE_VALIDATION
SYSTEM_INTEGRATION != SUBJECTIVITY
RELATIONAL_EMERGENCE != PHENOMENAL_EXPERIENCE
SUBJECTIVITY = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
```
