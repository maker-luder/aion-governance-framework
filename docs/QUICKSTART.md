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
```

### CLI stdout

The CLI emits a JSON status object. On success it contains:

```text
status = PASS
output = WRITTEN
artifacts = { ... artifact hashes ... }
mutation_performed = false
canonical_effect = NONE
deployment = false
model_execution = false
network_access = false
```

### Generated `interop-manifest.json` boundaries

Inspect the generated artifact separately:

```powershell
Get-Content "$outside\interop-manifest.json"
```

Its `boundaries` object includes, among other closed fields:

```text
subjectivity_conclusion = NOT_ESTABLISHED
canonical_effect = NONE
deployment = false
model_execution = false
network_access = false
```

```text
CLI_STDOUT != INTEROP_MANIFEST_BOUNDARIES
```

The output location must be outside the repository root. Delete it after inspection if it is no longer needed.

## 2. Run the standalone public API example

```powershell
python .\examples\evidence_interop_export.py --root .
```

The example derives the exact checked-out Git head, reads the committed Evidence Interop fixture by default, decodes the returned bytes, and prints the JSON manifest. It performs no network access, model execution, writeback, canonical effect, or authority grant.

## 3. Run the focused regression suite

```powershell
python -m pytest -q .\components\aion_evidence_interop_v0.1.0\tests
```

## Next steps

- Interface details: [`API.md`](API.md)
- Copyable JSON/subprocess integration: [`INTEROPERABILITY.md`](INTEROPERABILITY.md)
- More repository maps: [`START_HERE.md`](START_HERE.md)
