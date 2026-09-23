"""Complete, content-addressed embodiment archive coverage accounting."""

from __future__ import annotations

import ast
from dataclasses import asdict, dataclass
from enum import StrEnum
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ARCHIVE_HEADS_V0_2: dict[int, str] = {
    190: "066ed1afccebee869eb658c09691b7f096694332",
    191: "48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2",
    192: "861e6a556a21afffd04b187714c0608fe73ea4fc",
    202: "7f84ae8c95f1b7caaaa0c3850a0b6cfd049b7108",
}


class EmbodimentAxis(StrEnum):
    ANATOMY = "ANATOMY"
    ANTHROPOMETRY = "ANTHROPOMETRY"
    PHYSIOLOGY = "PHYSIOLOGY"
    SIGNAL_CHANNELS = "SIGNAL_CHANNELS"
    MOTOR_CONTROL = "MOTOR_CONTROL"
    OBSERVABILITY = "OBSERVABILITY"
    SENSORIMOTOR = "SENSORIMOTOR"
    BODY_MODEL = "BODY_MODEL"
    MULTISENSORY_INTEGRATION = "MULTISENSORY_INTEGRATION"
    HOMEOSTASIS_ALLOSTASIS = "HOMEOSTASIS_ALLOSTASIS"
    DRIVE_MOTIVATION = "DRIVE_MOTIVATION"
    BODY_DYNAMICS = "BODY_DYNAMICS"
    CALIBRATION_ADAPTATION = "CALIBRATION_ADAPTATION"
    CROSS_SESSION_RETENTION = "CROSS_SESSION_RETENTION"
    LONGITUDINAL_TRAJECTORY = "LONGITUDINAL_TRAJECTORY"
    RUNTIME_BINDING = "RUNTIME_BINDING"
    AVATAR_3D_PHYSICS = "AVATAR_3D_PHYSICS"
    ROLE_SPECIFIC_EXTENSIONS = "ROLE_SPECIFIC_EXTENSIONS"
    RESEARCH_GOVERNANCE_BOUNDARIES = "RESEARCH_GOVERNANCE_BOUNDARIES"


EMBODIMENT_AXIS_ORDER = tuple(EmbodimentAxis)
_AXIS_INDEX = {axis: index for index, axis in enumerate(EMBODIMENT_AXIS_ORDER)}


class ArtifactKind(StrEnum):
    SOURCE = "SOURCE"
    SCHEMA = "SCHEMA"
    DATA = "DATA"
    TEST = "TEST"
    DOCUMENT = "DOCUMENT"


class CoverageClassification(StrEnum):
    SHARED_CORE = "SHARED_CORE"
    ROLE_SPECIFIC_EXTENSION = "ROLE_SPECIFIC_EXTENSION"
    EXTERNAL_DEFERRED = "EXTERNAL_DEFERRED"
    ARCHIVE_RECORD = "ARCHIVE_RECORD"


class CoverageDisposition(StrEnum):
    ADOPTED = "ADOPTED"
    DEFERRED = "DEFERRED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVE_ONLY = "ARCHIVE_ONLY"
    MISSING_UNACCOUNTED = "MISSING_UNACCOUNTED"


CANONICAL_ORDER_FIELDS = ("source_pr", "source_path", "semantic_unit_id")
_SHA40 = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True, slots=True)
class SourceHeadBinding:
    source_pr: int
    source_head: str


@dataclass(frozen=True, slots=True)
class SourceArtifact:
    artifact_id: str
    source_pr: int
    source_head: str
    source_path: str
    git_blob_sha: str
    artifact_kind: ArtifactKind
    semantic_coverage_required: bool
    v0_1_explicit_row: bool


@dataclass(frozen=True, slots=True)
class InventorySummary:
    pr192_implementation_modules: int
    pr192_teacher_modules: int
    pr192_v0_1_explicit_modules: int
    pr192_v0_1_unexplicit_modules: int
    pr202_external_implementation_modules: int
    pr192_plus_pr202_unexplicit_modules: int


