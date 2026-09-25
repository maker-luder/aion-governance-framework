from __future__ import annotations

import hashlib
import io
import re
import subprocess
import tarfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

REPOSITORY = "maker-luder/aion-governance-framework"
_SHA40 = re.compile(r"^[0-9a-f]{40}$")


class SupplyChainError(ValueError):
    """Fail-closed error for bounded supply-chain evidence generation."""


@dataclass(frozen=True, slots=True)
class ArtifactDefinition:
    repository: str
    source_head: str
    artifact_name: str
    artifact_type: str
    artifact_sha256: str
    artifact_path: str
    output_count: int = 1
    digest_algorithm: str = "sha256"
    official_release_artifact: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "repository": self.repository,
            "source_head": self.source_head,
            "artifact_name": self.artifact_name,
            "artifact_type": self.artifact_type,
            "artifact_sha256": self.artifact_sha256,
            "artifact_path": self.artifact_path,
            "output_count": self.output_count,
            "digest_algorithm": self.digest_algorithm,
            "official_release_artifact": self.official_release_artifact,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }


def _git(repo: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=repo,
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SupplyChainError(f"git command failed: {' '.join(args)}") from exc


def _validate_archive_bytes(data: bytes, source_sha: str) -> None:
    prefix = f"aion-{source_sha}/"
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
            members = archive.getmembers()
    except tarfile.TarError as exc:
        raise SupplyChainError("git archive output is not a readable tar archive") from exc
    if not members:
        raise SupplyChainError("source snapshot must not be empty")
    for member in members:
        path = PurePosixPath(member.name)
        root_entry = member.name.rstrip("/") == prefix.rstrip("/")
        if (
            path.is_absolute()
            or ".." in path.parts
            or (not root_entry and not member.name.startswith(prefix))
        ):
            raise SupplyChainError("source snapshot contains an unsafe or unexpected member path")
        if member.issym() or member.islnk():
            link = PurePosixPath(member.linkname)
            if link.is_absolute() or ".." in link.parts:
                raise SupplyChainError("source snapshot contains an unsafe link target")


def build_snapshot(repo: Path, source_sha: str, out_dir: Path) -> ArtifactDefinition:
    repo = repo.resolve()
    out_dir = out_dir.resolve()
    if _SHA40.fullmatch(source_sha) is None:
        raise SupplyChainError("source_sha must be an exact lowercase 40-hex commit")
    if not repo.is_dir():
        raise SupplyChainError("repository path must exist")

    resolved = _git(repo, "rev-parse", "--verify", f"{source_sha}^{{commit}}")
    if resolved != source_sha:
        raise SupplyChainError("source_sha did not resolve to the exact requested commit")
    if _git(repo, "rev-parse", "HEAD") != source_sha:
        raise SupplyChainError("repository HEAD drifted from source_sha")
    if _git(repo, "status", "--porcelain=v1", "--untracked-files=all"):
        raise SupplyChainError("repository must be clean before snapshot generation")

    try:
        proc = subprocess.run(
            [
                "git",
                "archive",
                "--format=tar",
                f"--prefix=aion-{source_sha}/",
                source_sha,
            ],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SupplyChainError("git archive failed") from exc

    data = proc.stdout
    _validate_archive_bytes(data, source_sha)
    out_dir.mkdir(parents=True, exist_ok=True)
    artifact_name = f"aion-source-snapshot-{source_sha}.tar"
    artifact_path = out_dir / artifact_name
    artifact_path.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()

    return ArtifactDefinition(
        repository=REPOSITORY,
        source_head=source_sha,
        artifact_name=artifact_name,
        artifact_type="source-archive",
        artifact_sha256=digest,
        artifact_path=str(artifact_path),
    )
