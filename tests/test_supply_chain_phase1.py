from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from scripts.supply_chain.sbom import (
    SYFT_ARCHIVE_SHA256,
    bind_sbom_to_subject,
    validate_spdx_sbom,
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
                "packages": [{"SPDXID": "SPDXRef-Package-aion", "name": "aion"}],
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
        ({"spdxVersion": "SPDX-3.0.1"}, "SPDX-2.3"),
        ({"packages": [], "files": []}, "must not be empty"),
        ({"relationships": []}, "DESCRIBES"),
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


def test_pinned_syft_digest_is_exact_sha256() -> None:
    assert len(SYFT_ARCHIVE_SHA256) == 64
    int(SYFT_ARCHIVE_SHA256, 16)
