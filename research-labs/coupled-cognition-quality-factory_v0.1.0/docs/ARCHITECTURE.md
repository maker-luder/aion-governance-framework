# Architecture — Quality Factory for Coupled Human–LLM Inquiry

## Why a factory model

A conversational research loop has a special failure mode: both participants can progressively align on the same explanation. Alignment improves fluency and local coherence but can reduce epistemic diversity. Therefore, quality control must be **structural**, not merely conversational.

The quality factory introduces separate inspection surfaces instead of asking the same reasoning loop to certify itself.

### 1. IQC — incoming quality control
Checks source identity, provenance, scope, freshness, and whether an input is observation, model output, repository artifact, test result, or external evidence.

### 2. IPQC — in-process quality control
Checks hypothesis drift, unsupported causal jumps, authority drift, hidden goal changes, source circularity, and whether the pair is converging faster than the evidence.

### 3. Counterevidence lane
A mandatory negative-evidence route. The system must register at least one explicit challenge before final QA. A counterexample may be accepted, rebutted only with evidence, or marked out of scope with justification. It cannot silently disappear.

### 4. NCR
A nonconformance record is opened for defects such as unsupported claims, provenance gaps, mutual-confirmation loops, failed falsifiers, stale evidence, governance violations, or test/evidence mismatch.

### 5. CAPA
Corrective and preventive action is not complete when a fix is merely applied. Effectiveness evidence is required before NCR closure.

### 6. Final QA
Final QA is blocked by open counterevidence, open NCR/CAPA, absent falsifier, or absent evidence independent from the current human–AI pair. For HIGH/CRITICAL research claims, at least one independent primary source or test result is required.

## Key distinction

`THE_PAIR_CORRECTED_EACH_OTHER` is useful, but it is still internal process evidence.

It is not equivalent to `THE_CLAIM_WAS_INDEPENDENTLY_CORROBORATED`.

## Claim-quality integration

The provenance ledger and factory remain separate responsibilities, connected by
the opt-in `ProvenanceClaimQualityGate` adapter:

```text
source-role provenance
-> observation / inference / hypothesis separation
-> supporting and challenging evidence bindings
-> competing explanations + falsifier
-> dependency / revision freshness
-> transfer and scope checks
-> existing factory final QA
-> bounded-record admission or HOLD
```

The adapter is deliberately fail-closed and non-canonical. It checks structural
admissibility and promotion boundaries, not whether a claim is true. It does not
replace the persistent claim-revision service or the standing subjectivity-evidence
protocol.

`ResearchClaimRecord` is a typed admission view, not a second evidence schema.
Each assessment must load the repository-native
`schemas/research_evidence_record_v0.2.0.schema.json` and the protocol named by
that schema. The adapter checks the complete claim-level mapping, schema version,
closed-schema marker, protocol reference and every adapter-field mapping. Drift
fails closed rather than allowing the Python representation and JSON evidence
contract to evolve as parallel truth sources.

```text
ADAPTER != CANONICAL_SCHEMA
TYPED_REPRESENTATION != SECOND_TRUTH_SOURCE
SCHEMA_BINDING_PASS != EVIDENCE_TRUE
```

Observed evidence is not forced to be supporting evidence. Typed relations permit
`OBSERVES`, `SUPPORTS`, `CHALLENGES`, `NEUTRAL` and `UNRESOLVED`; only explicitly
supporting evidence enters claim-level promotion checks.

L4 admission requires at least two repeated held-out records plus declared and
traceable separation: distinct producers, distinct runtime/context references,
source references and non-unknown replication provenance. These declarations are
structural review inputs, not independent IV&V or scientific validation.

A resolved challenge marker is insufficient. Every marker must name a current
claim/version resolution, a non-circular resolution reference and non-unknown
provenance. Where the bounded claim has a `ClaimRevision`, the resolution must
link to that revision's rationale reference. The reference may point to an
inspection-only export or receipt from the existing claim-revision service; this
adapter does not create another revision database or independently authenticate
the referenced record.
