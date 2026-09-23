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
from .coverage_matrix import (
    EmbodimentArchiveCoverageMatrix,
    coverage_matrix_hash,
    validate_coverage_matrix,
)
from .materialization_map import (
    EmbodimentMaterializationMap,
    MaterializationAdmissionStatus,
    materialization_map_gate_counts,
    materialization_map_hash,
    validate_materialization_map,
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
    coverage_matrix_sha256: str
    materialization_map_sha256: str
    shared_core_sha256: str
    materialized_semantic_unit_ids: tuple[str, ...]
    kept_deferred_count: int
    superseded_count: int
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
    matrix: EmbodimentArchiveCoverageMatrix,
) -> tuple[tuple[str, str], ...]:
    if type(extensions) is not tuple:
        raise ValueError("extensions must be a tuple")
    bindings: list[tuple[str, str]] = []
    for extension in extensions:
        digest = validate_role_specific_extension(extension, core, matrix)["extension_hash"]
        bindings.append((extension.extension_id, digest))
    ids = [identifier for identifier, _ in bindings]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate extension IDs")
    return tuple(sorted(bindings))


def _validate_ledger_bindings(
    ledger: ConvergenceLedger,
) -> None:
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
    ledger_sha256: str,
    matrix_sha256: str,
    materialization_sha256: str,
    core_sha256: str,
    materialized_semantic_unit_ids: tuple[str, ...],
    kept_deferred_count: int,
    superseded_count: int,
    extension_bindings: tuple[tuple[str, str], ...],
) -> str:
    return "ACTIVE_EMBODIMENT_" + deterministic_hash({
        "ledger": ledger_sha256,
        "matrix": matrix_sha256,
        "materialization": materialization_sha256,
        "core": core_sha256,
        "materialized_semantic_unit_ids": materialized_semantic_unit_ids,
        "kept_deferred_count": kept_deferred_count,
        "superseded_count": superseded_count,
        "extensions": extension_bindings,
    })


def build_active_embodiment_baseline(
    core: SharedEmbodimentCore,
    ledger: ConvergenceLedger,
    matrix: EmbodimentArchiveCoverageMatrix,
    materialization: EmbodimentMaterializationMap,
    extensions: tuple[RoleSpecificEmbodimentExtension, ...] = (),
) -> ActiveEmbodimentBaseline:
    validate_convergence_ledger(ledger)
    validate_coverage_matrix(matrix)
    validate_materialization_map(materialization, matrix)
    ledger_hash = convergence_ledger_hash(ledger)
    matrix_hash = coverage_matrix_hash(matrix)
    materialization_hash = materialization_map_hash(materialization)
    materialized_ids = tuple(
        entry.semantic_unit_id
        for entry in materialization.entries
        if entry.admission_status is MaterializationAdmissionStatus.ACTIVE_VERIFIED
    )
    counts = materialization_map_gate_counts(materialization)
    core_hash = shared_embodiment_core_hash(core)
    bindings = _extension_bindings(extensions, core, matrix)
    _validate_ledger_bindings(ledger)
    baseline = ActiveEmbodimentBaseline(
        baseline_id=_baseline_id(
            ledger_hash,
            matrix_hash,
            materialization_hash,
            core_hash,
            materialized_ids,
            counts["KEEP_DEFERRED_COUNT"],
            counts["SUPERSEDED_COUNT"],
            bindings,
        ),
        convergence_ledger_sha256=ledger_hash,
        coverage_matrix_sha256=matrix_hash,
        materialization_map_sha256=materialization_hash,
        shared_core_sha256=core_hash,
        materialized_semantic_unit_ids=materialized_ids,
        kept_deferred_count=counts["KEEP_DEFERRED_COUNT"],
        superseded_count=counts["SUPERSEDED_COUNT"],
        role_extension_ids=tuple(identifier for identifier, _ in bindings),
        role_extension_sha256s=tuple(digest for _, digest in bindings),
    )
    validate_active_embodiment_baseline(
        baseline, core, ledger, matrix, materialization, extensions
    )
    return baseline


def validate_active_embodiment_baseline(
    baseline: ActiveEmbodimentBaseline,
    core: SharedEmbodimentCore,
    ledger: ConvergenceLedger,
    matrix: EmbodimentArchiveCoverageMatrix,
    materialization: EmbodimentMaterializationMap,
    extensions: tuple[RoleSpecificEmbodimentExtension, ...] = (),
) -> dict[str, str]:
    if type(baseline) is not ActiveEmbodimentBaseline:
        raise ValueError("baseline must be a typed record")
    validate_convergence_ledger(ledger)
    validate_coverage_matrix(matrix)
    validate_materialization_map(materialization, matrix)
    ledger_hash = convergence_ledger_hash(ledger)
    matrix_hash = coverage_matrix_hash(matrix)
    materialization_hash = materialization_map_hash(materialization)
    materialized_ids = tuple(
        entry.semantic_unit_id
        for entry in materialization.entries
        if entry.admission_status is MaterializationAdmissionStatus.ACTIVE_VERIFIED
    )
    counts = materialization_map_gate_counts(materialization)
    core_hash = shared_embodiment_core_hash(core)
    bindings = _extension_bindings(extensions, core, matrix)
    _validate_ledger_bindings(ledger)
    if baseline.convergence_ledger_sha256 != ledger_hash:
        raise ValueError("convergence ledger hash mismatch")
    if baseline.coverage_matrix_sha256 != matrix_hash:
        raise ValueError("coverage matrix hash mismatch")
    if baseline.materialization_map_sha256 != materialization_hash:
        raise ValueError("materialization map hash mismatch")
    if (
        type(baseline.materialized_semantic_unit_ids) is not tuple
        or baseline.materialized_semantic_unit_ids != materialized_ids
    ):
        raise ValueError("materialized semantic unit binding mismatch")
    if (
        type(baseline.kept_deferred_count) is not int
        or baseline.kept_deferred_count != counts["KEEP_DEFERRED_COUNT"]
    ):
        raise ValueError("kept deferred count mismatch")
    if (
        type(baseline.superseded_count) is not int
        or baseline.superseded_count != counts["SUPERSEDED_COUNT"]
    ):
        raise ValueError("superseded count mismatch")
    if baseline.shared_core_sha256 != core_hash:
        raise ValueError("shared core hash mismatch")
    if type(baseline.role_extension_ids) is not tuple or baseline.role_extension_ids != tuple(identifier for identifier, _ in bindings):
        raise ValueError("role extension binding mismatch or duplicate IDs")
    if type(baseline.role_extension_sha256s) is not tuple or baseline.role_extension_sha256s != tuple(digest for _, digest in bindings):
        raise ValueError("role extension content hash mismatch")
    if baseline.baseline_id != _baseline_id(
        ledger_hash,
        matrix_hash,
        materialization_hash,
        core_hash,
        materialized_ids,
        counts["KEEP_DEFERRED_COUNT"],
        counts["SUPERSEDED_COUNT"],
        bindings,
    ):
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
            "coverage_matrix_sha256": matrix_hash,
            "materialization_map_sha256": materialization_hash,
            "canonical_effect": "NONE"}
