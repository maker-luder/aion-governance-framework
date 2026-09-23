"""Verify Phase A v0.2 semantic coverage and exact Git bindings."""

from __future__ import annotations

import json
from pathlib import Path

from aion_astra_twin_embodiment.coverage_matrix import (
    coverage_matrix_hash,
    load_coverage_matrix,
    validate_coverage_matrix_bindings,
)


COMPONENT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]
MATRIX_PATH = COMPONENT_ROOT / "data" / "EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2.json"
HASH_PATH = MATRIX_PATH.with_suffix(".sha256")


def main() -> int:
    matrix = load_coverage_matrix(MATRIX_PATH)
    result = validate_coverage_matrix_bindings(matrix, REPOSITORY_ROOT)
    digest = coverage_matrix_hash(matrix)
    expected = HASH_PATH.read_text(encoding="ascii").strip().split()[0]
    if digest != expected:
        raise ValueError("canonical content hash mismatch")
    print(
        json.dumps(
            {
                **result,
                "CANONICAL_CONTENT_SHA256": digest,
                "SOURCE_ARTIFACT_COUNT": len(matrix.source_inventory),
                "SEMANTIC_UNIT_COUNT": len(matrix.semantic_units),
                "PR202_IMPORT_OR_MODIFICATION": "NONE",
                "ENGINEERING_PASS": True,
                "SCIENTIFIC_VALIDATION": False,
                "SUBJECTIVITY": "NOT_ESTABLISHED",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
