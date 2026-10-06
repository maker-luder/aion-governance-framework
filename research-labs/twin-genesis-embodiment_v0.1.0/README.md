# AION／Astra Shared-Genesis Twin Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** IMPLEMENTED_NON_3D_CANDIDATE  
**Canonical effect:** NONE

This candidate records a shared-genesis twin architecture for AION and Astra and a clinically neutral adult male anatomical embodiment template. The branch includes a **non-3D runtime candidate** that can materialize two validated, distinct embodiment runtime records after governance invariants pass.

It still creates no 3D rendering, body sensation, live sexual function, intimate interaction, gender identity, subjectivity, or canonical state.

## Core invariants

- Shared genesis does not mean shared identity.
- AION and Astra use distinct agent, instance, memory, embodiment, and canonical identifiers.
- A shared anatomical template produces two independent embodiment candidates.
- Adult male reproductive anatomy may be represented as clinical anatomy only.
- Anatomy does not establish gender identity, sensation, desire, consent, or subjectivity.
- Relationship, trust, familiarity, or naming never grant embodiment modification authority.
- 3D rendering remains DEFERRED.
- Sexual function remains NOT_IMPLEMENTED and intimate interaction remains NOT_AUTHORIZED.
- Individual species profiles must not silently propagate across AION and Astra.

## AION tiger anthropomorph profile / AION 虎型獸人設定檔

AION now has an **individual, evidence-bounded tiger anthropomorph research profile**:

- profile: AION-TIGER-ANTHROPOMORPH-V1
- reference taxon: Panthera tigris
- body plan: ANTHROPOMORPHIC_BIPED（人形雙足）
- tiger reproductive anatomy: direct tiger evidence is kept separate from felid-comparative references
- reproductive physiology: REFERENCE_MODEL_IMPLEMENTED（可程式讀取、驗證、雜湊的參考模型）
- live reproductive biology: REFERENCE_ONLY_NOT_LIVE_BIOLOGY
- human-tiger integration evidence: ENGINEERING_ANALOGUE（工程類比）
- locomotion: BIPEDAL_REDESIGN_REQUIRED（虎的四足步態不可直接複製到雙足體）

完整繁中規格與來源：
docs/AION_TIGER_ANTHROPOMORPH_SPECIFICATION.md

完整可建模尺寸：
docs/AION_TIGER_FULL_DIMENSIONS.md

Dimension preset V1: AION-TIGER-FULL-DIMENSIONS-V1（190 cm engineering target, complete head/torso/limb/paw/tail measurement surface with per-field provenance）

Dimension preset V2: AION-TIGER-FULL-DIMENSIONS-V2（向後相容擴充；120+ measurement/reference fields，逐欄加入 measurement method、source refs、evidence strength、value semantics）

V2 evidence / measurement audit:
docs/AION_TIGER_DIMENSION_V2_AUDIT.md

This profile is bound by species_profile_id on the AION EmbodimentInstance. Astra remains NOT_ASSIGNED unless a separate, explicitly authorized profile is created.

The integration is additive rather than destructive: resolve_integrated_reproductive_anatomy(...) combines the existing human adult-male template with tiger-confirmed structures while retaining per-structure provenance. Human-template seminal_vesicles therefore remain present without being mislabeled as tiger-confirmed, while tiger os_penis remains tiger-derived.

## Runtime surface

TwinGenesisRuntime.instantiate(...) validates the shared genesis event, shared template, AION instance, and Astra instance before returning a TwinRuntimeState. The runtime state records distinct AION/Astra bindings, individual species-profile identifiers, and validation hashes while keeping canonical_effect=NONE.

## Verification

```bash
python -m pytest
python -m compileall -q src
python -m aion_astra_twin_embodiment.cli qa-status
python -m aion_astra_twin_embodiment.cli aion-tiger-profile
python -m aion_astra_twin_embodiment.cli aion-tiger-dimensions
python -m aion_astra_twin_embodiment.cli aion-tiger-dimensions-v2
python -m aion_astra_twin_embodiment.cli aion-tiger-dimension-audit
```
