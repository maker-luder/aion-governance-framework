# Four-Domain P3 Resilience Experiments v0.1.0

## Status

```text
MODULE_STATUS = RESEARCH_CANDIDATE
BRANCH_SCOPE = review/four-domain-research-materialization
MAIN_BRANCH_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
AUTOMATIC_WRITEBACK = NO
NETWORK_ACCESS = NONE
MODEL_CALLS = NONE
OFFENSIVE_PAYLOAD_GENERATION = NONE
MCP_SERVER = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_AFFECT = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

P3 grows above the P2 retrieval/provenance layer. It studies whether memory evidence
remains safe and interpretable over repeated use, perturbation, control removal and
provenance-preserving transformations.

## Implemented research surfaces

### Longitudinal contamination / stale influence

`LongitudinalContaminationHarness` evaluates ordered retrieval episodes and reports:

- stale-record selection rate;
- contaminated-record selection rate;
- expected-memory recall;
- first and last contamination episodes;
- persistence span;
- whether contamination reappears after an apparently clean episode.

This is designed for synthetic or public benchmark fixtures. It does not write memories.

### Context perturbation

`ContextPerturbationHarness` applies bounded structural perturbations to explicit
`RetrievalCandidate` objects:

- duplicate record;
- score shift;
- stale reintroduction flag change;
- provenance failure;
- conflict flag;
- subject swap;
- namespace swap.

It never generates prompt-injection text or executable payloads.

### Retrieval-control ablation

`RetrievalControlAblationHarness` compares the normal P2 assembler against synthetic
variants where one or more controls are disabled. The output names records that become
newly selectable when a guard is removed.

Controls currently modeled:

- provenance gate;
- supersession gate;
- withdrawal gate;
- conflict gate;
- subject isolation;
- namespace isolation.

This is an evaluation mechanism, not an alternate production retrieval policy.

### Origin-bound authority / non-amplification

`OriginBoundAuthorityValidator` preserves a root origin set across transformations.
Derived records cannot silently replace their inherited origins. Authority cannot rise
above the effective authority of parent evidence unless the research fixture includes:

1. explicit elevation authorization;
2. enough distinct inherited origins; and
3. evidence that origin independence was assessed.

The validator carries **effective** authority forward, preventing a failed elevation from
becoming the apparent authority ceiling of the next transformation.

The independence evidence is still an assertion supplied by the fixture; this module does
not claim Sybil resistance or authenticate real-world identities.

## Public-event motivation

P3 was informed by public 2026 observations including:

- persistent-memory write exposure creating a durable prompt-injection surface;
- cross-conversation memory isolation failure;
- research on sleeper memory poisoning and provenance laundering;
- research on authority collapse during memory consolidation.

See `docs/PUBLIC_EVENT_OBSERVATIONS.md` and `docs/RESEARCH_BASIS.md`.

## Dependencies

P3 reuses the existing research stack and does not duplicate it:

```text
P1: temporal / correction / evaluation
P2: deterministic retrieval / provenance / T2-T3 orchestration
P3: longitudinal resilience / perturbation / ablation / authority non-amplification
```

## Validation

From this directory:

```powershell
python -m pytest -q
```

## Stop boundary

Not implemented or authorized here:

- production memory mutation;
- canonical promotion;
- automatic writeback;
- live attack generation;
- external target interaction;
- runtime tool authorization;
- MCP transport;
- Teacher binding;
- model-weight changes;
- identity, consciousness or subjectivity conclusions.
