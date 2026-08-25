from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .canonical import InteropError

_HEX_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
_USES_LINE = re.compile(r"^\s*(?:-\s*)?uses\s*:\s*(?P<target>.*?)\s*$")
STATUS_VOCABULARY = (
    "EXTERNAL_VERIFICATION_REQUIRED",
    "INTENTIONALLY_DISABLED",
    "LOCAL_EVIDENCE_MISSING",
    "LOCAL_EVIDENCE_PRESENT",
    "OUT_OF_SCOPE_FROZEN",
)


def _confined_file(root: Path, relative: str) -> Path | None:
    path = root / relative
    if not path.exists() and not path.is_symlink():
        return None
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise InteropError(
            f"repository evidence path escapes repository root: {relative}",
            category="path_confinement_failure",
        ) from exc
    if not resolved.is_file():
        return None
    return resolved


def _read_text(root: Path, relative: str) -> str:
    path = _confined_file(root, relative)
    if path is None:
        return ""
    return path.read_text(encoding="utf-8")


def _workflow_action_pinning(root: Path) -> dict[str, Any]:
    workflows = root / ".github" / "workflows"
    action_uses: list[dict[str, Any]] = []
    mutable: list[dict[str, Any]] = []
    if not workflows.is_dir():
        return {
            "workflow_count": 0,
            "external_action_uses": 0,
            "sha_pinned_external_action_uses": 0,
            "mutable_external_action_uses": [],
        }

    paths = sorted(
        list(workflows.glob("*.yml")) + list(workflows.glob("*.yaml")),
        key=lambda item: item.as_posix(),
    )
    for path in paths:
        relative = path.relative_to(root).as_posix()
        confined = _confined_file(root, relative)
        if confined is None:
            continue
        for line_number, line in enumerate(confined.read_text(encoding="utf-8").splitlines(), 1):
            match = _USES_LINE.match(line)
            if match is None:
                continue
            target = match.group("target").split("#", 1)[0].strip().strip("\"'")
            if target.startswith("./") or "://" in target:
                continue
            entry = {
                "workflow": relative,
                "line": line_number,
                "uses": target,
            }
            action_uses.append(entry)
            if "@" not in target:
                mutable.append(entry)
                continue
            ref = target.rsplit("@", 1)[1]
            if not _HEX_SHA.fullmatch(ref):
                mutable.append(entry)

    return {
        "workflow_count": len(paths),
        "external_action_uses": len(action_uses),
        "sha_pinned_external_action_uses": len(action_uses) - len(mutable),
        "mutable_external_action_uses": mutable,
    }


def _check(
    check_id: str,
    status: str,
    *,
    evidence_refs: list[str] | None = None,
    note: str,
) -> dict[str, Any]:
    if status not in STATUS_VOCABULARY:
        raise ValueError(f"unknown Scorecard crosswalk status: {status}")
    return {
        "check": check_id,
        "status": status,
        "evidence_refs": sorted(evidence_refs or []),
        "note": note,
    }


