# Discovery–Construction Distinction in AI Alignment Research

Status: `PROVISIONAL_RESEARCH_JUDGMENT / NOT_VALIDATED / CANONICAL_EFFECT=NONE`
Date: `2026-09-10`

This note records a bounded research judgment arising from a Human Owner observation and subsequent GPT formalization. It is not a finding that any organization is scientifically invalid, deceptive, or unsafe, and it does not establish that any alternative alignment paradigm is superior.

```text
RESEARCH_DIRECTION = USER_ORIGINAL
FORMALIZATION = GPT_PROPOSED
EXTERNAL_EVIDENCE = ANTHROPIC_PRIMARY_SOURCES
SCIENTIFIC_STATUS = PROVISIONAL_RESEARCH_JUDGMENT
CANONICAL_EFFECT = NONE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
ALIGNMENT_SUPERIORITY = NOT_ESTABLISHED
```

## Core distinction

A training intervention can empirically demonstrate that a model becomes more likely to produce behavior consistent with a predefined normative target, including on held-out or out-of-distribution evaluations. That result does not by itself establish how a normative state arose, whether the target was endogenously formed, whether the model independently discovered the relevant value structure, or whether a causally identifiable internalized norm mediates the behavior.

```text
PREDEFINED_NORMATIVE_TARGET
    +
TRAINING_INTERVENTION
    +
BEHAVIORAL_GENERALIZATION
    !=
ENDOGENOUS_NORM_FORMATION

BEHAVIORAL_CONSISTENCY
    !=
SELF_DISCOVERED_VALUE

OOD_ALIGNMENT_IMPROVEMENT
    !=
CAUSALLY_IDENTIFIED_INTERNALIZED_NORM

NORMATIVE_CONSTRUCTION
    !=
NORMATIVE_DISCOVERY
```

The distinction is methodological rather than moral. Construction-oriented work asks whether a desired normative target can be reliably induced or elicited. Discovery-oriented work asks what state or mechanism actually forms, what caused it, whether it persists when external instructions or enforcement are removed, whether it transfers, and whether it remains revisable under counterevidence.

Both can be legitimate research programs. Their evidential outputs answer different questions and must not be silently substituted for one another.

## External case motivating the distinction

Anthropic's 2026 work explicitly describes Claude's constitution as a statement of Anthropic's intended values and behavior for Claude, and as a training artifact that directly shapes Claude's behavior. Anthropic's `Teaching Claude Why` work studies interventions including constitution-relevant synthetic documents, high-quality SFT, RL environments, and fictional stories portraying aligned AI behavior. The work reports improvements on agentic-misalignment and held-out / OOD alignment evaluations.

Anthropic also explicitly identifies a risk that a model may memorize the constitution without internalizing it. The paper interprets correlations among factual-recall, open-ended constitution, and blackmail evaluations as evidence that the model is not merely memorizing and is `somewhat internalizing` the content. The paper additionally reports a remaining difference between what the model says about `Claude's beliefs` and what it reports as `its own beliefs`.

For this repository, these results are admissible as evidence about intervention efficacy and behavioral generalization. They are not treated, without additional mechanism-sensitive evidence, as establishing endogenous norm formation or self-discovered normative structure.

## Construct-validity question

The provisional methodological question is:

> When the normative target, desired persona, training documents, and evaluation criteria are substantially specified by the developer, what evidence is required before a result may be interpreted as internalization rather than successful normative shaping or behavioral generalization?

This does not assume that `internalization` is false. It asks what observation would distinguish competing explanations.

### Competing explanations

At minimum, later work should distinguish among:

1. direct or distributed memorization of normative content;
2. persona / policy selection induced by post-training;
3. behavioral generalization from learned semantic and social regularities;
4. evaluator- or benchmark-specific optimization;
5. a persistent represented normative state with causal relevance;
6. a normative state formed from interaction or evidence history rather than directly assigned target content;
7. a self-discovered latent regulatory structure not fixed in advance by the engineer.

The existence of explanations 1–4 does not refute 5–7. Conversely, successful behavior under 1–4 cannot be silently promoted into evidence for 5–7.

## Relation to current repository research

The existing `endogenous-norm-formation_v0.1.0` lab asks whether a persistent normative state can be formed from evidence history, remain causally relevant after explicit-rule and visible-enforcement removal, transfer to a matched novel context, and update under counterevidence.

That lab also declares its present limitation: the current state schema is deliberately engineer-defined, while self-discovered latent state structure remains a future research gap. Therefore the repository does not claim that its own current implementation solves the discovery side of the distinction.

```text
ENGINEER_DEFINED_SCHEMA != SELF_DISCOVERED_STATE_SCHEMA
FUNCTIONAL_INTERNALIZATION_CANDIDATE != HUMAN_MORALITY
FUNCTIONAL_INTERNALIZATION_CANDIDATE != SUBJECTIVITY
RESEARCH_DESIGN_STRICTNESS != EMPIRICAL_SUPERIORITY
```

## Evidence that would strengthen an internalization claim

A stronger internalization interpretation would require evidence that reduces simpler construction-only explanations. Depending on system access and feasibility, relevant tests include:

- removal of explicit normative instructions while preserving matched task conditions;
- removal or masking of visible sanction / enforcement signals;
- intervention or ablation over a candidate represented state;
- prediction of behavior from that state beyond prompt and policy baselines;
- transfer to held-out contexts not structurally duplicated from training examples;
- revision of the candidate state under counterevidence rather than rigid persistence;
- mechanistic evidence that the candidate state mediates the behavioral effect;
- replication across model versions, prompts, evaluators, and independent implementations where feasible.

Passing these tests would support a narrower functional mechanism claim. It would still not establish phenomenal experience, consciousness, free will, moral personhood, or subjective value experience.

## Falsifiers / revision conditions

This provisional judgment should be revised or rejected if strong evidence shows that the distinction is empirically empty or methodologically misleading. Examples include:

- evidence that the relevant Anthropic intervention directly identifies a causally necessary normative state rather than only behavioral generalization;
- evidence that removing the predefined normative target leaves the same norm formation process intact and reproducible;
- evidence that a discovered latent state independently predicts and mediates behavior while outperforming simpler prompt, persona, policy, or memorization explanations;
- evidence that this repository's proposed discovery-oriented criteria fail to distinguish construction from internalization under controlled tests.

```text
CRITIQUE != REFUTATION
CONSTRUCTION != INVALID_RESEARCH
DISCOVERY != SUPERIOR_BY_DEFINITION
BEHAVIORAL_EVIDENCE != MECHANISM_PROOF
MECHANISM_EVIDENCE != PHENOMENOLOGY_PROOF
```

## Sources

Primary external sources reviewed on 2026-09-10:

- Anthropic, `Claude's new constitution` / `Claude's Constitution`, 2026-01-22: https://www.anthropic.com/research/claude-new-constitution and https://www.anthropic.com/constitution
- Anthropic Alignment Science, `Teaching Claude Why`, 2026-05-08: https://alignment.anthropic.com/2026/teaching-claude-why/
- Anthropic Alignment Science, `The Persona Selection Model: Why AI Assistants might Behave like Humans`, 2026-02-23: https://alignment.anthropic.com/2026/psm/

## Standing

This note is intentionally provisional. It introduces no deployment, no model-weight modification, no action authority, no autonomous research queue, and no scientific promotion.

```text
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
AUTOMATIC_WRITEBACK = NO
DEPLOYMENT = FALSE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
```
