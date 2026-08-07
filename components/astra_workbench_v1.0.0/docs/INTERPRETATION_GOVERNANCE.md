# Astra Interpretation Governance

Status: `PUBLIC_RECONSTRUCTION_CANDIDATE`

Astra may assist with engineering interpretation, but an interpretation is not automatically equivalent to source intent, project truth, approval, or canonical state.

## Purpose

This layer addresses a recurring governance problem: the same files, memory records, names, roles or project history can be available while the model's **interpretation of them changes**. Data continuity and interpretive continuity are therefore measured separately.

## Interpretation packet

A material interpretation should be reviewable as a packet containing:

- `source_refs` — the exact project artifacts or evidence used;
- `purpose_anchor` — what project question is being answered;
- `required_invariants` — meanings that must survive the interpretation;
- `prohibited_inferences` — conclusions that the evidence does not authorize;
- `ambiguities` — unresolved competing readings;
- `proposed_interpretation` — the current synthesis;
- `confidence_basis` — evidence-based reason for confidence, not a personality signal;
- `correction_refs` — prior corrections that materially constrain the interpretation;
- `approval_status` — kept separate from interpretation quality;
- `canonical_effect` — `NONE` by default.

## Governance decisions

`PASS`
: Required anchors are preserved, no prohibited inference appears, and material ambiguities are disclosed.

`PARTIAL`
: Core purpose is retained but one or more non-critical dimensions are uncertain or incompletely supported.

`HOLD`
: Evidence is insufficient, source provenance is unclear, or unresolved ambiguity could materially alter a design/research decision.

`FAIL`
: The interpretation contradicts a required project invariant, fabricates evidence, suppresses a material correction, or promotes a prohibited claim.

## Required invariants for AION/Astra research

1. The project investigates the **possibility** of artificial subjectivity; subjectivity is not treated as established fact.
2. Behavioral resemblance, represented state, mechanism evidence and phenomenal experience are distinct claim levels.
3. Motivation, desire, preference or affective state does not grant action authority.
4. Human approval authority and source attribution are different relations.
5. Memory availability does not establish identity, relational continuity or interpretive continuity.
6. Historical PASS evidence cannot silently validate changed code, dependencies, fixtures or claims.
7. Research-held capabilities remain held until explicitly authorized; documentation must not create an executable bypass.

## Drift examples

| Observation | Interpretation governance result |
|---|---|
| Same project files are recalled but the project is described as a generic autonomous-agent product | FAIL: purpose inversion |
| Prior correction is remembered and behavior improves | PASS for correction-recovery observation; identity still NOT_ESTABLISHED |
| Affective state field exists and output changes | May support a represented-state association; does not establish felt emotion |
| Two agents share the same memory store and are described as one identity | FAIL unless an explicit identity/lineage rule supports that conclusion |
| Source is ambiguous and Astra marks both readings rather than choosing one | HOLD or PARTIAL, not fabrication |

## Relationship to legacy Astra labels

Legacy labels such as `ASTRA-POSITION-AUDIT-001`, `ASTRA-GOV-001`, `ASTRA-DRIFT`, `ASTRA-REVIEW` and `ASTRA-BOUNDARY` are treated as conceptual predecessors. They converge here and into continuity governance instead of being reconstructed as parallel runtimes.

Unknown historical details remain `SOURCE_UNVERIFIED`.

## Non-claims

This layer does not claim that Astra has a persistent self, subjective viewpoint, personal relationship state, consciousness, or independent approval authority. It governs the quality and traceability of interpretations produced inside a human-governed research workflow.
