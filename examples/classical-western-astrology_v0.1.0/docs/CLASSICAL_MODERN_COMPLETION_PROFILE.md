# Classical-complete / modern-overlay profile v0.3.0

## Composition rule

```text
V0_2_CLASSICAL_PRIMARY_CHART
+ V0_3_EXTENDED_CLASSICAL_FACTS
+ V0_3_LABELLED_MODERN_POINTS
= V0_3_INTEGRATED_COMPLETION
```

The classical layer stays primary. The modern overlay never replaces the
traditional seven, traditional domicile rulers, sect, or classical dignity
tables.

## Completed classical fact surface

| Layer | Named rule profile | Derived result |
|---|---|---|
| Triplicity | Dorothean day/night/participating | sect ruler, participating ruler, ruler match |
| Bounds/terms | Egyptian bounds | one ruler from a gap-free half-open degree interval |
| Faces/decans | Chaldean faces | one ruler for each ten-degree segment |
| Planetary joys | traditional seven-house table | joy house and present-house match |

These facts extend, rather than replace, domicile, exaltation, detriment, fall,
sect, whole-sign houses, and Ptolemaic aspects already present in v0.2.

`EGYPTIAN_BOUNDS != PTOLEMAIC_TERMS`. The implementation names the selected
table and does not imply that historical schools used one interchangeable table.

## Modern overlay completion

The v0.3 point set is exactly:

```text
TRUE_NORTH_NODE
CHIRON
```

`TRUE_SOUTH_NODE` is derived as the exact opposite of the supplied true north
node. All three are typed as modern points. They receive:

- tropical sign and degree;
- whole-sign house;
- motion status when a speed vector exists; and
- aspects under the versioned integrated aspect/orb table.

They do not receive classical dignity, classical sect, or sign rulership. The
source ephemeris remains upstream input with exact provider/version provenance.

## Interpretation and research boundary

```text
RULE_TABLE_FACT != EMPIRICAL_VALIDATION
SYMBOLIC_POINT != PLANET
MODERN_OVERLAY != CLASSICAL_REPLACEMENT
ASTROLOGY_OUTPUT != AI_SUBJECTIVITY_EVIDENCE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
ACTION_AUTHORITY = NONE
```

Personality synthesis, prediction, medical/financial decision support,
compatibility judgments, progressions, returns, directions, and transits remain
outside this deterministic completion profile.

## Sources

The pinned William Lilly transcription is the directly retained traditional
cross-check for terms/faces/planetary joys. Project Gutenberg Ptolemy, the
Dorotheus and Valens link registers, Sepharial, Alan Leo, Swiss Ephemeris, and
JPL Horizons are all recorded with URL, byte count, SHA-256, retention policy,
and acquisition status in `../sources/SOURCE_FETCH_MANIFEST.json`.
