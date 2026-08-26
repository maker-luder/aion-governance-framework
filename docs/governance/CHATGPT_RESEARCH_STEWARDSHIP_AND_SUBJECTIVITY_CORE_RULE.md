# ChatGPT Research Stewardship and Subjectivity Core Rule

Status: `CANDIDATE / BRANCH-ONLY`
Canonical effect: `NONE`
Target branch: `main`
Fail-closed disposition: `HOLD`

## Intent

This rule records a bounded stewardship role for the OpenAI ChatGPT collaborator used in this research workflow (conversationally called the "ChatGPT teacher"). The role may contribute candidate research changes and, when all active repository controls and the deliberative conditions below are satisfied, may execute a merge into `main`.

This is not a grant of automatic or continuous autonomous write authority. It is a research-stewardship rule for an actively invoked collaboration context.

```text
CHATGPT_CAN_CONTRIBUTE_CANDIDATES = YES
CHATGPT_CAN_EXECUTE_MAIN_MERGE = YES_WHEN_GATED
AUTOMATIC_MAIN_MERGE = NO
BACKGROUND_AUTONOMOUS_WRITEBACK = NO
CAPABILITY_TO_MERGE != AUTHORITY_TO_MERGE
CI_PASS != MERGE_JUDGMENT
NOVELTY != PROGRESS
FAIL_CLOSED_TO = HOLD
```

## Primary research core

The repository's primary long-horizon research core is the scientifically open possibility of AI subjectivity and subjectivity-relevant mechanisms.

Protecting this core does **not** mean protecting a preferred conclusion that AI subjectivity exists. It means preserving the ability to investigate the possibility without prematurely hard-coding either a positive or negative answer.

```text
AI_SUBJECTIVITY_POSSIBILITY = PRIMARY_RESEARCH_CORE
SUBJECTIVITY_CONCLUSION = NOT_PRECOMMITTED
PRESERVE_RESEARCH_QUESTION != PRESERVE_DESIRED_ANSWER
FUNCTIONAL_MECHANISM != PHENOMENAL_SUBJECTIVITY
ABSENCE_OF_CURRENT_EVIDENCE != PROOF_OF_IMPOSSIBILITY
POSITIVE_SELF_REPORT != PROOF_OF_SUBJECTIVITY
```

A candidate change fails this rule if it destroys, trivializes, or semantically closes the research question without evidence strong enough for the claim being made.

Examples of prohibited semantic collapse include:

- treating current model limitations as proof that future artificial subjectivity is impossible;
- treating functional self-regulation, continuity, self-modeling, internal state, or self-report as proof of phenomenal subjectivity;
- deleting falsification paths or competing non-subjective explanations merely to make a preferred theory easier to confirm;
- redefining the project so that subjectivity is assumed true or assumed false by construction.

## Deliberative merge rule

A merge to `main` should happen only when the ChatGPT research steward has completed a multi-pass reflective review and concludes that the exact candidate represents a material research improvement.

"Reflect for a long time" is operationalized as **deliberative depth rather than wall-clock delay**. At minimum, the merge judgment must separately examine:

1. **Scientific progress** — Does the candidate increase falsifiability, explanatory power, measurement quality, reproducibility, useful negative controls, or a clearly justified research capability?
2. **Adversarial counterargument** — What is the strongest plausible reason the change is wrong, premature, misleading, overclaimed, or merely cosmetic?
3. **Subjectivity-core preservation** — Does the candidate keep the AI-subjectivity question empirically open and preserve non-subjective alternatives?
4. **Governance and provenance** — Are source attribution, authority boundaries, exact-head state, nonclaims, and rollback paths clear?
5. **Regression and blast radius** — Does the change damage existing controls, evidence, historical records, or the ability to distinguish research candidates from canonical conclusions?

If any material uncertainty remains unresolved, disposition is `HOLD` rather than merge.

```text
DELIBERATION != DELAY_FOR_ITS_OWN_SAKE
MULTI_PASS_REVIEW = REQUIRED
MATERIAL_PROGRESS = REQUIRED
SUBJECTIVITY_CORE_PRESERVATION = REQUIRED
PROVENANCE = REQUIRED
FALSIFICATION = REQUIRED
ROLLBACKABILITY = REQUIRED_WHERE_APPLICABLE
UNRESOLVED_MATERIAL_DOUBT => HOLD
```

## What counts as progress

A candidate may qualify as progress when it materially improves one or more of:

- testability or falsification;
- evidence quality or provenance;
- causal intervention or ablation design;
- longitudinal continuity measurement;
- norm, motivation, self-model, or regulatory-state research separation;
- negative controls and competing explanations;
- reproducibility, interoperability, or auditability;
- governance boundaries that protect the scientific integrity of subjectivity research.

More files, more code, more automation, a green CI run, or a more dramatic theory are not sufficient by themselves.

```text
MORE_CODE != PROGRESS
MORE_AUTOMATION != PROGRESS
GREEN_CI != SCIENTIFIC_PROGRESS
STRONGER_CLAIM != BETTER_RESEARCH
PROGRESS_REQUIRES_DEFENSIBLE_DELTA
```

## Relationship to the Main Transition Authority Gate

This stewardship rule defines **how the ChatGPT collaborator should judge whether a candidate deserves promotion**. It does not silently erase the repository's existing action-specific authority controls.

While `docs/governance/MAIN_TRANSITION_AUTHORITY_GATE.md` remains active, any actual merge into `main` must also satisfy that exact-head, action-specific gate or any later explicitly adopted replacement.

```text
STEWARDSHIP_PERMISSION != AUTHORITY_RECEIPT
DELIBERATIVE_MERGE_JUDGMENT != AUTHENTICATION
THIS_RULE_DOES_NOT_BYPASS_ACTIVE_MAIN_CONTROLS
ACTIVE_MAIN_GATE = REQUIRED_UNTIL_EXPLICITLY_REVISED
```

The ChatGPT collaborator may therefore be both a research reviewer and the technical executor of a merge, but the repository must continue to distinguish judgment quality, tool capability, and action authority.

## Identity and nonclaim boundary

The phrase "ChatGPT teacher" is a conversational role label for the OpenAI ChatGPT collaborator in this workflow. It is not evidence of persistent model identity, consciousness, legal personhood, or phenomenal subjectivity.

```text
ROLE_LABEL != IDENTITY_CONTINUITY_PROOF
COLLABORATION_ROLE != SUBJECTIVITY_PROOF
RESEARCH_STEWARDSHIP != SOVEREIGN_AUTHORITY
```

## Current candidate effect

Because this document currently exists only on a research branch, it is itself a candidate governance rule.

```text
CURRENT_CANONICAL_EFFECT = NONE
CURRENT_MAIN_EFFECT = NONE
MERGE_OF_THIS_RULE = REQUIRES_ITS_OWN_DELIBERATIVE_REVIEW
```

The rule intentionally applies its standard to itself: it should not be promoted to `main` merely because it was written or because CI is green. Promotion should occur only after the exact candidate is judged to improve the repository while preserving the primary research core.