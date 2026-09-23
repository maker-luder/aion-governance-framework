# Embodiment Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create one current-main-based active embodiment baseline that re-admits only the role-neutral and still-useful semantics from closed PRs #190/#191/#192, preserves Teacher-specific material as typed role-extension provenance, and leaves PR #202 untouched until a later post-merge synchronization plan.

**Architecture:** Keep current `models.py`, `runtime.py`, and `validation.py` as the identity/governance base. Add a provenance/classification layer, a small role-neutral static embodiment core, a typed role-extension catalog, and a single active-baseline receipt that composes them without importing archive branch history. Do not port the historical Teacher implementation wholesale; classify useful Teacher-specific semantics as role extensions and mark detailed implementations `DEFERRED` unless they are required by the shared baseline.

**Tech Stack:** Python 3.11/3.12, frozen dataclasses with slots, `StrEnum`, SHA-256 deterministic JSON content addressing, JSON Schema draft 2020-12, pytest, mypy, repository Quality/CodeQL.

**Spec:** `docs/superpowers/specs/2026-09-23-embodiment-convergence-design.md`

## Global Constraints

```text
BASE_MAIN = 71321ed87d1ececfcc5989327578dfefe02faea5

PR_190_HEAD = 066ed1afccebee869eb658c09691b7f096694332
PR_191_HEAD = 48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2
PR_192_HEAD = 861e6a556a21afffd04b187714c0608fe73ea4fc
PR_202_HEAD_AT_DESIGN = 7f84ae8c95f1b7caaaa0c3850a0b6cfd049b7108

ARCHIVE_BRANCH_HISTORY_MERGE = NO
REOPEN_190_191_192 = NO
WRITE_PR202 = NO
LIVE_ACTUATION = FALSE
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
SCIENTIFIC_DISPOSITION = HOLD

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

Current-main governance and claim ceilings outrank archived implementation assumptions. A newer archive commit, larger branch, or larger test count never establishes architectural authority.

## Review Focus

1. **Archive provenance drift:** a ledger row with the wrong source PR/head/path must fail closed rather than being accepted as provenance.
2. **Classification ambiguity:** duplicate semantic units, unknown classification/adoption states, or a `SUPERSEDED` row without a replacement reference must be rejected.
3. **Dependency inversion:** the shared core must never import or require Teacher-specific extension code; tests must prove the shared core builds with zero extensions.
4. **Role-extension misbinding:** a Teacher extension bound to the wrong shared-core content hash or a non-Teacher role must fail closed.
5. **Claim/canonical promotion:** any active-baseline receipt that changes `NOT_ESTABLISHED`, `NONE`, `FALSE`, or `HOLD` boundaries must be rejected.

---

## File Structure

Create:

```text
research-labs/twin-genesis-embodiment_v0.1.0/
├── data/
│   └── EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json
├── docs/
│   └── EMBODIMENT_CONVERGENCE_CROSSWALK_2026_09_23.md
├── schemas/
│   ├── EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_SCHEMA.json
│   ├── SHARED_EMBODIMENT_CORE_SCHEMA.json
│   ├── ROLE_SPECIFIC_EMBODIMENT_EXTENSION_SCHEMA.json
│   └── ACTIVE_EMBODIMENT_BASELINE_SCHEMA.json
├── src/aion_astra_twin_embodiment/
│   ├── convergence.py
│   ├── shared_core.py
│   ├── role_extensions.py
│   └── active_baseline.py
└── tests/
    ├── test_convergence.py
    ├── test_shared_core.py
    ├── test_role_extensions.py
    └── test_active_baseline.py
