from __future__ import annotations

import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_twin_embodiment.active_baseline import (
    build_active_embodiment_baseline,
    validate_active_embodiment_baseline,
)
from aion_astra_twin_embodiment.convergence import (
    AdoptionStatus,
    ConvergenceClassification,
    load_convergence_ledger,
)
from aion_astra_twin_embodiment.models import EmbodimentTemplate
from aion_astra_twin_embodiment.role_extensions import (
    build_teacher_extension_manifest,
    validate_role_specific_extension,
)
from aion_astra_twin_embodiment.shared_core import (
    build_shared_embodiment_core,
    shared_embodiment_core_hash,
)

ROOT = Path(__file__).parents[1]
LEDGER_PATH = ROOT / "data" / "EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json"
SCHEMA_PATH = ROOT / "schemas" / "ACTIVE_EMBODIMENT_BASELINE_SCHEMA.json"


def _fixture(include_teacher: bool = True):
    ledger = load_convergence_ledger(LEDGER_PATH)
    core = build_shared_embodiment_core(EmbodimentTemplate("adult-template", "v0.1"))
    teacher = build_teacher_extension_manifest(core)
    extensions = (teacher,) if include_teacher else ()
    baseline = build_active_embodiment_baseline(core, ledger, extensions)
    return baseline, core, ledger, extensions


def test_baseline_binds_one_core_and_deferred_sensorimotor_layer() -> None:
    baseline, core, ledger, extensions = _fixture()
    assert baseline.shared_core_sha256 == shared_embodiment_core_hash(core)
    assert baseline.role_extension_ids == (extensions[0].extension_id,)
    assert baseline.sensorimotor_layer_status == "DEFERRED_TO_PR_202"
    assert baseline.scientific_disposition == "HOLD"
    assert baseline.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert validate_active_embodiment_baseline(baseline, core, ledger, extensions)["result"] == "PASS"


def test_baseline_binds_extension_content_not_only_its_id() -> None:
    baseline, core, ledger, extensions = _fixture()
    changed = replace(extensions[0], capabilities=tuple(reversed(extensions[0].capabilities)))
    assert (validate_role_specific_extension(changed, core)["extension_hash"]
            != validate_role_specific_extension(extensions[0], core)["extension_hash"])
    changed_baseline = build_active_embodiment_baseline(core, ledger, (changed,))
    assert changed_baseline.baseline_id != baseline.baseline_id
    assert changed_baseline.role_extension_sha256s != baseline.role_extension_sha256s
    assert build_active_embodiment_baseline(core, ledger, extensions) == baseline
    with pytest.raises(ValueError):
        validate_active_embodiment_baseline(baseline, core, ledger, (changed,))


def test_baseline_reconciles_ledger_and_teacher_capability_provenance() -> None:
    _, core, ledger, extensions = _fixture()
    changed_entries = tuple(
        replace(entry, classification=ConvergenceClassification.ARCHIVE_ONLY,
                adoption_status=AdoptionStatus.HISTORICAL_ONLY,
                target_owner="archive:teacher-anthropometry")
        if entry.source_path_or_semantic_unit == "teacher_anthropometry.py :: 62-measure profile"
        else entry for entry in ledger.entries
    )
    changed = replace(ledger, entries=changed_entries)
    with pytest.raises(ValueError):
        build_active_embodiment_baseline(core, changed, extensions)


def test_baseline_independent_of_teacher_extension() -> None:
    baseline, core, _, _ = _fixture(False)
    assert baseline.role_extension_ids == ()
    assert baseline.shared_core_sha256 == shared_embodiment_core_hash(core)


def test_baseline_rejects_wrong_hash_duplicate_extension_and_claim_promotion() -> None:
    baseline, core, ledger, extensions = _fixture()
    for changed in (
        replace(baseline, shared_core_sha256="0" * 64),
        replace(baseline, convergence_ledger_sha256="0" * 64),
        replace(baseline, role_extension_ids=(extensions[0].extension_id,) * 2),
        replace(baseline, sensorimotor_layer_status="IMPLEMENTED"),
        replace(baseline, subjectivity_conclusion="ESTABLISHED"),
        replace(baseline, canonical_effect="MERGE"),
        replace(baseline, deployment=True),
    ):
        with pytest.raises(ValueError):
            validate_active_embodiment_baseline(changed, core, ledger, extensions)


def test_baseline_rejects_wrong_extension_core_binding() -> None:
    baseline, core, ledger, extensions = _fixture()
    with pytest.raises(ValueError, match="shared core"):
        validate_active_embodiment_baseline(
            baseline, core, ledger,
            (replace(extensions[0], shared_core_sha256="0" * 64),),
        )


def test_baseline_schema_is_exact_and_fails_closed() -> None:
    baseline, _, _, _ = _fixture()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    payload = json.loads(json.dumps(asdict(baseline)))
    assert not list(validator.iter_errors(payload))
    assert list(validator.iter_errors({**payload, "unreviewed": True}))
    assert list(validator.iter_errors({**payload, "scientific_disposition": "PASS"}))


def test_package_exports_converged_baseline_without_role_import_in_shared_core() -> None:
    import aion_astra_twin_embodiment as package
    from aion_astra_twin_embodiment import shared_core

    assert package.build_active_embodiment_baseline is build_active_embodiment_baseline
    assert package.build_shared_embodiment_core is build_shared_embodiment_core
    assert package.build_teacher_extension_manifest is build_teacher_extension_manifest
    assert "role_extensions" not in shared_core.__dict__
