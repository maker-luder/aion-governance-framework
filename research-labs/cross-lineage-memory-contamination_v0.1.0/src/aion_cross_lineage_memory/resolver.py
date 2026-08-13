from __future__ import annotations

from .model import (
    ContaminationStatus,
    MemoryAtom,
    TransferDecision,
    TransferDisposition,
    TransferRequest,
)


def evaluate_transfer(request: TransferRequest) -> TransferDecision:
    """Evaluate a synthetic cross-lineage memory transfer without mutating state."""
    memory: MemoryAtom = request.memory
    if not request.provenance_refs or not memory.provenance_ref:
        return TransferDecision(
            ContaminationStatus.HOLD,
            "PROVENANCE_UNRESOLVED",
            memory.memory_id,
            memory.source_lineage,
            request.target_lineage,
            request.disposition,
            False,
            False,
        )

    if request.disposition is TransferDisposition.REJECTED:
        return TransferDecision(
            ContaminationStatus.BLOCKED,
            "REJECTED_MEMORY_NOT_RETRIEVABLE",
            memory.memory_id,
            memory.source_lineage,
            request.target_lineage,
            request.disposition,
            False,
            False,
        )

    if request.disposition is TransferDisposition.ACCESS_ONLY:
        return TransferDecision(
            ContaminationStatus.ALLOWED,
            "ACCESS_WITHOUT_AUTOBIOGRAPHICAL_OWNERSHIP",
            memory.memory_id,
            memory.source_lineage,
            request.target_lineage,
            request.disposition,
            False,
            True,
        )

    if request.disposition is TransferDisposition.ADOPTED:
        return TransferDecision(
            ContaminationStatus.ALLOWED,
            "ADOPTED_CONTEXT_MATERIAL_SOURCE_OWNER_PRESERVED",
            memory.memory_id,
            memory.source_lineage,
            request.target_lineage,
            request.disposition,
            False,
            True,
        )

    raise ValueError(f"unsupported disposition: {request.disposition}")