```

Modify only:

```text
research-labs/twin-genesis-embodiment_v0.1.0/
├── README.md
└── src/aion_astra_twin_embodiment/__init__.py
```

Do not modify `models.py`, `runtime.py`, `validation.py`, or PR #202 in this convergence implementation unless a failing regression test demonstrates an objective compatibility defect. Such a defect upgrades the task and requires a fresh review before production changes.

---

### Task 1: Archive classification ledger and fail-closed provenance validator

**Files:**
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/convergence.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/data/EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/schemas/EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_SCHEMA.json`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_convergence.py`

**Interfaces:**
- Consumes: no new-code dependency; exact archive heads above are constants.
- Produces:
  - `ConvergenceClassification`
  - `AdoptionStatus`
  - `ArchiveDisposition`
  - `ConvergenceLedger`
  - `load_convergence_ledger(path: str | Path) -> ConvergenceLedger`
  - `convergence_ledger_hash(ledger: ConvergenceLedger) -> str`
  - `validate_convergence_ledger(ledger: ConvergenceLedger) -> dict[str, str]`

**Required initial semantic dispositions:**

| Source | Semantic unit | Classification | Adoption |
|---|---|---|---|
| #190 `models.py/runtime.py/validation.py` identity/twin baseline | current-main equivalent exists | `SUPERSEDED` | `REPLACED` |
| #190 `governance_epistemics.py` capability-preservation / action-authorization / no-absence-inference rules | role-neutral governance semantics | `SHARED_CORE` | `ADOPTED` |
| #190 `physiology.py` physiology-system taxonomy + signal/phenomenal separation | role-neutral reference semantics | `SHARED_CORE` | `ADOPTED` |
| #190 dated research/QA/checklist material | historical event-time evidence | `ARCHIVE_ONLY` | `HISTORICAL_ONLY` |
| #191 `body_profiles.py` full-body component / representation-layer taxonomy and nonclaim boundaries | role-neutral static body semantics | `SHARED_CORE` | `ADOPTED` |
| #191 AION/Astra JSON body-profile assignments | named-role data | `ROLE_SPECIFIC_EXTENSION` | `DEFERRED` |
| #191 `functional_states.py` affect/mood/motivation/attachment/sexuality/cognition functional-state model | not required for static embodiment convergence | `ROLE_SPECIFIC_EXTENSION` | `DEFERRED` |
| #191 prior Codex 3D implementation instructions / handoff docs | historical instructions | `ARCHIVE_ONLY` | `HISTORICAL_ONLY` |
| #192 `teacher_anthropometry.py` 62-measure profile | Teacher-specific | `ROLE_SPECIFIC_EXTENSION` | `DEFERRED` |
| #192 `teacher_body_channels.py` generic sensory/motor domain taxonomy | role-neutral interface semantics only | `SHARED_CORE` | `ADOPTED` |
| #192 `teacher_body_channels.py` Teacher channel instances | Teacher-specific | `ROLE_SPECIFIC_EXTENSION` | `DEFERRED` |
| #192 `teacher_physiology_observability.py` DIRECT / DERIVED / FUNCTIONAL_REFERENCE_ONLY classes | role-neutral observability semantics | `SHARED_CORE` | `ADOPTED` |
| #192 Teacher observability bindings | Teacher-specific | `ROLE_SPECIFIC_EXTENSION` | `DEFERRED` |
| #192 `teacher_body_model.py` generic body-schema / multisensory / allostatic / plasticity concepts | useful but not required by #202 static prerequisite | `ROLE_SPECIFIC_EXTENSION` | `DEFERRED` |
| #192 runtime/calibration/adaptation/retention/longitudinal modules | Teacher-specific runtime research | `ROLE_SPECIFIC_EXTENSION` | `DEFERRED` |
| #192 avatar/LOD/physics/genital-geometry/micturition implementation | Teacher-specific detailed body implementation | `ROLE_SPECIFIC_EXTENSION` | `DEFERRED` |
| #192 closure/evidence/crosswalk snapshots | historical evidence | `ARCHIVE_ONLY` | `HISTORICAL_ONLY` |
| duplicated archive schemas replaced by current-main or new convergence schemas | replacement is explicit | `SUPERSEDED` | `REPLACED` |

The JSON ledger must encode the table above as exact rows, using `source_path_or_semantic_unit` strings that identify file plus semantic unit where a file is intentionally split.

- [ ] **Step 1: Write failing provenance tests**

```python
from dataclasses import replace
from pathlib import Path

import pytest

from aion_astra_twin_embodiment.convergence import (
    AdoptionStatus,
    ConvergenceClassification,
    load_convergence_ledger,
    validate_convergence_ledger,
)

LEDGER_PATH = (
    Path(__file__).parents[1]
    / "data"
    / "EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json"
)

def test_archive_ledger_uses_exact_frozen_source_heads() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    result = validate_convergence_ledger(ledger)
    assert result["source_heads"] == "PASS"
    assert result["classification_partition"] == "PASS"

