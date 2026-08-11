from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "research-workbench" / "four-domain-materialization" / "2026-08-11" / "RESEARCH_SCOPE_LOCK_2026-08-11.json"
CHARTER = ROOT / "research-workbench" / "four-domain-materialization" / "2026-08-10" / "RESEARCH_BRANCH_FREE_GROWTH_CHARTER.md"

REQUIRED_TOP_LEVEL = {
    "branch": "review/four-domain-research-materialization",
    "research_object": "POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY",
    "subjectivity_conclusion": "NOT_ESTABLISHED",
    "consciousness_conclusion": "NOT_ESTABLISHED",
    "identity_continuity_conclusion": "NOT_ESTABLISHED",
    "main_effect": "NONE",
    "canonical_effect": "NONE",
}

REQUIRED_ROLES = {
    "HYPOTHESIS",
    "MEASUREMENT",
    "FALSIFIER",
    "EXPERIMENTAL_SUBSTRATE",
    "ENABLING_ONLY",
}

REQUIRED_BLOCKS = {
    "ENGINEERING_ARTIFACT_COUNTED_AS_SUBJECTIVITY_EVIDENCE",
    "TEST_PASS_PROMOTED_TO_ONTOLOGY_CLAIM",
    "RUNTIME_EXPANSION_WITHOUT_SUBJECTIVITY_RESEARCH_LINK",
    "DEPLOYMENT_OR_SERVICE_MATURITY_TREATED_AS_SUBJECTIVITY_PROGRESS",
    "MEMORY_OR_CONTINUITY_BEHAVIOR_TREATED_AS_IDENTITY_OR_SUBJECTIVITY_PROOF",
    "UNREVIEWED_MAIN_GOVERNANCE_DELTA_BEFORE_MAJOR_FEATURE_GROWTH",
}


def fail(message: str) -> None:
    raise SystemExit(f"research scope lock failed: {message}")


def main() -> None:
    if not LOCK.is_file():
        fail(f"missing {LOCK.relative_to(ROOT)}")

    data = json.loads(LOCK.read_text(encoding="utf-8"))

    for key, expected in REQUIRED_TOP_LEVEL.items():
        if data.get(key) != expected:
            fail(f"{key}={data.get(key)!r}, expected {expected!r}")

    roles = set(data.get("allowed_epistemic_roles", []))
    if roles != REQUIRED_ROLES:
        fail(f"allowed_epistemic_roles={sorted(roles)!r}")

    runtime = data.get("runtime", {})
    if runtime.get("epistemic_role") != "EXPERIMENTAL_SUBSTRATE":
        fail("AION Runtime must remain EXPERIMENTAL_SUBSTRATE")
    if runtime.get("is_subjectivity_evidence") is not False:
        fail("AION Runtime cannot be counted as subjectivity evidence")
    if runtime.get("unlinked_expansion") != "PROHIBITED":
        fail("unlinked Runtime expansion must be PROHIBITED")

    engineering = data.get("engineering", {})
    if engineering.get("artifacts_are_subjectivity_evidence") is not False:
        fail("engineering artifacts cannot become subjectivity evidence by implementation alone")
    if engineering.get("test_pass_is_theory_confirmation") is not False:
        fail("test pass cannot become theory confirmation")

    growth = data.get("growth_gate", {})
    if growth.get("new_major_module_requires_subjectivity_research_link") is not True:
        fail("major modules require an explicit subjectivity-research link")
    if growth.get("engineering_only_growth_without_research_link") != "HOLD":
        fail("unlinked engineering-only growth must HOLD")
    if growth.get("enabling_only_may_accumulate_as_subjectivity_evidence") is not False:
        fail("ENABLING_ONLY work cannot accumulate as subjectivity evidence")

    blocks = set(data.get("blocking_conditions", []))
    missing = REQUIRED_BLOCKS - blocks
    if missing:
        fail(f"missing blocking conditions: {sorted(missing)!r}")

    sync = data.get("main_compatibility", {})
    if sync.get("reviewed_main_head") != "0a93eaeaba23047f4b21f0904ae67ff7ee8d8d1f":
        fail("reviewed main head changed without updating the scope review")
    if sync.get("sync_mode") != "SELECTIVE_GOVERNANCE_MERGE":
        fail("main compatibility sync mode changed")

    charter = CHARTER.read_text(encoding="utf-8")
    required_charter_phrases = (
        "RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY",
        "FREE_GROWTH != UNBOUNDED_ENGINEERING_GROWTH",
        "ENGINEERING_ARTIFACTS != SUBJECTIVITY_EVIDENCE",
        "UNLINKED_ENGINEERING_GROWTH = HOLD",
    )
    for phrase in required_charter_phrases:
        if phrase not in charter:
            fail(f"charter missing invariant: {phrase}")

    print("research scope lock: PASS")


if __name__ == "__main__":
    main()
