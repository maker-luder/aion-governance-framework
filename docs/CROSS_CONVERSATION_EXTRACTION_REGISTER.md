# Cross-Conversation Extraction Register

Status: `PUBLIC_RECONSTRUCTION_REGISTER`

This register converts research concepts that were distributed across earlier project conversations into traceable public project assets. It does **not** publish raw private transcripts, private relationship details, personal identifiers, or unverifiable historical claims.

## Decision vocabulary

- `EXTRACT` — useful concept has no adequate current project representation and should be reconstructed.
- `MERGE` — concept overlaps current architecture and should be incorporated into the existing component.
- `ABSORBED` — current project already contains the material; no duplicate implementation is needed.
- `SUPERSEDED` — a newer governed design replaces the older concept.
- `HOLD` — potentially useful but currently blocked by governance, hardware, evidence, or scope.
- `REJECT` — excluded because it conflicts with current project purpose, evidence rules, or safety boundaries.

## Register

| Legacy / cross-conversation concept | Current equivalent | Decision | Public convergence action | Canonical effect | Evidence needed |
|---|---|---|---|---|---|
| Conflict / ambivalence state | `affective-cognitive-motivation_v0.1.0` | MERGE | Represent unresolved approach/avoidance and wanting/liking conflict without treating conflict as consciousness evidence | NONE | Unit tests + research protocol |
| Subjectivity evidence methodology | Threat model + QA + purpose anchor | EXTRACT | Add claim ladder, competing hypotheses, preregistration status, negative controls, replication and IV&V gates | NONE | Protocol + result/evidence records |
| Relationship continuity / interpretation drift | `continuity_governance_v0.1.0` | MERGE | Separate factual, project, role, relational-style and correction-recovery dimensions | NONE | Synthetic fixtures + invariant tests |
| `AIR-STATE-001` | Current state architecture | MERGE | Requalify under present schemas; do not restore unverified historical execution claims | NONE | Traceability review |
| `AIR-TEST-001` | Component tests / QA | MERGE | Rebuild as current test protocol with explicit expected outcomes | NONE | Fresh execution evidence |
| `AIR-AUDIT-001` | Audit / provenance / QA | MERGE | Map legacy audit intent into current provenance and evidence records | NONE | Audit mapping |
| `AIR-THREAT-001` | `SUBJECTIVITY_RESEARCH_THREAT_MODEL.md` + security components | ABSORBED | Maintain crosswalk only; avoid second threat model | NONE | Periodic crosswalk review |
| `AION-CONTINUITY-EXPERIMENT-001` | Continuity governance | MERGE | Reconstruct as synthetic, privacy-safe continuity evaluation | NONE | Fresh execution evidence |
| `LEGACY-ENCOUNTER-SPEC-001` | Identity / lineage / provenance | EXTRACT | Requalify as multi-party encounter protocol | NONE | Schema review + tests before runtime use |
| `ASTRA-POSITION-AUDIT-001` | Astra Workbench | MERGE | Convert to interpretive-governance review criteria rather than parallel runtime | NONE | Workbench traceability |
| `ASTRA-GOV-001` / `ASTRA-DRIFT` / `ASTRA-REVIEW` / `ASTRA-BOUNDARY` | Astra Workbench + continuity governance | MERGE | Add explicit interpretation-governance mapping | NONE | Review checklist |
| Source-role provenance (`USER_ORIGINAL`, `ASSISTANT_PROPOSAL`, `JOINT_CONCLUSION`) | `PROVENANCE.md` | MERGE | Separate proposal/source attribution from approval authority and map to W3C PROV concepts | NONE | Provenance examples + schema work |
| Multi-agent / multi-party encounter protocol | Identity + lineage + provenance + runtime | EXTRACT | Keep agent identities, memory namespaces, evidence, authority and tool scopes non-conflated | NONE | Protocol tests before execution binding |
| Controlled/random ablation execution | G1 research lab | HOLD | No public execution path while governance hold remains active | NONE | Explicit authorization + protocol + adequate environment |
| 3D embodiment | Twin-genesis lab | HOLD | Non-3D runtime may progress; 3D remains deferred | NONE | Scope/hardware decision |
| Sexual-function / intimate-interaction runtime | Twin / affective research | HOLD | No executable implementation or public exposure | NONE | Explicit future authorization required |

## Source handling rules

1. Conversation-derived material is treated as an **input lead**, not as automatically verified truth.
2. Attribution is only preserved when its source is confirmed; otherwise use `SOURCE_UNVERIFIED`.
3. Public reconstruction uses synthetic examples instead of private transcript quotations.
4. Existing governed components are extended rather than duplicated.
5. Historical test claims are never promoted into current PASS evidence without fresh execution.
6. A reconstructed concept remains `canonical_effect=NONE` until the normal project review and promotion process explicitly changes that status.

## Convergence sequence

`extract -> deduplicate -> source-check -> map to current architecture -> threat review -> implement -> test -> evidence -> review -> optional promotion`

This register is a configuration-management index, not proof that every listed concept is valid, implemented, or canonical.