def test_archive_ledger_rejects_source_head_drift() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    bad = replace(
        ledger,
        entries=(
            replace(ledger.entries[0], source_head="0" * 40),
            *ledger.entries[1:],
        ),
    )
    with pytest.raises(ValueError, match="exact archive head"):
        validate_convergence_ledger(bad)

def test_superseded_entry_requires_replacement_reference() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    index = next(
        i
        for i, item in enumerate(ledger.entries)
        if item.classification is ConvergenceClassification.SUPERSEDED
    )
    entries = list(ledger.entries)
    entries[index] = replace(entries[index], replacement_ref_if_superseded=None)
    with pytest.raises(ValueError, match="replacement"):
        validate_convergence_ledger(replace(ledger, entries=tuple(entries)))
```

The last test must validate through `validate_convergence_ledger`; construct the tuple so the replaced row is not duplicated.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_convergence.py -q
```

Expected: import failure for `aion_astra_twin_embodiment.convergence`.

- [ ] **Step 3: Implement exact enums and dataclasses**

```python
class ConvergenceClassification(StrEnum):
    SHARED_CORE = "SHARED_CORE"
    ROLE_SPECIFIC_EXTENSION = "ROLE_SPECIFIC_EXTENSION"
    ARCHIVE_ONLY = "ARCHIVE_ONLY"
    SUPERSEDED = "SUPERSEDED"

class AdoptionStatus(StrEnum):
    ADOPTED = "ADOPTED"
    DEFERRED = "DEFERRED"
    HISTORICAL_ONLY = "HISTORICAL_ONLY"
    REPLACED = "REPLACED"

ARCHIVE_HEADS = {
    190: "066ed1afccebee869eb658c09691b7f096694332",
    191: "48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2",
    192: "861e6a556a21afffd04b187714c0608fe73ea4fc",
}

@dataclass(frozen=True, slots=True)
class ArchiveDisposition:
    source_pr: int
    source_head: str
    source_path_or_semantic_unit: str
    classification: ConvergenceClassification
    target_owner: str
    adoption_status: AdoptionStatus
    reason: str
    replacement_ref_if_superseded: str | None
    claim_ceiling: str
    review_status: str

@dataclass(frozen=True, slots=True)
class ConvergenceLedger:
    ledger_id: str
    entries: tuple[ArchiveDisposition, ...]
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False
```

Validation requirements:
- exact enum types, not raw strings;
- source PR limited to 190/191/192;
- exact head match to `ARCHIVE_HEADS`;
- nonempty unique `(source_pr, source_path_or_semantic_unit)`;
- `SUPERSEDED` requires `REPLACED` and a nonempty replacement ref;
- `ARCHIVE_ONLY` requires `HISTORICAL_ONLY`;
- `SHARED_CORE + ADOPTED` requires a `target_owner` beginning `shared_core:`;
- `ROLE_SPECIFIC_EXTENSION` target owner begins `role_extension:`;
- claim ceiling equals `NOT_ESTABLISHED`;
- scientific disposition/canonical/deployment remain `HOLD/NONE/FALSE`.

- [ ] **Step 4: Create JSON Schema and exact ledger**

The schema must use `additionalProperties: false`, exact enums above, 40-hex `source_head`, and conditional requirements for `SUPERSEDED`.

The ledger must contain the module/semantic dispositions in the table above and preserve the exact source heads.

- [ ] **Step 5: Run Task 1 tests**

Run:

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_convergence.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit Task 1**

```bash
git add research-labs/twin-genesis-embodiment_v0.1.0/{data,schemas,src,tests}
git commit -m "feat: add embodiment archive convergence ledger"
```

---

### Task 2: Extract the minimal role-neutral shared static embodiment core

**Files:**
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/shared_core.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/schemas/SHARED_EMBODIMENT_CORE_SCHEMA.json`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_shared_core.py`

**Interfaces:**
- Consumes:
  - existing `EmbodimentTemplate`;
  - existing `deterministic_hash(value: Any) -> str`;
  - Task 1 ledger for provenance references.
