# Quickstart

This quickstart creates a deterministic, inspection-only Evidence Interop bundle from a committed fixture. It is the shortest current path that exercises a public command, JSON input, JSON output, and the repository's non-claim boundaries.

## 1. Prepare Python and install the component

Follow [`INSTALLATION.md`](INSTALLATION.md), then run:

```powershell
$head = git rev-parse HEAD
$outside = Join-Path $env:TEMP "aion-evidence-interop"
Remove-Item -Recurse -Force $outside -ErrorAction SilentlyContinue
python -m aion_evidence_interop.cli `
  --root . `
  --record components/aion_evidence_interop_v0.1.0/fixtures/valid_minimal.json `
  --expected-head $head `
  --output $outside
Get-Content "$outside\interop-manifest.json"
```

Expected CLI result includes `"status": "PASS"` and these invariant values:

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
MODEL_EXECUTION = FALSE
NETWORK_ACCESS = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

The output location must be outside the repository root. Delete it after inspection if it is no longer needed.

## 2. Run the focused regression suite

```powershell
python -m pytest -q .\components\aion_evidence_interop_v0.1.0\tests
```

## Next steps

- Interface details: [`API.md`](API.md)
- Copyable JSON/subprocess integration: [`INTEROPERABILITY.md`](INTEROPERABILITY.md)
- More repository maps: [`START_HERE.md`](START_HERE.md)
