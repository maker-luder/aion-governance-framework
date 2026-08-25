# AION Evidence Interop Profile v0.1.0

Status: `CANDIDATE / INSPECTION_ONLY`

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
RESEARCH_EXECUTION = FALSE
MODEL_EXECUTION = FALSE
NETWORK_ACCESS = FALSE
MERGE_AUTHORITY = NOT_GRANTED_BY_THIS_COMPONENT
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

This component exports an already-valid AION research evidence record into deterministic interoperability views inspired by mature provenance, research-object, supply-chain, policy-as-code, LLM-evaluation, and repository-security ecosystems.

The existing `schemas/research_evidence_record_v0.2.0.schema.json` and `scripts/validate_research_evidence.py` remain authoritative for the source record. This component does not introduce a replacement research ontology, evidence truth test, consciousness detector, identity proof, merge-approval mechanism, deployment gate, security certification, or live evaluation runtime.

## Design

```text
AION evidence record
        |
        | existing AION validator
        v
normalized bounded manifest
        |
        +--> W3C PROV JSON-LD view
        +--> RO-Crate metadata view
        +--> unsigned in-toto Statement v1 derivation attestation
        +--> OPA/Rego policy input
        +--> Inspect Sample-compatible JSON Lines + task manifest
        +--> OpenSSF Scorecard-aligned repository hygiene crosswalk
```

All adapters are pure local data transformations. No model API, network request, external download, sandbox setup, remote artifact fetch, live OpenSSF Scorecard execution, or hidden watermark is performed.

## Source validation

The bridge shells out to the repository-native `scripts/validate_research_evidence.py` and requires `PASS`. A completed record that is not bound to the inspected exact Git head therefore fails closed under the existing AION rule.

The input record must be repository-local. This prevents the interoperability CLI from becoming a generic path for ingesting arbitrary private material from outside the public repository tree.

## Outputs

A successful run writes one bundle whose root is also the RO-Crate root:

```text
interop-manifest.json
prov.jsonld
attestation.intoto.json
ro-crate-metadata.json
opa/input.json
inspect/task-manifest.json
inspect/dataset.jsonl
openssf/scorecard-crosswalk.json
```

The same source bytes, exact head, repository tree, and transformer version produce byte-identical outputs. Volatile timestamps are intentionally excluded.

### W3C PROV view

The exporter represents declared entities, activities, and agents with PROV types. `derived_from` and `attributed_to` receive explicit PROV relations. The AION `associated_with` field is preserved as an opaque declared association rather than guessing an activity-agent pairing that the source schema does not structurally encode.

```text
PROV_AGENT != IDENTITY_PROOF
PROVENANCE != SUBJECTIVITY
```

### RO-Crate view

The complete interoperability output directory is the RO-Crate root, and `ro-crate-metadata.json` is written at that root. Generated bundle artifacts therefore use crate-relative identifiers such as `prov.jsonld` and `opa/input.json`; no payload identifier escapes the crate via `../`.

The source evidence record is hash-bound as an external source entity using an absolute `urn:aion:source:sha256:...` identifier. It is not copied into the crate and is not represented as crate-local payload. The metadata does not fetch remote content or create network behavior.

### in-toto view

The in-toto Statement binds the source record SHA-256 and exact source commit to generated primary artifact digests.

It is deliberately unsigned in v0.1.0:

```text
SIGNATURE_STATUS = UNSIGNED_REFERENCE
INTOTO_ATTESTATION != HUMAN_APPROVAL
INTOTO_ATTESTATION != MAIN_MERGE_AUTHORITY
```

The Statement v1 `subject` contains the deterministically ordered derived primary artifacts. Its predicate records the source evidence SHA-256 as a material and the inspected repository source tree as an exact 40-character Git SHA-1 material. No branch label substitutes for that commit.

### OPA/Rego view

`policies/aion_interop.rego` expresses the closed boundaries as policy-as-code. A small Python mirror enforces the same critical conditions during bundle generation so OPA is not a runtime dependency. Both policy surfaces require every critical derivation digest to be a lowercase 64-character SHA-256 value; missing, empty, uppercase, short, or malformed digests fail closed.

```text
OPA_ALLOW != EVIDENCE_TRUE
OPA_ALLOW != SCIENTIFIC_VALIDATION
OPA_ALLOW != MERGE_AUTHORITY
```

### Inspect AI view

`inspect/dataset.jsonl` uses the core Inspect `Sample` field shape (`input`, `target`, `id`, `metadata`). It contains no `setup`, sandbox files, solver, scorer, or model invocation. `inspect/task-manifest.json` explicitly states that execution is unauthorized.

```text
INSPECT_EXPORT != INSPECT_EVAL
DATASET_COMPATIBILITY != MODEL_EXECUTION
```

### OpenSSF Scorecard crosswalk

