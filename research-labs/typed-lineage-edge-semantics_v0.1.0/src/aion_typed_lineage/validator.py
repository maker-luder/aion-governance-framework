from __future__ import annotations

from .model import EdgeDecision, EdgeStatus, EdgeType, LineageEdge


def validate_edge(edge: LineageEdge) -> EdgeDecision:
    if not edge.provenance_refs:
        return EdgeDecision(edge.edge_id, EdgeStatus.HOLD, "PROVENANCE_REQUIRED", edge.edge_type)
    if edge.edge_type is EdgeType.AUTHORITY_OFFER and not edge.offered_authorities:
        return EdgeDecision(edge.edge_id, EdgeStatus.HOLD, "EMPTY_AUTHORITY_OFFER", edge.edge_type)
    if edge.edge_type is EdgeType.AUTHORITY_OFFER and not edge.accepted_authorities.issubset(edge.offered_authorities):
        return EdgeDecision(edge.edge_id, EdgeStatus.REJECTED, "AUTHORITY_ACCEPTANCE_EXCEEDS_OFFER", edge.edge_type)
    if edge.edge_type is EdgeType.MEMORY_ACCESS and edge.target_autobiographical_ownership:
        return EdgeDecision(edge.edge_id, EdgeStatus.REJECTED, "ACCESS_CANNOT_TRANSFER_OWNERSHIP", edge.edge_type)
    if edge.edge_type is EdgeType.MEMORY_ADOPTION and edge.target_autobiographical_ownership:
        return EdgeDecision(edge.edge_id, EdgeStatus.REJECTED, "ADOPTION_CANNOT_TRANSFER_OWNERSHIP", edge.edge_type)
    return EdgeDecision(edge.edge_id, EdgeStatus.ACCEPTED, "TYPED_PROVENANCE_EDGE_ACCEPTED", edge.edge_type)
