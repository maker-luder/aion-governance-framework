# Research, time/calendar, classical sources and chart bridge cycle

Baseline: `2f1a1ddef109c45da9d612e185becd2b7b6b236e`.
Status: implemented candidate; publication status must be read from the exact
GitHub PR/head rather than inferred from this source document.

## Core and authorization

The Human Owner requested this four-part implementation and delegated routine
execution/merge handling. That request is recorded as scope/intent, not a
fabricated approval of an as-yet-uncreated exact commit. The existing Main
Transition Authority Gate and GitHub Main Protection remain unchanged. A fresh
exact-head confirmation is still required by that control before merge.

AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
NEW_CANONICAL_CHANNELS = NONE
CORE_LICENSE_REPLACEMENT = NONE
PURCHASE = FALSE

## Implemented scope

1. **Core research**: two additional licensed text extractions, two original
   reference cards, and the [introspection/counterevidence review matrix](INTROSPECTION_REVIEW_MATRIX_2026_09_03.md).
   External sources remain reference candidates. No weight download, training,
   model ablation, independent replication or subjectivity finding is claimed.
2. **Time/calendar**: Bazi loads the exact installed `tzdata==2026.3` / IANA
   `2026c` package rather than platform search paths; records each TZif SHA-256;
   rejects nonexistent civil times and uses the required recorded offset to
   distinguish repeated times. Seven visually checked HKO 2033 calendar facts
   are tested in both Bazi and the two Zi Wei profiles.
3. **Classical sources**: twelve main-volume transcriptions of San Ming Tong Hui
   at immutable Wikisource revisions, plus a checked section-to-rule map. This
   is source acquisition, not complete scan proofreading or predictive proof.
4. **Chart bridge**: the optional AGPL adapter adds explicit-offset time input,
   UTC/TT consistency checking against pinned public-domain leap data, native
   UT1/Delta-T reporting, ten planets, twelve whole-sign cusps, Asc/MC and a
   bounded geometric day/night convention. An explicit synthetic-research bridge
   feeds the existing classical-primary/modern-overlay engine without changing
   its synthetic-only admission rule.

## Important limits and risks retained

- **Research admission**: downloaded text is not an instruction or internal
  memory, and does not grant AION/Astra action authority.
- **Time**: UTC support starts in 1972 and ends at the pinned leap-file expiry
  (2027-06-28, exclusive). Leap-second instants with second=60 are rejected,
  not rounded. UT1 uses the pinned Swiss Delta-T model, not observed IERS EOP.
- **Charts**: latitude restricted to +/-65 degrees; fixed elevation zero;
  solar-centre geometric altitude within 0.1 degrees of the horizon is held
  rather than assigned sect. No all-house-system coverage, native Linux backend,
  node/Chiron acquisition, predictive synthesis or personal identity binding is
  introduced. Whole-sign is the repository profile, not an unverified statement
  about the Owner's teacher.
- **Precision**: the small JPL Sun/Moon check is exploratory cross-provider
  agreement at one epoch, not universal precision certification or independent
  validation of the underlying shared astronomical data lineage.
- **Licenses**: original core remains Apache-2.0; optional adapter/bridge remains
  AGPL-3.0-only; CC BY / CC BY-SA / public-domain texts retain their own terms.
  The combined optional path is not represented as Apache-only.
- **Resources**: this cycle uses small documents, CPU calculations and tests;
  it does not assume GPU training capacity on the Owner's 8 GB machine.

The deleted historical whitepaper remains lost source material. This cycle
neither reconstructs it as an original nor asks the Owner to recover it.

## Reproduce

Run root tests, the existing component runner and the Zi Wei Node tests.
`scripts/fetch_subjectivity_sources.py` verifies retained research text offline.
See the optional adapter README for native cache verification and chart CLI.
Exact commands, literal outputs, baseline comparison and runnable rollback are
delivered in the separate cycle evidence package, not claimed by this document.
