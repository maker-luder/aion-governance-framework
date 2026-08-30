# Classical-primary / Modern-overlay Profile v0.2.0

`CLASSICAL_PRIMARY_MODERN_OVERLAY_V2` is an explicit fusion profile. It retains
the traditional seven, tropical zodiac, whole-sign houses, Ptolemaic aspects,
sect, and sign-based classical dignities, then adds modern facts in labelled
fields.

| Surface | Classical-primary value | Modern-overlay value |
|---|---|---|
| Bodies | Sun through Saturn | Uranus, Neptune, Pluto |
| Rulership | Traditional ruler is always retained | Scorpio/Pluto, Aquarius/Uranus, Pisces/Neptune are additional |
| Dignity | Domicile, exaltation, detriment, fall for traditional seven | `NOT_APPLICABLE_TO_CLASSICAL_DIGNITY` for outer planets |
| Sect | Traditional seven only | `NOT_APPLICABLE_TO_CLASSICAL_SECT` for outer planets |
| Aspects | 0, 60, 90, 120, 180 degrees | 30, 45, 72, 135, 144, 150 degrees |
| Motion | Upstream longitude speed | Direct/retrograde/stationary; missing speed remains unresolved |
| Phase | Derived from a small forward step only when both speed vectors exist | Applying/separating/indeterminate |
| Signs | Tropical sign | Element, modality, polarity |

The profile does not assert that all classical or modern schools agree on
orbs, house systems, rulership, dignities, or interpretation. It preserves
these as versioned engineering rules and source-labelled facts. Quadrant house
cusps, asteroids, nodes, midpoints, harmonics, progressions, and interpretive
synthesis remain outside this calculation release.

Source families and exact acquisition hashes are recorded in
[`../sources/SOURCE_FETCH_MANIFEST.json`](../sources/SOURCE_FETCH_MANIFEST.json).

