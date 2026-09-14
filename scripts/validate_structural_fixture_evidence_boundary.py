from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DETERMINISTIC_MODE = "DETERMINISTIC_SYNTHETIC_FIXTURE"
STRUCTURAL_QA = "STRUCTURAL_QA"
RESEARCH_EVIDENCE = "RESEARCH_EVIDENCE"
ALLOWED_ROLES = frozenset({STRUCTURAL_QA, RESEARCH_EVIDENCE})


@dataclass(frozen=True, slots=True)
class StructuralFixtureBoundaryResult:
    status: str
    requested_role: str
    diagnostics: tuple[str, ...]
    evidence_admissibility: str
    mutation_performed: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "requested_role": self.requested_role,
            "diagnostics": list(self.diagnostics),
            "evidence_admissibility": self.evidence_admissibility,
            "mutation_performed": self.mutation_performed,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }


def assess_receipt(
    receipt: Any,
    *,
    requested_role: str,
) -> StructuralFixtureBoundaryResult:
    """Keep deterministic no-model fixtures on the structural-QA side of evidence admission."""
    if requested_role not in ALLOWED_ROLES:
        return StructuralFixtureBoundaryResult(
            "HOLD",
            requested_role,
            ("requested_role is outside the bounded admission vocabulary",),
            "NOT_ASSESSED",
        )
    if not isinstance(receipt, dict):
        return StructuralFixtureBoundaryResult(
            "HOLD",
            requested_role,
            ("receipt must be a JSON object",),
            "NOT_ASSESSED",
        )
    if receipt.get("mode") != DETERMINISTIC_MODE:
        return StructuralFixtureBoundaryResult(
            "HOLD",
            requested_role,
            ("receipt is outside the deterministic synthetic fixture boundary",),
            "NOT_ASSESSED",
        )

    diagnostics: list[str] = []
    required_boundaries = {
        "model_invoked": False,
        "empirical_result": "SYNTHETIC_FIXTURE_ONLY",
        "causal_identification": "NOT_ESTABLISHED",
        "population_generalization": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "scientific_disposition": "HOLD",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    for key, expected in required_boundaries.items():
        if receipt.get(key) != expected:
            diagnostics.append(f"{key} must equal {expected!r} for deterministic structural fixtures")

    if requested_role == RESEARCH_EVIDENCE:
        diagnostics.append(
            "deterministic no-model fixture output is structural QA only and cannot be "
            "admitted as empirical research evidence"
        )

    status = "PASS" if not diagnostics else "FAIL"
    admissibility = "STRUCTURAL_QA_ONLY" if status == "PASS" else "NOT_ADMISSIBLE_AS_REQUESTED"
    return StructuralFixtureBoundaryResult(
        status,
        requested_role,
        tuple(diagnostics),
        admissibility,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail closed when deterministic structural fixtures are requested as research evidence"
    )
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--requested-role", choices=sorted(ALLOWED_ROLES), required=True)
    args = parser.parse_args(argv)
    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = StructuralFixtureBoundaryResult(
            "HOLD",
            args.requested_role,
            (f"receipt is unavailable or invalid: {type(exc).__name__}",),
            "NOT_ASSESSED",
        )
    else:
        result = assess_receipt(receipt, requested_role=args.requested_role)
    print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
    return 0 if result.status == "PASS" else 2 if result.status == "FAIL" else 10


if __name__ == "__main__":
    raise SystemExit(main())
