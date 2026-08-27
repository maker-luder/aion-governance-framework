from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_external_usability_documents_are_linked_and_preserve_boundaries() -> None:
    required = {
        "README.md": ("docs/INSTALLATION.md", "docs/QUICKSTART.md", "docs/API.md", "docs/INTEROPERABILITY.md"),
        "docs/QUICKSTART.md": ("CANONICAL_EFFECT = NONE", "DEPLOYMENT = FALSE", "SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED"),
        "docs/API.md": ("SUPPORTED_PUBLIC", "EXPERIMENTAL", "PUBLIC_API != STABILITY_GUARANTEE"),
        "docs/INTEROPERABILITY.md": ("REFERENCE_INTEGRATION != NATIVE_IMPLEMENTATION", "CANONICAL_EFFECT = NONE"),
        "docs/RELEASE_READINESS.md": ("RELEASE_READY = FALSE", "RELEASE != SCIENTIFIC_VALIDATION"),
        "CONTRIBUTING.md": ("CONTRIBUTOR_CAN_PROPOSE_CHANGE = TRUE", "CONTRIBUTOR_CAN_SELF_AUTHORIZE_MAIN = FALSE"),
    }
    for relative, markers in required.items():
        text = _read(relative)
        for marker in markers:
            assert marker in text, f"{relative} missing {marker}"


def test_public_interop_contract_is_backed_by_existing_component_schema() -> None:
    schema = ROOT / "components/aion_evidence_interop_v0.1.0/schemas/interop_manifest_v0.1.0.schema.json"
    assert schema.is_file()
    assert "canonical_effect" in schema.read_text(encoding="utf-8")
