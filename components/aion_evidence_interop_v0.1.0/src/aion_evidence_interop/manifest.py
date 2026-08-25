from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical import (
    InteropError,
    SourceValidation,
    canonical_json_bytes,
    sha256_bytes,
    validate_source_record,
)
from .inspect_export import export_inspect
from .intoto_export import export_intoto
from .opa_export import evaluate_boundaries, policy_input
from .prov_export import export_prov
from .rocrate_export import export_rocrate
from .scorecard_export import export_scorecard_crosswalk


PROFILE_VERSION = "0.1.0"
OUTPUT_PATHS = (
    "attestation.intoto.json",
    "inspect/dataset.jsonl",
    "inspect/task-manifest.json",
    "interop-manifest.json",
    "opa/input.json",
    "openssf/scorecard-crosswalk.json",
    "prov.jsonld",
    "ro-crate-metadata.json",
)


def _artifact_digest(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def _jsonl_bytes(value: dict[str, Any]) -> bytes:
    return canonical_json_bytes(value)


def _base_manifest(validation: SourceValidation) -> dict[str, Any]:
    return {
        "profile_version": PROFILE_VERSION,
        "source": {
            "record_ref": validation.record_ref,
            "record_sha256": validation.record_sha256,
            "code_commit": validation.expected_head,
            "validation_status": validation.status,
            "result_status": validation.result_status,
        },
        "boundaries": {
            "canonical_effect": "NONE",
            "deployment": False,
            "research_execution": False,
            "model_execution": False,
            "network_access": False,
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "independent_ivv": "NOT_ACHIEVED",
            "human_identity_inferred": False,
            "human_presence_inferred": False,
            "merge_authority_inferred": False,
        },
        "exports": {
            "w3c_prov": "prov.jsonld",
            "ro_crate": "ro-crate-metadata.json",
            "in_toto": "attestation.intoto.json",
            "opa": "opa/input.json",
            "inspect_task": "inspect/task-manifest.json",
            "inspect_dataset": "inspect/dataset.jsonl",
            "openssf_scorecard_crosswalk": "openssf/scorecard-crosswalk.json",
        },
    }


def build_bundle(
    root: Path,
    record_path: Path,
    *,
    expected_head: str,
) -> dict[str, bytes]:
    record, validation = validate_source_record(
        root,
        record_path,
        expected_head=expected_head,
    )
    manifest = _base_manifest(validation)

    prov = export_prov(record, validation.record_ref)
    inspect_task, inspect_sample = export_inspect(record, validation.record_ref)
    scorecard_crosswalk = export_scorecard_crosswalk(root, expected_head)

    primary_digests = {
        "prov.jsonld": _artifact_digest(prov),
        "inspect/task-manifest.json": _artifact_digest(inspect_task),
        "inspect/dataset.jsonl": sha256_bytes(_jsonl_bytes(inspect_sample)),
        "openssf/scorecard-crosswalk.json": _artifact_digest(scorecard_crosswalk),
    }

    rocrate = export_rocrate(
        record,
        source_ref=validation.record_ref,
        source_sha256=validation.record_sha256,
        artifact_digests=primary_digests,
        represented_artifacts=[
            name
            for name in OUTPUT_PATHS
            if name != "ro-crate-metadata.json"
        ],
    )
    primary_digests["ro-crate-metadata.json"] = _artifact_digest(rocrate)

    intoto = export_intoto(
        record,
        source_ref=validation.record_ref,
        source_sha256=validation.record_sha256,
        expected_head=expected_head,
        artifact_digests=primary_digests,
    )
    artifact_digests = dict(primary_digests)
    artifact_digests["attestation.intoto.json"] = _artifact_digest(intoto)
    manifest["artifact_digests"] = dict(sorted(artifact_digests.items()))

    opa_input = policy_input(manifest)
    allow, reasons = evaluate_boundaries(opa_input)
    if not allow:
        raise InteropError(
            "interop policy boundary failed closed: " + ", ".join(reasons),
            category="policy_boundary_failure",
        )
    opa_input["decision"] = {"allow": True, "deny_reasons": []}
    artifact_digests["opa/input.json"] = _artifact_digest(opa_input)
    manifest["artifact_digests"] = dict(sorted(artifact_digests.items()))
    manifest["policy"] = {
        "python_mirror_allow": True,
        "opa_policy_ref": "policies/aion_interop.rego",
        "deny_reasons": [],
    }

    return {
        "interop-manifest.json": canonical_json_bytes(manifest),
        "prov.jsonld": canonical_json_bytes(prov),
        "attestation.intoto.json": canonical_json_bytes(intoto),
        "ro-crate-metadata.json": canonical_json_bytes(rocrate),
        "opa/input.json": canonical_json_bytes(opa_input),
        "inspect/task-manifest.json": canonical_json_bytes(inspect_task),
        "inspect/dataset.jsonl": _jsonl_bytes(inspect_sample),
        "openssf/scorecard-crosswalk.json": canonical_json_bytes(scorecard_crosswalk),
    }


def write_bundle(output: Path, bundle: dict[str, bytes]) -> None:
    try:
        if output.is_symlink():
            raise InteropError(
                "output path must not be a symbolic link",
                category="write_failure",
            )
        output = output.absolute()
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise InteropError(
                "output path must be absent or an empty directory",
                category="write_failure",
            )
        output.mkdir(parents=True, exist_ok=True)
        for relative, data in sorted(bundle.items()):
            relative_path = Path(relative)
            if relative_path.is_absolute() or ".." in relative_path.parts:
                raise InteropError(
                    "bundle contains a non-confined output path",
                    category="write_failure",
                )
            target = output / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    except InteropError:
        raise
    except OSError as exc:
        raise InteropError(
            "interoperability bundle could not be written",
            category="write_failure",
        ) from exc


def bundle_hashes(bundle: dict[str, bytes]) -> dict[str, str]:
    return {
        name: sha256_bytes(data)
        for name, data in sorted(bundle.items())
    }
