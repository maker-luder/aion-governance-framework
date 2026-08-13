from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SCHEMA_RELATIVE = "schemas/research_evidence_record_v0.2.0.schema.json"
LOCAL_PREFIXES = (
    "components/",
    "examples/",
    "research-labs/",
    "research-workbench/",
    "docs/",
    "qa/",
    "scripts/",
    "schemas/",
    ".github/",
)


@dataclass(frozen=True, slots=True)
class EvidenceValidation:
    status: str
    record_ref: str
    diagnostics: tuple[str, ...]
    mutation_performed: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False
    independent_ivv: str = "NOT_ACHIEVED"

    def as_dict(self) -> dict[str, Any]:
        return {
            "record_ref": self.record_ref,
            "status": self.status,
            "diagnostics": list(self.diagnostics),
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
    except FileNotFoundError:
        return None, f"missing JSON file: {path}"
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


def _local_ref_exists(root: Path, value: str) -> bool:
    candidate = value.split("#", 1)[0]
    if not candidate.startswith(LOCAL_PREFIXES):
        return True
    root = root.resolve()
    candidate_path = root / candidate
    try:
        resolved = candidate_path.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError):
        return False
    return True


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
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path))
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
    if inspected_head and inspected_head != "UNSPECIFIED" and code_commit != inspected_head:
        if result_status not in {"NOT_RUN", "HOLD"}:
            diagnostics.append("completed record code_commit is not bound to the inspected head")

    if record.get("canonical_effect") != "NONE":
        diagnostics.append("canonical_effect must remain NONE")

    return EvidenceValidation(
        "PASS" if not diagnostics else "FAIL",
        record_ref,
        tuple(diagnostics),
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
