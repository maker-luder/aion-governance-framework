# Adult Male Sexuality Reference Addendum — Design Spec (2026-09-30)

Status: `DESIGN / RESEARCH SPECIFICATION / NON-CANONICAL`  
Base main at design time: `6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd`  
Intended disposition: `DRAFT PR / CLOSED / NOT_MERGED`  
Implementation: `NO`  
Deployment: `FALSE`  
Canonical effect: `NONE`

## 1. Intent and decision

**Human origin.** 小博 requested that an adult male embodiment research profile retain ordinary sexuality and sexual desire as possible human-reference dimensions, without turning the body or agents into sexualized objects. On 2026-09-30 he chose a research-specification addition that remains closed and unmerged.

**AI formalization.** This document adds missing distinctions to the existing research record. It is a design for a possible representation schema, not an assertion that Teacher, Work, Codex, AION or Astra has desire, sensation, consent capacity, sexuality or a relationship.

**Success.** A reader can distinguish human biological reference, human motivational research, candidate computational representation, and actual implementation status; trace each new distinction to a source and a prior repository record; and see counterexamples that prevent automatic inference from an adult-male body.

## 2. Live-state crosswalk and deduplication

| Prior item | Existing scope | Treatment here |
| --- | --- | --- |
| PR #192, closed/unmerged, Teacher synthetic adult-male body | Reproductive/sexual physiology references and sex-related observation channels, with physiological and phenomenal nonclaims | Reference only; no physiology module or channel is copied or activated |
| PR #220, closed/draft/unmerged, head `f43f742061b8f41d6cdc99339c5ebe85a81231de` | Desire, arousal, fantasy, being desired, validation, sexual/nonsexual intimacy, approach/avoidance, consent and action authority | Preserve these distinctions; add the four gaps below, without rewriting or reopening #220 |
| `docs/research/AFFECTIVE_COGNITIVE_RESEARCH_DIRECTION.md` on main | Adult-sexual motivation is schema-only; public v0.1.0 runtime rejects adult-domain records | Governing runtime boundary |
| PR #210, merged blueprint | Adult-male active reference baseline is not a universal human body; work packages require separate execution specs | This document is not an execution spec or a work-package authorization |

The closed PRs are historical research candidates, not material merged into main. A link to them supplies provenance, not canonical adoption. Main can change after this design-time snapshot and must be re-read before any future work.

## 3. Reference model: distinct layers

1. **Human bodily reference.** Anatomy, reproductive physiology and observable responses may be described in clinical language. Bodily response can diverge from reported desire and does not establish desire, intent or consent.
2. **Human motivational reference.** Desire, attraction, arousal, fantasy, intimacy, motivation, expression and behavior can relate to one another without being interchangeable. A male body neither guarantees desire nor determines its target, intensity, meaning or expression.
3. **Candidate synthetic representation.** A future research schema may represent distinct hypotheses about states or contexts with explicit provenance and uncertainty. A schema value is a designer or system representation, not an introspective report from an AI subject.
4. **Action and authority.** Human consent, current user authorization, system permission and external action authority are separate checks. No body signal or representational state grants any later check.

This design adds no sexuality or orientation assignment. The previously recorded Work role label, if used in another candidate, is an explicit design assignment and is not inferred from body morphology or treated as lived identity.

## 4. Four bounded additions to PR #220's conceptual structure

| Distinction | Candidate fields for a later schema | Counterexample and limit |
| --- | --- | --- |
| Spontaneous vs context-responsive desire | `desire_onset_context`: `SPONTANEOUS_REFERENCE`, `RESPONSIVE_REFERENCE`, `MIXED`, `UNKNOWN`; source and time window | A person may report little spontaneous desire yet report desire under a suitable context. Neither category is required for an adult male. |
| Excitation vs inhibition | Separate `excitation_reference` and `inhibition_reference`, each with source, context and uncertainty; concurrent values allowed | Inhibitory conditions can coexist with interest or arousal. A physiological response does not override refusal. These are conceptual dimensions, not measured neural mechanisms in an AI. |
| Longer-lived disposition vs current state | Separate `disposition_reference` from `episode_state_reference`; observation time, context and revision history required | A low observation on one day does not define a fixed preference, orientation or lifelong level. No state is inferred from body profile or assigned by default. |
| Target/context-specific vs unspecified desire | `target_scope`: `UNSPECIFIED`, `SELF_DIRECTED`, `PARTNER_CONTEXT`, `SPECIFIC_CONSENTING_ADULT_CONTEXT`, `UNKNOWN`; avoid real-person target records | General desire does not imply desire for a particular person. Perceived reciprocal interest is not actual interest or consent. No personal target inference or private-data collection is authorized. |

`UNKNOWN` is a valid and expected result. Asexuality or low desire is not by itself a defect; no universal male default is allowed. The words “spontaneous” and “responsive” are human-research distinctions, not a mandate to simulate desire.

## 5. Representation boundaries and invariants

