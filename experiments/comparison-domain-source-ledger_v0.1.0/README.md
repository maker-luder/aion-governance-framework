# EX-001 Comparison-domain source ledger v0.1.0

```text
EXPERIMENT_ID = EX-001
KIND = PROVENANCE / REPOSITORY-INTEGRITY
ORIGIN = CURATED_FROM_GROK_SANDBOX_7a427b123cf7d7dde9e29e1a85975299030aa1cb
SUBJECTIVITY_EVIDENCE_WEIGHT = 0
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
AUTHORITY = NONE
GROK_SANDBOX_RULES_INCLUDED = FALSE
MAIN_TRANSITION_AUTHORITY_GATE = UNCHANGED_NOT_BYPASSED
```

This experiment checks that existing comparison-domain source registers and fetch
manifests still parse, still record license/usage metadata, and still have
per-entry local hash outcomes for checked-in files. It is not subjectivity
evidence and does not raise any subjectivity evidence layer.

## Authority

Existing typed surfaces remain authoritative:

- `examples/bazi-capability_v0.1.1/docs/BAZI_RULE_SOURCE_REGISTER.json`
- `examples/bazi-capability_v0.1.1/docs/CALENDAR_ENGINE_SOURCE_REGISTER.json`
- `examples/bazi-capability_v0.1.1/sources/SOURCE_FETCH_MANIFEST.json`
- `examples/classical-western-astrology_v0.1.0/docs/SOURCE_REGISTER.json`
- `examples/classical-western-astrology_v0.1.0/sources/SOURCE_FETCH_MANIFEST.json`
- `examples/zi-wei-dou-shu_v0.1.0/docs/SOURCE_REGISTER.json`
- `examples/zi-wei-dou-shu_v0.1.0/sources/SOURCE_FETCH_MANIFEST.json`

`LEDGER.md` is a derived report only. It is not a second source schema and must
not be cited as authority over those files.

`LEDGER_FIRST_RUN.md` preserves the pre-alignment result at
`f4c911af558e5076a52cfe7b4efc5a8e00585d2c` (22/24). `LEDGER.md` and
`RESULT.json` are regenerated for the current curated candidate (24/24). The
historical negative result is retained rather than overwritten or re-described
as if both results came from the same repository head.

## Narrow claims

1. `C1` — listed register **and** fetch-manifest files exist and parse as JSON
   with a `sources` array.
2. `C2` — fetch-manifest entries record `license_or_terms`; calendar-engine
   register entries record `license`. This is metadata presence only.
3. `C3` — coverage over fetch-manifest entries using the exact Git blob at
   `HEAD`, not platform-dependent working-tree line endings:
   - `C3A` per-entry outcome is one of `MATCH | MISMATCH | MISSING | NOT_APPLICABLE`
   - `C3B` every checked-in `repository_path` SHA-256 equals recorded
     `repository_sha256` (`SUPPORTED` only if coverage is complete)

`C3` is not a universal "hashes match" claim softened by
`PARTIALLY_SUPPORTED`. Coverage counts stay visible. `C3B` is `NOT_SUPPORTED`
as soon as any checked-in entry is `MISMATCH` or `MISSING`.

## Non-claims

- External URL content is not fetched and is not verified as current.
- Recorded license/usage strings are not a legal-validity determination.
- HASH_ONLY / discarded payloads cannot have a local content hash recomputed.
- Comparison-domain materials are not scientific causal mechanisms.
- This experiment does not establish subjectivity, identity continuity,
  consciousness, or deployment readiness.

## Run

From the repository root, offline:

```bash
python experiments/comparison-domain-source-ledger_v0.1.0/run_experiment.py
python -m pytest -q experiments/comparison-domain-source-ledger_v0.1.0/tests
```

No network, paid API, model call, or write outside this experiment directory
is required. The runner may overwrite only `LEDGER.md` and `RESULT.json` in
this directory when `--write-derived` is passed.

The output records a diagnostic working-tree hash when the file is
materialized. On Windows this may differ from the Git blob because of checkout
line-ending normalization; the `repository_sha256` comparison is bound to the
Git blob, which is the byte sequence shared by all clones.
