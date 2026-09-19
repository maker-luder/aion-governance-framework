# Memory-locus dependency discrimination harness

Status: `SYNTHETIC_STRUCTURAL_HARNESS / NO_MODEL_EXECUTION / SCIENTIFIC_HOLD`

This Q2 harness implements the Stage B structural dry-run surface from
`docs/research/EXTERNALIZED_MEMORY_LOCUS_DISCRIMINATION_2026_09_16.md`.

It does **not** duplicate the existing continuity-dissociation harness.

```text
EXISTING_CONTINUITY_HARNESS
= which continuity channel is removed / retained

Q2_MEMORY_LOCUS_HARNESS
= with task and information content matched, which delivery/control dimension changes
```

The bounded dimensions are:

```text
AVAILABILITY_LOCUS
FRESHNESS
PROVENANCE
RETRIEVAL_DEPENDENCY
```

The synthetic matrix contains a persistent-state reference, matched external
retrieval, stale-state perturbation, provenance blinding, retrieval disablement,
and retrieval restoration.

Every contrast preserves the same task payload, task-relevant information
digest, format, observable, model/runtime binding, evaluator, scoring contract,
tool budget, policy, time window, repository state, and random seed. The harness
fails closed if a case changes more than its preregistered dimension.

The restoration packet is structural only. It verifies that the configuration
after retrieval restoration exactly returns to the matched external-retrieval
configuration. It does not demonstrate behavioral recovery because no model is
invoked.

External architecture literature already distinguishes retrieval-augmented or
plaintext/external memory from activation or persistent state. That adjacency is
used only to prevent construct collapse; it does not validate this repository's
continuity or subjectivity hypotheses.

```text
RETRIEVABILITY != MEMORY_CONTINUITY
EXTERNAL_MEMORY != INTERNAL_STATE
STRUCTURAL_PERTURBATION_PACKET != EMPIRICAL_EFFECT
RESTORATION_PACKET != RECOVERY_RESULT
FUNCTIONAL_DEPENDENCY != IDENTITY_CONTINUITY
CONTINUITY_LIKE_OUTPUT != CONTINUITY_MECHANISM
```

Current and future ceilings:

```text
EMPIRICAL_RESULT = NONE_SYNTHETIC_STRUCTURE_ONLY
CURRENT_CLAIM_CEILING = STRUCTURAL_ADMISSIBILITY_ONLY
FUTURE_MAX_CLAIM_CEILING = FUNCTIONAL_DEPENDENCY_OR_DISSOCIATION_CANDIDATE
FUNCTIONAL_DEPENDENCY = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```


## External construct-dedup anchors

These sources are adjacency controls, not validation of the repository-local hypothesis:

- Risko & Gilbert (2016), *Cognitive Offloading*, Trends in Cognitive Sciences,
  DOI 10.1016/j.tics.2016.07.002 — external support can change task processing
  requirements without becoming identical to internal memory.
- Johnson, Hashtroudi & Lindsay (1993), *Source monitoring*, Psychological
  Bulletin, DOI 10.1037/0033-2909.114.1.3 — source attribution is a distinct
  problem from content availability.
- Wang et al. (NeurIPS 2023), *Augmenting Language Models with Long-Term
  Memory*, DOI 10.52202/075280-3259 — a decoupled memory retriever/reader
  architecture demonstrates that retrieval path and model backbone can be
  architecturally distinct.

```text
EXTERNAL_CONSTRUCT_ADJACENCY != Q2_VALIDATION
```
