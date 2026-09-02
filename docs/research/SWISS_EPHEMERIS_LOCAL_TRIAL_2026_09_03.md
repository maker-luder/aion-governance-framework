# Swiss Ephemeris: free local trial, unchanged Apache-2.0

Classification: `RESEARCH_REFERENCE`; decision date: 2026-09-03 (Asia/Taipei).

## Owner decision and license distinction

The Owner requests free-only work, retaining the repository's Apache-2.0 license,
without purchases or relicensing. [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)
is an open-source license, not Astrodienst's professional license.
[Astrodienst's official terms](https://www.astro.com/swisseph/swephinfo_e.htm)
offer AGPL or a separately purchased professional agreement; redistribution and
public-service integration require attention to those terms. Free does not mean
condition-free. This record is an engineering disposition, not a legal opinion.

**Current decision:** use the unmodified upstream standalone executable privately
for an independent local experiment only. Do not vendor, import, link, package or
activate a public Swiss-powered service in this repository. Keeping processes
separate is not asserted to settle any future combined-work licensing question.
No professional license has been acquired; no repository license has changed.

## Actual downloaded and executed artifacts

- Upstream: [official Swiss repository](https://github.com/aloistr/swisseph).
- Exact source/data commit: `3fd0f956d73898b91cc4f67cf18b21af656d1342`.
- Executable-reported version: `2.10.03`; executable `swetest64.exe`.
- Three `.se1` files: `sepl_18.se1`, `semo_18.se1`, `seas_18.se1`.
- Data family: DE441 according to the upstream declaration. Library version alone
  does not identify the data release; both commit and file hashes are recorded.
- Seven files, 3,235,498 bytes total, including upstream license notices and
  version header, retained **outside** this repository.
- [Acquisition receipt](sources/swiss-local-acquisition-20260903.json) records
  sizes, SHA-256 and upstream Git blob IDs. It contains no binary or source copy.

## Observed positive and negative controls

Input: J2000 **TT**, JD 2451545.0, ten planets, geocentric tropical ecliptic of
date, requested Swiss backend. This is not a UTC birth timestamp or full chart.

| Run | Exit | Observation |
|---|---|---|
| Pinned local data | 0 | Sun 280.3681656 degrees; Moon 223.3148705 degrees |
| Identical repeat | 0 | identical output, including positions and speeds |
| Deliberately absent data directory | 0 | warning that `sepl_18.se1` is absent; Moshier fallback |

Each measured process finished in under 0.02 seconds on the local workstation;
these are single-run observations, not a benchmark guarantee. No GPU or model
weights were needed. The missing-data run changed the Sun to 280.3681666 and
Moon to 223.3148946 degrees. **Exit status 0 alone is insufficient to establish
the requested backend.** Future integration must verify exact data and reject
or explicitly identify fallback, rather than silently label it Swiss data.

Exact command vectors, literal output, timings and exit statuses are retained
in the local evidence bundle. Public reproducibility uses the acquisition pins
and these standalone arguments, after independently satisfying upstream terms:

```text
swetest64.exe -bj2451545 -p0123456789 -eswe -edir<LOCAL_DATA_DIRECTORY> -fPls -g,
```

There is no computed ascendant, midheaven, location-specific sect, UTC conversion
contract, or complete chart in this trial. No such fields are fabricated to feed
the repository's existing chart input. Independent accuracy certification,
extended date coverage and a distributable integrated provider remain open.

`RUNTIME_INTEGRATION = NONE`; `PURCHASE = FALSE`; `LICENSE_CHANGE = NONE`;
`SUBJECTIVITY = NOT_ESTABLISHED`; `CANONICAL_EFFECT = NONE`; `DEPLOYMENT = FALSE`.
