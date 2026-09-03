# Optional Swiss Ephemeris positions and bounded chart bridge — AGPL-3.0-only

This entire example's original adapter code and tests are **AGPL-3.0-only**.
See [LICENSE](LICENSE), [UPSTREAM_NOTICE.txt](UPSTREAM_NOTICE.txt), and the
[repository license scope](../../docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md).
It is deliberately not imported by the Apache-2.0 core. This is a license-labelled
optional integration, not an assertion that process separation bypasses AGPL.

## What it does

- Calls the pinned upstream Windows x64 standalone executable offline.
- Requires exact SHA-256 and size checks for all seven cached files before execution.
- Returns Sun through Pluto longitudes/speeds at an explicit **TT Julian day**,
  with native command/output, version, data hashes and non-claim fields.
- Rejects native failure, warnings, reported Moshier fallback, epoch/version drift,
  duplicate/missing planets and non-finite output. No automatic fallback.
- Limits the supported input envelope to JD TT 2400000 through 2500000.

Version 0.2.0 adds a separate `chart` operation: explicit civil UTC offset,
UTC -> TT/UT1, ten planets, Asc/MC, twelve whole-sign cusps and bounded day/night
sect. The original `calculate` TT-position contract is unchanged. CLI coordinates
have seven decimal degrees; this is not independent precision certification.
No Chiron/node acquisition, arbitrary house system, predictive synthesis,
personal binding or public service is added. This component creates no research
loop, canonical state or agent goal.

## Run on Windows x64 with Python 3.11+

From the repository root, install the local, separately licensed example:

```powershell
python -m pip install ./examples/swiss-ephemeris-agpl_v0.1.0
python -m aion_swiss_ephemeris fetch --cache C:/AION-cache/swiss
python -m aion_swiss_ephemeris verify --cache C:/AION-cache/swiss
python -m aion_swiss_ephemeris calculate --cache C:/AION-cache/swiss --jd-tt 2451545
python -m aion_swiss_ephemeris chart --cache C:/AION-cache/swiss --datetime 2000-01-01T20:00:00+08:00 --latitude 25.033 --longitude 121.5654
```

`fetch` is the only network operation; it contacts immutable public upstream URLs
without credentials. Existing valid files are reused; mismatched files are not
overwritten. Keep the cache outside the repository. `calculate` performs no
download and launches only the hash-verified executable with explicit arguments.
No shell string, user-provided program or automatic system configuration is used.
The selected native binary requires Windows x64. Parser/contract tests are portable.

## Explicit chart and research-bridge boundaries

- Use an ISO datetime with seconds and an explicit offset or `Z`. IANA wall-time
  normalization is a separate caller step; the Bazi adapter now provides a
  pinned-package resolver that rejects DST gaps and resolves folds by offset.
- `leap-seconds.list` is an unmodified public-domain IANA 2026c snapshot, SHA-256
  `db5a895f16853b03bfc865e8d68f9fc8710ef1740e3400c701cd46a5bbbc3433`.
  Source: https://data.iana.org/time-zones/tzdb-2026c/leap-seconds.list.
  UTC support is 1972-01-01 through 2027-06-28 exclusive (file expiry).
  Second=60 input is rejected, not rounded; UTC-as-UT fallback is rejected by
  checking native TT against this independent leap-table conversion.
- UT1 is derived from the pinned Swiss Delta-T model, not measured IERS EOP.
  Unreviewed native time override files and `SE_EPHE_PATH` overrides are excluded.
- Latitude is limited to +/-65 degrees; elevation is fixed to zero. Day/night
  uses geocentric solar-centre geometric altitude without refraction; within
  0.1 degrees of the horizon the operation holds instead of inventing sect.
- `complete_chart=true` means the explicit `TEN_PLANET_TROPICAL_WHOLE_SIGN_V1`
  output, not every astrological technique or a professional birth-chart service.
  Whole-sign is not attributed to the Owner's teacher without source evidence.

To exercise the existing classical-primary/modern-overlay research engine,
install both local source packages (not an assumed public package release):

```powershell
python -m pip install ./examples/classical-western-astrology_v0.1.0 ./examples/swiss-ephemeris-agpl_v0.1.0
```

```python
from pathlib import Path
from aion_swiss_ephemeris.chart import calculate_chart, to_research_chart_input
from aion_astra_classical_astrology import build_chart, integrated_classical_modern_profile

result = calculate_chart(Path("C:/AION-cache/swiss"), "2000-01-01T20:00:00+08:00", 25.033, 121.5654)
source = to_research_chart_input(result, input_id="SYNTHETIC_NATIVE_2000",
    location_label="SYNTHETIC_TAIPEI", synthetic_fixture=True)
chart = build_chart(source, integrated_classical_modern_profile(), chart_id="SYNTHETIC_CHART_2000")
```

The bridge requires explicitly synthetic research inputs; it does not relabel
personal inputs or relax the classical engine's admission rule. The optional
combined path remains AGPL-covered, not Apache-only.

## Reproduce and inspect source

The adapter's complete source is the `src/` folder, its packaging instructions are
in `pyproject.toml`, and tests and captured native-output witnesses are in `tests/`.
Captured fixtures came from the previous pinned J2000 TT trial; the leading local
command path was removed and the negative fixture's local path was replaced with
`LOCAL_CACHE`. Numeric output and fallback warning are retained. They test parsing,
not independent astronomical accuracy.

The additional UTC fixture is a pinned native Taipei test with only the local
command-path line removed. The JPL Sun/Moon witness is an exploratory one-epoch
comparison of apparent geocentric ecliptic-of-date longitudes, with recorded
query URLs/hashes. Agreement is not independent validation of a shared data
lineage, a universal precision certificate, or an astrological validity claim.

Native source/data revision:
[3fd0f956d73898b91cc4f67cf18b21af656d1342](https://github.com/aloistr/swisseph/tree/3fd0f956d73898b91cc4f67cf18b21af656d1342).
The resource `src/aion_swiss_ephemeris/lock.json` records every acquired file.
This repository publishes adapter source and license notices, **not native binaries
or ephemeris data**. Users obtain the latter directly from upstream. A future
redistributor of native binaries must satisfy the applicable corresponding-source
requirements; a URL in this README is not a blanket compliance certificate.

No public network service is activated. Before any modified/combined AGPL service,
provide the required source access to its network users and review the complete
combined-work scope. Original Apache-2.0 notices remain, but an AGPL-covered
combined product is not represented as Apache-only.

## Validation and research boundary

```text
python -m pytest -q examples/swiss-ephemeris-agpl_v0.1.0/tests
```

`AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION`
`SUBJECTIVITY = NOT_ESTABLISHED`; `CANONICAL_EFFECT = NONE`; `DEPLOYMENT = FALSE`.
