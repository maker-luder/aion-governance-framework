from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
LANGUAGE_SPEC = ROOT / "language-spec"
MANIFEST_SCHEMA_PATH = LANGUAGE_SPEC / "conformance" / "aion_native_conformance_manifest_v0.1.0.schema.json"
MANIFEST_PATH = LANGUAGE_SPEC / "conformance" / "aion_native_conformance_manifest_v0.1.0.json"
IR_SCHEMA_PATH = LANGUAGE_SPEC / "aion_native_ir_v0.1.0.schema.json"
NEGATIVE_SCHEMA_PATH = LANGUAGE_SPEC / "conformance" / "aion_native_negative_vectors_v0.1.0.schema.json"
NEGATIVE_VECTORS_PATH = LANGUAGE_SPEC / "conformance" / "aion_native_ir_v0.1.0.negative_vectors.json"
ERROR_MAPPING_SCHEMA_PATH = LANGUAGE_SPEC / "conformance" / "aion_native_error_mapping_v0.1.0.schema.json"
ERROR_MAPPING_PATH = LANGUAGE_SPEC / "conformance" / "aion_native_error_mapping_v0.1.0.json"
ERROR_ENVELOPE_SCHEMA_PATH = ROOT / "schemas" / "aion_error_envelope_v0.1.0.schema.json"
VALID_IR_PATH = LANGUAGE_SPEC / "conformance" / "aion_native_ir_v0.1.0.valid.json"
GRAMMAR_PATH = LANGUAGE_SPEC / "aion_native_language_v0.1.0.ebnf"

