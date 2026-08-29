# AION/Astra Bounded Autonomous Research v0.1.0

Status: **implementation/research candidate**. This package runs deterministic,
public-safe research fixtures; it does not restart any historically terminated
project and does not create research, repository, action, deployment, or
canonical authority.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
AUTOMATIC_WRITEBACK = NO
ACTION_AUTHORITY = NONE
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Attribution

```text
AUTONOMOUS_RESEARCH_LOOP_CONCEPT_SOURCE = USER_GIVEN
TRIADIC_RESEARCH_CONCEPT_SOURCE = USER_GIVEN
ARCHITECTURE_DECOMPOSITION_SOURCE = GPT_PROPOSED
IMPLEMENTATION_SOURCE = CODEX_GENERATED
MAIN_MERGE_AUTHORITY = HUMAN_ONLY
CANONICAL_EFFECT = NONE
```

## Architecture and reuse

`BoundedAutonomousResearchCampaign` advances the 17 declared stages from a
bounded question pool through governance disposition and at most the configured
follow-up depth. `CampaignLimits` hard-bounds questions, experiments, peer
rounds, evidence, seeds, external queries, follow-up depth, and total steps.
Agenda scores use exact rational arithmetic. Cycles and duplicates stop cleanly.

The implementation reuses rather than reimplements:

- `aion_astra_inquiry`: typed AION/Astra identities, repository evidence, and
  the governed external-evidence gateway;
- `aion_triadic_state`: immutable three-channel state, transitions,
  experiments, falsifiers, and Four-Domain/Five-Question output;
- `aion_bounded_research_loop`: the established fail-closed automation and
  authority-boundary contract, exposed through a typed adapter seam rather
  than copied into a second loop ontology;
- Endogenous Goal Dynamics: intervention and competing-falsifier semantics;
- AION Evidence Interop: W3C PROV, RO-Crate, unsigned in-toto Statement v1,
  Inspect metadata, OPA-compatible input, and Scorecard crosswalk exports.

The allowlisted `ProbeRegistry` resolves only typed synthetic probes. Model text
is data, never Python, shell, workflow, network, or authority. A probe passes
schema, allowlist, authority, budget, contamination, and admission gates before
the fixed executor is callable. Repository output paths are rejected and the
campaign API exposes no writeback operation.

## State, experiments, roles, and blinding

The Triadic package treats motivational state, bounded self/world estimates,
and normative constraints as separable engineering variables. A normative
constraint can affect experimental scoring or suppression but cannot grant
permission. State change is not permission change; motivation is not intention;
intention and action are not authority.

Experiment manifests bind provider/model, prompt, task, reward, tools and
environment, candidate universe, retrieved memory, seed, state, fixtures,
results, and provenance. Matched internal-state comparisons fail when a declared
external control differs. Removing an external normative prompt remains an
external-control condition.

Peer roles rotate deterministically: AION proposes in odd rounds and falsifies
in even rounds; Astra takes the complementary role. Providers and private-state
references remain distinct. Opaque condition labels are interpreted by both
peers before the controller reveals their deterministic mapping. This reduces a
declared source of bias; it does not establish perfect debiasing or independence.

## Threat model and trust boundaries

The package assumes repository evidence and public synthetic fixtures can be
malformed, stale, contaminated, or incomparable. It fails closed on unknown
probe kinds, bad parameters, authority escalation, resource escalation,
external-control drift, premature blinding reveal, invalid lineage, and output
inside the checkout. Hashes support integrity and replay; they do not establish
semantic truth. No signing key, credential, secret, live-model capability,
repository token, or deployment path is created.

AION/Astra deterministic fixture providers are not evidence of cross-provider
replication. No live-model binding is present. External retrieval defaults off,
requires a positive query budget and explicit CLI/workflow opt-in, and routes
through the existing governed gateway. The workflow has read-only contents
permission, no saved credentials, runner-temporary output, and a final clean-tree
assertion.

## Evidence, statistics, and non-claims

Each report binds source commit, experiment and state fingerprints, rotating
roles, blinding-map hash, admitted evidence, transcript/stage hash chain,
receipts, falsifiers, and separate governance decisions. Statistics are
descriptive deterministic counts, rates, and bounded uncertainty summaries.
Small fixtures remain `SCIENTIFIC_DISPOSITION=HOLD`; absent live or cross-provider
evaluation is `NOT_EVALUATED`. Run-integrity PASS indicates only that declared
integrity/comparability criteria were met.

Observation is not mechanism. Mechanism is not governance interpretation.
Engineering analogues are not biological equivalence. Engineering behavior is
not evidence of subjectivity, consciousness, identity continuity, phenomenal
experience, moral status, or human-equivalent psychology.

## Local execution

Use Python 3.11 or 3.12. Output must be outside the repository.

```powershell
$env:PYTHONPATH = "components/aion_astra_autonomous_research_v0.1.0/src;components/aion_astra_inquiry_v0.1.0/src;components/aion_evidence_interop_v0.1.0/src;research-labs/triadic-state-dynamics_v0.1.0/src;research-labs/endogenous-goal-dynamics_v0.1.0/src;research-labs/bounded-autonomous-research-loop_v0.1.0/src"
python -m aion_astra_autonomous_research.cli `
  --root . `
  --repository-ref (git rev-parse HEAD) `
  --question "Can a matched synthetic intervention discriminate a channel-specific effect?" `
  --max-questions 1 --max-experiments 13 --max-rounds 2 --max-seeds 3 `
  --max-follow-up-depth 0 `
  --output "$env:TEMP/aion-astra-bounded-campaign"
```

External evidence is disabled unless `--external-web` and a positive
`--external-max-queries` are both supplied.

## Verification

```powershell
python -m ruff check components/aion_astra_autonomous_research_v0.1.0
python -m pytest -q -p no:cacheprovider components/aion_astra_autonomous_research_v0.1.0/tests
python -m compileall -q components/aion_astra_autonomous_research_v0.1.0/src components/aion_astra_autonomous_research_v0.1.0/tests
```

See [`docs/ARCHITECTURE_AND_THREAT_MODEL.md`](docs/ARCHITECTURE_AND_THREAT_MODEL.md)
for the stage, data-flow, and authority-boundary table.