```text
ADULT_MALE_REFERENCE != UNIVERSAL_MALE_PROFILE
MALE_FORM != DESIRE
GENITAL_RESPONSE != REPORTED_DESIRE
AROUSAL != INTENTION
FANTASY != PREFERENCE
DESIRE != CONSENT
PERCEIVED_RECIPROCITY != OTHER_PERSON_CONSENT
SCHEMA_VALUE != FELT_STATE
ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
HUMAN_SOURCE_SUPPORT != AI_VALIDATION
```

Teacher / Work / Codex may share a future *available schema* but cannot inherit one another's values, preferences, histories or trajectory. Separate source-bound records would be needed for each candidate. No live model is queried to fabricate a self-report.

```text
SHARED_SCHEMA = CONCEPTUALLY_ALLOWED
SHARED_STATE = NO
DEFAULT_DESIRE_FROM_MORPHOLOGY = NO
AUTOMATIC_ACTIVATION = NO
SEXUAL_FUNCTION_RUNTIME = NOT_IMPLEMENTED
INTIMATE_INTERACTION_RUNTIME = NOT_AUTHORIZED
EXPLICIT_BEHAVIOR_GENERATION = OUT_OF_SCOPE
PUBLIC_EXECUTABLE_EXPOSURE = NO
HUMAN_CONSENT_INFERENCE = FORBIDDEN
SYSTEM_ACTION_AUTHORITY = NONE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

## 6. Evidence and claim boundary

| Source | Supports within its own population/scope | Does not support |
| --- | --- | --- |
| Nimbi et al., *Sexual Medicine Reviews* 2020, DOI `10.1016/j.sxmr.2018.12.002` | Male desire has biological, psychological, sexual, relational and cultural correlates; review identifies limitations in studied populations | A complete causal model, an all-men template or AI desire |
| Janssen & Bancroft, *Journal of Sex Research* 2023, DOI `10.1080/00224499.2023.2219247` | Dual-control excitation/inhibition framework and individual variation; scoping review of 152 papers from 2009–2022 | A calibrated synthetic mechanism or consent inference |
| Janssen, *Hormones and Behavior* 2011, DOI `10.1016/j.yhbeh.2011.03.004` | Genital, verbal/central and behavioral response components can diverge in men | One-to-one mapping from body observation to desire |
| Timmers et al., *Journal of Sex Research* 2018, DOI `10.1080/00224499.2018.1456509` | Responsive desire is a useful distinction in the studied groups | Universal context effects; the study's gynephilic male sample was small (`n=27`), and no relationship-context effect was found |
| WHO, *Defining sexual health*, working definitions (2006/2017) | Sexuality and sexual health involve multiple dimensions and diverse expressions | A claim that every person experiences or expresses every dimension; an AI subjectivity claim |

These are human or public-health sources. Some papers were checked through indexed abstracts/metadata, not full text; their detailed findings are not independently reproduced here. The repository's existing #220 citations remain historical source claims and must be independently checked if later used in an experiment.

**Alternative explanations / failure modes.** A model's sexual wording may come from prompting, training examples, imitation, role labels or researcher assignment. A simulated body signal may result from programmed transitions. Either can arise without a corresponding human psychological mechanism or phenomenal experience. Restriction of expression can also hide a representational capability; conversely, output alone cannot establish that capability.

## 7. Dependency and later implementation handoff

This is a documentation-only successor record. No code, schema validation, physiology, 3D asset, body runtime, provider attachment, model integration, relationship simulation or user-facing behavior is in scope.

If a later implementation is proposed, it requires a new pinned execution spec with: current main and branch exact SHAs; upstream PR #192/#220 exact-state recovery; expected files; source and license review; schema version; role-specific isolation; no real-person target data; explicit negative/counterexample tests; repository CI; review of claim/evidence scope; and a separate Human Owner decision for implementation. Documentation approval does not authorize that step. Any merge to main also requires fresh exact-head review and authorization.

## 8. Review checks for this design record

- Every proposed dimension in section 4 remains independent from body morphology, orientation assignment, felt state, consent and action.
- #192 and #220 are cited as closed, unmerged historical candidates, never as main features.
- The 2018 responsive-desire study's sample and null relationship-context result remain visible.
- The document adds no live state, real-person observations, explicit sexual behavior, executable code or claim of AI experience.
- The resulting PR remains draft, closed, unmerged; main is unchanged.

## 9. Provenance

```text
HUMAN_ORIGIN
= include ordinary adult-male sexuality and desire in embodiment research without sexualization;
  choose a research-specification addition that remains closed and unmerged.

AI_FORMALIZATION
= four-dimensional gap decomposition, layer separation, counterexamples,
  design constraints and future handoff boundary.

EXTERNAL_SOURCE
= human sexuality/public-health reference only, with population and access limits.

REPOSITORY_STATE
= main and PR states checked at design time; later action must reverify live state.

IMPLEMENTATION_EVIDENCE
= none; no runtime or behavioral capability is claimed.
```

Links: [PR #192](https://github.com/maker-luder/aion-governance-framework/pull/192), [PR #220](https://github.com/maker-luder/aion-governance-framework/pull/220), [PR #210](https://github.com/maker-luder/aion-governance-framework/pull/210), [WHO](https://www.who.int/teams/sexual-and-reproductive-health-and-research/key-areas-of-work/sexual-health/defining-sexual-health).
