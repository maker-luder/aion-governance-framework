"""Content-addressed synthetic embodiment baseline without live execution."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .convergence import (
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


def _extension_ids(
    extensions: tuple[RoleSpecificEmbodimentExtension, ...],
    core: SharedEmbodimentCore,
) -> tuple[str, ...]:
    if type(extensions) is not tuple:
        raise ValueError("extensions must be a tuple")
    ids: list[str] = []
    for extension in extensions:
        validate_role_specific_extension(extension, core)
        ids.append(extension.extension_id)
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate extension IDs")
    return tuple(sorted(ids))


def _baseline_id(
    ledger_sha256: str, core_sha256: str, extension_ids: tuple[str, ...]
) -> str:
    return "ACTIVE_EMBODIMENT_" + deterministic_hash({
        "ledger": ledger_sha256, "core": core_sha256,
        "extensions": extension_ids,
    })


def build_active_embodiment_baseline(
    core: SharedEmbodimentCore,
    ledger: ConvergenceLedger,
    extensions: tuple[RoleSpecificEmbodimentExtension, ...] = (),
) -> ActiveEmbodimentBaseline:
    validate_convergence_ledger(ledger)
    ledger_hash = convergence_ledger_hash(ledger)
    core_hash = shared_embodiment_core_hash(core)
    extension_ids = _extension_ids(extensions, core)
    baseline = ActiveEmbodimentBaseline(
        baseline_id=_baseline_id(ledger_hash, core_hash, extension_ids),
        convergence_ledger_sha256=ledger_hash,
        shared_core_sha256=core_hash,
        role_extension_ids=extension_ids,
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
    extension_ids = _extension_ids(extensions, core)
    if baseline.convergence_ledger_sha256 != ledger_hash:
        raise ValueError("convergence ledger hash mismatch")
    if baseline.shared_core_sha256 != core_hash:
        raise ValueError("shared core hash mismatch")
    if type(baseline.role_extension_ids) is not tuple or baseline.role_extension_ids != extension_ids:
        raise ValueError("role extension binding mismatch or duplicate IDs")
    if baseline.baseline_id != _baseline_id(ledger_hash, core_hash, extension_ids):
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
