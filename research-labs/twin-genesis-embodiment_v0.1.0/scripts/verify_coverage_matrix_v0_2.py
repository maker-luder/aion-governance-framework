"""Verify Phase A v0.2 semantic coverage and exact Git bindings."""

from __future__ import annotations

import json
from pathlib import Path

from aion_astra_twin_embodiment.coverage_matrix import (
    coverage_matrix_hash,
    load_coverage_matrix,
    validate_coverage_matrix_bindings,
)
from aion_astra_twin_embodiment.materialization_map import (
    load_materialization_map,
    materialization_map_gate_counts,
    materialization_map_hash,
    validate_materialization_map_bindings,
)


COMPONENT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]
MATRIX_PATH = COMPONENT_ROOT / "data" / "EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2.json"
HASH_PATH = MATRIX_PATH.with_suffix(".sha256")
MATERIALIZATION_PATH = (
    COMPONENT_ROOT / "data" / "EMBODIMENT_MATERIALIZATION_MAP_v0.1.json"
)
MATERIALIZATION_HASH_PATH = MATERIALIZATION_PATH.with_suffix(".sha256")


def main() -> int:
    matrix = load_coverage_matrix(MATRIX_PATH)
    result = validate_coverage_matrix_bindings(matrix, REPOSITORY_ROOT)
    digest = coverage_matrix_hash(matrix)
    expected = HASH_PATH.read_text(encoding="ascii").strip().split()[0]
    if digest != expected:
        raise ValueError("canonical content hash mismatch")
    materialization = load_materialization_map(MATERIALIZATION_PATH)
    materialization_result = validate_materialization_map_bindings(
        materialization, matrix, REPOSITORY_ROOT
    )
    materialization_digest = materialization_map_hash(materialization)
    expected_materialization = MATERIALIZATION_HASH_PATH.read_text(
        encoding="ascii"
    ).strip().split()[0]
    if materialization_digest != expected_materialization:
        raise ValueError("materialization map canonical content hash mismatch")
    materialization_counts = materialization_map_gate_counts(materialization)
    print(
        json.dumps(
            {
                **result,
                "CANONICAL_CONTENT_SHA256": digest,
                "SOURCE_ARTIFACT_COUNT": len(matrix.source_inventory),
                "SEMANTIC_UNIT_COUNT": len(matrix.semantic_units),
                "MATERIALIZATION_MAP_SHA256": materialization_digest,
                "MATERIALIZATION_SEMANTIC_UNIT_COUNT": materialization_counts[
                    "SEMANTIC_UNIT_COUNT"
                ],
                "IMPLEMENT_EXISTING_TARGET_COUNT": materialization_counts[
                    "IMPLEMENT_EXISTING_TARGET_COUNT"
                ],
                "EXTEND_EXISTING_TARGET_COUNT": materialization_counts[
                    "EXTEND_EXISTING_TARGET_COUNT"
                ],
                "KEEP_DEFERRED_COUNT": materialization_counts[
                    "KEEP_DEFERRED_COUNT"
                ],
                "PHASE_B_SUPERSEDED_COUNT": materialization_counts[
                    "SUPERSEDED_COUNT"
                ],
                "ARCHIVE_ONLY_MATERIALIZATION_COUNT": materialization_counts[
                    "ARCHIVE_ONLY_COUNT"
                ],
                "NEEDS_NEW_TARGET_COUNT": materialization_counts[
                    "NEEDS_NEW_TARGET_COUNT"
                ],
                "ACTIVE_VERIFIED_COUNT": materialization_counts[
                    "ACTIVE_VERIFIED_COUNT"
                ],
                "MISSING_MATERIALIZATION_DECISION_COUNT": materialization_result[
                    "MISSING_MATERIALIZATION_DECISION_COUNT"
                ],
                "DUPLICATE_ACTIVE_OWNERSHIP_COUNT": materialization_result[
                    "DUPLICATE_ACTIVE_OWNERSHIP_COUNT"
                ],
                "PR202_ADMISSION_DECISION": "KEEP_DEFERRED",
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