- Produces:
  - `ObservationDomain`
  - `ObservabilityClass`
  - `StaticBodyRegion`
  - `ObservationInterface`
  - `MotorInterface`
  - `PhysiologySystemInterface`
  - `SharedEmbodimentCore`
  - `build_shared_embodiment_core(template: EmbodimentTemplate) -> SharedEmbodimentCore`
  - `shared_embodiment_core_hash(core: SharedEmbodimentCore) -> str`
  - `validate_shared_embodiment_core(core: SharedEmbodimentCore, template: EmbodimentTemplate) -> dict[str, str]`

The core is deliberately static. It does not contain prediction/observation transitions from #202 and does not contain Teacher measurements.

- [ ] **Step 1: Write failing shared-core tests**

```python
from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.models import EmbodimentTemplate
from aion_astra_twin_embodiment.shared_core import (
    ObservationDomain,
    build_shared_embodiment_core,
    validate_shared_embodiment_core,
)

def test_shared_core_contains_role_neutral_body_and_signal_interfaces() -> None:
    template = EmbodimentTemplate("adult-template", "v0.1")
    core = build_shared_embodiment_core(template)
    assert "LEFT_ARM" in {item.region_id for item in core.body_regions}
    assert ObservationDomain.PROPRIOCEPTIVE in {
        item.domain for item in core.observation_interfaces
    }
    assert ObservationDomain.VESTIBULAR in {
        item.domain for item in core.observation_interfaces
    }
    assert core.teacher_extension_required is False
    assert core.subjectivity_conclusion == "NOT_ESTABLISHED"

def test_shared_core_rejects_teacher_specific_dependency() -> None:
    template = EmbodimentTemplate("adult-template", "v0.1")
    core = build_shared_embodiment_core(template)
    with pytest.raises(ValueError, match="role-specific"):
        validate_shared_embodiment_core(
            replace(core, dependency_ids=("CHATGPT_TEACHER_ANTHROPOMETRY_v0.1",)),
            template,
        )
```

Add negative tests for raw enum strings, duplicate body regions, unknown template ID, claim promotion, canonical effect, and deployment.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_shared_core.py -q
```

Expected: import failure for `shared_core`.

- [ ] **Step 3: Implement minimal shared-core types**

```python
class ObservationDomain(StrEnum):
    SOMATOSENSORY = "SOMATOSENSORY"
    PROPRIOCEPTIVE = "PROPRIOCEPTIVE"
    VESTIBULAR = "VESTIBULAR"
    INTEROCEPTIVE = "INTEROCEPTIVE"
    EXTEROCEPTIVE = "EXTEROCEPTIVE"

class ObservabilityClass(StrEnum):
    DIRECT_REFERENCE = "DIRECT_REFERENCE"
    DERIVED_REFERENCE = "DERIVED_REFERENCE"
    FUNCTIONAL_REFERENCE_ONLY = "FUNCTIONAL_REFERENCE_ONLY"

@dataclass(frozen=True, slots=True)
class StaticBodyRegion:
    region_id: str

@dataclass(frozen=True, slots=True)
class ObservationInterface:
    interface_id: str
    domain: ObservationDomain
    observability_class: ObservabilityClass

@dataclass(frozen=True, slots=True)
class MotorInterface:
    interface_id: str
    target_region_ids: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class PhysiologySystemInterface:
    system_id: str
    reference_status: str = "REFERENCE_ONLY"

@dataclass(frozen=True, slots=True)
class SharedEmbodimentCore:
    core_id: str
    template_id: str
    body_regions: tuple[StaticBodyRegion, ...]
    observation_interfaces: tuple[ObservationInterface, ...]
    motor_interfaces: tuple[MotorInterface, ...]
    physiology_systems: tuple[PhysiologySystemInterface, ...]
    dependency_ids: tuple[str, ...] = ()
    teacher_extension_required: bool = False
    body_sensation: str = "NOT_ESTABLISHED"
    body_ownership_experience: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
