from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Callable
from urllib.request import urlopen

from .source_snapshot import ArtifactDefinition, SupplyChainError

SYFT_VERSION = "1.52.0"
SYFT_URL = (
    "https://github.com/anchore/syft/releases/download/v1.52.0/"
    "syft_1.52.0_linux_amd64.tar.gz"
)
SYFT_ARCHIVE_SHA256 = "caeedb81fb0491615f1ebd1761e4145d41ee86dd2cc7bf80669f9f5ad9d6133d"
SPDX_SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "schemas"
    / "vendor"
    / "spdx-2.3"
    / "spdx-schema.json"
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    destination = destination.resolve()
    for member in archive.getmembers():
        path = PurePosixPath(member.name)
        if path.is_absolute() or ".." in path.parts:
            raise SupplyChainError("archive contains an unsafe member path")
        if member.issym() or member.islnk():
            link = PurePosixPath(member.linkname)
            if link.is_absolute() or ".." in link.parts:
                raise SupplyChainError("archive contains an unsafe link target")
    data_filter = getattr(tarfile, "data_filter", None)
    if data_filter is None:
        raise SupplyChainError("secure tar extraction filter is unavailable")
    try:
        archive.extractall(destination, filter=data_filter)
    except (tarfile.TarError, OSError) as exc:
        raise SupplyChainError("archive failed secure data-filter extraction") from exc


def fetch_pinned_syft(
    *,
    opener: Callable[..., BinaryIO] = urlopen,
) -> bytes:
    try:
        with opener(SYFT_URL, timeout=30) as response:
            data = response.read()
    except OSError as exc:
        raise SupplyChainError("pinned Syft download failed") from exc
    if _sha256_bytes(data) != SYFT_ARCHIVE_SHA256:
        raise SupplyChainError("pinned Syft archive SHA-256 mismatch")
    return data


def extract_pinned_syft(archive_bytes: bytes, destination: Path) -> Path:
    if _sha256_bytes(archive_bytes) != SYFT_ARCHIVE_SHA256:
        raise SupplyChainError("pinned Syft archive SHA-256 mismatch")
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = destination / "syft.tar.gz"
    archive_path.write_bytes(archive_bytes)
    try:
        with tarfile.open(archive_path, mode="r:gz") as archive:
            _safe_extract(archive, destination)
    except tarfile.TarError as exc:
        raise SupplyChainError("pinned Syft archive is unreadable") from exc
    binary = destination / "syft"
    if not binary.is_file():
        raise SupplyChainError("pinned Syft archive did not contain the syft executable")
    binary.chmod(binary.stat().st_mode | 0o111)
    return binary


