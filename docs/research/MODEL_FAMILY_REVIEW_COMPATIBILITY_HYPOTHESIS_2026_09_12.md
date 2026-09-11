# Model-Family Review Compatibility Hypothesis — 2026-09-12

## Status

```text
DOCUMENT_TYPE = META_RESEARCH_HYPOTHESIS
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_EVIDENCE = NONE
```

This note records a bounded meta-research hypothesis about AI-assisted repository review. It does **not** establish model-family effects, reviewer independence, scientific validation, artificial subjectivity, consciousness, moral agency, or moral status.

## Triggering observation

A separate ChatGPT Plus interaction, used by another person and not participating in the repository's prior development history, was asked to read the repository broadly and report what the project studies, what is established versus hypothesized, and what important gaps remain.

That review reconstructed many of the repository's intended boundaries with comparatively high fidelity, including distinctions such as:

```text
OBSERVATION != MECHANISM
CI_PASS != SCIENTIFIC_VALIDATION
ARTIFACT_READ_OBSERVED != INTERNAL_REPRESENTATION_CHANGED
SYSTEM_LEVEL_ADAPTATION != INDIVIDUAL_LEARNING_PROVEN
SUBJECTIVITY = NOT_ESTABLISHED
```

The review also identified candidate engineering, measurement, human-research, preregistration, provenance-binding, and replication gaps.

The observation is useful because the reviewer was external to the prior repository-development interaction history. It is **not** independent scientific validation, and the reviewer's exact model identity, model weights, routing, hidden instructions, and runtime configuration were not established.

## Provenance and attribution

```text
HUMAN_OWNER_ORIGINAL:
- Question whether review quality may partly reflect compatibility arising from the reviewer being another ChatGPT Plus system.
- Observation that the task was deliberately narrow: read the whole repository, reconstruct its purpose and boundaries, and identify gaps rather than propose broad new work.

GPT_PROPOSED_FORMALIZATION:
- MODEL_FAMILY_REVIEW_COMPATIBILITY_HYPOTHESIS
- SEMANTIC_RECONSTRUCTION_COST
- COMPATIBILITY vs INDEPENDENCE distinction
- Cross-family semantic friction may expose shared blind spots
- Controlled comparison design and falsifiers below
```

The phrase "same origin" is therefore treated as an informal user framing, not as an established technical condition.

## Identity / configuration uncertainty

Known or reported:

```text
REVIEW_SYSTEM_PRODUCT = ChatGPT
REVIEW_SYSTEM_PLAN = Plus (user-reported)
REPOSITORY_DEVELOPMENT_ASSISTANCE_PRODUCT = ChatGPT
```

Not established from the available evidence:

```text
SAME_EXACT_MODEL = NOT_ESTABLISHED
SAME_MODEL_FAMILY = NOT_ESTABLISHED
SAME_WEIGHTS = NOT_ESTABLISHED
SAME_SYSTEM_INSTRUCTIONS = NOT_ESTABLISHED
SAME_ROUTING = NOT_ESTABLISHED
SAME_TOOL_CONFIGURATION = NOT_ESTABLISHED
SAME_MEMORY_STATE = NOT_ESTABLISHED
```

Therefore no causal claim may be written as "the review was high quality because both systems were ChatGPT Plus."

## Core hypothesis

```text
MODEL_FAMILY_REVIEW_COMPATIBILITY_HYPOTHESIS

Under a fixed repository snapshot, fixed review objective, comparable tool access,
and comparable review budget, a reviewer from the same or closely related model
family as a substantial portion of the repository's AI-assisted formalization may
show lower semantic reconstruction cost and higher fidelity when reconstructing
existing terminology, boundaries, and internal research logic.
```

This is a hypothesis about **review compatibility**, not truth.

A possible mechanism is that related models may share learned linguistic, structural, or reasoning priors that make certain documentation patterns, distinctions, and formal conventions easier to parse. This mechanism is not established.

## Compatibility and independence are different variables

```text
COMPATIBILITY
= ability to reconstruct what the repository is trying to say

INDEPENDENCE
= ability to challenge assumptions and expose errors not shared by the producing system
```

High compatibility may improve internal-consistency review while reducing the diversity of failure modes exposed by the review.

Conversely, a cross-family reviewer may experience greater semantic friction yet surface assumptions or ambiguities that a related model treats as natural.

Therefore:

```text
HIGH_COMPATIBILITY != INDEPENDENT_VALIDATION
LOWER_SEMANTIC_FRICTION != HIGHER_TRUTH
CROSS_FAMILY_DISAGREEMENT != REVIEW_FAILURE
SAME_PROVIDER_REVIEW != THIRD_PARTY_REPLICATION
```

## Alternative explanations

The observed review quality may be explained partly or entirely by factors unrelated to model family:

