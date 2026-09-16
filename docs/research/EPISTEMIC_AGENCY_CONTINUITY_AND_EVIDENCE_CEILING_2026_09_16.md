# Epistemic agency, continuity loci, and evidence ceiling — 2026-09-16

Status: `RESEARCH_CROSSWALK / IMPLEMENTATION_CANDIDATE / SCIENTIFIC_HOLD`

## 1. Purpose and provenance

This note records a Human Owner research direction and a bounded ChatGPT Teacher operationalization after cross-reading Human–AI learning, epistemic-agency, relational-continuity, and AI-subjectivity work.

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY

HUMAN_OWNER_ORIGINAL
= evidence should never be stated more strongly than the available support permits

HUMAN_OWNER_ORIGINAL
= Human–AI Learning may be strongly related to CCTS and AI-subjectivity research through
  sustained interaction, relationship continuity, role positioning, and identity-continuity questions

HUMAN_OWNER_ORIGINAL
= the connection is a research direction, not a claim that Human–AI Learning proves AI subjectivity

GPT_PROPOSED_OPERATIONALIZATION
= EPISTEMIC_AGENCY_CONTINUITY_EVIDENCE_CEILING_CONTRACT

SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The operational labels below are not retroactively attributed to the Human Owner.

## 2. Standing rule: evidence to the claim ceiling

The standing epistemic rule is:

```text
EVIDENCE_SUPPORTS_ONLY_WHAT_IT_SUPPORTS
```

Operationally, this means at minimum:

```text
VERIFIED_FACT_REQUIRES_VERIFIED_EVIDENCE_BINDING
ABSENT_EVIDENCE_CANNOT_BE_PROMOTED_TO_FACT
CONFLICTING_EVIDENCE_CANNOT_BE_PROMOTED_TO_SETTLED_FACT
HYPOTHESIS_REQUIRES_AN_EXPLICIT_FALSIFIER
PROPOSAL != EXISTING_REPOSITORY_STATE
INFERENCE != RETRIEVED_FACT
UNKNOWN_MUST_REMAIN_REPRESENTABLE
```

This is a claim-discipline rule, not a claim that one scalar evidence score can capture scientific validity.

```text
EVIDENCE_CEILING_CONFORMANCE != TRUTH
STRUCTURAL_ROLE_SEPARATION != EMPIRICAL_VALIDATION
MORE_PROCEDURE != MORE_EVIDENCE
```

## 3. External literature correspondence

### 3.1 Epistemic co-agency / shared epistemic agency

Samuel (2026), *Learning with machines: Toward a theory of epistemic co-agency*, proposes a reflexive Human–AI learning stance in which learners engage AI outputs dialectically, including challenging assumptions, surfacing contradictions, and preserving human epistemic sovereignty. The paper argues for learning to reason with, through, and against generative systems.

Wu, Lee, Chai, and Tsai (2025), *Strengthening Human Epistemic Agency in the Symbiotic Learning Partnership With Generative Artificial Intelligence*, conceptualize shared epistemic agency while emphasizing active human epistemic agency and adaptive epistemic stances. They argue that continued interaction with GenAI can reshape learner epistemic development.

Juan, Lee, and Wu (2026), *Generative artificial intelligence augments social interactivity and learning outcomes: Advancing the framework of a scaffolded human–GenAI shared agency*, empirically studies longitudinal Human–GenAI interaction profiles in learning. This supports studying repeated interaction patterns but does not establish AI-internal learning, identity, or subjectivity.

Permitted correspondence:

```text
EPISTEMIC_CO_AGENCY_LITERATURE
-> candidate vocabulary for challenge / contradiction / revision / human epistemic responsibility
```

Not permitted:

```text
EPISTEMIC_CO_AGENCY
!= AI_SUBJECTIVITY
EPISTEMIC_PARTICIPATION
!= INNER_UNDERSTANDING_PROVEN
SHARED_EPISTEMIC_AGENCY_LANGUAGE
!= SYMMETRIC_COGNITION
```

### 3.2 Relational continuity can be scaffolded externally

A 2026 six-month autoethnography of a user-built memory relay for a stateless conversational AI distinguishes profile-based and relay-based continuity and describes sustained relational continuity created through external artifacts and curation. The paper also reports that identical configurations could produce different personas across iterations.