def export_scorecard_crosswalk(root: Path, expected_head: str) -> dict[str, Any]:
    """Build a deterministic local-evidence crosswalk for selected Scorecard checks.

    This deliberately does not execute OpenSSF Scorecard and must not be interpreted
    as a Scorecard score, security certification, or substitute for GitHub-hosted
    repository state checks.
    """

    root = root.resolve()
    security = _confined_file(root, "SECURITY.md") is not None
    quality_ref = next(
        (
            name
            for name in (".github/workflows/quality.yml", ".github/workflows/quality.yaml")
            if _confined_file(root, name) is not None
        ),
        None,
    )
    codeql_ref = next(
        (
            name
            for name in (".github/workflows/codeql.yml", ".github/workflows/codeql.yaml")
            if _confined_file(root, name) is not None
        ),
        None,
    )
    dependabot_ref = next(
        (
            name
            for name in (".github/dependabot.yml", ".github/dependabot.yaml")
            if _confined_file(root, name) is not None
        ),
        None,
    )
    quality = quality_ref is not None
    codeql = codeql_ref is not None
    dependabot = dependabot_ref is not None
    readme = _read_text(root, "README.md")
    frozen = (
        "PROJECT_WORK_LOOP = TERMINATED" in readme
        and "ACTIVE_ENGINEERING = NO" in readme
    )
    upstream_tracking_disabled = "NEW_UPSTREAM_TRACKING = NO" in readme
    pinning = _workflow_action_pinning(root)
    all_external_actions_sha_pinned = (
        pinning["external_action_uses"] > 0
        and not pinning["mutable_external_action_uses"]
    )

    checks = [
        _check(
            "Security-Policy",
            "LOCAL_EVIDENCE_PRESENT" if security else "LOCAL_EVIDENCE_MISSING",
            evidence_refs=["SECURITY.md"] if security else [],
            note="Local security reporting policy is present; this is not a security certification.",
        ),
        _check(
            "CI-Tests",
            "LOCAL_EVIDENCE_PRESENT" if quality else "LOCAL_EVIDENCE_MISSING",
            evidence_refs=[quality_ref] if quality_ref else [],
            note="Repository-native Quality CI exists; this crosswalk does not reproduce the upstream Scorecard heuristic.",
        ),
        _check(
            "SAST",
            "LOCAL_EVIDENCE_PRESENT" if codeql else "LOCAL_EVIDENCE_MISSING",
            evidence_refs=[codeql_ref] if codeql_ref else [],
            note="CodeQL workflow presence is local evidence only; scan success must be verified on the target ref.",
        ),
        _check(
            "Pinned-Dependencies",
            "LOCAL_EVIDENCE_PRESENT" if all_external_actions_sha_pinned else "LOCAL_EVIDENCE_MISSING",
            evidence_refs=[".github/workflows"] if pinning["workflow_count"] else [],
            note="This local check covers GitHub Actions uses-references only, not the full OpenSSF dependency heuristic.",
        ),
        _check(
            "Token-Permissions",
            "EXTERNAL_VERIFICATION_REQUIRED",
            evidence_refs=[
                ref
                for ref in [
                    quality_ref or "",
                    codeql_ref or "",
                ]
                if ref
            ],
            note="Representative workflows declare permissions, but effective token privilege requires workflow-level external evaluation.",
        ),
        _check(
            "Branch-Protection",
            "EXTERNAL_VERIFICATION_REQUIRED",
            note="Rulesets and branch-protection state are hosted GitHub configuration and are not inferred from repository files.",
        ),
        _check(
            "Code-Review",
            "EXTERNAL_VERIFICATION_REQUIRED",
            note="Required-review and merge-policy state must be checked from GitHub configuration and PR history.",
        ),
        _check(
            "Dangerous-Workflow",
            "EXTERNAL_VERIFICATION_REQUIRED",
            evidence_refs=[".github/workflows"] if pinning["workflow_count"] else [],
            note="This profile does not claim to reimplement the OpenSSF dangerous-workflow analyzer.",
        ),
        _check(
            "Vulnerabilities",
            "EXTERNAL_VERIFICATION_REQUIRED",
            note="Repository vulnerability alerts and advisory state are external GitHub security data.",
        ),
        _check(
            "Dependency-Update-Tool",
            (
                "LOCAL_EVIDENCE_PRESENT"
                if dependabot
                else "INTENTIONALLY_DISABLED"
                if frozen and upstream_tracking_disabled
                else "LOCAL_EVIDENCE_MISSING"
            ),
            evidence_refs=[dependabot_ref] if dependabot_ref else ["README.md"] if frozen else [],
            note=(
                "Dependabot configuration is present."
                if dependabot
                else "Automatic upstream tracking is intentionally disabled by the preserved-project boundary."
                if frozen and upstream_tracking_disabled
                else "No dependency-update configuration was found."
            ),
        ),
        _check(
            "Maintained",
            "OUT_OF_SCOPE_FROZEN" if frozen else "EXTERNAL_VERIFICATION_REQUIRED",
            evidence_refs=["README.md"] if frozen else [],
            note="A preserved historical checkpoint is intentionally not scored here as an actively maintained product.",
        ),
    ]

    return {
        "schema_version": "0.1.0",
        "profile": "OPENSSF_SCORECARD_CROSSWALK_ONLY",
        "expected_head": expected_head,
        "openssf_scorecard_executed": False,
        "score": None,
        "scope": "SELECTED_REPOSITORY_HYGIENE_CHECKS",
        "status_vocabulary": list(STATUS_VOCABULARY),
        "pinning_summary": pinning,
        "checks": checks,
        "boundaries": {
            "canonical_effect": "NONE",
            "deployment": False,
            "security_certification": "NOT_ESTABLISHED",
            "independent_ivv": "NOT_ACHIEVED",
        },
    }
