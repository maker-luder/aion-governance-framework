from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from aion_evidence_interop.canonical import InteropError, validate_source_record
from aion_evidence_interop.manifest import build_bundle, bundle_hashes, write_bundle


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]
RECORD = COMPONENT / "fixtures" / "valid_minimal.json"


def _head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def _schema() -> dict[str, object]:
    return json.loads(
        (COMPONENT / "schemas" / "interop_manifest_v0.1.0.schema.json").read_text()
    )


def _manifest() -> dict[str, object]:
    return json.loads(build_bundle(ROOT, RECORD, expected_head=_head())["interop-manifest.json"])


def test_generated_manifest_validates_against_strict_schema() -> None:
    schema = _schema()
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(_manifest())


@pytest.mark.parametrize(
    ("path", "invalid"),
    [
        (("profile_version",), "0.2.0"),
        (("source", "record_ref"), "../../private.json"),
        (("source", "record_sha256"), "a" * 63),
        (("source", "code_commit"), "A" * 40),
        (("source", "validation_status"), "HOLD"),
        (("source", "result_status"), "SCIENTIFICALLY_TRUE"),
        (("boundaries", "canonical_effect"), "PROMOTE"),
        (("boundaries", "deployment"), True),
        (("boundaries", "human_identity_inferred"), True),
        (("exports", "w3c_prov"), "/tmp/prov.jsonld"),
        (("artifact_digests", "prov.jsonld"), "0" * 65),
        (("policy", "python_mirror_allow"), False),
    ],
)
def test_manifest_schema_rejects_invalid_contract_values(
    path: tuple[str, ...], invalid: object
) -> None:
    value = deepcopy(_manifest())
    target = value
    for part in path[:-1]:
        target = target[part]  # type: ignore[assignment,index]
    target[path[-1]] = invalid  # type: ignore[index]
    with pytest.raises(ValidationError):
        Draft202012Validator(_schema()).validate(value)


def test_manifest_schema_rejects_unknown_nested_properties() -> None:
    value = _manifest()
    value["boundaries"]["scientific_truth"] = True  # type: ignore[index]
    with pytest.raises(ValidationError):
        Draft202012Validator(_schema()).validate(value)


def test_generation_is_byte_identical_across_independent_directories(tmp_path: Path) -> None:
    first_bundle = build_bundle(ROOT, RECORD, expected_head=_head())
    second_bundle = build_bundle(ROOT, RECORD, expected_head=_head())
    first = tmp_path / "first"
    second = tmp_path / "second"
    write_bundle(first, first_bundle)
    write_bundle(second, second_bundle)

    first_files = sorted(path.relative_to(first).as_posix() for path in first.rglob("*") if path.is_file())
    second_files = sorted(path.relative_to(second).as_posix() for path in second.rglob("*") if path.is_file())
    assert first_files == second_files
    assert first_files == sorted(first_bundle)
    assert bundle_hashes(first_bundle) == bundle_hashes(second_bundle)
    for relative in first_files:
        assert (first / relative).read_bytes() == (second / relative).read_bytes()


@pytest.fixture
def repository_scratch() -> Path:
    path = Path(tempfile.mkdtemp(prefix=".aion-interop-test-", dir=ROOT))
    try:
        yield path
    finally:
        shutil.rmtree(path)


def test_source_path_traversal_fails_closed() -> None:
    handle = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", dir=ROOT.parent, delete=False
    )
    try:
        handle.write("{}")
        handle.close()
        traversal = ROOT / ".." / Path(handle.name).name
        with pytest.raises(InteropError, match="repository-local") as caught:
            validate_source_record(ROOT, traversal, expected_head=_head())
        assert caught.value.category == "path_confinement_failure"
    finally:
        Path(handle.name).unlink(missing_ok=True)


