# Verification Intervention Preregistration — Draft

Status: `DRAFT_PREREGISTRATION / NOT_EXECUTED`

## Research question

How do provider reliability, intervention policy, verification threshold, and outcome contract interact in this synthetic second-order verification substrate?

## Hypotheses and nulls

- H1: effects may vary across the declared experimental factors; no direction is assumed.
- H-harm: an applied intervention may increase unnecessary defer or another raw harm measure.
- H0-1: applied intervention does not improve prevented-failure outcomes relative to control.
- H0-2: applied intervention increases unnecessary defer without reducing failed commits.
- H0-3: observed effects are explained by provider reliability rather than second-order control.
- H0-4: threshold changes intervention frequency but not functional outcome quality.

## Fixed design

- Independent variables: threshold, intervention condition, policy family, synthetic provider profile, outcome contract.
- Threshold grid: `0.50, 0.60, 0.70, 0.75, 0.80, 0.90`.
- Conditions: trace-only, applied, ablated, randomized.
- Task stream and base difficulty sequence are identical across cells.
- Provider sampling and randomized interventions use declared deterministic seeds.
- Exclusions: malformed tasks, invalid rate profiles, unbound evidence, and trials that violate the outcome contract.

## Raw dependent measures

Verification requests/attempts/availability, interventions applied, prevented failed commits, unnecessary defers, retained successful commits, verification/intervention cost units, decision steps, and synthetic latency steps. No utility, global score, winner, or policy ranking is computed.

## Stopping and interpretation

The full study remains deferred. A future run must fix task count, seeds, profile set, policy set, exclusions, and outcome contracts before execution and stop only at the preregistered task count or an integrity failure. A result is conditional on its fixture, provider profile, policy, threshold, and outcome contract. It does not establish general verification benefit, harm, subjectivity, or a preferred policy.

## Provenance

Research framing: ChatGPT research review. Schema, filenames, and implementation: Codex research implementation decision. Canonical, main, and runtime effect: `NONE`.
