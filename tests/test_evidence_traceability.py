from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_evidence_traceability as generator  # noqa: E402


def write_index(root: Path, implementation_ref: str = "components/example") -> None:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (root / "qa").mkdir(parents=True, exist_ok=True)
    (root / "qa" / "evidence.json").write_text("{}\n", encoding="utf-8")
    (root / "tests").mkdir(parents=True, exist_ok=True)
    (root / "tests" / "test_example.py").write_text("def test_example(): pass\n", encoding="utf-8")
    (docs / "C0_ACCEPTANCE_EVIDENCE_INDEX_2026-08-08.md").write_text(
        "\n".join(
            [
                "| Criterion | Requirement | Implementation | Test | Evidence | State | Limitation |",
                "|---|---|---|---|---|---|---|",
                f"| `AC-SCOPE-01` | requirement | `{implementation_ref}` | `tests/test_example.py` | `qa/evidence.json` | AVAILABLE | structural only |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_traceability_report_passes_with_existing_local_reference(tmp_path: Path) -> None:
    (tmp_path / "components" / "example").mkdir(parents=True)
    write_index(tmp_path)
    report = generator.build_report(tmp_path, target_head="abc123")
    assert report["status"] == "PASS"
    assert report["criterion_count"] == 1
    assert report["target_head"] == "abc123"
    assert report["acceptance_decision"] == "NOT_EVALUATED"
    assert report["canonical_effect"] == "NONE"
    assert report["deployment"] is False
    assert report["independent_ivv"] == "NOT_ACHIEVED"
    assert report["mutation_performed"] is False


def test_traceability_report_holds_for_missing_local_reference(tmp_path: Path) -> None:
    write_index(tmp_path, implementation_ref="components/missing")
    report = generator.build_report(tmp_path, target_head="abc123")
    assert report["status"] == "HOLD"
    assert report["diagnostics"]["missing_local_refs"] == ["components/missing"]


def test_parse_index_ignores_non_acceptance_tables(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    (docs / "C0_ACCEPTANCE_EVIDENCE_INDEX_2026-08-08.md").write_text(
        "| Header | Other |\n|---|---|\n| not-a-criterion | x |\n", encoding="utf-8"
    )
    assert generator.parse_index(tmp_path) == ()
