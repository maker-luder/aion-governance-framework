from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"aion_test_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_historical_tag_object_mismatch_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    verifier = load_script("verify_release")

    def fake_git_text(*args: str) -> str:
        if args[-1] == verifier.HISTORICAL_RC_REF:
            return "0" * 40
        return verifier.EXPECTED_PEELED_COMMIT

    monkeypatch.setattr(verifier, "git_text", fake_git_text)
    result = verifier.verify_historical_rc()
    assert result["status"] == "FAIL"
    assert result["historical_reference_drift"] is True
    assert any("tag-object mismatch" in error for error in result["errors"])


def test_historical_peeled_commit_mismatch_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    verifier = load_script("verify_release")

    def fake_git_text(*args: str) -> str:
        if args[-1] == verifier.HISTORICAL_RC_REF:
            return verifier.EXPECTED_TAG_OBJECT
        return "f" * 40

    monkeypatch.setattr(verifier, "git_text", fake_git_text)
    result = verifier.verify_historical_rc()
    assert result["status"] == "FAIL"
    assert result["historical_reference_drift"] is True
    assert any("peeled-commit mismatch" in error for error in result["errors"])


@pytest.mark.parametrize("script_name", ["verify_release", "scan_public_tree"])
def test_windows_private_path_patterns_cover_plain_serialized_and_case(script_name: str) -> None:
    module = load_script(script_name)
    slash = "\\"
    plain = "C:" + slash + "Users" + slash + "Example" + slash + "file.txt"
    serialized = "C:" + slash * 2 + "Users" + slash * 2 + "Example" + slash * 2 + "file.txt"
    case_variant = "c:" + slash + "uSeRs" + slash + "EXAMPLE" + slash + "file.txt"
    benign = "C:" + slash + "Project" + slash + "public" + slash + "file.txt"
    for value in (plain, serialized, case_variant):
        assert any(pattern.search(value) for pattern in module.PATH_PATTERNS)
    assert not any(pattern.search(benign) for pattern in module.PATH_PATTERNS)


@pytest.mark.parametrize("script_name", ["verify_release", "scan_public_tree"])
def test_posix_private_path_patterns_cover_bare_home_and_nested(script_name: str) -> None:
    module = load_script(script_name)
    for value in ("/home/example", "/home/example/file.txt"):
        assert any(pattern.search(value) for pattern in module.PATH_PATTERNS)
    assert not any(pattern.search("/srv/public/home/example") for pattern in module.PATH_PATTERNS)


def test_generic_manifest_invocation_cannot_overwrite_frozen_evidence() -> None:
    generator = load_script("generate_manifest")
    frozen = sorted(generator.FROZEN_OUTPUTS, key=str)
    before = {path: sha256(path) for path in frozen}
    with pytest.raises(SystemExit) as exc_info:
        generator.main([])
    assert exc_info.value.code == 2
    assert {path: sha256(path) for path in frozen} == before


def test_explicit_frozen_manifest_destination_is_rejected() -> None:
    generator = load_script("generate_manifest")
    frozen = sorted(generator.FROZEN_OUTPUTS, key=str)
    before = {path: sha256(path) for path in frozen}
    with pytest.raises(SystemExit) as exc_info:
        generator.main(
            [
                "--baseline",
                "current-head",
                "--output-dir",
                str(generator.FROZEN_MANIFEST_DIR),
            ]
        )
    assert exc_info.value.code == 2
    assert {path: sha256(path) for path in frozen} == before


def test_explicit_non_frozen_manifest_destination(tmp_path: Path) -> None:
    generator = load_script("generate_manifest")
    output = tmp_path / "current-head-TEST"
    assert generator.main(
        ["--baseline", "current-head-TEST", "--output-dir", str(output)]
    ) == 0
    manifest = output / "FILE_MANIFEST.json"
    sums = output / "SHA256SUMS.txt"
    assert manifest.is_file()
    assert sums.is_file()
    assert '"baseline": "current-head-TEST"' in manifest.read_text(encoding="utf-8")


def test_generated_build_dist_and_egg_info_are_ignored_by_release_tools(tmp_path: Path) -> None:
    generator = load_script("generate_manifest")
    scanner = load_script("scan_public_tree")
    generated = [
        tmp_path / "build" / "a" / "artifact.txt",
        tmp_path / "dist" / "artifact.whl",
        tmp_path / "pkg.egg-info" / "PKG-INFO",
    ]
    for path in generated:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("/home/privateuser\n", encoding="utf-8")
    regular = tmp_path / "src" / "kept.txt"
    regular.parent.mkdir(parents=True, exist_ok=True)
    regular.write_text("kept\n", encoding="utf-8")
    monkeypatch = pytest.MonkeyPatch()
    try:
        monkeypatch.setattr(generator, "ROOT", tmp_path)
        records = generator.build_records(tmp_path / "out")
        assert [record["path"] for record in records] == ["src/kept.txt"]
        assert scanner.scan_root(tmp_path) == []
    finally:
        monkeypatch.undo()


def test_workflow_keeps_both_historical_verification_layers() -> None:
    workflow = (ROOT / ".github" / "workflows" / "quality.yml").read_text(encoding="utf-8")
    assert "historical-self-verification:" in workflow
    assert "ref: v0.1.0-rc.1" in workflow
    assert "current-historical-revalidation:" in workflow
    assert "fetch-depth: 0" in workflow
    assert "fetch-tags: true" in workflow
    assert "python scripts/verify_release.py --baseline historical-rc" in workflow
