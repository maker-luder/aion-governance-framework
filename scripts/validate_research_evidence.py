from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Any, Iterable
from urllib.parse import urlsplit

SCHEMA_RELATIVE = "schemas/research_evidence_record_v0.2.0.schema.json"


@dataclass(frozen=True, slots=True)
class EvidenceValidation:
    status: str
    record_ref: str
    diagnostics: tuple[str, ...]
    mutation_performed: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False
    independent_ivv: str = "NOT_ACHIEVED"
    protocol_binding: str = "NOT_CHECKED"

    def as_dict(self) -> dict[str, Any]:
        return {
            "record_ref": self.record_ref,
            "status": self.status,
            "diagnostics": list(self.diagnostics),
            "protocol_binding": self.protocol_binding,
            "mutation_performed": self.mutation_performed,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
            "independent_ivv": self.independent_ivv,
        }


def _git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.STDOUT
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNSPECIFIED"


def _load_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, UnicodeError) as exc:
        return None, f"unavailable JSON file: {path}: {type(exc).__name__}"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {path}: {exc}"


def _record_ref(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _iter_declared_refs(value: Any, key: str | None = None) -> Iterable[str]:
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from _iter_declared_refs(child, child_key)
        return
    if key is not None and key.endswith("_ref") and isinstance(value, str):
        yield value
        return
    if key is not None and key.endswith("_refs") and isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                yield item


def _local_path(root: Path, value: str) -> Path | None:
    """Resolve relative paths; URI references are opaque and never downloaded."""
    candidate = value.split("#", 1)[0]
    if not candidate or "\\" in candidate or PureWindowsPath(candidate).drive:
        raise ValueError("invalid repository-relative reference")
    parsed = urlsplit(candidate)
    if parsed.scheme == "file" or Path(candidate).is_absolute():
        raise ValueError("reference must be repository-relative")
    if parsed.scheme or ("/" not in candidate and "." not in candidate):
        return None
    resolved = (root / candidate).resolve(strict=True)
    resolved.relative_to(root.resolve())
    return resolved


def _local_ref_exists(root: Path, value: str) -> bool:
    try:
        _local_path(root, value)
    except (OSError, ValueError, RuntimeError):
        return False
    return True


def _protocol_binding(root: Path, record: dict[str, Any]) -> tuple[str, str | None]:
    if str(record.get("result_status")) in {"NOT_RUN", "HOLD"}:
        return "DEFERRED", None
    try:
        protocol = _local_path(root, str(record.get("protocol_ref", "")))
        if protocol is None:
            return "UNVERIFIED", "completed protocol requires a retained repository-local file"
        if not protocol.is_file():
            return "UNVERIFIED", "completed protocol reference must resolve to a regular file"
        with protocol.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
    except (OSError, ValueError, RuntimeError):
        return "UNVERIFIED", "completed protocol bytes are unavailable or outside repository"
    if digest != record.get("protocol_hash"):
        return "MISMATCH", "protocol_hash does not match exact protocol file bytes"
    return "VERIFIED", None


def _schema_diagnostics(schema: dict[str, Any], record: dict[str, Any]) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return ["jsonschema dependency is unavailable"]
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema-error subclasses
        return [f"v0.2 schema is invalid: {exc}"]
    validator = Draft202012Validator(schema)
    return [
        f"schema validation: {error.message}"
        for error in sorted(validator.iter_errors(record), key=lambda item: tuple(str(part) for part in item.absolute_path))
    ]


def validate_record(
    root: Path,
    record_path: Path,
    *,
    expected_head: str | None = None,
) -> EvidenceValidation:
    root = root.resolve()
    record_path = record_path.resolve()
    record_ref = _record_ref(root, record_path)
    schema, schema_error = _load_json(root / SCHEMA_RELATIVE)
    record, record_error = _load_json(record_path)
    if schema_error or record_error:
        diagnostics = tuple(item for item in (schema_error, record_error) if item)
        return EvidenceValidation("HOLD", record_ref, diagnostics)
    if not isinstance(schema, dict) or not isinstance(record, dict):
        return EvidenceValidation(
            "HOLD",
            record_ref,
            ("schema or evidence record is not a JSON object",),
        )

    diagnostics = _schema_diagnostics(schema, record)

    for ref in sorted(set(_iter_declared_refs(record))):
        if not _local_ref_exists(root, ref):
            diagnostics.append(f"local evidence reference does not exist: {ref}")

    inspected_head = expected_head if expected_head is not None else _git_head(root)
    code_commit = str(record.get("code_commit", ""))
    result_status = str(record.get("result_status", ""))
    if result_status not in {"NOT_RUN", "HOLD"}:
        if re.fullmatch(r"[0-9a-f]{40}", inspected_head or "") is None:
            diagnostics.append("completed record requires an exact inspected head")
        elif code_commit != inspected_head:
            diagnostics.append("completed record code_commit is not bound to the inspected head")

    protocol_binding, protocol_error = _protocol_binding(root, record)
    if protocol_error:
        diagnostics.append(protocol_error)

    if record.get("canonical_effect") != "NONE":
        diagnostics.append("canonical_effect must remain NONE")

    return EvidenceValidation(
        "PASS" if not diagnostics else "FAIL",
        record_ref,
        tuple(diagnostics),
        protocol_binding=protocol_binding,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate additive research evidence records without promotion"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--expected-head", default=None)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    record = args.record if args.record.is_absolute() else root / args.record
    result = validate_record(
        root,
        record,
        expected_head=args.expected_head if args.expected_head is not None else _git_head(root),
    )
    print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
    return 0 if result.status == "PASS" else 2 if result.status == "FAIL" else 10


if __name__ == "__main__":
    raise SystemExit(main())
