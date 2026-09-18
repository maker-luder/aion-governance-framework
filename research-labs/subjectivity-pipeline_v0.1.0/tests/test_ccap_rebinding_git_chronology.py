from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
BOUNDARY_PATH = "docs/research/CCAP_ASSESSMENT_SYSTEM_BOUNDARY_2026_09_18.md"
REBINDING_PATH = "docs/research/CCAP_PROSPECTIVE_DIMENSION_REBINDING_2026_09_18.md"
BOUNDARY_SEMANTICS_COMMIT = "1637ec057f60a868a85bfac1f26f002398bd5bf8"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ("git", *args),
        cwd=REPO_ROOT,
        check=check,
        text=True,
        capture_output=True,
    )


def introducing_commit(path: str) -> str:
    result = git("log", "--diff-filter=A", "--format=%H", "--", path)
    commits = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    assert commits, f"no introducing commit found for {path}"
    return commits[-1]


def test_corrected_system_boundary_exists_at_declared_semantics_commit() -> None:
    git("cat-file", "-e", f"{BOUNDARY_SEMANTICS_COMMIT}:{BOUNDARY_PATH}")
    content = git("show", f"{BOUNDARY_SEMANTICS_COMMIT}:{BOUNDARY_PATH}").stdout

    assert "HISTORICAL_PRE_INDICATOR_INDIVIDUATION = NOT_ACHIEVED" in content
    assert "BOUNDARY_FIXED_FOR_FUTURE_REBINDING = TRUE" in content


def test_boundary_semantics_commit_precedes_prospective_rebinding_commit() -> None:
    rebinding_commit = introducing_commit(REBINDING_PATH)

    result = git(
        "merge-base",
        "--is-ancestor",
        BOUNDARY_SEMANTICS_COMMIT,
        rebinding_commit,
        check=False,
    )

    assert result.returncode == 0
    assert rebinding_commit != BOUNDARY_SEMANTICS_COMMIT


def test_prospective_rebinding_artifact_did_not_exist_before_its_intro_commit() -> None:
    rebinding_commit = introducing_commit(REBINDING_PATH)

    prior = git(
        "cat-file",
        "-e",
        f"{rebinding_commit}^:{REBINDING_PATH}",
        check=False,
    )

    assert prior.returncode != 0


def test_rebinding_manifest_preserves_historical_hold_and_future_only_promotion() -> None:
    content = (REPO_ROOT / REBINDING_PATH).read_text(encoding="utf-8")

    assert "BOUNDARY_PRECEDES_THIS_REBINDING = MUST_BE_VERIFIED_FROM_GIT_HISTORY" in content
    assert "GIT_ANCESTRY = TEMPORAL_BINDING_EVIDENCE" in content
    assert "PROSPECTIVE_REBINDING_READY != EMPIRICAL_SEPARABILITY" in content
    assert "D2 is not promoted into direct CCAP relevance by this manifest." in content
