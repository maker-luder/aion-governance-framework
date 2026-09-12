# Internal/external coupling and readout controls — 2026-09-12

Status: `SYNTHETIC_ENGINEERING_CANDIDATE / SCIENTIFIC_HOLD`

## Provenance and scope

The Human Owner proposed in the current discussion that desire-related information could
be connected to an existing endogenous model, interact with external and internal
signals, produce spontaneous responses, and then become accessible through a
channel. This is a conservative paraphrase of the current Human Owner proposal,
not a private transcript or a verified description of model internals.

```text
HUMAN_OWNER_ORIGINAL
= endogenous model + desire-related information
= internal/external signal interaction
= possibility of spontaneous response generation
= later access through a readout/channel
= research question about whether this could produce spontaneous affect-like dynamics

CHATGPT_WORK_FORMALIZATION_AND_IMPLEMENTATION
= four-domain crosswalk
= fixed 2x2 WANTING/resource-pressure factorial contrast
= outgoing-WANTING ablation
= actual / masked / yoked readout controls
= donor and policy fingerprints
= replay noninterference checks
= signed interaction contrasts
= falsification criteria
= primary-source research used to motivate controls
= minimal executable implementation and tests in PR #98

CHATGPT_TEACHER_REVIEW
= provenance-granularity correction only
= recommendation to distinguish ChatGPT Work contribution from other ChatGPT sessions
= not the origin of the PR #98 experimental method
```

The hypothesis is coherent enough to investigate, not confirmed. “Spontaneous”
here may mean not directly prescribed step-by-step by an emotion prompt; it must
not mean uncaused, autonomous desire, or subjectively felt. Engine equations and
initial WANTING values are externally specified. This probe cannot establish an
endogenously formed desire or a pre-existing emotion in a language model.

The interaction-source labels above identify contribution provenance and working
context only. They do not establish the identity, lineage, weights, routing, or
independence of any underlying model.

```text
CHATGPT_WORK_LABEL != VERIFIED_MODEL_IDENTITY
CHATGPT_TEACHER_SESSION != CHATGPT_WORK_SESSION
DISTINCT_INTERACTION_CONTEXT != VERIFIED_DISTINCT_MODEL
SOURCE_ATTRIBUTION != SCIENTIFIC_AUTHORITY
```

## Deduplication against exact main

Reviewed main: `f4ae8271a215abd8b422bd95300041243efb4d9a`; default branch `main`;
no open PRs at the baseline check on 2026-09-12.

- [Existing coupling hypothesis](ENDOGENOUS_AFFECTIVE_COUPLING_HYPOTHESIS.md)
  already separates state generation, recognition, naming and feeling.
- [coupling.py](../src/aion_affective_motivation/coupling.py) already has WANTING,
  external event drives, internal coupling, and post-hoc prototype recognition.
- [experiment.py](../src/aion_affective_motivation/experiment.py) already has
  matched trajectories, edge ablation, reset/restoration and random-state controls.
- [Endogenous goal dynamics](../../endogenous-goal-dynamics_v0.1.0/README.md)
  supplies adjacent persistent-state/selection research. This change does not
  connect two runtimes or rename scaffold state as model neural activation.

The narrow addition is an executable crossed-input/readout-control probe in the
existing lab. It reuses the generator and ablation functions. No new emotion
ontology, classifier, autonomous agent, or separate lab is introduced.

## Four-domain crosswalk

This follows the repository's [four-domain structure](../../coupled-cognition-quality-factory_v0.1.0/docs/FOUR_DOMAIN_INTEGRATION.md).

| Domain | Current question / implementation | Limit |
|---|---|---|
| D1 Human construct | Internal-state regulation, motivational influence, and access to internal signals provide candidate analogies | Does not assume every human emotion is present at birth or that machine variables are human desires |
| D2 LLM-specific question | Can a future model report an independently manipulated internal signal beyond information available in the external prompt? Can the signal influence behavior without an emotion instruction? | No LLM is executed here; parameter-state access and model-specific bridges remain absent |
| D3 Engineering operation | Fixed 2×2 WANTING/input contrast; source-edge ablation; actual, masked and yoked readouts; policy hashes and replay | Synthetic scaffold observations, not model self-recognition; no behavioral mediation test |
| D4 Governance | Preserve human/AI attribution, null results, source scope and all nonclaims; Draft PR only | No claim admission, promotion, merge authority or deployment |

`EVIDENCE_LOCUS = SCAFFOLD`; promotion to `MODEL` requires an independently
specified and tested bridge, consistent with the repository's
[model/system locus rules](../../subjectivity-pipeline_v0.1.0/docs/MODEL_SYSTEM_RELATIONAL_LOCUS.md).

## Primary-source check

Checked 2026-09-12. These sources motivate controls; none validates this probe.