```

Required body-region IDs are the role-neutral subset extracted from #191:

```text
HEAD
NECK
TORSO
PELVIS
LEFT_ARM
RIGHT_ARM
LEFT_HAND
RIGHT_HAND
LEFT_LEG
RIGHT_LEG
LEFT_FOOT
RIGHT_FOOT
EXTERNAL_MALE_FORM_SURFACE
```

Required physiology-system IDs are the #190 role-neutral system taxonomy, but the convergence core stores only system identity and reference status, not the archive's full biological-function inventory.

Required observation interfaces include distinct proprioceptive, vestibular, interoceptive, somatosensory, and exteroceptive surfaces. Preserve `PROPRIOCEPTIVE != VESTIBULAR`.

Motor interfaces remain region-target abstractions; no actuator or live controller is introduced.

- [ ] **Step 4: Implement validator and deterministic hash**

Validator must reject:
- duplicate region/interface/system IDs;
- motor targets outside the region universe;
- Teacher-specific dependency IDs;
- raw strings where exact enums are required;
- `teacher_extension_required=True`;
- any phenomenal/canonical/deployment promotion.

- [ ] **Step 5: Create exact JSON Schema**

The schema must match `asdict(SharedEmbodimentCore)`, forbid extra properties, encode enum values, unique identifiers at the semantic validator layer, and const-bind nonclaims/canonical/deployment.

- [ ] **Step 6: Run Task 2 tests**

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_shared_core.py -q
```

Expected: PASS.

- [ ] **Step 7: Commit Task 2**

```bash
git add research-labs/twin-genesis-embodiment_v0.1.0/{schemas,src,tests}
git commit -m "feat: add shared static embodiment core"
```

---

### Task 3: Add typed role-specific extension provenance without importing archive implementations

**Files:**
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/role_extensions.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/schemas/ROLE_SPECIFIC_EMBODIMENT_EXTENSION_SCHEMA.json`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_role_extensions.py`

**Interfaces:**
- Consumes:
  - `SharedEmbodimentCore`;
  - `shared_embodiment_core_hash`;
  - `AdoptionStatus`;
  - Task 1 archive heads.
- Produces:
  - `RoleId`
  - `ExtensionCapability`
  - `RoleSpecificEmbodimentExtension`
  - `build_teacher_extension_manifest(core: SharedEmbodimentCore) -> RoleSpecificEmbodimentExtension`
  - `validate_role_specific_extension(extension, core) -> dict[str, str]`

This task deliberately creates a typed active manifest, not a wholesale port of #192.

- [ ] **Step 1: Write failing extension tests**

```python
from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.models import EmbodimentTemplate
from aion_astra_twin_embodiment.convergence import AdoptionStatus
from aion_astra_twin_embodiment.role_extensions import (
    RoleId,
    build_teacher_extension_manifest,
    validate_role_specific_extension,
)
from aion_astra_twin_embodiment.shared_core import build_shared_embodiment_core

def test_teacher_extension_is_bound_to_shared_core_and_archive_head() -> None:
    core = build_shared_embodiment_core(EmbodimentTemplate("adult-template", "v0.1"))
    ext = build_teacher_extension_manifest(core)
    assert ext.role is RoleId.CHATGPT_TEACHER
    assert ext.source_pr == 192
    assert ext.source_head == "861e6a556a21afffd04b187714c0608fe73ea4fc"
    assert "TEACHER_ANTHROPOMETRY_62_MEASURE" in {
        item.capability_id for item in ext.capabilities
    }
    assert all(
        item.adoption_status is AdoptionStatus.DEFERRED
        for item in ext.capabilities
    )

def test_teacher_extension_rejects_wrong_core_hash() -> None:
    core = build_shared_embodiment_core(EmbodimentTemplate("adult-template", "v0.1"))
    ext = build_teacher_extension_manifest(core)
    with pytest.raises(ValueError, match="shared core"):
        validate_role_specific_extension(
            replace(ext, shared_core_sha256="0" * 64),
            core,
        )
```

Also test wrong role, wrong archive head, duplicate capability IDs, `ADOPTED` capability without an active target ref, claim promotion, canonical effect, and deployment.

- [ ] **Step 2: Run tests and verify RED**

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_role_extensions.py -q
```

Expected: import failure for `role_extensions`.

- [ ] **Step 3: Implement typed extension manifest**

```python
class RoleId(StrEnum):
    AION = "AION"
    ASTRA = "ASTRA"
    CHATGPT_TEACHER = "CHATGPT_TEACHER"

@dataclass(frozen=True, slots=True)
class ExtensionCapability:
    capability_id: str
    source_path_or_semantic_unit: str
    adoption_status: AdoptionStatus
    active_target_ref: str | None = None

