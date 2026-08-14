from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AuthoritySpec:
    framework: str
    authority_ref: str
    authority_sha: str
    packet_path: str
    schema_path: str


@dataclass(frozen=True)
class ReadOnlyAuthority:
    spec: AuthoritySpec
    packet: dict[str, Any]
    packet_sha256: str
    schema: dict[str, Any]
    schema_sha256: str
    resolved_ref: str


CSOMI_SPEC = AuthoritySpec(
    framework="CSOMI",
    authority_ref="research/cross-substrate-other-minds-inference-20260814",
    authority_sha="87405c1877c6f016c303971da13923a1ab690aae",
    packet_path="research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_PACKET_V0.1.0.json",
    schema_path="schemas/aion_csomi_packet_v0.1.0.schema.json",
)

SLSH_SPEC = AuthoritySpec(
    framework="SLSH",
    authority_ref="frozen/slsh-semantic-reconciliation-20260814",
    authority_sha="893d8dc0c1c9d8f9a4188860520143c8d1d3977b",
    packet_path="research-workbench/subjective-load-sensitivity-hypothesis-2026-08-14/SLSH_PACKET_V0.1.0.json",
    schema_path="schemas/aion_slsh_packet_v0.1.0.schema.json",
)


class AuthorityInputError(ValueError):
    """Raised when a frozen authority input cannot be resolved exactly."""


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _resolve_exact_ref(root: Path, spec: AuthoritySpec) -> tuple[str, str]:
    candidates = (
        spec.authority_sha,
        spec.authority_ref,
        f"refs/remotes/origin/{spec.authority_ref}",
        f"refs/heads/{spec.authority_ref}",
    )
    for candidate in candidates:
        try:
            resolved = _git(root, "rev-parse", f"{candidate}^{{commit}}").strip()
        except subprocess.CalledProcessError:
            continue
        if resolved == spec.authority_sha:
            return candidate, resolved
    raise AuthorityInputError(
        f"{spec.framework} authority does not resolve to pinned SHA {spec.authority_sha}"
    )


def _show_json(root: Path, resolved_ref: str, path: str) -> tuple[dict[str, Any], str]:
    raw = _git(root, "show", f"{resolved_ref}:{path}").encode("utf-8")
    try:
        value = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise AuthorityInputError(f"invalid JSON at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuthorityInputError(f"expected object JSON at {path}")
    return value, hashlib.sha256(raw).hexdigest()


def load_read_only_authority(root: Path, spec: AuthoritySpec) -> ReadOnlyAuthority:
    resolved_ref, resolved_sha = _resolve_exact_ref(root, spec)
    packet, packet_hash = _show_json(root, resolved_ref, spec.packet_path)
    schema, schema_hash = _show_json(root, resolved_ref, spec.schema_path)
    return ReadOnlyAuthority(
        spec=spec,
        packet=packet,
        packet_sha256=packet_hash,
        schema=schema,
        schema_sha256=schema_hash,
        resolved_ref=resolved_ref,
    )


def load_default_authorities(root: Path) -> tuple[ReadOnlyAuthority, ReadOnlyAuthority]:
    return (
        load_read_only_authority(root, CSOMI_SPEC),
        load_read_only_authority(root, SLSH_SPEC),
    )


def assert_authority_semantics(authority: ReadOnlyAuthority) -> None:
    packet = authority.packet
    if authority.spec.framework == "CSOMI":
        expected = {
            "packet_id": "AION_CSOMI_PACKET_V0.1.0",
            "canonical_effect": "NONE",
            "deployment": False,
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "positioning_rule": "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION",
        }
    else:
        expected = {
            "packet_id": "AION_SLSH_PACKET_V0.1.0",
            "canonical_effect": "NONE",
            "deployment": False,
            "experiment_executed": False,
            "runtime_executed": False,
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "positioning_rule": "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION",
            "functional_rule": "FUNCTIONAL_LOAD_STATE != SUBJECTIVE_LOAD",
        }
    for field, expected_value in expected.items():
        if packet.get(field) != expected_value:
            raise AuthorityInputError(
                f"{authority.spec.framework} frozen semantic mismatch: "
                f"{field}={packet.get(field)!r}"
            )
    if authority.spec.framework == "SLSH":
        interface = packet.get("csomi_interface", {})
        if interface.get("accepted_csomi_source_sha") != CSOMI_SPEC.authority_sha:
            raise AuthorityInputError("SLSH CSOMI interface does not pin the accepted CSOMI SHA")
        if interface.get("status") != "CONDITIONAL_READ_ONLY_NO_IMPLEMENTATION":
            raise AuthorityInputError("SLSH CSOMI interface is not read-only/no-implementation")
