# Derivation and Ephemeris Boundary

The v0.1.0 component deliberately separates two layers.

## Upstream astronomical layer

The caller supplies:

- geocentric tropical ecliptic longitude of date for each traditional planet;
- Ascendant and Midheaven longitudes;
- a day/night determination;
- exact ephemeris source and version;
- UTC event timestamp and synthetic location metadata.

The component does not claim that these values were independently recomputed or validated against a second ephemeris.

## Local deterministic rule layer

The component derives:

- sign and degree within sign;
- whole-sign house from the Ascendant sign;
- sign ruler;
- major sign-based dignity/debility labels;
- day/night sect status, leaving Mercury unresolved without solar phase;
- classical aspects within explicit per-aspect orbs;
- a canonical SHA-256 derivation receipt.

Applying/separating phase is `NOT_DERIVED_WITHOUT_SPEED_VECTORS`. Interpretation is `NOT_PERFORMED`.