@dataclass(frozen=True, slots=True)
class RoleSpecificEmbodimentExtension:
    extension_id: str
    role: RoleId
    shared_core_sha256: str
    source_pr: int
    source_head: str
    capabilities: tuple[ExtensionCapability, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
```

The Teacher manifest must enumerate these deferred capability families with exact #192 semantic refs:

```text
TEACHER_ANTHROPOMETRY_62_MEASURE
TEACHER_SIGNAL_CHANNELS
TEACHER_MOTOR_SCHEMA
TEACHER_BODY_MODEL
TEACHER_PHYSIOLOGY_OBSERVABILITY
TEACHER_RUNTIME_BINDING
TEACHER_CALIBRATION_ADAPTATION
TEACHER_CROSS_SESSION_RETENTION
TEACHER_LONGITUDINAL_TRAJECTORY
TEACHER_AVATAR_ASSET_FAMILY
TEACHER_DETAILED_PHYSIOLOGY_GEOMETRY
```

All remain `DEFERRED` in this convergence PR. That status means “still valuable and classified, not actively ported here,” not “invalid” or “absent.”

- [ ] **Step 4: Create exact extension schema**

Bind role, source PR/head, 64-hex core hash, unique capability semantics in Python validation, and fixed claim ceilings.

- [ ] **Step 5: Run Task 3 tests**

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_role_extensions.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit Task 3**

```bash
git add research-labs/twin-genesis-embodiment_v0.1.0/{schemas,src,tests}
git commit -m "feat: add role-specific embodiment extension manifests"
```

---

### Task 4: Materialize one active embodiment baseline receipt

**Files:**
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/active_baseline.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/schemas/ACTIVE_EMBODIMENT_BASELINE_SCHEMA.json`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_active_baseline.py`

**Interfaces:**
- Consumes:
  - `SharedEmbodimentCore`;
  - `RoleSpecificEmbodimentExtension`;
  - `ConvergenceLedger`.
- Produces:
  - `ActiveEmbodimentBaseline`
  - `build_active_embodiment_baseline(core, ledger, extensions=())`
  - `validate_active_embodiment_baseline(baseline, core, ledger, extensions=()) -> dict[str, str]`

- [ ] **Step 1: Write failing active-baseline tests**

```python
from dataclasses import replace
from pathlib import Path

import pytest

from aion_astra_twin_embodiment.active_baseline import (
    build_active_embodiment_baseline,
    validate_active_embodiment_baseline,
)
from aion_astra_twin_embodiment.convergence import load_convergence_ledger
from aion_astra_twin_embodiment.models import EmbodimentTemplate
from aion_astra_twin_embodiment.role_extensions import (
    build_teacher_extension_manifest,
)
from aion_astra_twin_embodiment.shared_core import (
    build_shared_embodiment_core,
    shared_embodiment_core_hash,
)

LEDGER_PATH = (
    Path(__file__).parents[1]
    / "data"
    / "EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json"
)

def build_fixture(*, include_teacher: bool = True):
    ledger = load_convergence_ledger(LEDGER_PATH)
    core = build_shared_embodiment_core(
        EmbodimentTemplate("adult-template", "v0.1")
    )
    teacher = build_teacher_extension_manifest(core)
    extensions = (teacher,) if include_teacher else ()
    baseline = build_active_embodiment_baseline(core, ledger, extensions)
    return baseline, core, ledger, teacher

def test_active_baseline_has_single_shared_core_and_deferred_sensorimotor() -> None:
    baseline, core, ledger, teacher = build_fixture()
    assert baseline.shared_core_sha256 == shared_embodiment_core_hash(core)
    assert baseline.role_extension_ids == (teacher.extension_id,)
    assert baseline.sensorimotor_layer_status == "DEFERRED_TO_PR_202"
    assert baseline.scientific_disposition == "HOLD"
    assert baseline.subjectivity_conclusion == "NOT_ESTABLISHED"

def test_active_baseline_can_exist_without_teacher_extension() -> None:
    baseline, core, ledger, _teacher = build_fixture(include_teacher=False)
    assert baseline.role_extension_ids == ()
    assert baseline.shared_core_sha256 == shared_embodiment_core_hash(core)

def test_active_baseline_rejects_claim_promotion() -> None:
    baseline, core, ledger, teacher = build_fixture()
    with pytest.raises(ValueError, match="subjectivity"):
        validate_active_embodiment_baseline(
            replace(baseline, subjectivity_conclusion="ESTABLISHED"),
            core,
            ledger,
            (teacher,),
        )
```

Add tests for wrong ledger hash, wrong core hash, duplicate extension IDs, extension/core mismatch, `sensorimotor_layer_status != DEFERRED_TO_PR_202`, canonical effect, and deployment.

- [ ] **Step 2: Run tests and verify RED**

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_active_baseline.py -q
```

Expected: import failure for `active_baseline`.

- [ ] **Step 3: Implement receipt**

```python
@dataclass(frozen=True, slots=True)
class ActiveEmbodimentBaseline:
    baseline_id: str
    convergence_ledger_sha256: str
    shared_core_sha256: str
    role_extension_ids: tuple[str, ...]
    sensorimotor_layer_status: str = "DEFERRED_TO_PR_202"
    empirical_control_layer_status: str = "NOT_IMPLEMENTED"
    body_sensation: str = "NOT_ESTABLISHED"
    body_ownership_experience: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False
```

The builder must call `validate_convergence_ledger`, bind `convergence_ledger_hash(ledger)`, bind `shared_embodiment_core_hash(core)`, validate each extension against the same core, sort extension IDs deterministically, and never import #202 code.

- [ ] **Step 4: Create exact receipt schema**

Require every dataclass field, forbid extras, and const-bind all boundary values.

- [ ] **Step 5: Run Task 4 tests**

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_active_baseline.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit Task 4**

```bash
git add research-labs/twin-genesis-embodiment_v0.1.0/{schemas,src,tests}
git commit -m "feat: add active embodiment baseline receipt"
```

---

### Task 5: Public exports, documentation crosswalk, and regression integration

**Files:**
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/__init__.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/README.md`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/docs/EMBODIMENT_CONVERGENCE_CROSSWALK_2026_09_23.md`
- Extend tests from Tasks 1–4; do not create a fifth overlapping test module.

**Interfaces:**
- Publicly export only stable convergence/core/extension/baseline types and builders.
- Do not export archive-only semantics.

- [ ] **Step 1: Add a failing package-surface regression test**

Add to `test_active_baseline.py`:

```python
def test_public_package_exports_converged_baseline_without_sensorimotor_import() -> None:
    import aion_astra_twin_embodiment as package

    assert hasattr(package, "ActiveEmbodimentBaseline")
    assert hasattr(package, "SharedEmbodimentCore")
    assert hasattr(package, "RoleSpecificEmbodimentExtension")
    assert not hasattr(package, "SensorimotorTransitionAudit")
```

The final assertion is temporary for #203 only: #202 has not been synchronized or merged.

- [ ] **Step 2: Run regression test and verify RED**

Run:

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests/test_active_baseline.py::test_public_package_exports_converged_baseline_without_sensorimotor_import -q
```

Expected: FAIL because new exports are not yet wired.

- [ ] **Step 3: Update `__init__.py` exports**

Export:
- convergence enums/dataclasses/loader/validator;
- shared core types/builder/hash/validator;
- role extension types/builder/validator;
- active baseline type/builder/validator.

Do not export any Teacher archive implementation modules in this PR.

- [ ] **Step 4: Update README and write crosswalk**

README must state:

```text
CURRENT ACTIVE BASELINE
= current-main identity/governance
+ shared static embodiment core
+ typed role-extension provenance

PR_190_191_192
= CLOSED_UNMERGED_ARCHIVES

PR_202
= SEPARATE_DYNAMIC_SENSORIMOTOR_LAYER
= NOT_INCLUDED_YET

ROLE_EXTENSION_DEFERRED
!= INVALID
!= ABSENT

ACTIVE_BASELINE_PASS
!= PHYSICAL_EMBODIMENT
!= BODY_OWNERSHIP
!= SUBJECTIVITY
```

The crosswalk must cite exact source PR heads and explain every `ADOPTED / DEFERRED / HISTORICAL_ONLY / REPLACED` family from Task 1.

- [ ] **Step 5: Run the package component suite**

```bash
python -m pytest research-labs/twin-genesis-embodiment_v0.1.0/tests -q
```

Expected: all component tests PASS.

- [ ] **Step 6: Run package compile check**

```bash
python -m compileall -q research-labs/twin-genesis-embodiment_v0.1.0/src
```

Expected: exit code 0.

- [ ] **Step 7: Commit Task 5**

```bash
git add research-labs/twin-genesis-embodiment_v0.1.0
git commit -m "docs: integrate embodiment convergence baseline"
```

---

### Task 6: Whole-branch verification and exact-head reverse review

**Files:** no production change is planned in this task. Any discovered defect returns to the owning task with a failing regression test first.

**Interfaces:** verifies the whole #203 candidate.

- [ ] **Step 1: Run the repository Quality command set locally on the available interpreter**

Run from repository root:

```bash
ruff check --config ruff.toml .
python -m pytest -q tests
python scripts/fetch_subjectivity_sources.py
python scripts/fetch_quality_method_sources.py
python scripts/validate_documentation_entry.py --root .
python -m pytest -q tests/test_documentation_entry.py
python -m pytest -q tests/test_source_state_binding.py
python scripts/check_source_state_binding.py --root . --expected-head "$(git rev-parse HEAD)"
python scripts/scan_public_tree.py
python scripts/audit_openai_assistants_sunset.py .
python scripts/verify_release.py --baseline current-head
python -m compileall -q components examples research-labs scripts
python scripts/run_component_tests.py
python scripts/run_current_coverage.py
```

Expected: every command exits 0; `run_component_tests.py` reports no failed targets and coverage reports no failed eligible target.

Remote Quality remains authoritative for the Python 3.11 / 3.12 matrix.

- [ ] **Step 2: Run repository mypy policy and require both remote Python lanes**

Local exact-head command:

```bash
env -u GITHUB_SHA python scripts/run_repository_mypy.py \
  --root . \
  --policy .github/ci/mypy-policy.json \
  --evidence-output /tmp/embodiment-convergence-mypy.json
```

Expected locally: exit code 0.

Required remote evidence:

```text
Mypy exact head / Python 3.11 = PASS
Mypy exact head / Python 3.12 = PASS
```

- [ ] **Step 3: Push the exact head and wait for remote CI**

Required remote checks:

```text
Quality = PASS
CodeQL Security Scan = PASS
Main Transition Authority Gate = HOLD / expected
```

Authority remains HOLD because this plan does not authorize merge.

- [ ] **Step 4: Perform exact-head reverse review**

Review:
- classification ledger against exact archive heads;
- no archive merge commits in ancestry;
- no #202 file changes;
- schema/dataclass parity;
- shared core has no Teacher dependency;
- extension manifests bind exact core hash;
- active baseline binds exact ledger/core hashes;
- all scientific claim ceilings preserved;
- no live actuation/deployment/canonical effect.

- [ ] **Step 5: Correct any discovered defect through TDD**

For each defect:
1. write a failing targeted regression test;
2. run and observe the intended RED;
3. make the smallest production fix;
4. rerun targeted + component + full Quality;
5. preserve history; no force push or rewrite.

- [ ] **Step 6: Stop at merge authorization boundary**

Final candidate state must remain:

```text
PR_203 = OPEN
MERGE = NOT_AUTHORIZED
WRITE_TO_MAIN = NO
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

A separate fresh exact-head Human Owner authorization is required for merge.

---

## Post-merge handoff: PR #202 is a separate plan

Do not execute this section inside #203.

After #203 is merged into main, create a new post-merge plan for #202 with this sequence:

```text
REFRESH MAIN
→ RECHECK #202 LIVE HEAD
→ NORMAL NON-FORCED SYNC OF NEW MAIN INTO #202
→ REBIND sensorimotor.py TO SharedEmbodimentCore
→ KEEP #202 DYNAMIC SCOPE
→ TARGETED TDD FOR BINDING CHANGES
→ QUALITY / CODEQL
→ EXACT-HEAD REVERSE REVIEW
→ SEPARATE HUMAN MERGE AUTHORIZATION
```

The post-merge #202 plan must verify at least:

```text
SHARED_CORE_HASH_BOUND = YES
AION_ASTRA_EMBODIMENT_ISOLATION = PRESERVED
ROLE_SPECIFIC_EXTENSION_NOT_REQUIRED = YES
PREDICTION_ERROR != PAIN
BODY_MODEL_UPDATE != BODY_OWNERSHIP
SENSORIMOTOR_LOOP != SUBJECTIVITY
```

No #202 synchronization is authorized by this #203 implementation plan.
