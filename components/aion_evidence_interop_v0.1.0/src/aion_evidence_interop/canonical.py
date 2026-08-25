from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class InteropError(RuntimeError):
    """Raised when an interoperability boundary fails closed."""


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


def load_record(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InteropError(f"source evidence record is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise InteropError(f"source evidence record is invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InteropError("source evidence record must be a JSON object")
    return value


def _record_ref(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _source_validator(root: Path) -> Path:
    return root / "scripts" / "validate_research_evidence.py"


def validate_source_record(
    root: Path,
    record_path: Path,
    *,
    expected_head: str,
) -> tuple[dict[str, Any], SourceValidation]:
    root = root.resolve()
    record_path = record_path.resolve()
    try:
        record_path.relative_to(root)
    except ValueError as exc:
        raise InteropError("source evidence record must be repository-local") from exc
    if re.fullmatch(r"[0-9a-f]{40}", expected_head) is None:
        raise InteropError("expected_head must be an exact lowercase 40-hex Git commit SHA")

    validator = _source_validator(root)
    if not validator.is_file():
        raise InteropError(f"AION source validator is missing: {validator}")

    record = load_record(record_path)
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
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise InteropError(
            "AION source validator did not return machine-readable JSON"
        ) from exc
    if not isinstance(result, dict):
        raise InteropError("AION source validator returned a non-object result")

    status = str(result.get("status", "HOLD"))
    diagnostics = tuple(str(item) for item in result.get("diagnostics", []))
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

    raw = record_path.read_bytes()
    validation = SourceValidation(
        status="PASS",
        diagnostics=diagnostics,
        record_ref=_record_ref(root, record_path),
        record_sha256=sha256_bytes(raw),
        expected_head=expected_head,
        result_status=str(record.get("result_status", "")),
        canonical_effect=canonical_effect,
        independent_ivv="NOT_ACHIEVED",
    )
    return record, validation
