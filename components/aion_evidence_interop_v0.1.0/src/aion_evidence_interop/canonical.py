from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Any, Iterable
from urllib.parse import urlsplit


MAX_SOURCE_RECORD_BYTES = 4 * 1024 * 1024
VALIDATOR_TIMEOUT_SECONDS = 30
MAX_VALIDATOR_OUTPUT_CHARS = 1024 * 1024


class InteropError(RuntimeError):
    """Raised when an interoperability boundary fails closed."""

    def __init__(self, message: str, *, category: str = "source_validation_failure") -> None:
        super().__init__(message)
        self.category = category


@dataclass(frozen=True, slots=True)
class SourceValidation:
    status: str
    diagnostics: tuple[str, ...]
    record_ref: str
    record_sha256: str
    expected_head: str
    result_status: str
    canonical_effect: str
    independent_ivv: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "diagnostics": list(self.diagnostics),
            "record_ref": self.record_ref,
            "record_sha256": self.record_sha256,
            "expected_head": self.expected_head,
            "result_status": self.result_status,
            "canonical_effect": self.canonical_effect,
            "independent_ivv": self.independent_ivv,
        }


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_record(path: Path, *, display_ref: str | None = None) -> tuple[dict[str, Any], bytes]:
    label = display_ref or path.name
    try:
        size = path.stat().st_size
    except FileNotFoundError as exc:
        raise InteropError(f"source evidence record is missing: {label}") from exc
    except OSError as exc:
        raise InteropError(f"source evidence record cannot be inspected: {label}") from exc
    if not path.is_file():
        raise InteropError(f"source evidence record is not a regular file: {label}")
    if size > MAX_SOURCE_RECORD_BYTES:
        raise InteropError(
            f"source evidence record exceeds {MAX_SOURCE_RECORD_BYTES} bytes: {label}"
        )
    try:
        raw = path.read_bytes()
        if len(raw) > MAX_SOURCE_RECORD_BYTES:
            raise InteropError(
                f"source evidence record exceeds {MAX_SOURCE_RECORD_BYTES} bytes: {label}"
            )
        text = raw.decode("utf-8")
        value = json.loads(text)
    except UnicodeDecodeError as exc:
        raise InteropError(f"source evidence record is not valid UTF-8: {label}") from exc
    except json.JSONDecodeError as exc:
        raise InteropError(
            f"source evidence record is invalid JSON: {label}: line {exc.lineno} column {exc.colno}"
        ) from exc
    except RecursionError as exc:
        raise InteropError(
            f"source evidence record exceeds safe JSON nesting: {label}"
        ) from exc
    except OSError as exc:
        raise InteropError(f"source evidence record cannot be read: {label}") from exc
    if not isinstance(value, dict):
        raise InteropError("source evidence record must be a JSON object")
    return value, raw


def _record_ref(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _source_validator(root: Path) -> Path:
    return root / "scripts" / "validate_research_evidence.py"


def _iter_declared_refs(value: Any, key: str | None = None) -> Iterable[str]:
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from _iter_declared_refs(child, child_key)
    elif key is not None and key.endswith("_ref") and isinstance(value, str):
        yield value
    elif key is not None and key.endswith("_refs") and isinstance(value, list):
        yield from (item for item in value if isinstance(item, str))


def _validate_reference_confinement(root: Path, record: dict[str, Any]) -> None:
    """Reject path-shaped declared references that can escape the repository.

    URI-like references remain opaque references and are never fetched. Existing
    repository-native validation remains responsible for existence checks.
    """

    for value in sorted(set(_iter_declared_refs(record))):
        candidate = value.split("#", 1)[0]
        parsed = urlsplit(candidate)
        if PureWindowsPath(candidate).is_absolute():
            raise InteropError(
                f"local evidence reference must be repository-relative: {value}",
                category="path_confinement_failure",
            )
        if parsed.scheme and parsed.scheme != "file":
            continue
        path = Path(candidate)
        if parsed.scheme == "file" or path.is_absolute():
            raise InteropError(
                f"local evidence reference must be repository-relative: {value}",
                category="path_confinement_failure",
            )
        try:
            (root / path).resolve(strict=False).relative_to(root)
        except (OSError, ValueError) as exc:
            raise InteropError(
                f"local evidence reference escapes repository root: {value}",
                category="path_confinement_failure",
            ) from exc


def _inspected_git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.STDOUT,
            timeout=10,
        ).strip()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise InteropError(
            "repository Git head cannot be inspected",
            category="invalid_expected_head",
        ) from exc


