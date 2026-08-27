from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEROP_SRC = ROOT / "components/aion_evidence_interop_v0.1.0/src"


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _function_signature(relative: str, name: str) -> tuple[list[str], str]:
    tree = ast.parse(_read(relative))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
    args = [argument.arg for argument in [*function.args.posonlyargs, *function.args.args]]
    args.extend(argument.arg for argument in function.args.kwonlyargs)
    return args, ast.unparse(function.returns)


def test_external_usability_documents_are_linked_and_preserve_boundaries() -> None:
    required = {
        "README.md": ("docs/INSTALLATION.md", "docs/QUICKSTART.md", "docs/API.md", "docs/INTEROPERABILITY.md"),
        "docs/QUICKSTART.md": ("CLI_STDOUT != INTEROP_MANIFEST_BOUNDARIES", "subjectivity_conclusion = NOT_ESTABLISHED"),
        "docs/API.md": ("dict[str, bytes]", "tuple[dict[str, Any], SourceValidation]", "PUBLIC_API != STABILITY_GUARANTEE"),
        "docs/EXAMPLES.md": ("evidence_interop_export.py",),
        "docs/INTEROPERABILITY.md": ("REFERENCE_INTEGRATION != NATIVE_IMPLEMENTATION", "CANONICAL_EFFECT = NONE"),
        "docs/RELEASE_READINESS.md": ("RELEASE_READY = FALSE", "RELEASE != SCIENTIFIC_VALIDATION"),
        "CONTRIBUTING.md": ("CONTRIBUTOR_CAN_PROPOSE_CHANGE = TRUE", "CONTRIBUTOR_CAN_SELF_AUTHORIZE_MAIN = FALSE"),
    }
    for relative, markers in required.items():
        text = _read(relative)
        for marker in markers:
            assert marker in text, f"{relative} missing {marker}"


def test_documented_public_signatures_match_implementation() -> None:
    build_args, build_return = _function_signature("components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/manifest.py", "build_bundle")
    source_args, source_return = _function_signature("components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/canonical.py", "validate_source_record")
    api = _read("docs/API.md")
    assert build_args == ["root", "record_path", "expected_head"]
    assert build_return == "dict[str, bytes]"
    assert source_args == ["root", "record_path", "expected_head"]
    assert source_return == "tuple[dict[str, Any], SourceValidation]"
    assert "build_bundle(root, record_path, *, expected_head)" in api
    assert "validate_source_record(root, record_path, *, expected_head)" in api
    assert build_return in api
    assert source_return in api


def test_standalone_example_executes_and_prints_manifest() -> None:
    env = {**__import__("os").environ, "PYTHONPATH": str(INTEROP_SRC)}
    result = subprocess.run(
        [sys.executable, "examples/evidence_interop_export.py", "--root", "."],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    manifest = json.loads(result.stdout)
    assert manifest["boundaries"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert manifest["boundaries"]["canonical_effect"] == "NONE"


def test_public_interop_contract_is_backed_by_existing_component_schema() -> None:
    schema = ROOT / "components/aion_evidence_interop_v0.1.0/schemas/interop_manifest_v0.1.0.schema.json"
    assert schema.is_file()
    assert "canonical_effect" in schema.read_text(encoding="utf-8")
