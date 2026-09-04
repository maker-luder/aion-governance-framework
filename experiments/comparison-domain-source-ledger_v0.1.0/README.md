# EX-001 Comparison-domain source ledger v0.1.0

```text
EXPERIMENT_ID = EX-001
KIND = PROVENANCE / REPOSITORY-INTEGRITY
BRANCH = grok/experimental-sandbox
SUBJECTIVITY_EVIDENCE_WEIGHT = 0
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
AUTHORITY = NONE
```

This experiment checks that existing comparison-domain source registers and fetch
manifests still describe checked-in files. It is not subjectivity evidence and
does not raise any subjectivity evidence layer.

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

## Narrow claims

1. Listed register and manifest files exist and parse as JSON with a `sources` array.
2. Fetch-manifest entries record license/usage metadata (`license_or_terms`).
   Calendar-engine register entries record `license`.
3. Fetch-manifest entries that name a checked-in `repository_path` and
   `repository_sha256` have a local file whose SHA-256 matches that field.

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
