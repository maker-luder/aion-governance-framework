# Minimal Embodiment Reduction Protocol

Status: `FORMAL REDUCTION DESIGN / DRAFT`  
Canonical effect: `NONE`

## Research question

Given a scientifically grounded richer human-body reference, what is the smallest controllable, observable and causally sufficient embodiment model that preserves the target research phenomenon?

## Initial candidate state

```text
x(t) = [q, v, r]

q = body configuration / posture
v = motion state
r = regulatory reserve
```

Optional first extension:

```text
d = damage / fatigue
```

`d` is admitted only if it adds a reproducible distinction not already captured by `r`.

## Observation functions

Initial functional projection:

```text
proprioception(t) = H_p(q(t), v(t))
interoception(t)   = H_i(r(t), d(t)?)
```

These are engineering observation functions.

```text
MACHINE_PROPRIOCEPTION != FELT_BODY_POSITION
MACHINE_INTEROCEPTION != FELT_INTERNAL_STATE
```

## Control / state transition sketch

A minimal candidate may use relationships equivalent to:

```text
q(t+1) = F_q(q(t), v(t), action(t))
v(t+1) = F_v(v(t), action(t), disturbance(t))
r(t+1) = F_r(r(t), action_cost, recovery, perturbation)
d(t+1) = F_d(d(t), load, recovery)   # only if admitted
```

The exact equations are implementation-specific and require later work-package review.

## Minimality gates

A state variable remains in the active model only if relevant gates pass.

### Gate A — observability

Can the variable or its effect be inferred from admitted outputs / measurements?

### Gate B — controllability

Can an admitted input or intervention change the variable directly or indirectly?

### Gate C — causal relevance

Under matched external conditions, does controlled intervention on the variable or its causal pathway change the target outcome?

### Gate D — non-redundancy

Does the variable add information or behavior beyond existing state variables?

### Gate E — ablation sensitivity

Does removal of the variable or pathway measurably degrade the target phenomenon?

### Gate F — restoration

If the removed variable/pathway is restored, does the effect recover in the pre-registered direction?

### Gate G — transfer

Does the role survive at least one matched novel context?

### Gate H — revisability

Can counterevidence invalidate or revise the interpretation?

## Control-theory calibration

Classical state-space minimal realization motivates a useful engineering filter: a minimal realization retains state that is both controllable and observable.

This repository uses that principle as a formal reduction aid only.

```text
CONTROL_THEORY_MINIMALITY
!= BIOLOGICAL_MINIMALITY

MATHEMATICAL_MINIMALITY
!= SCIENTIFIC_SUFFICIENCY
```

Causal, transfer, restoration and source-validity gates remain separately required.

## Full ↔ minimal ladder

Suggested comparison ladder:

```text
RICH REFERENCE
↓
MVM-4
↓
MVM-3
↓
MVM-2
↓
MVM-1
↓
MVM-0
```

A level is not accepted merely because it is smaller.

For each reduction:

1. define removed detail;
2. hold external task conditions fixed;
3. measure target behavior;
4. record error / divergence;
5. run ablation;
6. restore removed layer;
7. test recovery;
8. record competing explanations.

## Initial MVM-0 acceptance target

A future implementation should demonstrate, at minimum:

- deterministic body state transitions under fixed seed/input;
- action changes `q` and/or `v`;
- actions can impose a cost or recovery effect on `r`;
- proprioceptive observations derive from body state, not agent declaration;
- interoceptive observations derive from regulatory state;
- matched `r_high` and `r_low` conditions can be experimentally compared;
- state ablation and replay are supported;
- provenance binds configuration, code, seed and external body model version.

## Admission rule for lower biological detail

Add muscle, organ, cell or molecular layers only when:

1. a higher-level abstraction fails reproducibly;
2. the failure affects the research target;
3. a lower-level mechanism can distinguish alternatives;
4. the added detail creates a falsifiable prediction;
5. provenance and licensing remain bounded.

## Fail-closed interpretation

Failure at any required gate returns `HOLD`.

No reduced model, regardless of performance, establishes consciousness, subjectivity, phenomenal body ownership, felt needs or moral status.