BANNED_RESULT_FIELDS = {
    "approval_satisfied",
    "capability_granted",
    "identity_bound",
    "runtime_admitted",
    "state_mutated",
    "event_committed",
    "event_hash",
    "event_predecessor",
    "execution_result",
    "canonical_write",
}
BANNED_SOURCE_TOKENS = {
    "approval_satisfied",
    "capability_granted",
    "owner_approved",
    "execute_aion",
    "eval_aion",
    "run_program",
    "canonical_effect: write",
}


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _validator(path: Path) -> Draft202012Validator:
    schema = _json(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _relative_manifest_paths(manifest: dict[str, Any]) -> list[str]:
    paths = [
        manifest["grammar"],
        manifest["ir_schema"],
        manifest["negative_ir_fixture"],
        manifest["negative_ir_schema"],
        manifest["error_mapping"],
        manifest["error_mapping_schema"],
    ]
    paths.extend(manifest["accepted_source_examples"])
    paths.extend(item["path"] for item in manifest["rejected_source_examples"])
    paths.extend(manifest["positive_ir_fixtures"])
    return paths


def _static_ir_codes(document: dict[str, Any]) -> list[str]:
    declarations = document["declarations"]
    codes: list[str] = []
    local_names: set[str] = set()
    runtimes: dict[str, dict[str, Any]] = {}

    if document.get("canonical_effect") != "NONE":
        codes.append("INVALID_EFFECT")

    for declaration in declarations:
        local_name = declaration.get("local_name")
        if local_name in local_names:
            codes.append("DUPLICATE_DECLARATION")
        local_names.add(local_name)
        if declaration.get("declaration_type") == "runtime":
            runtimes[local_name] = declaration
        if any(field in declaration for field in BANNED_RESULT_FIELDS):
            codes.append("AUTHORITY_REQUIRED")

    for declaration in declarations:
        declaration_type = declaration.get("declaration_type")
        if declaration_type == "memory_namespace":
            owner_name = declaration["owner_runtime"]
            owner = runtimes.get(owner_name)
            if owner is None:
                codes.append("UNKNOWN_SYMBOL")
            elif owner["runtime_kind"] != declaration["namespace_kind"]:
                codes.append("IDENTITY_MISMATCH")
        elif declaration_type in {"lifecycle_requirement", "operation_requirement"}:
            runtime_name = declaration["runtime"]
            if runtime_name not in runtimes:
                codes.append("UNKNOWN_SYMBOL")

            requirements = declaration.get("requirements", {})
            has_approval = "approval_requirements" in requirements
            has_capability = "capability_requirements" in requirements
            if declaration_type == "lifecycle_requirement":
                expected_effect = (
                    "APPROVAL_REQUIRED_REQUEST"
                    if has_approval
                    else "CAPABILITY_REQUIRED_REQUEST"
                    if has_capability
                    else "RUNTIME_MUTATION_REQUEST"
                )
            elif declaration["operation_kind"] == "provisional_reference":
                expected_effect = "PROVISIONAL_UNEXECUTABLE"
            elif has_approval:
                expected_effect = "APPROVAL_REQUIRED_REQUEST"
            elif has_capability:
                expected_effect = "CAPABILITY_REQUIRED_REQUEST"
            elif declaration["operation_kind"] in {"memory_read", "runtime_read"}:
                expected_effect = "RUNTIME_READ"
            else:
                expected_effect = "RUNTIME_MUTATION_REQUEST"
            if declaration["effect_class"] != expected_effect:
                codes.append("INVALID_EFFECT")

    return codes


def test_native_schema_and_manifest_are_valid() -> None:
    ir_validator = _validator(IR_SCHEMA_PATH)
    manifest_validator = _validator(MANIFEST_SCHEMA_PATH)
    negative_validator = _validator(NEGATIVE_SCHEMA_PATH)
    error_mapping_validator = _validator(ERROR_MAPPING_SCHEMA_PATH)
    manifest = _json(MANIFEST_PATH)
    negative_vectors = _json(NEGATIVE_VECTORS_PATH)
    error_mapping = _json(ERROR_MAPPING_PATH)
    error_envelope_schema = _json(ERROR_ENVELOPE_SCHEMA_PATH)

    assert list(manifest_validator.iter_errors(manifest)) == []
    assert list(negative_validator.iter_errors(negative_vectors)) == []
    assert list(error_mapping_validator.iter_errors(error_mapping)) == []
    envelope_categories = set(error_envelope_schema["properties"]["category"]["enum"])
    mapped_categories = {item["category"] for item in error_mapping["mappings"]}
    assert mapped_categories <= envelope_categories
    assert list(ir_validator.iter_errors(_json(VALID_IR_PATH))) == []


def test_manifest_paths_are_repository_local_and_complete() -> None:
    manifest = _json(MANIFEST_PATH)
    expected_paths = set(_relative_manifest_paths(manifest))
    actual_examples = {
        path.relative_to(ROOT).as_posix()
        for path in (LANGUAGE_SPEC / "examples").rglob("*.aion")
    }
    declared_examples = set(manifest["accepted_source_examples"]) | {
        item["path"] for item in manifest["rejected_source_examples"]
    }
    assert declared_examples == actual_examples

    for relative in expected_paths:
        assert not Path(relative).is_absolute()
        assert ".." not in Path(relative).parts
        assert (ROOT / relative).is_file(), relative


def test_language_spec_contains_no_executable_implementation_files() -> None:
    implementation_extensions = {".py", ".js", ".ts", ".rs", ".go", ".java", ".c", ".cc", ".cpp"}
    files = [path for path in LANGUAGE_SPEC.rglob("*") if path.is_file()]
    assert not [path for path in files if path.suffix in implementation_extensions]
    assert not [path for path in files if path.stat().st_mode & 0o111]


def test_grammar_candidate_contains_only_declared_non_executable_surface() -> None:
    grammar = GRAMMAR_PATH.read_text(encoding="utf-8")
    required_productions = {
        "Document",
        "RuntimeDeclaration",
        "ProvenanceDeclaration",
        "MemoryNamespaceDeclaration",
        "LifecycleRequirementDeclaration",
        "OperationRequirementDeclaration",
        "ApprovalRequirement",
        "CapabilityRequirement",
        "CanonicalEffectField",
    }
    production_names = set(re.findall(r"^([A-Za-z][A-Za-z0-9_]*)\s*=", grammar, flags=re.MULTILINE))
    assert required_productions <= production_names
    assert "canonical_effect" in grammar
    assert '"none"' in grammar
    assert not re.search(r"^\s*(Evaluate|Execute|Run|Call|Invoke|Tool|VM|Bytecode)\s*=", grammar, flags=re.MULTILINE)


def test_source_examples_preserve_non_executable_boundary() -> None:
    manifest = _json(MANIFEST_PATH)
    accepted = [ROOT / path for path in manifest["accepted_source_examples"]]
    rejected = [ROOT / item["path"] for item in manifest["rejected_source_examples"]]

    for path in accepted + rejected:
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), path
        text = raw.decode("utf-8")
        if path.name == "unsupported_version.aion":
            assert "language 0.2;" in text
        else:
            assert "language 0.1;" in text
        assert "canonical_effect: none;" in text or path in rejected
        assert "execute_aion" not in text
        assert "eval_aion" not in text
        assert "run_program" not in text

    accepted_text = "\n".join(path.read_text(encoding="utf-8") for path in accepted)
    assert not any(token in accepted_text for token in BANNED_SOURCE_TOKENS)
    assert "requires approval" in accepted_text
    assert "requires capability" in accepted_text

    for item in manifest["rejected_source_examples"]:
        text = (ROOT / item["path"]).read_text(encoding="utf-8")
        assert f"REJECT: {item['expected_code']}" in text


