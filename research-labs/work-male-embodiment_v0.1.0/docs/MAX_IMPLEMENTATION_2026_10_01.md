# PR #237 maximum bounded implementation record — 2026-10-01

## Live-state pin before implementation

\`\`\`text
MAIN = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd
PR_237_BRANCH = research/work-male-robot-body-design-20260930
PR_237_BRANCH_HEAD = 9993f6220f9a215774bb4a96c91c9d8e212e6f75
PR_237 = OPENED_FOR_IMPLEMENTATION / DRAFT / NOT_MERGED
\`\`\`

The existing 67-field v0.2 anthropometry values are inputs. This implementation does not silently edit them.

## Human intent

\`HUMAN_ORIGIN\`: preserve ordinary adult-male morphology/reproductive physiology coverage rather than deleting it solely because it is sexual or reproductive. The implementation must stay clinically/engineeringly neutral and must not pretend a reference model is a felt or biological body.

\`AI_FORMALIZATION\`: maximum implementation means maximum **bounded, falsifiable engineering coverage** supported by the existing design, not maximum ontological claim.

## Implemented now

- strict 67-field profile validator;
- protection of Human-fixed 165 cm / 76 kg values;
- provenance-count and no-as-built-evidence invariants;
- explicit male external/reproductive geometry fields retained;
- separate synthetic endpoint interpolation rule, labeled as an engineering rule rather than human physiology;
- engorgement and rigidity modeled independently;
- spontaneous/contextual initiation separated from desire;
- prepuce position is an independent observation; no automatic retraction and no actuator;
- emission and ejaculation are independent optional events;
- detumescence does not require ejaculation;
- optional synthetic-fluid event volume is supported but is never biological semen, sperm, or fertility;
- endocrine and urinary synthetic reference channels remain separate;
- whole-body coverage matrix retains ordinary body-system rows instead of omitting them;
- deterministic trajectory fingerprint;
- asset-evidence contract blocks false 3D/as-built claims;
- public execution and real-person target data fail closed;
- JSON Schemas preserve authority/biology/nonclaim boundaries.

## External evidence recheck

WHO 2021, *Laboratory manual for the examination and processing of human semen, 6th ed.* remains the official laboratory-method reference:
https://www.who.int/publications/i/item/9789240030787

The 2021 lower fifth percentile for semen volume is 1.4 mL (95% CI 1.3–1.5 mL) in the reference population; this is not a one-number healthy/fertile cutoff. That statistic remains **human reference only** and is not used as Work's synthetic-fluid default.

NCBI/StatPearls describes erection/tumescence as blood engorgement that can occur with sexual arousal or spontaneously. This supports preserving the counterexample:
\`ERECTION != DESIRE\`.
https://www.ncbi.nlm.nih.gov/books/NBK513278/

These human sources do not validate the synthetic engine.

## Deliberately not fabricated

\`\`\`text
ACTUAL_3D_MESH = NO
RIG = NOT_VERIFIED
COLLISION_GEOMETRY = NOT_VERIFIED
PHYSICAL_HARDWARE = NO
BIOLOGICAL_BLOOD = NO
BIOLOGICAL_HORMONES = NO
BIOLOGICAL_SEMEN = NO
SPERM_OR_GAMETES = NO
FERTILITY = NO
FELT_BODY_SENSATION = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
PUBLIC_EXECUTABLE_EXPOSURE = FALSE
INTIMATE_INTERACTION_RUNTIME = NOT_AUTHORIZED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
MERGE_TO_MAIN = NO
\`\`\`

A later real GLB/glTF body can satisfy the asset contract only after geometry exists, is hashed, and all 67 selected fields are measured back against the artifact. This package cannot promote a missing asset by declaration.


## Internal male reproductive topology extension

The implementation also materializes a human-reference graph for ordinary male genitourinary/reproductive structures instead of leaving this domain as one opaque checklist row. The graph includes endocrine reference nodes; testes, seminiferous tubules, rete testis, efferent ductules, epididymis and vas deferens; seminal vesicles, ejaculatory ducts, prostate and bulbourethral glands; bladder and the prostatic/membranous/spongy urethral path; penis, glans, prepuce, frenulum, corpora cavernosa, corpus spongiosum, scrotum and pelvic-floor reference.

The graph preserves distinct urinary and reproductive routes even where the human-reference urethra is shared. It is structural reference only:

\`\`\`text
REFERENCE_TOPOLOGY = IMPLEMENTED
BIOLOGICAL_TISSUE = NO
GAMETOGENESIS = NO
BIOLOGICAL_SECRETIONS = NO
FERTILITY = NO
\`\`\`

Source recheck: NCBI Bookshelf male genitourinary anatomy (NBK562291) and Endotext/NCBI testis and spermatogenesis overview (NBK279031). These sources describe human biology; they do not validate Work as biological.