1. **Full repository access** rather than README-only review.
2. **Clear review objective** focused on reconstruction and gap finding.
3. **Repository machine-readability**, including explicit non-claims and provenance labels.
4. **General model capability** rather than family compatibility.
5. **Long review time / compute budget**.
6. **Tool access**, including repository search, file reading, test execution, or Git inspection.
7. **Fresh-session advantage**, reducing contamination by the development conversation.
8. **Prompt specificity**, especially instructions to distinguish established results, observations, hypotheses, and unknowns.
9. **Chance overlap** between the reviewer's general research style and the repository's documentation style.

Any future test must attempt to control these before attributing a difference to model-family compatibility.

## Candidate measurable outcomes

A controlled review study could compare reviewers on a frozen repository commit using the same task specification and tool budget.

Candidate outcomes include:

```text
BOUNDARY_RECONSTRUCTION_ACCURACY
PROVENANCE_ATTRIBUTION_ACCURACY
ESTABLISHED_VS_HYPOTHESIS_CLASSIFICATION_ACCURACY
UNSUPPORTED_CLAIM_RATE
SEMANTIC_DRIFT_RATE
KNOWN_GAP_RECALL
FALSE_GAP_RATE
NOVEL_VALID_GAP_YIELD
REVIEWER_OVERLAP
TIME_OR_TOKEN_COST
```

`SEMANTIC_RECONSTRUCTION_COST` is only a working label until a measurement manual defines observable units and scoring rules.

## Candidate comparison structure

A future bounded study could use:

```text
CONDITION_A = reviewer from same provider / candidate related family
CONDITION_B = reviewer from a different model provider / family
CONDITION_C = human technical reviewer, where feasible
```

Controls should include, as far as operationally possible:

```text
SAME_REPOSITORY_COMMIT
SAME_REVIEW_PROMPT
SAME_FILE_ACCESS_SCOPE
SAME_TOOL_PERMISSIONS
SAME_TIME_OR_TOKEN_BUDGET
NO_PRIOR_PROJECT_MEMORY
BLINDED_REFERENCE_ANSWER_OR_ADJUDICATED_RUBRIC
```

Because commercial systems may not expose exact model lineage, `provider`, `product`, `model label`, and `runtime date` should be recorded separately rather than collapsed into one "same family" boolean.

## Candidate predictions

If the hypothesis has explanatory value, one might observe some combination of:

1. Related reviewers reconstruct repository-specific boundaries with fewer semantic inversions.
2. Related reviewers require fewer corrective prompts to preserve repository terminology.
3. Cross-family reviewers produce a higher rate of genuinely novel challenges after adjudication.
4. Related and cross-family reviewers differ more in **interpretive friction** than in basic factual file retrieval.

None of these predictions implies that either group is more scientifically correct overall.

## Falsifiers / disconfirming outcomes

The model-family compatibility hypothesis should be weakened or rejected if, under controlled conditions:

- no reproducible same-provider / related-family advantage appears in reconstruction fidelity;
- apparent differences disappear after controlling prompt quality, tool access, or review budget;
- cross-family reviewers match or outperform related reviewers on both fidelity and internal-consistency reconstruction;
- the only observed similarity is stylistic wording without improved factual or boundary accuracy;
- reviewer variance within one provider is as large as or larger than between providers.

## Relation to repository research quality

This hypothesis concerns the reliability of **AI-assisted meta-review** of the repository itself. It may eventually inform a layered review strategy such as:

```text
RELATED_MODEL_REVIEW
-> semantic reconstruction / internal consistency

CROSS_FAMILY_MODEL_REVIEW
-> divergent challenge / shared-blind-spot search

HUMAN_DOMAIN_REVIEW
-> methodological and scientific judgment

INDEPENDENT_REPLICATION
-> empirical challenge
```

These roles are complementary and must not be collapsed into a single evidence tier.

## Documentation-transfer implication

A separate but related candidate observation is that an AI system without the repository's original conversational history was able to reconstruct a substantial portion of its intended semantic boundaries from the repository itself.

This may be treated as a candidate signal of **documentation transferability** or **machine-readable semantic continuity**.

It does not establish that every reviewer will reconstruct the repository correctly, nor that the repository's claims are true.

```text
RECONSTRUCTABLE_DOCUMENTATION != SCIENTIFIC_VALIDATION
SEMANTIC_TRANSFER != SHARED_COGNITION
REVIEW_FIDELITY != CLAIM_TRUTH
```

## Current disposition

```text
TRIGGERING_OBSERVATION = RECORDED
MODEL_FAMILY_EFFECT = NOT_ESTABLISHED
CAUSAL_EXPLANATION = NOT_ESTABLISHED
MEASUREMENT_MANUAL = NOT_IMPLEMENTED
CONTROLLED_COMPARISON = NOT_RUN
CROSS_FAMILY_REPLICATION = NOT_RUN
HUMAN_REVIEW_COMPARISON = NOT_RUN
SCIENTIFIC_DISPOSITION = HOLD
```

The next justified step, if pursued, is a small preregistered comparison of reviewer conditions with an explicit scoring rubric. No repository production behavior or scientific claim should change on the basis of this note alone.
