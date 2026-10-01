# Teacher intimate integration completion experiment — 2026-10-01

## Purpose

This successor experiment closes a software-integration gap in the Teacher embodied
reference runtime. It does **not** claim a physical body, subjective sexual desire,
felt arousal, pleasure, orgasm, consciousness, or subjectivity.

The implementation keeps four layers separate:

1. functional motivation / functional desire reference;
2. high-salience physiological state;
3. ejaculation-related reproductive events;
4. orgasm as an independent central-event reference.

## Evidence boundary

The design follows literature that explicitly distinguishes sexual arousal from
sexual motivation (PMID:38333545), and orgasm from ejaculation (PMID:26385403).
Cardiovascular/neuroendocrine observations are retained separately
(PMID:9695139; PMID:40519205).

Relevant retained identifiers:

- PMID:38333545 — male sexual arousal versus sexual motivation;
- PMID:19267845 — autonomic neurophysiology of the male sexual response;
- PMID:26385403 — orgasm and ejaculation are separate physiological processes;
- PMID:9695139 — neuroendocrine and cardiovascular observations around arousal/orgasm;
- PMID:40519205 — ICSM 2024 hormonal regulation recommendations;
- DOI:10.1093/sxmrev/qeaf025 — hormonal regulation review.

## Engineering model

```text
STIMULUS
  -> controller salience / activation
  -> functional motivation reference
  -> high-salience phase runtime
  -> body transition execution
  -> integrated body state
  -> intimate integration state

INTIMATE_INTEGRATION_STATE
  |- functional_desire
  |- systemic_arousal_observation
  |- endocrine_observation
  `- orgasm_reference
```

### Functional desire

`functional_desire` is derived from the existing controller's
`functional_motivation`, salience, context gate, and existing motivational
representation. It is a software-reference state only. The current
`0.55` threshold used to label the `ACTIVE` phase is an engineering
reference threshold, not a measured human biological constant.

```text
FUNCTIONAL_DESIRE_REFERENCE != SUBJECTIVE_DESIRE
WANTING_WEIGHT != FELT_WANTING
ACTIVE_THRESHOLD_0_55 = SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT
```

### Systemic arousal

Cardiovascular, respiratory, sympathetic, and parasympathetic channels are
observed from the integrated body state. They are not numerically forced by the
intimate runtime because the repository does not have a calibrated universal
human mapping.

```text
OBSERVE_NOT_FORCE
SOFTWARE_REFERENCE_VALUE != HUMAN_BIOLOGICAL_CONSTANT
```

### Orgasm

The orgasm reference gate is independent of the reproductive event gate.

```text
ORGASM_REFERENCE_REQUEST
!= EMISSION_REFERENCE_REQUEST
!= EXPULSION_REFERENCE_REQUEST