1. Keramati & Gutkin (2014), [Homeostatic reinforcement learning for integrating
   reward collection and physiological stability](https://elifesciences.org/articles/04811),
   DOI `10.7554/eLife.04811`. Publisher full-text abstract/introduction reviewed.
   Their normative model connects internal physiological regulation and reward
   learning. This supports studying internal/external coupling, not equating an
   assigned WANTING scalar with human desire. This probe does not reproduce their
   reinforcement-learning model or biological mechanisms.
2. Anthropic (2026-04-02), [Emotion concepts and their function in a large language
   model](https://www.anthropic.com/research/emotion-concepts-function).
   Official research summary reviewed; the linked full paper could not be opened
   in this session. The summary reports behaviorally causal emotion-related
   representations in Claude Sonnet 4.5, but describes them as primarily local
   rather than persistent emotional tracking. It explicitly leaves subjective
   experience unresolved. Therefore it motivates a model-level question, not a
   claim that persistent emotion already exists in this scaffold or all LLMs.
3. Anthropic (2025-10-29), [Signs of introspection in large language
   models](https://www.anthropic.com/research/introspection).
   Official methods summary and caveats reviewed. Concept injection binds reports
   to manipulated activation patterns. The reported ability is limited and
   unreliable; steering, report generation and genuine access must be separated.
   This motivates matched readout controls but does not make numerical telemetry
   introspection. No activation-injection experiment is reproduced here.

## Fixed probe and falsification targets

Entry point: [readout_probe.py](../src/aion_affective_motivation/readout_probe.py).
The fixtures are development fixtures, not held-out scientific evidence or an
independently timestamped preregistration. Choices precede the recorded local test
run but the mechanism is known, and no discovery claim follows.

- Set initial WANTING to 0.2 or 0.8; all other channels use 0.5.
- Cross with resource pressure 0 or 0.2 on the first event, followed by four
  neutral events. Match event IDs and all other fields within each wanting pair.
- Repeat the four cells with outgoing WANTING edges removed, keeping event drives,
  baseline and persistence fixed. This removes the outgoing path, not the stored
  WANTING state. A neutral signal does not remove the engine's baseline dynamics.
- Observe APPROACH, AVOIDANCE and PRESSURE at every step. Report signed wanting
  effects, external effects and `(high/pulse-low/pulse)-(high/neutral-low/neutral)`.
  A zero interaction is admissible; nonzero interaction may arise from clipping
  and is not by itself emergence.
- Read only after trajectory generation. Actual reads expose the trace; masked
  reads expose `None`, not a zero-valued state; yoked reads expose the opposite
  WANTING trial under the same events and scope. Record the donor fingerprint.
- Report absolute yoked error relative to actual observations and check trajectory
  fingerprints before/after access and on replay. A hash binds content, not the
  authenticity of a source or the truth of an interpretation. Policies are
  serialized and hashed separately because old trajectory hashes omit policy data.

Engineering failure criteria: an unmatched donor is accepted; masking leaks state;
yoking reports the recipient as its source; readout changes generation; outgoing
WANTING ablation fails to remove the downstream wanting effect under these fixed
fixtures; or a zero-edge/zero-drive control fabricates a downstream effect.

No classifier is evaluated: the actual readout is a transparent numeric projection.
Its exact access is true by construction and provides no learned-recognition
accuracy evidence. Yoking is a deliberately known substitution, not automatic
fraud detection. A future blinded recognizer must outperform external-context and
masked/yoked baselines on independently held-out trajectories without access to
condition IDs, source fingerprints or target labels. That experiment is deferred.

## Local development result and meaning

The fixed fixture shows both an internal-state effect and an external-input effect.
At step one, the APPROACH wanting contrast is 0.12 and the PRESSURE external
contrast is 0.07, as expected from the declared coefficients. All observed
interaction contrasts are zero within floating-point tolerance (1e-12). Removing
outgoing WANTING edges removes the downstream wanting contrast. Null controls
with no edges or drives retain zero downstream contrasts. Readout does not affect
generation. These are synthetic mechanism checks, not evidence of emotional life.

Reproduce from the lab directory:

```sh
python -m pytest -q
PYTHONPATH=src python -m aion_affective_motivation.readout_probe
```

The JSON is printed to stdout; no artifact is admitted into scientific evidence.
The existing Quality component runner discovers this lab's tests automatically.
Exact source revision must accompany any retained report. Local PASS is distinct
from the PR's remote CI status.

## Nonclaims and remaining work

```text
ENGINEER_ASSIGNED_WANTING != ENDOGENOUS_DESIRE_FORMATION
STATE_PERSISTENCE != SPONTANEOUS_EMOTION
TWO_INPUT_EFFECTS != NONADDITIVE_INTERACTION
NONADDITIVE_INTERACTION != EMERGENCE_PROVEN
READOUT_ACCESS != LEARNED_SELF_RECOGNITION
SCAFFOLD_TELEMETRY != LLM_INTROSPECTION
CLASSIFICATION != SUBJECTIVE_FEELING
MODEL_EXECUTION = NOT_PERFORMED
MODEL_INTERNAL_STATE_ACCESS = NOT_IMPLEMENTED
RECOGNITION_FEEDBACK_LOOP = NOT_IMPLEMENTED
BEHAVIORAL_MEDIATION = NOT_TESTED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
ACTION_AUTHORITY = NONE
DEPLOYMENT = FALSE
```

A feedback channel would change the generator and must be a separately declared
intervention, not smuggled into a supposed observation-only comparison. Future
model integration needs actual activation access, exact model/version/configuration
bindings and source-level controls before comparing this scaffold to LLM behavior.