def validate_source_record(
    root: Path,
    record_path: Path,
    *,
    expected_head: str,
) -> tuple[dict[str, Any], SourceValidation]:
    root = root.resolve()
    if not root.is_dir():
        raise InteropError(
            "repository root is not a directory",
            category="path_confinement_failure",
        )
    try:
        record_path = record_path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise InteropError("source evidence record is missing") from exc
    except OSError as exc:
        raise InteropError(
            "source evidence record path cannot be resolved",
            category="path_confinement_failure",
        ) from exc
    try:
        record_path.relative_to(root)
    except ValueError as exc:
        raise InteropError(
            "source evidence record must be repository-local",
            category="path_confinement_failure",
        ) from exc
    if re.fullmatch(r"[0-9a-f]{40}", expected_head) is None:
        raise InteropError(
            "expected_head must be an exact lowercase 40-hex Git commit SHA",
            category="invalid_expected_head",
        )
    if _inspected_git_head(root) != expected_head:
        raise InteropError(
            "expected_head does not match the exact inspected Git head",
            category="invalid_expected_head",
        )

    validator = _source_validator(root)
    if not validator.is_file():
        raise InteropError("AION source validator is missing")

    record_ref = _record_ref(root, record_path)
    record, raw = load_record(record_path, display_ref=record_ref)
    _validate_reference_confinement(root, record)
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(validator),
                "--root",
                str(root),
                "--record",
                str(record_path),
                "--expected-head",
                expected_head,
            ],
            cwd=root,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=VALIDATOR_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InteropError("AION source validator could not complete") from exc
    if len(proc.stdout) > MAX_VALIDATOR_OUTPUT_CHARS:
        raise InteropError("AION source validator output exceeds the inspection limit")
    try:
        result = json.loads(proc.stdout)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise InteropError(
            "AION source validator did not return machine-readable JSON"
        ) from exc
    if not isinstance(result, dict):
        raise InteropError("AION source validator returned a non-object result")
    if proc.returncode != 0 and result.get("status") == "PASS":
        raise InteropError("AION source validator returned inconsistent process status")

    status = str(result.get("status", "HOLD"))
    diagnostic_values = result.get("diagnostics", [])
    if not isinstance(diagnostic_values, list):
        raise InteropError("AION source validator returned invalid diagnostics")
    diagnostics = tuple(str(item) for item in diagnostic_values)
    if status != "PASS":
        detail = "; ".join(diagnostics) if diagnostics else "no diagnostics"
        raise InteropError(f"source evidence validation failed closed: {status}: {detail}")

    canonical_effect = str(record.get("canonical_effect", ""))
    if canonical_effect != "NONE":
        raise InteropError("source evidence canonical_effect must remain NONE")

    nonclaims = record.get("nonclaims")
    if not isinstance(nonclaims, dict):
        raise InteropError("source evidence nonclaims object is required")
    required_nonclaims = {
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "consciousness_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
        "main_effect": "NONE",
        "canonical_effect": "NONE",
        "live_runtime_effect": "NONE",
        "runtime_effect": "NONE",
    }
    for key, expected in required_nonclaims.items():
        if nonclaims.get(key) != expected:
            raise InteropError(f"source evidence nonclaim boundary is open: {key}")

    independent_ivv = str(record.get("independent_validation_status", ""))
    if independent_ivv == "IVV_ACHIEVED":
        raise InteropError(
            "interop v0.1.0 does not promote or independently verify IV&V claims"
        )

    validation = SourceValidation(
        status="PASS",
        diagnostics=diagnostics,
        record_ref=record_ref,
        record_sha256=sha256_bytes(raw),
        expected_head=expected_head,
        result_status=str(record.get("result_status", "")),
        canonical_effect=canonical_effect,
        independent_ivv="NOT_ACHIEVED",
    )
    return record, validation
