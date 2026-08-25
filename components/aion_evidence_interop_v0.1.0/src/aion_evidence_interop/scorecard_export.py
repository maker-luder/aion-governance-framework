from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_HEX_SHA = re.compile(r"^[0-9a-fA-F]{40}$")


def _read_text(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
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

    paths = sorted(list(workflows.glob("*.yml")) + list(workflows.glob("*.yaml")))
    for path in paths:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if not stripped.startswith("uses:"):
                continue
            target = stripped.split(":", 1)[1].split("#", 1)[0].strip().strip("\"'")
            if target.startswith("./"):
                continue
            entry = {
                "workflow": path.relative_to(root).as_posix(),
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
    security = (root / "SECURITY.md").is_file()
    quality = (root / ".github/workflows/quality.yml").is_file()
    codeql = (root / ".github/workflows/codeql.yml").is_file()
    dependabot = (root / ".github/dependabot.yml").is_file() or (
        root / ".github/dependabot.yaml"
    ).is_file()
    readme = _read_text(root, "README.md")
    frozen = "PROJECT_WORK_LOOP = TERMINATED" in readme or "ACTIVE_ENGINEERING = NO" in readme
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
            evidence_refs=[".github/workflows/quality.yml"] if quality else [],
            note="Repository-native Quality CI exists; this crosswalk does not reproduce the upstream Scorecard heuristic.",
        ),
        _check(
            "SAST",
            "LOCAL_EVIDENCE_PRESENT" if codeql else "LOCAL_EVIDENCE_MISSING",
            evidence_refs=[".github/workflows/codeql.yml"] if codeql else [],
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
                    ".github/workflows/quality.yml" if quality else "",
                    ".github/workflows/codeql.yml" if codeql else "",
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
            evidence_refs=[".github/dependabot.yml"] if dependabot else ["README.md"] if frozen else [],
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
        "pinning_summary": pinning,
        "checks": checks,
        "boundaries": {
            "canonical_effect": "NONE",
            "deployment": False,
            "security_certification": "NOT_ESTABLISHED",
            "independent_ivv": "NOT_ACHIEVED",
        },
    }
