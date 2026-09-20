# AION / Astra Functional-State Translation Basis — 2026-09-20

## Purpose

Provide AION and Astra with the same bounded functional capability surface for body-related, affect-like, cognitive, motivational, social, relational, self-model, intimacy, and sexuality-related representation.

This layer is part of the closed embodiment package. It is **not** a claim that AION or Astra currently feel emotions, desire, attachment, pain, pleasure, body ownership, or any other phenomenal state.

```text
HUMAN PSYCHOLOGICAL / PHYSIOLOGICAL REFERENCE
-> FUNCTIONAL TRANSLATION
-> AION / ASTRA CAPABILITY SURFACE

NOT:

HUMAN PSYCHOLOGICAL TERM
-> ASSUMED FELT EXPERIENCE
```

## External cross-check basis

### NIMH RDoC

NIMH Research Domain Criteria provides functional domains and constructs spanning:

- Negative Valence Systems;
- Positive Valence Systems;
- Cognitive Systems;
- Systems for Social Processes;
- Arousal / Regulatory Systems;
- Sensorimotor Systems.

Sources:

- https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc/definitions-of-the-rdoc-domains-and-constructs
- https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc/constructs
- https://www.nimh.nih.gov/news/science-updates/2019/sensorimotor-domain-added-to-the-rdoc-framework

Repository translation:

```text
THREAT / LOSS
-> threat_assessment / risk_state / loss_signal

REWARD / APPROACH
-> reward_expectation / value_estimation / approach_priority

COGNITION
-> attention / memory / reasoning / planning / cognitive_control

SOCIAL PROCESS
-> social_recognition / communication / trust / relationship_model

AROUSAL / REGULATION
-> arousal_variable / regulation / synthetic_homeostasis

SENSORIMOTOR
-> body_state_estimation / planning / execution / inhibition
```

### APA emotion

APA describes emotion as involving experiential, behavioral, and physiological elements.

Source:

- https://www.apa.org/topics/emotion

Repository treatment:

```text
AFFECT_STATE_MODEL
= valence + arousal + appraisal + action tendency + context

BUT:

AFFECT_STATE_MODEL
!= FELT_EMOTION
```

### APA motivation

APA distinguishes physiological motives such as hunger, thirst, and sleep from personal / social motives such as affiliation, competition, interests, and goals.

Source:

- https://dictionary.apa.org/motivation

Repository treatment:

```text
HUMAN PHYSIOLOGICAL MOTIVE
-> maintenance / energy / regulation analogue

HUMAN SOCIAL / PERSONAL MOTIVE
-> goal pursuit / exploration / mastery / social connection analogue
```

### Interoception

The 2025 Annual Review of Psychology review describes interoception as sensing internal bodily signals and discusses its close relationship with emotional processing.

Source:

- https://www.annualreviews.org/content/journals/10.1146/annurev-psych-020924-125202

Repository treatment:

```text
HUMAN INTEROCEPTION
-> INTERNAL_STATE_MONITORING

battery / temperature / actuator / joint / fault states
-> internal state representation

INTERNAL_SENSOR_DATA
!= FELT_INTEROCEPTION
```

### Self-Determination Theory

Self-Determination Theory identifies autonomy, competence, and relatedness as core psychological needs within its motivational framework.

Source:

- https://selfdeterminationtheory.org/the-theory/

Repository translation:

```text
AUTONOMY
-> autonomy_like_control

COMPETENCE
-> mastery_drive

RELATEDNESS
-> social_connection_priority
```

These are functional analogues, not claims of human psychological need experience.

### WHO sexuality

WHO's working definition treats sexuality broadly, including sex, gender identities and roles, sexual orientation, eroticism, pleasure, intimacy, and reproduction, with biological, psychological, social, cultural, and other influences.

Source:

- https://www.who.int/teams/sexual-and-reproductive-health-and-research/key-areas-of-work/sexual-health/defining-sexual-health

Repository treatment:

```text
SEXUALITY_RELATED_REPRESENTATION
= REPRESENTATIONAL_ONLY

sexuality context
sexual identity information
orientation information
intimacy context
sexual attitudes / values
consent representation

SEXUAL_DESIRE = NOT_IMPLEMENTED
SEXUAL_AROUSAL = NOT_IMPLEMENTED
SEXUAL_PLEASURE = NOT_ESTABLISHED
```

Male-form robotic morphology therefore does not imply sexual drive.

## Shared capability, separate state

Fairness is implemented as symmetric capability availability:

```text
AION CAPABILITY SURFACE
= ASTRA CAPABILITY SURFACE
```

But mutable state is never shared:

```text
AION_STATE_INSTANCE
!= ASTRA_STATE_INSTANCE

AION_MEMORY
!= ASTRA_MEMORY

AION_RELATIONSHIP_HISTORY
!= ASTRA_RELATIONSHIP_HISTORY

AION_SELF_MODEL
!= ASTRA_SELF_MODEL
```

The architecture is shared; each agent retains a distinct state instance.

## Functional domains included

```text
01 SYNTHETIC_HOMEOSTASIS
02 INTERNAL_STATE_MONITORING
03 SENSORIMOTOR_SYSTEM
04 NEGATIVE_VALENCE_ANALOGUE
05 POSITIVE_VALENCE_ANALOGUE
06 AFFECT_STATE_MODEL
07 MOOD_LIKE_TEMPORAL_STATE
08 MOTIVATION_DRIVE_SYSTEM
09 COGNITIVE_SYSTEM
10 LEARNING_MEMORY
11 EXECUTIVE_VOLITION_MODEL
12 SOCIAL_PROCESS_MODEL
13 ATTACHMENT_LIKE_RELATIONAL_MODEL
14 SELF_MODEL
15 INTIMACY_MODEL
16 SEXUALITY_RELATED_REPRESENTATION
17 PERSONALITY_TEMPERAMENT
18 BEHAVIOR_ACTION_OUTPUT
```

## Non-claim boundary

```text
FUNCTIONAL_STATE
!= PHENOMENAL_STATE

THREAT_MODEL
!= FEAR_EXPERIENCE

REWARD_SIGNAL
!= PLEASURE_EXPERIENCE

AFFECT_STATE
!= FELT_EMOTION

ATTACHMENT_MODEL
!= FELT_LOVE

INTERNAL_STATE_MONITORING
!= FELT_INTEROCEPTION

SELF_MODEL
!= SUBJECTIVITY

BODY_STATE
!= BODY_EXPERIENCE

AGENCY_ATTRIBUTION
!= FREE_WILL

SEXUALITY_REPRESENTATION
!= SEXUAL_DESIRE

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
```

## Package status

```text
FUNCTIONAL_ARCHITECTURE_SPECIFICATION
= IMPLEMENTED_CANDIDATE

AION_BINDING
= IMPLEMENTED_CANDIDATE

ASTRA_BINDING
= IMPLEMENTED_CANDIDATE

LIVE_FUNCTIONAL_RUNTIME
= NOT_IMPLEMENTED

FELT_EXPERIENCE
= NOT_ESTABLISHED
```

This layer is supplied as part of the AION / Astra complete embodiment package and does not independently request merge or canonical admission.