@dataclass(frozen=True, slots=True)
class SemanticUnitCoverage:
    primary_source_artifact_id: str
    source_pr: int
    source_head: str
    source_path: str
    source_blob_sha: str
    semantic_unit_id: str
    source_locator: str
    embodiment_axes: tuple[EmbodimentAxis, ...]
    classification: CoverageClassification
    disposition: CoverageDisposition
    target_ref: str
    active_target_ref: str | None
    reason: str
    replacement_ref_if_superseded: str | None
    supporting_artifacts: tuple[str, ...]
    claim_ceiling: str
    review_status: str


@dataclass(frozen=True, slots=True)
class EmbodimentArchiveCoverageMatrix:
    matrix_id: str
    source_heads: tuple[SourceHeadBinding, ...]
    source_inventory: tuple[SourceArtifact, ...]
    semantic_units: tuple[SemanticUnitCoverage, ...]
    inventory_summary: InventorySummary
    canonical_order: tuple[str, ...]
    missing_unaccounted_count: int
    duplicate_semantic_ownership: int
    scientific_disposition: str
    canonical_effect: str
    deployment: bool


_TOP_KEYS = {
    "matrix_id", "source_heads", "source_inventory", "semantic_units",
    "inventory_summary", "canonical_order", "missing_unaccounted_count",
    "duplicate_semantic_ownership", "scientific_disposition",
    "canonical_effect", "deployment",
}
_ARTIFACT_KEYS = {
    "artifact_id", "source_pr", "source_head", "source_path", "git_blob_sha",
    "artifact_kind", "semantic_coverage_required", "v0_1_explicit_row",
}
_UNIT_KEYS = {
    "primary_source_artifact_id", "source_pr", "source_head", "source_path",
    "source_blob_sha", "semantic_unit_id", "source_locator",
    "embodiment_axes", "classification", "disposition", "target_ref",
    "active_target_ref", "reason", "replacement_ref_if_superseded",
    "supporting_artifacts", "claim_ceiling", "review_status",
}
_SUMMARY_KEYS = {
    "pr192_implementation_modules", "pr192_teacher_modules",
    "pr192_v0_1_explicit_modules", "pr192_v0_1_unexplicit_modules",
    "pr202_external_implementation_modules",
    "pr192_plus_pr202_unexplicit_modules",
}


