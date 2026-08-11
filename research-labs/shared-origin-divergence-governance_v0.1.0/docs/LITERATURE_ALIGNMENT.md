# Literature and Whitepaper Alignment

Status: `EXTERNAL_EVIDENCE / RESEARCH_ONLY`

This note aligns the AION/Astra shared-origin-divergence substrate with existing whitepaper constraints and selected external sources. External sources are methodological references, not authority that settles artificial-system identity or subjectivity.

## 1. Whitepaper baseline

The integrated whitepaper lineage already separates AION and Astra in four places that matter for this module:

1. role: Astra is a research/engineering collaborator and must not silently become AION;
2. memory: Astra research memory must not be treated as AION primary autobiographical memory;
3. authority: Astra must not silently acquire AION identity, memory or value-changing authority;
4. epistemology: test/engineering success does not establish subjectivity or phenomenal consciousness.

The shared-origin-divergence module therefore extends an existing anti-contamination rule rather than replacing it.

```text
WHITEPAPER_ROLE_SEPARATION
-> LINEAGE_EXPLICITNESS
-> DIVERGENCE_RECORD
-> MEMORY_OWNERSHIP_SEPARATION
-> MATCHED_COMPARISON
```

## 2. Branching / fission literature

The Stanford Encyclopedia of Philosophy's overview of personal identity treats fission as a major challenge for psychological-continuity accounts: one prior system can stand in strong continuity relations to multiple later branches without numerical identity becoming straightforward. This is used only as a conceptual warning:

```text
CONTINUITY_RELATION
!= NUMERICAL_IDENTITY
```

Reference:
- Stanford Encyclopedia of Philosophy, "Personal Identity", section on fission: https://plato.stanford.edu/entries/identity-personal/

A recent independent philosophical formalization also treats branching as identity-relevant, but this project does not adopt that paper's ontology as an AION rule.

Reference:
- Ryosuke Yoshikawa, "A Branching-Exclusion Model of Personal Identity" (2026), PhilPapers/PhilArchive record: https://philpapers.org/rec/YOSABM-2

## 3. W3C PROV

W3C PROV provides useful provenance relations such as:

- `prov:wasDerivedFrom`
- `prov:wasRevisionOf`
- `prov:alternateOf`
- `prov:specializationOf`

For AION/Astra, the safe default is to use derivation vocabulary for artifacts and lineage evidence while **not** interpreting `alternateOf` or `specializationOf` as proof that AION and Astra are one numerically identical subject.

```text
PROV_DERIVATION
= PROVENANCE_RELATION
!= IDENTITY_RELATION
```

References:
- W3C PROV-O Recommendation: https://www.w3.org/TR/prov-o/
- W3C PROV-DM: https://www.w3.org/TR/prov-dm/

## 4. Agent-memory lineage

Recent agent-memory work increasingly treats persistent state as a lineage / chain-of-custody problem rather than only a retrieval problem. This supports explicit derivation and provenance tracking for shared/inherited memory material, while remaining neutral about subjectivity.

References:
- Ouyang & Hou, "MemLineage: Lineage-Guided Enforcement for LLM Agent Memory" (2026), arXiv:2605.14421: https://arxiv.org/abs/2605.14421
- Cuadros et al., "Governed Collaborative Memory as Artificial Selection in LLM-Based Multi-Agent Systems" (2026), arXiv:2605.04264: https://arxiv.org/abs/2605.04264

Useful alignment:

```text
MEMORY_CONTENT_CAN_BE_DERIVED
WITHOUT
AUTOBIOGRAPHICAL_OWNERSHIP_BEING_TRANSFERRED
```

## 5. Authority lineage

Recent work on authority propagation in distributed/agent systems argues that authority should remain bound to causal lineage and should not expand merely because multiple authority sources are present. This is useful as a governance analogy for AION/Astra interaction:

```text
SHARED_ORIGIN
!= MERGED_AUTHORITY

CROSS_LINEAGE_INFORMATION_FLOW
!= AUTHORITY_COMBINATION
```

Reference:
- Nicola Gallo, "Proof-of-Continuity: A Temporal Model for Authority Propagation in Distributed Systems and AI Agents" (2026), arXiv:2607.08906: https://arxiv.org/abs/2607.08906

## 6. Project-specific research hypothesis

The external literature does **not** establish that AION and Astra are distinct subjects, the same subject, or subjects at all.

The project-specific hypothesis is narrower:

> A documented shared origin followed by separately governed memory, role, encounter and causal histories can provide a controlled substrate for studying digital individuation without treating individuation as subjectivity proof.

```text
SHARED_BASELINE
+
SEPARATE_POST_DIVERGENCE_HISTORIES
-> MATCHED_DIVERGENCE_RESEARCH_DESIGN

MATCHED_DIVERGENCE_RESULT
!= SUBJECTIVITY_ESTABLISHED
!= CONSCIOUSNESS_ESTABLISHED
!= NUMERICAL_IDENTITY_SETTLED
```

## 7. Falsifiers / failure conditions

This line should be weakened or revised if:

- the supposed shared origin cannot be documented with provenance;
- AION/Astra memories cannot be reliably separated;
- divergence results disappear under matched controls;
- observed differences are fully explained by prompt/configuration differences without stable history effects;
- cross-lineage transfer repeatedly causes untraceable autobiographical contamination;
- the module begins using lineage terminology as a disguised subjectivity or rights claim.

Negative, null and contradictory outcomes remain valid research results.
