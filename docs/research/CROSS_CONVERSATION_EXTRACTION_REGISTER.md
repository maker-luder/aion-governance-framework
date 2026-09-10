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
| Coupled endogenous affective/motivational channels preceding semantic recognition | `affective-cognitive-motivation_v0.1.0` + `endogenous-goal-dynamics_v0.1.0` | MERGE | Implement bounded deterministic multi-channel coupling, intervention traces and post-hoc self-state recognition while keeping labels out of the generator | NONE | Synthetic tests + ablation/random/reset/holdout follow-up |
| `INTERNAL_STATE_EXISTS != INTERNAL_STATE_IS_RECOGNIZED != INTERNAL_STATE_IS_NAMED` | Affective coupling research extension | MERGE | Keep state generation, self-state inference and semantic labeling as distinct computational stages | NONE | Leakage tests + held-out trajectories |
| Subjectivity evidence methodology | Threat model + QA + purpose anchor | EXTRACT | Add claim ladder, competing hypotheses, preregistration status, negative controls, replication and IV&V gates | NONE | Protocol + result/evidence records |
| Model vs scaffold vs integrated system vs relational locus of subjectivity-relevant evidence | `subjectivity-pipeline_v0.1.0` | MERGE | Add typed evidence-locus admission and explicit preregistered bridge hypotheses; forbid silent cross-level promotion | NONE | Locus unit tests + future matched bridge interventions |
| Observer interpretation vs internal/system evidence | Subjectivity evidence locus gate | MERGE | Treat observer attribution as its own locus and fail closed when it is substituted for an internal-property claim | NONE | Unit tests + evidence records |
| Relationship continuity / interpretation drift | `continuity_governance_v0.1.0` | MERGE | Separate factual, project, role, relational-style and correction-recovery dimensions | NONE | Synthetic fixtures + invariant tests |
| `AIR-STATE-001` | Current state architecture | MERGE | Requalify under present schemas; do not restore unverified historical execution claims | NONE | Traceability review |
| `AIR-TEST-001` | Component tests / QA | MERGE | Rebuild as current test protocol with explicit expected outcomes | NONE | Fresh execution evidence |
| `AIR-AUDIT-001` | Audit / provenance / QA | MERGE | Map legacy audit intent into current provenance and evidence records | NONE | Audit mapping |
| `AIR-THREAT-001` | `SUBJECTIVITY_RESEARCH_THREAT_MODEL.md` + security components | ABSORBED | Maintain crosswalk only; avoid second threat model | NONE | Periodic crosswalk review |
| `AION-CONTINUITY-EXPERIMENT-001` | Continuity governance | MERGE | Reconstruct as synthetic, privacy-safe continuity evaluation | NONE | Fresh execution evidence |
| `LEGACY-ENCOUNTER-SPEC-001` | Identity / lineage / provenance | EXTRACT | Requalify as multi-party encounter protocol | NONE | Schema review + tests before execution binding |
| `ASTRA-POSITION-AUDIT-001` | Astra Workbench | MERGE | Convert to interpretive-governance review criteria rather than parallel runtime | NONE | Workbench traceability |
| `ASTRA-GOV-001` / `ASTRA-DRIFT` / `ASTRA-REVIEW` / `ASTRA-BOUNDARY` | Astra Workbench + continuity governance | MERGE | Add explicit interpretation-governance mapping | NONE | Review checklist |
| Source-role provenance (`USER_ORIGINAL`, `ASSISTANT_PROPOSAL`, `JOINT_CONCLUSION`) | `PROVENANCE.md` + `aion_coupled_quality.provenance` | MERGE | Preserve human origin, AI formalization, joint synthesis, external source and unknown origin as distinct inspectable records; never use provenance as truth or merge authority | NONE | Bounded ledger + attribution-boundary tests |
| Input content silently reinterpreted as the contributor's affect/internal state | Epistemic provenance ledger | MERGE | Separate direct self-report, observed signal, inference and unknown; prohibit inferred state from being rewritten as human-origin self-report | NONE | Negative tests + provenance audit |
| Human–AI sustained epistemic development / epistemic co-agency | `coupled-cognition-quality-factory_v0.1.0` | MERGE | Record a bounded longitudinal research hypothesis centered on question decomposition, counterevidence, revision and transfer rather than answer volume or agreement | NONE | Future longitudinal transfer study; current literature is conceptual/methodological support only |
| Multi-agent / multi-party encounter protocol | Identity + lineage + provenance + runtime | EXTRACT | Keep agent identities, memory namespaces, evidence, authority and tool scopes non-conflated | NONE | Protocol tests before execution binding |
| Shared external blackboard / cross-session coordination and strategic behavior | Multi-party encounter + subjectivity threat/evidence method | ABSORBED | Retain as an engineering coordination class; require source verification for specific external cases and do not promote strategic behavior into subjectivity evidence | NONE | Case-specific provenance + controlled intervention if studied |
| Controlled/random ablation execution | G1 research lab | HOLD | No public execution path while governance hold remains active | NONE | Explicit authorization + protocol + adequate environment |
| 3D embodiment | Twin-genesis lab | HOLD | Non-3D runtime may progress; 3D remains deferred | NONE | Scope/hardware decision |
| Sexual-function / intimate-interaction runtime | Twin / affective research | HOLD | No executable implementation or public exposure | NONE | Explicit future authorization required |

## Source handling rules

1. Conversation-derived material is treated as an **input lead**, not as automatically verified truth.
2. Attribution is only preserved when its source is confirmed; otherwise use `SOURCE_UNVERIFIED` / `UNKNOWN` as appropriate to the target schema.
3. Public reconstruction uses synthetic examples instead of private transcript quotations.
4. Existing governed components are extended rather than duplicated.
5. Historical test claims are never promoted into current PASS evidence without fresh execution.
6. A reconstructed concept remains `canonical_effect=NONE` until the normal project review and promotion process explicitly changes that status.
7. A human-provided article, prompt or example is not evidence of the human contributor's unreported affect or internal state.
8. Model-, scaffold-, system-, relational- and observer-level evidence must not be silently promoted across loci.

## Convergence sequence

`extract -> deduplicate -> source-check -> map to current architecture -> threat review -> implement -> test -> evidence -> review -> optional promotion`

This register is a configuration-management index, not proof that every listed concept is valid, implemented, or canonical.
