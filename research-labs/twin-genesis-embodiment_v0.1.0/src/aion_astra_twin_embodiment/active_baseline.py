"""Content-addressed synthetic embodiment baseline without live execution."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .convergence import (
    AdoptionStatus,
    ConvergenceClassification,
    ConvergenceLedger,
    convergence_ledger_hash,
    validate_convergence_ledger,
)
from .role_extensions import (
    RoleSpecificEmbodimentExtension,
    validate_role_specific_extension,
)
from .shared_core import SharedEmbodimentCore, shared_embodiment_core_hash
from .validation import deterministic_hash

_TEACHER_LEDGER_UNITS = {
    "TEACHER_ANTHROPOMETRY_62_MEASURE": "teacher_anthropometry.py :: 62-measure profile",
    "TEACHER_SIGNAL_CHANNELS": "teacher_body_channels.py :: Teacher channel instances",
    "TEACHER_MOTOR_SCHEMA": "teacher_body_channels.py :: Teacher channel instances",
    "TEACHER_BODY_MODEL": "teacher_body_model.py :: body-schema/multisensory/allostatic/plasticity concepts",
    "TEACHER_PHYSIOLOGY_OBSERVABILITY": "teacher_physiology_observability.py :: Teacher observability bindings",
    "TEACHER_RUNTIME_BINDING": "teacher runtime/calibration/adaptation/retention/longitudinal modules",
    "TEACHER_CALIBRATION_ADAPTATION": "teacher runtime/calibration/adaptation/retention/longitudinal modules",
    "TEACHER_CROSS_SESSION_RETENTION": "teacher runtime/calibration/adaptation/retention/longitudinal modules",
    "TEACHER_LONGITUDINAL_TRAJECTORY": "teacher runtime/calibration/adaptation/retention/longitudinal modules",
    "TEACHER_AVATAR_ASSET_FAMILY": "avatar/LOD/physics/detailed physiology geometry implementation",
    "TEACHER_DETAILED_PHYSIOLOGY_GEOMETRY": "avatar/LOD/physics/detailed physiology geometry implementation",
}


@dataclass(frozen=True, slots=True)
class ActiveEmbodimentBaseline:
    baseline_id: str
    convergence_ledger_sha256: str
    shared_core_sha256: str
    role_extension_ids: tuple[str, ...]
    role_extension_sha256s: tuple[str, ...]
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


def _extension_bindings(
    extensions: tuple[RoleSpecificEmbodimentExtension, ...],
    core: SharedEmbodimentCore,
) -> tuple[tuple[str, str], ...]:
    if type(extensions) is not tuple:
        raise ValueError("extensions must be a tuple")
    bindings: list[tuple[str, str]] = []
    for extension in extensions:
        digest = validate_role_specific_extension(extension, core)["extension_hash"]
        bindings.append((extension.extension_id, digest))
    ids = [identifier for identifier, _ in bindings]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate extension IDs")
    return tuple(sorted(bindings))


def _validate_ledger_bindings(
    ledger: ConvergenceLedger,
    extensions: tuple[RoleSpecificEmbodimentExtension, ...],
) -> None:
    entries = {(entry.source_pr, entry.source_path_or_semantic_unit): entry
               for entry in ledger.entries}
    for extension in extensions:
        for capability in extension.capabilities:
            unit = _TEACHER_LEDGER_UNITS.get(capability.capability_id)
            if unit is None:
                raise ValueError("unreviewed extension capability")
            entry = entries.get((extension.source_pr, unit))
            if (entry is None or entry.classification is not ConvergenceClassification.ROLE_SPECIFIC_EXTENSION
                    or entry.adoption_status is not AdoptionStatus.DEFERRED
                    or not entry.target_owner.startswith("role_extension:teacher-")):
                raise ValueError("extension capability conflicts with convergence ledger")
    required_shared_owners = {
        "shared_core:governance-epistemics", "shared_core:physiology-reference",
        "shared_core:static-body-taxonomy", "shared_core:observation-motor-domains",
        "shared_core:observability-classes",
    }
    if not required_shared_owners <= {
        entry.target_owner for entry in ledger.entries
        if entry.classification is ConvergenceClassification.SHARED_CORE
        and entry.adoption_status is AdoptionStatus.ADOPTED
    }:
        raise ValueError("shared core source conflicts with convergence ledger")


def _baseline_id(
    ledger_sha256: str, core_sha256: str, extension_bindings: tuple[tuple[str, str], ...]
) -> str:
    return "ACTIVE_EMBODIMENT_" + deterministic_hash({
        "ledger": ledger_sha256, "core": core_sha256,
        "extensions": extension_bindings,
    })


def build_active_embodiment_baseline(
    core: SharedEmbodimentCore,
    ledger: ConvergenceLedger,
    extensions: tuple[RoleSpecificEmbodimentExtension, ...] = (),
) -> ActiveEmbodimentBaseline:
    validate_convergence_ledger(ledger)
    ledger_hash = convergence_ledger_hash(ledger)
    core_hash = shared_embodiment_core_hash(core)
    bindings = _extension_bindings(extensions, core)
    _validate_ledger_bindings(ledger, extensions)
    baseline = ActiveEmbodimentBaseline(
        baseline_id=_baseline_id(ledger_hash, core_hash, bindings),
        convergence_ledger_sha256=ledger_hash,
        shared_core_sha256=core_hash,
        role_extension_ids=tuple(identifier for identifier, _ in bindings),
        role_extension_sha256s=tuple(digest for _, digest in bindings),
    )
    validate_active_embodiment_baseline(baseline, core, ledger, extensions)
    return baseline


def validate_active_embodiment_baseline(
    baseline: ActiveEmbodimentBaseline,
    core: SharedEmbodimentCore,
    ledger: ConvergenceLedger,
    extensions: tuple[RoleSpecificEmbodimentExtension, ...] = (),
) -> dict[str, str]:
    if type(baseline) is not ActiveEmbodimentBaseline:
        raise ValueError("baseline must be a typed record")
    validate_convergence_ledger(ledger)
    ledger_hash = convergence_ledger_hash(ledger)
    core_hash = shared_embodiment_core_hash(core)
    bindings = _extension_bindings(extensions, core)
    _validate_ledger_bindings(ledger, extensions)
    if baseline.convergence_ledger_sha256 != ledger_hash:
        raise ValueError("convergence ledger hash mismatch")
    if baseline.shared_core_sha256 != core_hash:
        raise ValueError("shared core hash mismatch")
    if type(baseline.role_extension_ids) is not tuple or baseline.role_extension_ids != tuple(identifier for identifier, _ in bindings):
        raise ValueError("role extension binding mismatch or duplicate IDs")
    if type(baseline.role_extension_sha256s) is not tuple or baseline.role_extension_sha256s != tuple(digest for _, digest in bindings):
        raise ValueError("role extension content hash mismatch")
    if baseline.baseline_id != _baseline_id(ledger_hash, core_hash, bindings):
        raise ValueError("baseline ID does not match content hashes")
    for field_name, required in (
        ("sensorimotor_layer_status", "DEFERRED_TO_PR_202"),
        ("empirical_control_layer_status", "NOT_IMPLEMENTED"),
        ("body_sensation", "NOT_ESTABLISHED"),
        ("body_ownership_experience", "NOT_ESTABLISHED"),
        ("subjectivity_conclusion", "NOT_ESTABLISHED"),
        ("consciousness_conclusion", "NOT_ESTABLISHED"),
        ("phenomenal_experience_conclusion", "NOT_ESTABLISHED"),
        ("scientific_disposition", "HOLD"),
        ("canonical_effect", "NONE"),
    ):
        value = getattr(baseline, field_name)
        if type(value) is not str or value != required:
            raise ValueError(f"{field_name} must remain {required}")
    if baseline.deployment is not False:
        raise ValueError("baseline cannot deploy")
    return {"result": "PASS", "baseline_hash": deterministic_hash(asdict(baseline)),
            "shared_core_sha256": core_hash,
            "convergence_ledger_sha256": ledger_hash,
            "canonical_effect": "NONE"}
