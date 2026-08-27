# Interoperability

## Scope

`aion_evidence_interop_v0.1.0` is the current language-neutral interoperability boundary. It exports deterministic JSON, JSON-LD, JSONL, in-toto, RO-Crate, OPA, and inspection views from an already validated source record. It is a `REFERENCE_INTEGRATION`, not a native SDK or an HTTP service.

```text
EXTERNAL_CLIENT -> JSON_RECORD -> BOUNDED_PYTHON_SUBPROCESS -> JSON_ARTIFACTS
REFERENCE_INTEGRATION != NATIVE_IMPLEMENTATION
CROSS_LANGUAGE_INTERFACE != MULTI_LANGUAGE_REIMPLEMENTATION
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Contract

Input: a source record accepted by the component's existing validation rules, plus an exact expected Git head. Invocation is `aion-evidence-interop --root ROOT --record RECORD --expected-head SHA --output DIRECTORY`.

Success stdout is a JSON object with `status: "PASS"`, artifact hashes, and boundary fields. Failure stdout is JSON with `status: "HOLD"`, diagnostics, and the same closed boundary fields. Unknown escalation fields are not accepted by the evidence-record validator; input validation fails closed rather than granting authority.

Output artifacts include `interop-manifest.json`, `prov.jsonld`, `attestation.intoto.json`, `ro-crate-metadata.json`, `opa/input.json`, and inspection JSON/JSONL views. The manifest schema is component-local at `components/aion_evidence_interop_v0.1.0/schemas/interop_manifest_v0.1.0.schema.json`.

## Node.js reference integration

```js
import { spawnSync } from 'node:child_process';
const result = spawnSync('aion-evidence-interop', [
  '--root', process.cwd(), '--record', 'record.json',
  '--expected-head', process.env.GIT_SHA, '--output', process.env.OUTPUT_DIR,
], { encoding: 'utf8' });
const response = JSON.parse(result.stdout);
if (result.status !== 0 || response.status !== 'PASS') throw new Error(response.diagnostics?.join('; '));
```

Go and Rust clients use the same subprocess + JSON approach (`os/exec` or `std::process::Command`). These snippets are conceptual reference integrations and are not separately compiled in CI.

## Performance boundary

The current implementation is Python-centric. Performance-sensitive deployments require profiling before a rewrite or bottleneck claim. `PERFORMANCE_CONCERN != MEASURED_BOTTLENECK`.