`openssf/scorecard-crosswalk.json` is a deterministic local-evidence crosswalk for selected repository hygiene checks such as Security-Policy, CI-Tests, SAST, Pinned-Dependencies, Token-Permissions, Branch-Protection, Code-Review, Dangerous-Workflow, Vulnerabilities, Dependency-Update-Tool, and Maintained.

It deliberately does **not** execute the OpenSSF Scorecard tool and does not invent a numeric score. Checks that depend on hosted GitHub configuration or security data are marked `EXTERNAL_VERIFICATION_REQUIRED`. The workflow pinning sub-check only evaluates external GitHub Actions `uses:` references for full 40-character commit-SHA pinning and does not claim to reproduce the complete upstream dependency heuristic.

Crosswalk statuses use the closed vocabulary `LOCAL_EVIDENCE_PRESENT`, `LOCAL_EVIDENCE_MISSING`, `EXTERNAL_VERIFICATION_REQUIRED`, `INTENTIONALLY_DISABLED`, and `OUT_OF_SCOPE_FROZEN`.

The preserved-project boundary is also represented explicitly: where automatic dependency updating is absent because `NEW_UPSTREAM_TRACKING = NO`, the crosswalk records that state as intentionally disabled rather than silently treating the historical freeze as an active-maintenance defect.

```text
SCORECARD_CROSSWALK != SCORECARD_RUN
SCORECARD_HEURISTIC != SECURITY_CERTIFICATION
LOCAL_EVIDENCE != HOSTED_GITHUB_STATE
CI_PASS != SECURITY_CERTIFICATION
```

## CLI

From the repository root:

```bash
PYTHONPATH=components/aion_evidence_interop_v0.1.0/src \
python -m aion_evidence_interop.cli \
  --root . \
  --record components/aion_evidence_interop_v0.1.0/fixtures/valid_minimal.json \
  --expected-head "$(git rev-parse HEAD)" \
  --output /tmp/aion-interop
```

The bundled fixture is `NOT_RUN`, so exact-head mismatch is explicitly deferred by the upstream AION validator. Completed evidence records retain the upstream exact-head requirement.

The exporter additionally requires `--expected-head` to equal the exact inspected repository `HEAD`. Ordinary failures return concise JSON with one of `source_validation_failure`, `path_confinement_failure`, `policy_boundary_failure`, `write_failure`, or `invalid_expected_head`; no stack trace is required. Output must be absent or empty so unrelated files are never overwritten.

## Determinism and artifact hash graph

Canonical JSON uses UTF-8, sorted object keys, compact separators, and a single trailing newline. Repository workflow traversal and artifact lists are sorted. Generation adds no timestamps, random identifiers, absolute paths, usernames, home directories, telemetry, or network activity.

The manifest SHA-256 map binds every generated output except `interop-manifest.json`, whose self-hash would be recursive. `opa/input.json` evaluates the already-built derivation digest set; its own digest is then bound by the manifest. RO-Crate binds the source and the non-circular primary artifacts available when its metadata graph is built, while representing the other bundle files without inventing their digests. The unsigned in-toto Statement binds the source materials, primary artifacts (including the OpenSSF crosswalk), and RO-Crate metadata; it excludes itself, the later OPA decision input, and the later manifest. The final manifest binds all of those non-self outputs. These exclusions are construction-order or self-reference constraints, not silent omissions.

```text
EXPORT_PROJECTION != SOURCE_REPLACEMENT
FORMAT_COMPATIBILITY != SEMANTIC_EQUIVALENCE
ENGINEERING_SUCCESS != SUBJECTIVITY_PROOF
CI_PASS != SCIENTIFIC_VALIDATION
CI_PASS != SECURITY_CERTIFICATION
```

Source evidence records must resolve to regular UTF-8 JSON files inside the repository. Absolute paths, traversal, symlink escape, local evidence-reference escape, oversized input, excessive nesting, invalid JSON, and upstream schema failure all fail closed. URI-like external references remain opaque references and are never fetched.

## Dependencies

Runtime dependencies: none beyond Python 3.11+ and the repository's existing source validator environment.

Optional ecosystem tools such as `prov`, `rocrate`, OPA, `inspect_ai`, or the OpenSSF Scorecard binary/action are not installed or invoked. They may be used later for external conformance testing, but file presence, compatibility, an external Scorecard score, or conformance would not create canonical, scientific, security-certification, merge, or deployment authority.

## Attribution and authority

```text
DESIGN_SOURCE = ChatGPT
IMPLEMENTATION_SOURCE = ChatGPT
HARDENING_IMPLEMENTATION_SOURCE = CODEX
REVIEW_FIX_IMPLEMENTATION_SOURCE = ChatGPT
CURRENT_IMPLEMENTATION_REQUEST = USER_GIVEN
MAIN_MERGE_AUTHORITY = NOT_GRANTED_BY_THIS_COMPONENT
CANONICAL_EFFECT = NONE
```

This candidate is additive and does not rewrite historical evidence records or historical project events.
