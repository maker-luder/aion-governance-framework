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

A successful run writes:

```text
interop-manifest.json
prov.jsonld
attestation.intoto.json
ro-crate/ro-crate-metadata.json
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

The RO-Crate metadata describes the source record and generated interoperability artifacts as a research-object package view. It does not copy remote content or fetch references.

### in-toto view

The in-toto Statement binds the source record SHA-256 and exact source commit to generated primary artifact digests.

It is deliberately unsigned in v0.1.0:

```text
SIGNATURE_STATUS = UNSIGNED_REFERENCE
INTOTO_ATTESTATION != HUMAN_APPROVAL
INTOTO_ATTESTATION != MAIN_MERGE_AUTHORITY
```

### OPA/Rego view

`policies/aion_interop.rego` expresses the closed boundaries as policy-as-code. A small Python mirror enforces the same critical conditions during bundle generation so OPA is not a runtime dependency.

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

## Dependencies

Runtime dependencies: none beyond Python 3.11+ and the repository's existing source validator environment.

Optional ecosystem tools such as `prov`, `rocrate`, OPA, `inspect_ai`, or the OpenSSF Scorecard binary/action are not installed or invoked. They may be used later for external conformance testing, but file presence, compatibility, an external Scorecard score, or conformance would not create canonical, scientific, security-certification, merge, or deployment authority.

## Attribution and authority

```text
DESIGN_SOURCE = ChatGPT
IMPLEMENTATION_SOURCE = ChatGPT
CURRENT_IMPLEMENTATION_REQUEST = USER_GIVEN
MAIN_MERGE_AUTHORITY = NOT_GRANTED_BY_THIS_COMPONENT
CANONICAL_EFFECT = NONE
```

This candidate is additive and does not rewrite historical evidence records or historical project events.