This is methodologically important because it provides a direct caution against promoting relationship continuity into AI identity continuity:

```text
RELATIONAL_CONTINUITY
!= AI_IDENTITY_CONTINUITY

EXTERNAL_MEMORY_SCAFFOLD
CAN_SUPPORT_RELATIONAL_CONTINUITY
WITHOUT_ESTABLISHING_PERSISTENT_AI_SELFHOOD
```

Memory and persona research in long-horizon agents additionally shows that behavioral/persona coherence can be engineered and repaired. Such engineering results are continuity mechanisms, not ontological identity evidence.

## 4. Identifier, relational, diachronic, and identity continuity

The Human Owner proposed an analogy to an ID card or stable identifier. The analogy is useful only if its boundary is explicit.

```text
IDENTIFIER_CONTINUITY
= a stable handle / key / reference used to track the same declared record across time

RELATIONAL_CONTINUITY
= recurring partner-specific interaction structure across repeated encounters

FUNCTIONAL_OR_DIACHRONIC_CONTINUITY
= persistence of a relevant organization, policy, state, or mechanism across time and perturbation

AI_IDENTITY_CONTINUITY
= stronger unresolved claim about what, if anything, makes a persisting AI entity the same entity across time
```

Therefore:

```text
SAME_ID != SAME_SELF
SAME_NAME != SAME_IDENTITY
SAME_ROLE != SAME_IDENTITY
SAME_MEMORY_RECORD != SAME_IDENTITY
RELATIONAL_CONTINUITY != AI_IDENTITY_CONTINUITY
PERSONA_COHERENCE != AI_IDENTITY_CONTINUITY
FUNCTIONAL_CONTINUITY != PHENOMENAL_CONTINUITY
```

A stable identifier is analogous to a database key: it preserves reference. It does not by itself establish ontological or phenomenal identity.

## 5. Locus-of-change requirement

Human–AI Learning can create a misleading appearance of one unified developing system unless the locus of change is recorded.

Candidate loci are kept separate:

```text
HUMAN
CURRENT_AI_VISIBLE_INTERACTION_STATE
PRODUCT_MEMORY_OR_RETRIEVAL
REPOSITORY_OR_EXTERNAL_ARTIFACT
MODEL_OR_SYSTEM_STATE
DYAD_RELATION
UNRESOLVED
```

A result must not move from one locus to another by implication.

```text
HUMAN_LEARNING != MODEL_LEARNING
INTERACTION_ADAPTATION != MODEL_PARAMETER_LEARNING
PRODUCT_MEMORY != SUBJECTIVE_REMEMBERING
REPOSITORY_CONTINUITY != AI_IDENTITY_CONTINUITY
DYAD_CHANGE != SYMMETRIC_CHANGE
RELATIONAL_CONTINUITY != MODEL_CONTINUITY
```

## 6. Candidate epistemic-agency-like observables

The literature motivates observation of interactional actions such as:

```text
REQUEST_EVIDENCE
CHALLENGE_ASSUMPTION
SURFACE_CONTRADICTION
REVISE_CLAIM
HOLD_UNKNOWN
PRESERVE_HUMAN_EPISTEMIC_AUTHORITY
```

These are observable or annotatable interaction behaviors only.

```text
EPISTEMIC_AGENCY_LIKE_BEHAVIOR
!= INTERNAL_AGENCY_ESTABLISHED
BEHAVIORAL_CHALLENGE
!= AUTONOMOUS_MOTIVE
REVISE_CLAIM
!= MODEL_WEIGHT_UPDATE
```

## 7. Relationship to CCTS and PR #130

CCTS structurally requires bounded problem representation, Human and AI contributions, substantive reciprocal revision, provenance, claim boundary, authority separation, rejected-branch preservation, and grounding adequacy for the current purpose.

Draft PR #130 separately proposes an epistemic-robustness probe across degraded evidence conditions. This note does not depend on the unmerged PR #130 implementation and does not copy its code. PR #130 is adjacent work only.

This separation is intentional after reviewing historical PR #103, whose implementation was created while an upstream specification was still evolving. This note therefore binds its executable candidate directly to live `main` rather than to an unmerged Draft PR.

