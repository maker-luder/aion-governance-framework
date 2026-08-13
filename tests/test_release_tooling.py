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


def test_scanner_posix_private_path_patterns_cover_bare_home_and_nested() -> None:
    scanner = load_script("scan_public_tree")
    slash = "/"
    private_root = slash + "home" + slash + "example"
    nested = private_root + slash + "file.txt"
    benign = slash + "srv" + slash + "public" + slash + "home" + slash + "example"
    for value in (private_root, nested):
        assert any(pattern.search(value) for pattern in scanner.PATH_PATTERNS)
    assert not any(pattern.search(benign) for pattern in scanner.PATH_PATTERNS)


def test_scanner_still_rejects_private_path_in_regular_file(tmp_path: Path) -> None:
    scanner = load_script("scan_public_tree")
    slash = "/"
    private_value = slash + "home" + slash + "example" + slash + "secret.txt"
    regular = tmp_path / "src" / "bad.txt"
    regular.parent.mkdir(parents=True, exist_ok=True)
    regular.write_text(private_value + "\n", encoding="utf-8")
    assert scanner.scan_root(tmp_path) == ["private path pattern: src/bad.txt"]


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
    slash = "/"
    private_value = slash + "home" + slash + "privateuser"
    for path in generated:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(private_value + "\n", encoding="utf-8")
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


def test_quality_workflow_keeps_current_and_frozen_verification_layers() -> None:
    workflow = (ROOT / ".github" / "workflows" / "quality.yml").read_text(encoding="utf-8")
    assert "python scripts/verify_release.py --baseline current-head" in workflow
    assert "frozen-release-verification:" in workflow
    assert "ref: v0.1.0-rc.1" in workflow
    assert "python scripts/verify_release.py --baseline historical-rc" in workflow



def test_scanner_ignores_symlink_targets_outside_root(tmp_path: Path) -> None:
    scanner = load_script("scan_public_tree")
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("/home/privateuser/secret.txt\n", encoding="utf-8")
    (root / "linked.txt").symlink_to(outside)

    assert scanner.scan_root(root) == []



def test_manifest_generator_ignores_symlink_targets_outside_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generator = load_script("generate_manifest")
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside\n", encoding="utf-8")
    (root / "linked.txt").symlink_to(outside)
    monkeypatch.setattr(generator, "ROOT", root)

    assert generator.build_records(root / "generated") == []



def test_current_snapshot_classifies_dangling_tracked_symlink_before_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    verifier = load_script("verify_release")
    (tmp_path / "linked.txt").symlink_to(tmp_path / "missing-target.txt")
    monkeypatch.setattr(verifier, "ROOT", tmp_path)
    monkeypatch.setattr(verifier, "git_text", lambda *args: "a" * 40)
    monkeypatch.setattr(
        verifier,
        "tree_entries",
        lambda ref: {"linked.txt": ("120000", "b" * 40)},
    )

    result = verifier.verify_current_snapshot("current-head")

    assert result["status"] == "FAIL"
    assert result["errors"] == [
        "symlink verification unsupported on this platform: linked.txt"
    ]


def test_historical_manifest_non_object_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    verifier = load_script("verify_release")

    def fake_git_text(*args: str) -> str:
        if args[-1] == verifier.HISTORICAL_RC_REF:
            return verifier.EXPECTED_TAG_OBJECT
        return verifier.EXPECTED_PEELED_COMMIT

    def fake_git_bytes(*args: str) -> bytes:
        assert args[0] == "show"
        assert args[1].endswith(f":{verifier.MANIFEST_PATH}")
        return b"[]"

    monkeypatch.setattr(verifier, "git_text", fake_git_text)
    monkeypatch.setattr(verifier, "tree_entries", lambda ref: {})
    monkeypatch.setattr(verifier, "git_bytes", fake_git_bytes)

    result = verifier.verify_historical_rc()

    assert result["status"] == "FAIL"
    assert result["errors"] == ["historical manifest must be a JSON object"]