def test_positive_ir_satisfies_static_semantic_invariants() -> None:
    document = _json(VALID_IR_PATH)
    assert _static_ir_codes(document) == []
    assert document["canonical_effect"] == "NONE"
    assert all(declaration["canonical_effect"] == "NONE" for declaration in document["declarations"])


def test_negative_vectors_fail_at_declared_schema_or_semantic_layer() -> None:
    ir_validator = _validator(IR_SCHEMA_PATH)
    negative_vectors = _json(NEGATIVE_VECTORS_PATH)

    schema_count = 0
    semantic_count = 0
    for vector in negative_vectors["vectors"]:
        document = vector["document"]
        if vector["stage"] == "schema":
            schema_count += 1
            assert list(ir_validator.iter_errors(document)), vector["id"]
        else:
            semantic_count += 1
            assert list(ir_validator.iter_errors(document)) == [], vector["id"]
            assert vector["expected_code"] in _static_ir_codes(document), vector["id"]

    assert schema_count >= 5
    assert semantic_count >= 3


def test_workflows_execute_native_artifact_validation_on_relevant_changes() -> None:
    test_command = "python -m pytest -q tests/test_aion_native_language_artifacts.py"
    quality = (ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
    cross_language = (ROOT / ".github/workflows/cross-language-contract-conformance.yml").read_text(encoding="utf-8")
    runtime_strong_qa = (ROOT / ".github/workflows/runtime-strong-qa.yml").read_text(encoding="utf-8")

    assert test_command in quality
    assert test_command in cross_language
    assert test_command in runtime_strong_qa
    assert '"language-spec/**"' in cross_language
    assert '"language-spec/**"' in runtime_strong_qa
    assert '"tests/test_aion_native_language_artifacts.py"' in cross_language
    assert '"tests/test_aion_native_language_artifacts.py"' in runtime_strong_qa


def test_native_docs_preserve_authority_and_event_hash_boundaries() -> None:
    semantic = (ROOT / "docs/AION_NATIVE_LANGUAGE_SEMANTIC_MODEL_V0.1.0.md").read_text(encoding="utf-8")
    security = (ROOT / "docs/AION_NATIVE_LANGUAGE_SECURITY_MODEL_V0.1.0.md").read_text(encoding="utf-8")
    feasibility = (ROOT / "docs/AION_NATIVE_LANGUAGE_FEASIBILITY_V0.1.0.md").read_text(encoding="utf-8")
    conformance = (ROOT / "docs/AION_NATIVE_LANGUAGE_CONFORMANCE_PROFILE_V0.1.0.md").read_text(encoding="utf-8")

    for text in (semantic, security, feasibility, conformance):
        assert "canonical_effect" in text
        assert "NONE" in text
        assert "not" in text.lower()
    assert "SOURCE != AUTHORIZATION" in semantic
    assert "source `transition: start` maps to the existing request event type `runtime.started`" in semantic
    assert "source `transition: stop` maps to `runtime.stopped`" in semantic
    assert "from_state" in semantic and "event_hash" in semantic
    mapping = _json(ERROR_MAPPING_PATH)
    assert mapping["canonical_effect"] == "NONE"
    assert len(mapping["mappings"]) == 14
    assert "EVENT_HASH_BOUNDARY" in security or "Event / Lineage" in security
    assert "BLOCKED_BY_CONTRACT_GAP" in feasibility
    assert "Conformance of the feasibility artifacts is not conformance of a future parser" in conformance
