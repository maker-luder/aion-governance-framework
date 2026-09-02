# Optional Swiss Ephemeris position provider — AGPL-3.0-only

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

No UTC birth-date conversion, houses, ascendant, midheaven, location-specific sect,
Chiron, nodes or complete horoscope is claimed. Do not fabricate those fields to
feed the existing classical chart model. CLI coordinates have seven decimal
degrees; upstream precision claims are not independent validation of this adapter.
This component creates no research loop, canonical state, agent goal or service.

## Run on Windows x64 with Python 3.11+

From the repository root, install the local, separately licensed example:

```powershell
python -m pip install ./examples/swiss-ephemeris-agpl_v0.1.0
python -m aion_swiss_ephemeris fetch --cache C:/AION-cache/swiss
python -m aion_swiss_ephemeris verify --cache C:/AION-cache/swiss
python -m aion_swiss_ephemeris calculate --cache C:/AION-cache/swiss --jd-tt 2451545
```

`fetch` is the only network operation; it contacts immutable public upstream URLs
without credentials. Existing valid files are reused; mismatched files are not
overwritten. Keep the cache outside the repository. `calculate` performs no
download and launches only the hash-verified executable with explicit arguments.
No shell string, user-provided program or automatic system configuration is used.
The selected native binary requires Windows x64. Parser/contract tests are portable.

## Reproduce and inspect source

The adapter's complete source is the `src/` folder, its packaging instructions are
in `pyproject.toml`, and tests and captured native-output witnesses are in `tests/`.
Captured fixtures came from the previous pinned J2000 TT trial; the leading local
command path was removed and the negative fixture's local path was replaced with
`LOCAL_CACHE`. Numeric output and fallback warning are retained. They test parsing,
not independent astronomical accuracy.

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