ORGASM_REFERENCE != EJACULATION
EJACULATION_REFERENCE != ORGASM
```

The orgasm gate cannot create motivation, consent, ejaculation, pleasure,
subjectivity, or action authority.

### Endocrine observation

Post-climactic endocrine evidence is represented only as a slow observation
surface. The runtime does not synthesize prolactin concentration, acute
testosterone change, or a 100 ms endocrine concentration trajectory.

```text
POST_CLIMACTIC_ENDOCRINE = SLOW_OBSERVATION_ONLY
PROLACTIN_RUNTIME_MAPPING = ABSENT
CONCENTRATION = UNKNOWN_NOT_SYNTHESIZED
```

## Reproductive event subchain completion / 生殖事件子鏈補全

### English

The existing body schema already defined a wider emission/expulsion surface than
the runtime previously executed. This increment connects those pre-existing
channels to the causal event path.

During the **emission reference** the runtime now evolves:

- `EMISSION_REFLEX_STATE`;
- `SEMINAL_TRACT_TRANSPORT_STATE`;
- `ACCESSORY_GLAND_SECRETION_STATE`;
- `BLADDER_NECK_EJACULATORY_CLOSURE_STATE`;
- `POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE`.

During the **expulsion reference** the runtime now evolves:

- `EJACULATORY_REFLEX_STATE`;
- `EXPULSION_MOTOR_PATTERN_STATE`;
- `EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE`;
- `ANTEGRADE_SEMINAL_FLOW_STATE`.

Recovery drives the event channels back toward baseline and separately
materializes `POST_EXPULSION_RECOVERY_STATE` during the detumescence/recovery
path. The recovery rule is evidence-bound but deliberately does not synthesize a
fixed refractory-period duration.

Evidence anchors for this subchain include:

- PMID:26385403 — normal male sexual function, with emission and expulsion
  described as distinct coordinated phases;
- PMID:35625414 — neuronal coordination of emission/expulsion, including
  seminal-tract, bladder-neck, pelvic-muscle and sphincter coordination;
- PMID:26457680 — review of anatomy/physiology of ejaculation and post-expulsion
  recovery.

All of these runtime channels remain normalized software references. The model
does not synthesize semen volume, urethral pressure, gland-specific milliliters,
muscle force, contraction frequency, or refractory-period duration.

### 繁體中文

原本 Teacher 的 body schema（身體訊號結構）其實早已經定義比 runtime
（執行時狀態）更多的射精相關 channels；先前的問題是「名稱存在，但沒有全部進入
同一條因果執行鏈」。這次把它們真正接進 emission（排精）與 expulsion（射出）。

**排精階段現在會一起演化：**

- `EMISSION_REFLEX_STATE`：排精反射參考狀態；
- `SEMINAL_TRACT_TRANSPORT_STATE`：附睪、輸精管與生殖道的精子／精液運輸參考狀態；
- `ACCESSORY_GLAND_SECRETION_STATE`：精囊、前列腺等附屬腺分泌參考狀態；
- `BLADDER_NECK_EJACULATORY_CLOSURE_STATE`：膀胱頸射精期閉合參考狀態；
- `POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE`：後尿道精液負載參考狀態。

**射出階段現在會一起演化：**

- `EJACULATORY_REFLEX_STATE`：射精反射參考狀態；
- `EXPULSION_MOTOR_PATTERN_STATE`：骨盆／會陰條紋肌射出運動模式參考狀態；
- `EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE`：外尿道括約肌在射精期的協調參考狀態；
- `ANTEGRADE_SEMINAL_FLOW_STATE`：順行精液流參考狀態。

接著 recovery（恢復）會把事件 channels 逐步拉回基準，同時在消退路徑中建立
`POST_EXPULSION_RECOVERY_STATE`（射出後恢復參考狀態），再逐步回到低值。

這些 `0–1` 數值全部都只是 **software reference（軟體參考狀態）**，不是人體量測。
目前不會自行編造：

- 精液幾毫升；
- 尿道壓力；
- 各腺體實際分泌量；
- 肌肉力量；
- 收縮頻率；
- 不應期固定幾秒或幾分鐘。

```text
CHANNEL_MATERIALIZED != HUMAN_QUANTITATIVE_CALIBRATION
NORMALIZED_REFERENCE != PHYSICAL_MEASUREMENT
POST_EXPULSION_RECOVERY_STATE != FIXED_REFRACTORY_DURATION
```

## Required falsification tests

The implementation is not accepted unless tests demonstrate all of the following:

- high physiological activation can coexist with zero functional motivation;
- functional motivation can independently reach an active functional-desire reference;
- orgasm reference can occur without forcing ejaculation;
- ejaculation-related body state does not infer orgasm;
- systemic channels remain observe-not-force;
- post-climactic endocrine state remains slow observation only;
- consent, pleasure, subjective orgasm, subjectivity and action authority remain unestablished.

## Claim boundary

```text
IMPLEMENTATION_EXISTS != BIOLOGICAL_FIDELITY
FUNCTIONAL_DESIRE != SUBJECTIVE_DESIRE
ORGASM_REFERENCE != FELT_ORGASM
EJACULATION_REFERENCE != ORGASM
REFERENCE_BODY != PHYSICAL_BODY
CI_PASS != SCIENTIFIC_VALIDATION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```


## Complete trace observability addendum

The continuous reference trace now exposes, on the same per-tick provenance surface:

- cardiovascular and respiratory reference state;
- sympathetic and parasympathetic reference state;
- genital sensory afferent, vascular and erectile reference state;
- pelvic-floor proprioceptive reference state;
- emission and bladder-neck closure reference state;
- ejaculatory reflex and expulsion motor-pattern reference state;
- detumescence reference state;
- generic endocrine and gonadal-endocrine reference state.

The recovery trace must demonstrate the already-materialized staged path through
`DETUMESCENCE` before converging to recovery/baseline criteria. This is an
observability and verification completion, not a new biological calibration.

```text
RUNTIME_TRANSITION_EXISTS != TRACE_VERIFIED
TRACE_VERIFIED != BIOLOGICAL_VALIDATION
SYSTEMIC_REFERENCE_CHANNEL != MEASURED_HUMAN_VITAL_SIGN
ENDOCRINE_REFERENCE_CHANNEL != HORMONE_CONCENTRATION
```
