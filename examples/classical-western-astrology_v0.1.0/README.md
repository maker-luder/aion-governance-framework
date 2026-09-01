# Classical-complete / Modern-overlay Western Astrology Example v0.3.0

This is an offline, deterministic Western-astrology fact-derivation example. The
classical Hellenistic/medieval common-core profile remains intact and primary;
v0.2.0 added a separately labelled modern overlay rather than silently replacing
traditional rulers or classical dignity/sect rules.

Its primary surface is:

- the seven traditional planets: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn;
- tropical zodiac;
- whole-sign houses;
- the five classical aspects: conjunction, sextile, square, trine, opposition;
- day/night sect, without guessing Mercury's sect from incomplete data;
- sign-based domicile, exaltation, detriment, and fall.

The integrated v0.2.0 profile additionally exposes:

- Uranus, Neptune, and Pluto as modern-overlay bodies;
- modern rulerships alongside, never in place of, traditional rulerships;
- element, modality, and polarity for every tropical sign;
- six versioned minor aspects (semisextile, semisquare, quintile,
  sesquisquare, biquintile, and quincunx);
- direct, retrograde, or stationary motion from an explicit longitude-speed
  vector; and applying/separating aspect phase only when both speeds exist.

The v0.3.0 completion layer adds, without rewriting the v0.2 chart:

- day/night/participating triplicity rulers under a named Dorothean profile;
- all twelve complete Egyptian-bound tables with half-open degree intervals;
- all thirty-six Chaldean faces/decans;
- the seven traditional planetary joys as whole-sign-house facts;
- true north/south lunar nodes and Chiron as modern **points**, never silently
  promoted to planets, classical dignities, sect members, or sign rulers;
- point-to-body and point-to-point aspects under the existing versioned orb
  profile; and
- one composed `build_integrated_completion(...)` result with deterministic
  provenance and explicit non-claim fields.

It does not calculate a high-precision ephemeris. Instead, it accepts
already-calculated geocentric tropical longitudes and optional speed vectors
together with an exact ephemeris source/version, then produces deterministic,
hash-bound facts. The fetched source manifest records JPL Horizons and Swiss
Ephemeris as provider references; Swiss Ephemeris is not vendored or added as a
dependency because its AGPL/professional dual-license choice must be decided
before integration.

Only synthetic fixtures are accepted. No real birth record is included.

```text
INTERPRETATION_STATUS = NOT_PERFORMED
PREDICTIVE_VALIDITY = NOT_ESTABLISHED
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
AGENT_ASTROLOGY_BINDING = NOT_CREATED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
ACTION_AUTHORITY = NONE
```

## Run the focused suite

From the repository root, use the repository-native multi-component source discovery:

```powershell
& 'C:\A15\venv\Scripts\python.exe' -c "from pathlib import Path; from scripts.run_component_tests import discover_source_roots, run_component_tests; root=Path.cwd(); target=root/'examples'/'classical-western-astrology_v0.1.0'; result=run_component_tests([target], root, discover_source_roots(root))[0]; raise SystemExit(result['returncode'])"
```

## Print the synthetic reference chart

After installing the package in editable mode, the module prints canonical JSON containing the derived chart facts and SHA-256 receipt:

```powershell
python -m pip install -e .\examples\classical-western-astrology_v0.1.0
python -m aion_astra_classical_astrology
```

## Source acquisition

`..\..\scripts\fetch_astrology_bazi_sources.py` has an exact URL allowlist.
It vendors the public-domain Project Gutenberg witnesses, and downloads/hashes
then discards references whose redistribution status was not established. See
[`sources/SOURCE_FETCH_MANIFEST.json`](sources/SOURCE_FETCH_MANIFEST.json) and
[`sources/README.md`](sources/README.md).

## Boundary

The component derives inspectable chart facts. It does not infer personality,
fate, health, compatibility, financial outcomes, identity, subjectivity,
permissions, or governance authority. See
[`docs/CLASSICAL_RULE_PROFILE.md`](docs/CLASSICAL_RULE_PROFILE.md),
[`docs/WESTERN_ASTROLOGY_FUSION_PROFILE.md`](docs/WESTERN_ASTROLOGY_FUSION_PROFILE.md),
[`docs/CLASSICAL_MODERN_COMPLETION_PROFILE.md`](docs/CLASSICAL_MODERN_COMPLETION_PROFILE.md),
[`docs/DERIVATION_AND_EPHEMERIS_BOUNDARY.md`](docs/DERIVATION_AND_EPHEMERIS_BOUNDARY.md),
and [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md).
