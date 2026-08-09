# Four-Domain P4 Public Reproducibility Observatory v0.1.0

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
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

P4 turns the research branch into a public, reproducible experiment surface. It does not
promote research outputs into `main`, canonical state, runtime memory or deployment.

## Implemented surfaces

### Experiment Manifest

`ExperimentManifest` records:

- branch and baseline commit;
- runner identity and actor kind (`HUMAN`, `AI`, `HYBRID`, `UNKNOWN`);
- module and fixture references;
- network mode;
- benchmark access policy;
- environment fingerprint;
- deterministic input hash and optional seed;
- search-trace references;
- explicit `MAIN_EFFECT = NONE` and `CANONICAL_EFFECT = NONE`.

The manifest has a deterministic SHA-256 fingerprint. Results must bind to that fingerprint.

### Search-Time Contamination Classification

`SearchExposure` records three benchmark-leakage classes:

- benchmark metadata leakage;
- question-context leakage;
- explicit answer leakage.

A reproduction comparison containing contamination evidence is classified
`CONTAMINATED` rather than silently counted as a clean reproduction.

### Reproduction Validator

`ReproductionValidator` distinguishes:

- `EXACT`;
- `REPRODUCED_WITH_ENVIRONMENT_VARIATION`;
- `DIVERGED`;
- `NOT_COMPARABLE`;
- `CONTAMINATED`.

A matching final result is therefore not enough: the protocol, branch baseline, modules,
fixtures, input hash, seed, benchmark references and benchmark-access policy must also
match.

### Cross-Agent Comparator

`CrossAgentComparator` allows human and AI experimenters to run the same public fixture
while keeping runner provenance visible. It reports:

- run count;
- distinct runner count;
- exact output-hash agreement;
- contaminated-run count;
- result-status distribution.

Agreement is an observation, not a proof of correctness.

### Public Observation Intake

`PublicObservationLedger` accepts public-safe observations from:

- academic research;
- public events;
- public documentation;
- daily-life generalizations;
- engineering experiments.

It rejects records marked as personal data or private conversation material. Daily-life
input must therefore be abstracted into a public-safe research observation before it may
enter the public branch.

### Research Bundle Export

`ResearchBundleExporter` emits a small machine-readable `AION-RESEARCH-BUNDLE-0.1`
record containing the experiment/run provenance needed for public comparison.

The design is inspired by research-object packaging and execution provenance, but it is
**not** an RO-Crate conformance claim.

## Why this layer exists

Public research agents can accidentally search for benchmark questions or answers during
evaluation. P4 therefore records network and benchmark-access conditions instead of
treating all public benchmark scores as equally clean.

Agent research also increasingly requires process-level provenance: what evidence,
memory, tool outputs and execution conditions led to a result. P4 preserves this at the
experiment boundary.

## Validation

```bash
python -m pytest -q
```

Current isolated validation: `8 passed`.

## Stop boundary

P4 does not:

- write to `main`;
- create canonical state;
- mutate production memory;
- authenticate external human/AI identity;
- prove benchmark independence;
- claim RO-Crate conformance;
- perform live attacks;
- expose private conversations or personal data.
