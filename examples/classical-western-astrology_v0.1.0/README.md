# Classical Western Astrology Capability Example v0.1.0

This is an offline, deterministic fact-derivation example for **classical Western astrology**, with a deliberately narrow Hellenistic/medieval common-core profile.

Its primary surface is:

- the seven traditional planets: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn;
- tropical zodiac;
- whole-sign houses;
- the five classical aspects: conjunction, sextile, square, trine, opposition;
- day/night sect, without guessing Mercury's sect from incomplete data;
- sign-based domicile, exaltation, detriment, and fall.

It does not calculate a high-precision ephemeris in v0.1.0. Instead, it accepts already-calculated geocentric tropical longitudes together with an exact ephemeris source and version, then produces deterministic and hash-bound chart facts. This keeps astronomical calculation provenance separate from astrological rule derivation.

Only synthetic fixtures are accepted in v0.1.0. No real birth record is included.

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

## Boundary

The component derives inspectable chart facts. It does not infer personality, fate, health, compatibility, financial outcomes, identity, subjectivity, permissions, or governance authority. See [`docs/CLASSICAL_RULE_PROFILE.md`](docs/CLASSICAL_RULE_PROFILE.md), [`docs/DERIVATION_AND_EPHEMERIS_BOUNDARY.md`](docs/DERIVATION_AND_EPHEMERIS_BOUNDARY.md), and [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md).
