from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from scripts.supply_chain.sbom import (
    SYFT_ARCHIVE_SHA256,
    bind_sbom_to_subject,
    generate_sbom,
    validate_spdx_sbom,
    verify_syft_version,
)
from scripts.supply_chain.source_snapshot import SupplyChainError, build_snapshot


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def _repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "AION Test"], cwd=repo, check=True)
    (repo / "alpha.txt").write_text("alpha\n", encoding="utf-8")
    subprocess.run(["git", "add", "alpha.txt"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=repo, check=True)
    return repo, _git(repo, "rev-parse", "HEAD")


def _valid_spdx(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "spdxVersion": "SPDX-2.3",
                "SPDXID": "SPDXRef-DOCUMENT",
                "dataLicense": "CC0-1.0",
                "name": "aion-test-sbom",
                "documentNamespace": "https://example.invalid/spdx/aion-test-sbom",
                "creationInfo": {
                    "created": "2026-09-25T00:00:00Z",
                    "creators": ["Tool: aion-test"],
                },
                "packages": [
                    {
                        "SPDXID": "SPDXRef-Package-aion",
                        "name": "aion",
                        "downloadLocation": "NOASSERTION",
                    }
                ],
                "relationships": [
                    {
                        "spdxElementId": "SPDXRef-DOCUMENT",
                        "relationshipType": "DESCRIBES",
                        "relatedSpdxElement": "SPDXRef-Package-aion",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_source_snapshot_is_deterministic_and_non_authoritative(tmp_path: Path) -> None:
    repo, head = _repo(tmp_path)
    first = build_snapshot(repo, head, tmp_path / "out-a")
    second = build_snapshot(repo, head, tmp_path / "out-b")
    assert first.artifact_sha256 == second.artifact_sha256
    assert Path(first.artifact_path).read_bytes() == Path(second.artifact_path).read_bytes()
    assert first.source_head == head
    assert first.output_count == 1
    assert first.official_release_artifact is False
    assert first.canonical_effect == "NONE"
    assert first.deployment is False


def test_source_snapshot_rejects_dirty_or_drifted_repository(tmp_path: Path) -> None:
    repo, head = _repo(tmp_path)
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    with pytest.raises(SupplyChainError, match="clean"):
        build_snapshot(repo, head, tmp_path / "out")

    subprocess.run(["git", "add", "dirty.txt"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "drift"], cwd=repo, check=True)
    with pytest.raises(SupplyChainError, match="drifted"):
        build_snapshot(repo, head, tmp_path / "out")


@pytest.mark.parametrize(
    "mutation,match",
    [
        ({"spdxVersion": "SPDX-3.0.1"}, "schema validation|SPDX-2.3"),
        ({"packages": [], "files": []}, "must not be empty"),
        ({"relationships": []}, "DESCRIBES"),
        ({"creationInfo": {}}, "schema validation"),
    ],
)
def test_spdx_validation_fails_closed(
    tmp_path: Path,
    mutation: dict[str, object],
    match: str,
) -> None:
    path = tmp_path / "sbom.json"
    _valid_spdx(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(mutation)
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(SupplyChainError, match=match):
        validate_spdx_sbom(path)


def test_sbom_binding_preserves_claim_ceiling(tmp_path: Path) -> None:
    repo, head = _repo(tmp_path)
    subject = build_snapshot(repo, head, tmp_path / "out")
    sbom = tmp_path / "sbom.json"
    _valid_spdx(sbom)
    record = bind_sbom_to_subject(subject, sbom)
    assert record["source_head"] == head
    assert record["artifact_sha256"] == subject.artifact_sha256
    assert record["spdx_version"] == "SPDX-2.3"
    assert record["official_release_artifact"] is False
    assert record["slsa_level"] == "NOT_CLAIMED"
    assert record["canonical_effect"] == "NONE"


def test_sbom_binding_rejects_subject_mutation(tmp_path: Path) -> None:
    repo, head = _repo(tmp_path)
    subject = build_snapshot(repo, head, tmp_path / "out")
    Path(subject.artifact_path).write_bytes(b"mutated")
    sbom = tmp_path / "sbom.json"
    _valid_spdx(sbom)
    with pytest.raises(SupplyChainError, match="SHA-256"):
        bind_sbom_to_subject(subject, sbom)


def test_syft_version_is_pinned(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    binary = tmp_path / "syft"
    binary.write_text("fixture", encoding="utf-8")

    def good_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess([], 0, stdout="Application: syft\nVersion: 1.52.0\n")

    monkeypatch.setattr("scripts.supply_chain.sbom.subprocess.run", good_run)
    verify_syft_version(binary)

    def bad_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess([], 0, stdout="Application: syft\nVersion: 1.51.1\n")

    monkeypatch.setattr("scripts.supply_chain.sbom.subprocess.run", bad_run)
    with pytest.raises(SupplyChainError, match="1.52.0"):
        verify_syft_version(binary)


def test_pinned_syft_digest_is_exact_sha256() -> None:
    assert len(SYFT_ARCHIVE_SHA256) == 64
    int(SYFT_ARCHIVE_SHA256, 16)


def test_generate_sbom_rejects_unpinned_archive_before_execution(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    snapshot = tmp_path / "snapshot.tar"
    snapshot.write_bytes(b"placeholder")
    executed = False

    class BadResponse:
        def __enter__(self) -> "BadResponse":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return b"not-the-pinned-syft-archive"

    def opener(*args: object, **kwargs: object) -> BadResponse:
        return BadResponse()

    def forbidden_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal executed
        executed = True
        raise AssertionError("Syft must not execute before archive digest verification")

    monkeypatch.setattr("scripts.supply_chain.sbom.subprocess.run", forbidden_run)

    with pytest.raises(SupplyChainError, match="SHA-256 mismatch"):
        generate_sbom(snapshot, tmp_path / "sbom.json", opener=opener)

    assert executed is False


def test_secure_extraction_rejects_special_files(tmp_path: Path) -> None:
    import io
    import tarfile

    from scripts.supply_chain.sbom import _safe_extract

    archive_bytes = io.BytesIO()
    with tarfile.open(fileobj=archive_bytes, mode="w") as archive:
        fifo = tarfile.TarInfo("unsafe-fifo")
        fifo.type = tarfile.FIFOTYPE
        archive.addfile(fifo)
    archive_bytes.seek(0)

    with tarfile.open(fileobj=archive_bytes, mode="r:") as archive:
        with pytest.raises(SupplyChainError, match="secure data-filter extraction"):
            _safe_extract(archive, tmp_path / "extract")