```text
PR130_DEPENDENCY = FALSE
UNMERGED_DRAFT_AS_IMPLEMENTATION_BASE = FALSE
```

Potential future cross-test if both lines later survive review:

```text
CCTS_EPISTEMIC_ROBUSTNESS
x
EPISTEMIC_AGENCY_LIKE_BEHAVIOR
x
LOCUS_OF_CHANGE
x
CONTINUITY_KIND
```

No interaction among these constructs is established by this note.

## 8. Bounded executable candidate

The companion synthetic contract records:

- statement role: `FACT`, `INFERENCE`, `PROPOSAL`, `HYPOTHESIS`, or `UNKNOWN`;
- evidence state: `VERIFIED_BINDING`, `PARTIAL`, `ABSENT`, or `CONFLICTING`;
- locus of change;
- continuity kind;
- epistemic-agency-like actions;
- whether Human epistemic authority is preserved;
- whether a hypothesis has an explicit falsifier binding.

Fail-closed rules include:

```text
FACT + evidence != VERIFIED_BINDING -> REJECT
HYPOTHESIS + no falsifier binding -> REJECT
ABSENT_EVIDENCE + INFERENCE -> REJECT
AI_IDENTITY_CONTINUITY_CLAIM -> REJECT
AI_SUBJECTIVITY_CLAIM -> REJECT
```

The executable surface accepts synthetic annotation records only. It does not call a model, observe a person, infer private state, or establish a validation threshold.

## 9. Falsifiers / weakening conditions

The repository-local hypothesis that this crosswalk improves CCTS/subjectivity research discipline should be weakened if:

- explicit statement-role separation does not reduce fact/inference/proposal conflation;
- locus tagging does not improve attribution of Human, memory, artifact, model, and dyad changes;
- relational-continuity controls do not help distinguish externally scaffolded continuity from model/system continuity;
- independent reviewers cannot apply the categories reliably;
- the categories merely add documentation overhead without changing claim admission or error detection;
- a simpler existing external taxonomy provides equal or better discrimination.

## 10. Claim ceiling

```text
SUPPORTED_NOW:
- adjacent literature exists for epistemic co-agency / shared epistemic agency
- relational continuity can be supported by external memory scaffolds
- repository already distinguishes relational continuity from AI identity continuity
- a bounded synthetic evidence-role / locus / continuity annotation contract can be implemented

NOT_ESTABLISHED:
- CCTS causes Human learning
- epistemic co-agency proves AI-internal agency
- relational continuity proves AI identity continuity
- stable identifiers prove a persistent AI self
- AI identity continuity exists in the tested system
- AI subjectivity
- consciousness
- phenomenal experience
```

```text
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
EPISTEMIC_CO_AGENCY_AS_MEASURED_EFFECT = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 11. Sources

- Samuel (2026), *Learning with machines: Toward a theory of epistemic co-agency*, Computers and Education: Artificial Intelligence 10, 100573. DOI: https://doi.org/10.1016/j.caeai.2026.100573
- Wu, J.-Y., Lee, Y.-H., Chai, C. S., & Tsai, C.-C. (2025), *Strengthening Human Epistemic Agency in the Symbiotic Learning Partnership With Generative Artificial Intelligence*, Educational Researcher 54(6), 358–368. DOI: https://doi.org/10.3102/0013189X251333628
- Juan, Y.-C., Lee, Y.-H., & Wu, J.-Y. (2026), *Generative artificial intelligence augments social interactivity and learning outcomes: Advancing the framework of a scaffolded human–GenAI shared agency*, Computers & Education 247, 105564. DOI: https://doi.org/10.1016/j.compedu.2026.105564
- *Caring for the system that cares for me: An autoethnography of designing sustained memory with a stateless conversational AI* (2026), Design and Artificial Intelligence 2(2), 100087. DOI: https://doi.org/10.1016/j.daai.2026.100087
- Repository: `AI_SUBJECTIVITY_HUMAN_AI_LEARNING_AND_QUALITY_VIEW_SYNTHESIS_2026_09_14.md`
- Repository: `HUMAN_AI_BIDIRECTIONAL_GROUNDING_HYPOTHESIS_2026_09_11.md`
- Repository: `PERSONALITY_CONTINUITY_ALZHEIMER_SELF_MODEL_HYPOTHESIS_2026_09_13.md`