def _exact_mapping(value: object, keys: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise ValueError(f"{label} must be an object")
    mapping = value
    if set(mapping) != keys:
        raise ValueError(f"{label} key drift")
    return mapping


def _text(value: object, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _integer(value: object, label: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{label} must be an integer")
    return value


def _boolean(value: object, label: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{label} must be a boolean")
    return value


def _optional_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _text(value, label)


def _tuple_of_text(value: object, label: str) -> tuple[str, ...]:
    if type(value) is not list or any(type(item) is not str or not item.strip() for item in value):
        raise ValueError(f"{label} must be an array of nonempty strings")
    return tuple(value)


def _load_artifact(value: object) -> SourceArtifact:
    item = _exact_mapping(value, _ARTIFACT_KEYS, "source artifact")
    try:
        kind = ArtifactKind(_text(item["artifact_kind"], "artifact_kind"))
    except ValueError as exc:
        raise ValueError("unknown artifact kind") from exc
    return SourceArtifact(
        artifact_id=_text(item["artifact_id"], "artifact_id"),
        source_pr=_integer(item["source_pr"], "source_pr"),
        source_head=_text(item["source_head"], "source_head"),
        source_path=_text(item["source_path"], "source_path"),
        git_blob_sha=_text(item["git_blob_sha"], "git_blob_sha"),
        artifact_kind=kind,
        semantic_coverage_required=_boolean(
            item["semantic_coverage_required"], "semantic_coverage_required"
        ),
        v0_1_explicit_row=_boolean(item["v0_1_explicit_row"], "v0_1_explicit_row"),
    )


def _load_unit(value: object) -> SemanticUnitCoverage:
    item = _exact_mapping(value, _UNIT_KEYS, "semantic unit")
    raw_axes = _tuple_of_text(item["embodiment_axes"], "embodiment_axes")
    try:
        axes = tuple(EmbodimentAxis(axis) for axis in raw_axes)
        classification = CoverageClassification(
            _text(item["classification"], "classification")
        )
        disposition = CoverageDisposition(_text(item["disposition"], "disposition"))
    except ValueError as exc:
        raise ValueError("unknown coverage enum") from exc
    return SemanticUnitCoverage(
        primary_source_artifact_id=_text(
            item["primary_source_artifact_id"], "primary_source_artifact_id"
        ),
        source_pr=_integer(item["source_pr"], "source_pr"),
        source_head=_text(item["source_head"], "source_head"),
        source_path=_text(item["source_path"], "source_path"),
        source_blob_sha=_text(item["source_blob_sha"], "source_blob_sha"),
        semantic_unit_id=_text(item["semantic_unit_id"], "semantic_unit_id"),
        source_locator=_text(item["source_locator"], "source_locator"),
        embodiment_axes=axes,
        classification=classification,
        disposition=disposition,
        target_ref=_text(item["target_ref"], "target_ref"),
        active_target_ref=_optional_text(item["active_target_ref"], "active_target_ref"),
        reason=_text(item["reason"], "reason"),
        replacement_ref_if_superseded=_optional_text(
            item["replacement_ref_if_superseded"],
            "replacement_ref_if_superseded",
        ),
        supporting_artifacts=_tuple_of_text(
            item["supporting_artifacts"], "supporting_artifacts"
        ),
        claim_ceiling=_text(item["claim_ceiling"], "claim_ceiling"),
        review_status=_text(item["review_status"], "review_status"),
    )


def load_coverage_matrix(path: str | Path) -> EmbodimentArchiveCoverageMatrix:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    payload = _exact_mapping(raw, _TOP_KEYS, "coverage matrix")
    raw_heads = payload["source_heads"]
    if type(raw_heads) is not list:
        raise ValueError("source_heads must be an array")
    heads = tuple(
        SourceHeadBinding(
            source_pr=_integer(
                _exact_mapping(value, {"source_pr", "source_head"}, "source head")["source_pr"],
                "source_pr",
            ),
            source_head=_text(value["source_head"], "source_head"),
        )
        for value in raw_heads
    )
    raw_inventory = payload["source_inventory"]
    raw_units = payload["semantic_units"]
    if type(raw_inventory) is not list or type(raw_units) is not list:
        raise ValueError("inventory and semantic_units must be arrays")
    summary_raw = _exact_mapping(payload["inventory_summary"], _SUMMARY_KEYS, "inventory summary")
    summary = InventorySummary(
        **{key: _integer(summary_raw[key], key) for key in _SUMMARY_KEYS}
    )
    matrix = EmbodimentArchiveCoverageMatrix(
        matrix_id=_text(payload["matrix_id"], "matrix_id"),
        source_heads=heads,
        source_inventory=tuple(_load_artifact(value) for value in raw_inventory),
        semantic_units=tuple(_load_unit(value) for value in raw_units),
        inventory_summary=summary,
        canonical_order=_tuple_of_text(payload["canonical_order"], "canonical_order"),
        missing_unaccounted_count=_integer(
            payload["missing_unaccounted_count"], "missing_unaccounted_count"
        ),
        duplicate_semantic_ownership=_integer(
            payload["duplicate_semantic_ownership"], "duplicate_semantic_ownership"
        ),
        scientific_disposition=_text(
            payload["scientific_disposition"], "scientific_disposition"
        ),
        canonical_effect=_text(payload["canonical_effect"], "canonical_effect"),
        deployment=_boolean(payload["deployment"], "deployment"),
    )
    validate_coverage_matrix(matrix)
    return matrix


def _artifact_order(item: SourceArtifact) -> tuple[int, str, str]:
    return item.source_pr, item.source_path, item.artifact_id


def _unit_order(item: SemanticUnitCoverage) -> tuple[int, str, str]:
    return item.source_pr, item.source_path, item.semantic_unit_id


def _derived_inventory_summary(
    inventory: tuple[SourceArtifact, ...],
) -> InventorySummary:
    pr192 = [
        item for item in inventory
        if item.source_pr == 192
        and item.artifact_kind is ArtifactKind.SOURCE
        and item.semantic_coverage_required
    ]
    teacher = [item for item in pr192 if Path(item.source_path).name.startswith("teacher_")]
    explicit = [item for item in pr192 if item.v0_1_explicit_row]
    pr202 = [
        item for item in inventory
        if item.source_pr == 202
        and item.artifact_kind is ArtifactKind.SOURCE
        and item.semantic_coverage_required
    ]
    return InventorySummary(
        pr192_implementation_modules=len(pr192),
        pr192_teacher_modules=len(teacher),
        pr192_v0_1_explicit_modules=len(explicit),
        pr192_v0_1_unexplicit_modules=len(pr192) - len(explicit),
        pr202_external_implementation_modules=len(pr202),
        pr192_plus_pr202_unexplicit_modules=len(pr192) - len(explicit) + len(pr202),
    )


def coverage_matrix_gate_counts(
    matrix: EmbodimentArchiveCoverageMatrix,
) -> dict[str, int]:
    required_artifacts = {
        item.artifact_id
        for item in matrix.source_inventory
        if item.semantic_coverage_required
    }
    covered_artifacts = {
        unit.primary_source_artifact_id for unit in matrix.semantic_units
    }
    ownership = [
        (unit.primary_source_artifact_id, unit.source_locator)
        for unit in matrix.semantic_units
    ]
    return {
        "ADOPTED_COUNT": sum(
            unit.disposition is CoverageDisposition.ADOPTED
            for unit in matrix.semantic_units
        ),
        "DEFERRED_COUNT": sum(
            unit.disposition is CoverageDisposition.DEFERRED
            for unit in matrix.semantic_units
        ),
        "SUPERSEDED_COUNT": sum(
            unit.disposition is CoverageDisposition.SUPERSEDED
            for unit in matrix.semantic_units
        ),
        "ARCHIVE_ONLY_COUNT": sum(
            unit.disposition is CoverageDisposition.ARCHIVE_ONLY
            for unit in matrix.semantic_units
        ),
        "MISSING_UNACCOUNTED_COUNT": sum(
            unit.disposition is CoverageDisposition.MISSING_UNACCOUNTED
            for unit in matrix.semantic_units
        ) + len(required_artifacts - covered_artifacts),
        "DUPLICATE_SEMANTIC_OWNERSHIP": len(ownership) - len(set(ownership)),
        "UNCOVERED_SOURCE_MODULE_COUNT": len(required_artifacts - covered_artifacts),
    }


def validate_coverage_matrix(
    matrix: EmbodimentArchiveCoverageMatrix,
) -> dict[str, int | str]:
    if type(matrix) is not EmbodimentArchiveCoverageMatrix:
        raise ValueError("matrix must use the typed record")
    if matrix.matrix_id != "EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2":
        raise ValueError("unexpected matrix id")
    if matrix.canonical_order != CANONICAL_ORDER_FIELDS:
        raise ValueError("canonical order fields changed")
    if matrix.scientific_disposition != "HOLD":
        raise ValueError("scientific disposition must remain HOLD")
    if matrix.canonical_effect != "NONE" or matrix.deployment is not False:
        raise ValueError("matrix cannot have canonical effect or deployment")
    expected_heads = tuple(
        SourceHeadBinding(pr, head) for pr, head in sorted(ARCHIVE_HEADS_V0_2.items())
    )
    if matrix.source_heads != expected_heads:
        raise ValueError("source heads must match exact canonical bindings")
    if not matrix.source_inventory or not matrix.semantic_units:
        raise ValueError("matrix requires inventory and semantic units")
    if matrix.source_inventory != tuple(sorted(matrix.source_inventory, key=_artifact_order)):
        raise ValueError("source inventory is not in canonical order")
    if matrix.semantic_units != tuple(sorted(matrix.semantic_units, key=_unit_order)):
        raise ValueError("semantic units are not in canonical order")

    artifacts: dict[str, SourceArtifact] = {}
    artifact_paths: set[tuple[int, str]] = set()
    for artifact in matrix.source_inventory:
        if type(artifact) is not SourceArtifact:
            raise ValueError("source inventory requires typed artifacts")
        if artifact.artifact_id in artifacts:
            raise ValueError("duplicate artifact id")
        if artifact.source_pr not in ARCHIVE_HEADS_V0_2:
            raise ValueError("unknown source PR")
        if artifact.source_head != ARCHIVE_HEADS_V0_2[artifact.source_pr]:
            raise ValueError("artifact source head drift")
        if not _SHA40.fullmatch(artifact.git_blob_sha):
            raise ValueError("artifact requires exact Git blob SHA")
        if not artifact.source_path or "\\" in artifact.source_path:
            raise ValueError("artifact source path must be repository-relative POSIX")
        path_key = artifact.source_pr, artifact.source_path
        if path_key in artifact_paths:
            raise ValueError("duplicate source artifact path")
        artifact_paths.add(path_key)
        if type(artifact.artifact_kind) is not ArtifactKind:
            raise ValueError("artifact kind must use exact enum")
        if artifact.semantic_coverage_required and artifact.artifact_kind is not ArtifactKind.SOURCE:
            raise ValueError("only source modules require semantic coverage")
        artifacts[artifact.artifact_id] = artifact

    ids: set[str] = set()
    ownership: set[tuple[str, str]] = set()
    used_axes: set[EmbodimentAxis] = set()
    for unit in matrix.semantic_units:
        if type(unit) is not SemanticUnitCoverage:
            raise ValueError("semantic units require typed records")
        if unit.semantic_unit_id in ids:
            raise ValueError("duplicate semantic unit id")
        ids.add(unit.semantic_unit_id)
        owner = unit.primary_source_artifact_id, unit.source_locator
        if owner in ownership:
            raise ValueError("duplicate semantic ownership")
        ownership.add(owner)
        primary = artifacts.get(unit.primary_source_artifact_id)
        if primary is None:
            raise ValueError("semantic unit primary source is not inventoried")
        if (
            unit.source_pr != primary.source_pr
            or unit.source_head != primary.source_head
            or unit.source_path != primary.source_path
            or unit.source_blob_sha != primary.git_blob_sha
        ):
            raise ValueError("semantic unit source binding drift")
        if type(unit.classification) is not CoverageClassification:
            raise ValueError("classification must use exact enum")
        if type(unit.disposition) is not CoverageDisposition:
            raise ValueError("disposition must use exact enum")
        if not unit.embodiment_axes or any(
            type(axis) is not EmbodimentAxis for axis in unit.embodiment_axes
        ):
            raise ValueError("semantic unit requires exact embodiment axes")
        if len(unit.embodiment_axes) != len(set(unit.embodiment_axes)):
            raise ValueError("duplicate embodiment axis")
        if unit.embodiment_axes != tuple(
            sorted(unit.embodiment_axes, key=_AXIS_INDEX.__getitem__)
        ):
            raise ValueError("embodiment axes are not in canonical order")
        used_axes.update(unit.embodiment_axes)
        if not unit.target_ref:
            raise ValueError("semantic unit target ref is required")
        if unit.disposition is CoverageDisposition.ADOPTED:
            if unit.active_target_ref is None:
                raise ValueError("adopted semantic unit requires active target")
            if unit.target_ref != unit.active_target_ref:
                raise ValueError("adopted target_ref must equal active target")
            if unit.replacement_ref_if_superseded is not None:
                raise ValueError("adopted semantic unit cannot claim replacement")
        elif unit.disposition is CoverageDisposition.DEFERRED:
            if unit.active_target_ref is not None:
                raise ValueError("deferred semantic unit cannot claim active target")
            if unit.replacement_ref_if_superseded is not None:
                raise ValueError("deferred semantic unit cannot claim replacement")
            if not unit.target_ref.startswith("deferred:"):
                raise ValueError("deferred target_ref must identify the deferral boundary")
        elif unit.disposition is CoverageDisposition.SUPERSEDED:
            if unit.replacement_ref_if_superseded is None:
                raise ValueError("superseded semantic unit requires replacement")
            if unit.target_ref != unit.replacement_ref_if_superseded:
                raise ValueError("superseded target_ref must equal replacement")
            if unit.active_target_ref is not None:
                raise ValueError("superseded semantic unit uses replacement, not active target")
        elif unit.disposition is CoverageDisposition.ARCHIVE_ONLY:
            if not unit.target_ref.startswith("archive:"):
                raise ValueError("archive-only semantic unit must use archive target")
            if unit.active_target_ref is not None or unit.replacement_ref_if_superseded is not None:
                raise ValueError("archive-only semantic unit cannot claim active surface")
        else:
            raise ValueError("MISSING_UNACCOUNTED is forbidden in final matrix")
        if unit.classification is CoverageClassification.EXTERNAL_DEFERRED:
            if unit.source_pr != 202 or unit.disposition is not CoverageDisposition.DEFERRED:
                raise ValueError("external deferred classification is reserved for PR #202")
        if unit.source_pr == 202 and unit.classification is not CoverageClassification.EXTERNAL_DEFERRED:
            raise ValueError("PR #202 must remain external deferred provenance")
        if unit.supporting_artifacts != tuple(sorted(unit.supporting_artifacts)):
            raise ValueError("supporting artifacts are not in canonical order")
        if len(unit.supporting_artifacts) != len(set(unit.supporting_artifacts)):
            raise ValueError("duplicate supporting artifact")
        if unit.primary_source_artifact_id in unit.supporting_artifacts:
            raise ValueError("primary source cannot duplicate supporting artifact")
        if any(identifier not in artifacts for identifier in unit.supporting_artifacts):
            raise ValueError("supporting artifact is not inventoried")
        if unit.claim_ceiling != "NOT_ESTABLISHED":
            raise ValueError("claim ceiling must remain NOT_ESTABLISHED")
        if unit.review_status != "REVIEWED_FOR_PHASE_A_V0_2":
            raise ValueError("semantic unit review status is incomplete")
    if used_axes != set(EMBODIMENT_AXIS_ORDER):
        raise ValueError("matrix does not cover every embodiment axis")

    derived_summary = _derived_inventory_summary(matrix.source_inventory)
    if matrix.inventory_summary != derived_summary:
        raise ValueError("inventory summary does not match exact inventory")
    if derived_summary != InventorySummary(19, 17, 4, 15, 1, 16):
        raise ValueError("archive inventory count contract changed")
    counts = coverage_matrix_gate_counts(matrix)
    if counts["UNCOVERED_SOURCE_MODULE_COUNT"]:
        raise ValueError("uncovered source module")
    if counts["DUPLICATE_SEMANTIC_OWNERSHIP"]:
        raise ValueError("duplicate semantic ownership")
    if counts["MISSING_UNACCOUNTED_COUNT"]:
        raise ValueError("missing unaccounted semantic coverage")
    if matrix.missing_unaccounted_count != 0 or matrix.duplicate_semantic_ownership != 0:
        raise ValueError("persisted completion gates must remain zero")
    return {"result": "PASS", **counts}


def _canonical_payload(matrix: EmbodimentArchiveCoverageMatrix) -> dict[str, Any]:
    payload = asdict(matrix)
    payload["source_heads"] = sorted(
        payload["source_heads"], key=lambda item: item["source_pr"]
    )
    payload["source_inventory"] = sorted(
        payload["source_inventory"],
        key=lambda item: (item["source_pr"], item["source_path"], item["artifact_id"]),
    )
    units = []
    for raw in payload["semantic_units"]:
        item = dict(raw)
        item["embodiment_axes"] = sorted(
            item["embodiment_axes"],
            key=lambda axis: _AXIS_INDEX[EmbodimentAxis(axis)],
        )
        item["supporting_artifacts"] = sorted(item["supporting_artifacts"])
        units.append(item)
    payload["semantic_units"] = sorted(
        units,
        key=lambda item: (
            item["source_pr"], item["source_path"], item["semantic_unit_id"]
        ),
    )
    return payload


def coverage_matrix_hash(matrix: EmbodimentArchiveCoverageMatrix) -> str:
    encoded = json.dumps(
        _canonical_payload(matrix),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _git(
    repository_root: Path,
    *args: str,
    git_executable: str = "git",
) -> str:
    proc = subprocess.run(
        [git_executable, "-C", str(repository_root), *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise ValueError(proc.stderr.strip() or "Git binding command failed")
    return proc.stdout.strip()


def _python_symbols(source: str) -> set[str]:
    tree = ast.parse(source)
    symbols: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.add(node.name)
        elif isinstance(node, ast.Assign):
            symbols.update(
                target.id for target in node.targets if isinstance(target, ast.Name)
            )
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            symbols.add(node.target.id)
    return symbols


def _verify_source_locator(path: str, locator: str, source: str) -> None:
    if locator == "MODULE_WHOLE":
        return
    if locator.startswith("heading:") or locator.startswith("text:") or locator.startswith("json:"):
        needle = locator.split(":", 1)[1]
        if needle not in source:
            raise ValueError(f"source locator not found: {locator}")
        return
    symbol, _, detail = locator.partition(":")
    if path.endswith(".py") and symbol not in _python_symbols(source):
        raise ValueError(f"source symbol not found: {locator}")
    if detail and detail not in source:
        raise ValueError(f"source semantic detail not found: {locator}")


def _verify_current_ref(repository_root: Path, ref: str, label: str) -> None:
    relative_path, marker, symbol = ref.partition("#")
    path = repository_root / relative_path
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise ValueError(f"{label} does not exist: {ref}") from exc
    root = repository_root.resolve()
    if root not in resolved.parents and resolved != root:
        raise ValueError(f"{label} escapes repository: {ref}")
    if marker and symbol:
        source = path.read_text(encoding="utf-8")
        if path.suffix == ".py":
            if symbol not in _python_symbols(source):
                raise ValueError(f"{label} symbol does not exist: {ref}")
        elif symbol not in source:
            raise ValueError(f"{label} locator does not exist: {ref}")


def validate_coverage_matrix_bindings(
    matrix: EmbodimentArchiveCoverageMatrix,
    repository_root: str | Path,
    *,
    git_executable: str = "git",
) -> dict[str, int | str]:
    validate_coverage_matrix(matrix)
    root = Path(repository_root).resolve()
    if not (root / ".git").exists():
        git_dir = _git(root, "rev-parse", "--git-dir", git_executable=git_executable)
        if not git_dir:
            raise ValueError("repository root has no Git metadata")
    source_cache: dict[str, str] = {}
    for artifact in matrix.source_inventory:
        object_ref = f"{artifact.source_head}:{artifact.source_path}"
        try:
            blob = _git(root, "rev-parse", object_ref, git_executable=git_executable)
        except ValueError as exc:
            raise ValueError(
                f"source artifact does not exist at exact head: {artifact.artifact_id}"
            ) from exc
        if blob != artifact.git_blob_sha:
            raise ValueError(f"source artifact blob mismatch: {artifact.artifact_id}")
        source_cache[artifact.artifact_id] = _git(
            root, "show", object_ref, git_executable=git_executable
        )
    for unit in matrix.semantic_units:
        _verify_source_locator(
            unit.source_path,
            unit.source_locator,
            source_cache[unit.primary_source_artifact_id],
        )
        if unit.active_target_ref is not None:
            _verify_current_ref(root, unit.active_target_ref, "active target")
        if unit.replacement_ref_if_superseded is not None:
            _verify_current_ref(
                root,
                unit.replacement_ref_if_superseded,
                "replacement",
            )
    counts = coverage_matrix_gate_counts(matrix)
    return {
        "result": "PASS",
        "SOURCE_BINDINGS": "PASS",
        "TARGET_BINDINGS": "PASS",
        "REPLACEMENT_BINDINGS": "PASS",
        "SUPPORTING_ARTIFACT_BINDINGS": "PASS",
        **counts,
    }