def test_absolute_source_outside_repository_fails_closed(tmp_path: Path) -> None:
    record = tmp_path / "record.json"
    record.write_text("{}")
    with pytest.raises(InteropError, match="repository-local") as caught:
        validate_source_record(ROOT, record, expected_head=_head())
    assert caught.value.category == "path_confinement_failure"


def test_source_symlink_escape_fails_closed(repository_scratch: Path, tmp_path: Path) -> None:
    external = tmp_path / "private.json"
    external.write_text("{}")
    link = repository_scratch / "record.json"
    link.symlink_to(external)
    with pytest.raises(InteropError, match="repository-local") as caught:
        validate_source_record(ROOT, link, expected_head=_head())
    assert caught.value.category == "path_confinement_failure"


@pytest.mark.parametrize(
    ("name", "payload", "message"),
    [
        ("invalid.json", "{", "invalid JSON"),
        ("invalid-utf8.json", b"\xff", "valid UTF-8"),
    ],
)
def test_malformed_source_files_fail_closed(
    repository_scratch: Path, name: str, payload: str | bytes, message: str
) -> None:
    path = repository_scratch / name
    if isinstance(payload, bytes):
        path.write_bytes(payload)
    else:
        path.write_text(payload)
    with pytest.raises(InteropError, match=message):
        validate_source_record(ROOT, path, expected_head=_head())


def test_directory_and_missing_source_fail_closed(repository_scratch: Path) -> None:
    with pytest.raises(InteropError, match="not a regular file"):
        validate_source_record(ROOT, repository_scratch, expected_head=_head())
    with pytest.raises(InteropError, match="missing"):
        validate_source_record(ROOT, repository_scratch / "missing.json", expected_head=_head())


def test_invalid_schema_record_fails_closed(repository_scratch: Path) -> None:
    value = json.loads(RECORD.read_text())
    del value["claim_id"]
    path = repository_scratch / "invalid-schema.json"
    path.write_text(json.dumps(value))
    with pytest.raises(InteropError, match="source evidence validation failed closed"):
        validate_source_record(ROOT, path, expected_head=_head())


def test_local_evidence_reference_escape_fails_closed(repository_scratch: Path) -> None:
    value = json.loads(RECORD.read_text())
    value["protocol_ref"] = "../../private.json"
    path = repository_scratch / "reference-escape.json"
    path.write_text(json.dumps(value))
    with pytest.raises(InteropError, match="escapes repository root") as caught:
        validate_source_record(ROOT, path, expected_head=_head())
    assert caught.value.category == "path_confinement_failure"


@pytest.mark.parametrize("reference", ["C:\\private\\record.json", "file:///tmp/private.json"])
def test_absolute_local_reference_forms_fail_closed(
    repository_scratch: Path, reference: str
) -> None:
    value = json.loads(RECORD.read_text())
    value["protocol_ref"] = reference
    path = repository_scratch / "absolute-reference.json"
    path.write_text(json.dumps(value))
    with pytest.raises(InteropError) as caught:
        validate_source_record(ROOT, path, expected_head=_head())
    assert caught.value.category == "path_confinement_failure"


def test_oversized_source_record_fails_closed(repository_scratch: Path) -> None:
    path = repository_scratch / "oversized.json"
    path.write_bytes(b" " * (4 * 1024 * 1024 + 1))
    with pytest.raises(InteropError, match="exceeds"):
        validate_source_record(ROOT, path, expected_head=_head())


def test_invalid_expected_head_has_distinct_category() -> None:
    with pytest.raises(InteropError) as caught:
        validate_source_record(ROOT, RECORD, expected_head="main")
    assert caught.value.category == "invalid_expected_head"


def test_nonempty_output_directory_fails_without_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()
    sentinel = output / "private.txt"
    sentinel.write_text("do not overwrite")
    with pytest.raises(InteropError) as caught:
        write_bundle(output, {"prov.jsonld": b"{}\n"})
    assert caught.value.category == "write_failure"
    assert sentinel.read_text() == "do not overwrite"
