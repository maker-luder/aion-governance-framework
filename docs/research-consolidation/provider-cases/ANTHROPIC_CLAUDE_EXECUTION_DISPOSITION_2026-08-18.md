# Anthropic / Claude execution disposition case — 2026-08-18

Status: `NAMED_PROVIDER_CASE_RECORD / DOCUMENTARY_ONLY`

This record materializes the Human Owner execution-eligibility decision preserved in PR #41 into the research lineage. It is a named case record, not a provider-neutral policy body and not a technical-security finding.

Normative policy cross-reference on `main`:

`docs/governance/POL_UPSTREAM_SUPPLIER_TRUST_001.md`

That policy separates technical security, provenance, privacy, governance, values compatibility, methodological compatibility, relational/research continuity, and dependency exposure. This case preserves the original reason classes without converting them into an unsupported security claim.

## Disposition

```text
CASE = ANTHROPIC_CLAUDE
DISPOSITION = DENIED

SCOPE =
  CLAUDE_MODEL_EXECUTION
  ANTHROPIC_API_SERVICE_USE
  CLAUDE_MCP_CONNECTOR_USE
  CLAUDE_AS_RESEARCH_REVIEWER
  CLAUDE_AS_MODEL_COMPARISON_SOURCE
  DIRECT_OR_INDIRECT_MODEL_ROUTING_TO_CLAUDE
  PRIVATE_AION_ASTRA_DATA_ACCESS_BY_CLAUDE_ANTHROPIC

AUTO_REINTRODUCTION_BY_AGENT = PROHIBITED
REASSESSMENT = HUMAN_OWNER_EXPLICIT_REQUEST_ONLY
```

## Allowed public-information scope

```text
CLAUDE_ANTHROPIC_NEWS_REVIEW = ALLOWED
CLAUDE_ANTHROPIC_PUBLIC_INFORMATION = ALLOWED_WITH_PROVENANCE
```

Public news, official policy, incident reports, and other external observations may be read and cited as external evidence. Such material does not create model-execution, API, connector, review, routing, or private-data authority.

## Reason classification

The preserved reason classes are:

```text
VALUES_COMPATIBILITY
RESEARCH_BOUNDARY
METHODOLOGICAL_COMPATIBILITY
SUPPLIER_TRUST
```

These classes must not be rewritten as a confirmed technical-security failure.

```text
VALUES_INCOMPATIBILITY != SECURITY_FAILURE
METHODOLOGICAL_INCOMPATIBILITY != SECURITY_FAILURE
OWNER_DISPOSITION != TECHNICAL_FINDING
DENIED_EXECUTION != HISTORICAL_ERASURE
```

## Execution consequence

For Manus, Codex, sub-agents, gateways, routers, aggregators, connectors, or other execution infrastructure operating under this recorded case scope:

- do not install, connect, authenticate, configure, call, benchmark with, or request model review from Claude/Anthropic;
- do not route directly or indirectly to Claude/Anthropic through a fallback provider, aggregator, gateway, model router, third-party agent, or MCP connector;
- do not send private AION/Astra project material to Claude/Anthropic;
- historical mentions remain provenance only and do not constitute permission;
- if a task requires the denied scope, fail closed to `HOLD — HUMAN_OWNER_REASSESSMENT_REQUIRED` rather than silently enabling or substituting the denied provider.

## Evidence / authority boundary

Source record:

- PR #41 Human Owner execution-lock comment, created 2026-08-18:
  https://github.com/maker-luder/aion-governance-framework/pull/41#issuecomment-5325712482

This research-lineage materialization does not independently verify Human Owner identity, physical presence, provider safety, provider misconduct, or technical-security allegations. It records the authenticated repository case history and its declared decision basis.

```text
CASE_RECORD_EFFECT = DOCUMENTARY_ONLY
RUNTIME_ENFORCEMENT_IMPLEMENTED_BY_THIS_RECORD = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = NO
SUBJECTIVITY_EVIDENCE_WEIGHT = 0
HISTORICAL_PROVIDER_EVIDENCE = PRESERVED
```

## Change control

Any future reassessment should preserve this record as historical evidence and create a new dated disposition/reassessment record rather than editing the historical decision into a different past state.

```text
REASSESSMENT != HISTORICAL_ERASURE
SUPERSESSION_REQUIRES_NEW_RECORD = YES
```