def verify_syft_version(syft_binary: Path) -> None:
    if not syft_binary.is_file():
        raise SupplyChainError("Syft executable does not exist")
    try:
        result = subprocess.run(
            [str(syft_binary), "version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SupplyChainError("Syft version check failed") from exc
    if re.search(r"(?<![0-9])1\.52\.0(?![0-9])", result.stdout) is None:
        raise SupplyChainError(f"Syft executable version must be {SYFT_VERSION}")


def _load_official_spdx_schema() -> dict[str, Any]:
    try:
        schema = json.loads(SPDX_SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SupplyChainError("pinned official SPDX 2.3 schema is unavailable") from exc
    if not isinstance(schema, dict):
        raise SupplyChainError("pinned official SPDX 2.3 schema must be a JSON object")
    return schema


def _validate_official_spdx_schema(data: dict[str, Any]) -> None:
    try:
        from jsonschema import Draft7Validator
    except ImportError as exc:
        raise SupplyChainError("jsonschema dependency is unavailable") from exc
    schema = _load_official_spdx_schema()
    try:
        Draft7Validator.check_schema(schema)
    except Exception as exc:
        raise SupplyChainError("pinned official SPDX 2.3 schema is invalid") from exc
    errors = sorted(
        Draft7Validator(schema).iter_errors(data),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        raise SupplyChainError(
            f"SBOM failed official SPDX 2.3 schema validation: {errors[0].message}"
        )


def validate_spdx_sbom(sbom_path: Path) -> dict[str, Any]:
    try:
        data = json.loads(sbom_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SupplyChainError("SBOM must be readable SPDX JSON") from exc
    if not isinstance(data, dict):
        raise SupplyChainError("SBOM root must be a JSON object")
    _validate_official_spdx_schema(data)
    if data.get("spdxVersion") != "SPDX-2.3":
        raise SupplyChainError("SBOM spdxVersion must be SPDX-2.3")
    if data.get("SPDXID") != "SPDXRef-DOCUMENT":
        raise SupplyChainError("SBOM must use SPDXRef-DOCUMENT as the document identifier")
    if data.get("dataLicense") != "CC0-1.0":
        raise SupplyChainError("SBOM dataLicense must be CC0-1.0")
    packages = data.get("packages")
    files = data.get("files")
    package_count = len(packages) if isinstance(packages, list) else 0
    file_count = len(files) if isinstance(files, list) else 0
    if package_count + file_count == 0:
        raise SupplyChainError("SBOM inventory must not be empty")
    relationships = data.get("relationships")
    if not isinstance(relationships, list) or not any(
        isinstance(item, dict)
        and item.get("spdxElementId") == "SPDXRef-DOCUMENT"
        and item.get("relationshipType") == "DESCRIBES"
        for item in relationships
    ):
        raise SupplyChainError("SBOM must contain a document DESCRIBES relationship")
    return {
        "spdx_version": "SPDX-2.3",
        "package_count": package_count,
        "file_count": file_count,
    }


def generate_sbom(
    snapshot_path: Path,
    sbom_path: Path,
    *,
    opener: Callable[..., BinaryIO] = urlopen,
) -> dict[str, Any]:
    if not snapshot_path.is_file():
        raise SupplyChainError("source snapshot does not exist")

    with tempfile.TemporaryDirectory(prefix="aion-sbom-") as temp:
        temp_root = Path(temp)
        syft_binary = extract_pinned_syft(
            fetch_pinned_syft(opener=opener),
            temp_root / "syft",
        )
        verify_syft_version(syft_binary)

        root = temp_root / "snapshot"
        root.mkdir()
        try:
            with tarfile.open(snapshot_path, mode="r:") as archive:
                _safe_extract(archive, root)
        except tarfile.TarError as exc:
            raise SupplyChainError("source snapshot is unreadable") from exc

        env = dict(os.environ)
        env["SYFT_CHECK_FOR_APP_UPDATE"] = "false"
        try:
            subprocess.run(
                [
                    str(syft_binary),
                    f"dir:{root}",
                    "-o",
                    f"spdx-json@2.3={sbom_path}",
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            raise SupplyChainError("Syft SBOM generation failed") from exc

    summary = validate_spdx_sbom(sbom_path)
    summary.update(
        {
            "sbom_path": str(sbom_path.resolve()),
            "sbom_sha256": hashlib.sha256(sbom_path.read_bytes()).hexdigest(),
            "generator": f"syft@v{SYFT_VERSION}",
        }
    )
    return summary


def _verify_subject_bytes(subject: ArtifactDefinition) -> Path:
    path = Path(subject.artifact_path)
    if not path.is_file():
        raise SupplyChainError("subject artifact does not exist")
    if path.name != subject.artifact_name:
        raise SupplyChainError("subject artifact name does not match the definition")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != subject.artifact_sha256:
        raise SupplyChainError("subject artifact SHA-256 no longer matches the definition")
    return path


def bind_sbom_to_subject(
    subject: ArtifactDefinition,
    sbom_path: Path,
) -> dict[str, Any]:
    _verify_subject_bytes(subject)
    summary = validate_spdx_sbom(sbom_path)
    return {
        "repository": subject.repository,
        "source_head": subject.source_head,
        "artifact_name": subject.artifact_name,
        "artifact_sha256": subject.artifact_sha256,
        "sbom_sha256": hashlib.sha256(sbom_path.read_bytes()).hexdigest(),
        "spdx_version": summary["spdx_version"],
        "generator": f"syft@v{SYFT_VERSION}",
        "official_release_artifact": False,
        "canonical_effect": "NONE",
        "deployment": False,
        "slsa_level": "NOT_CLAIMED",
    }
