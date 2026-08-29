from __future__ import annotations

from dataclasses import dataclass

from aion_bounded_research_loop import BOUNDARY


@dataclass(frozen=True, slots=True)
class ExistingLoopContract:
    """Auditable seam to the repository's established bounded research loop."""

    owner_module: str
    contract: tuple[str, ...]
    canonical_effect: str
    deployment: bool
    autonomous_merge: bool
    autonomous_repository_writeback: bool


def existing_loop_contract() -> ExistingLoopContract:
    """Reuse and verify the established loop boundary without copying its ontology."""

    contract = BOUNDARY.as_contract()
    required = {
        "CANONICAL_EFFECT = NONE",
        "DEPLOYMENT = FALSE",
        "AUTONOMOUS_MERGE = NO",
        "AUTONOMOUS_REPOSITORY_WRITEBACK = NO",
    }
    if not required.issubset(contract):
        raise ValueError("existing bounded-loop authority contract is incomplete")
    return ExistingLoopContract(
        owner_module="aion_bounded_research_loop",
        contract=contract,
        canonical_effect=BOUNDARY.canonical_effect,
        deployment=BOUNDARY.deployment,
        autonomous_merge=BOUNDARY.autonomous_merge,
        autonomous_repository_writeback=BOUNDARY.autonomous_repository_writeback,
    )
