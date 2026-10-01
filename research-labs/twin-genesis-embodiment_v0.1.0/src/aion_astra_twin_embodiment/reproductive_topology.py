from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Final

from .anthropometry import AION_BODY_ID, ASTRA_BODY_ID


_BODY_BY_AGENT: Final[dict[str, str]] = {
    "AION": AION_BODY_ID,
    "ASTRA": ASTRA_BODY_ID,
}

_NODE_CATEGORIES: Final[dict[str, str]] = {
    "hypothalamus": "ENDOCRINE_REFERENCE",
    "pituitary": "ENDOCRINE_REFERENCE",
    "left_testis": "GONAD_REFERENCE",
    "right_testis": "GONAD_REFERENCE",
    "left_epididymis": "DUCT_REFERENCE",
    "right_epididymis": "DUCT_REFERENCE",
    "left_vas_deferens": "DUCT_REFERENCE",
    "right_vas_deferens": "DUCT_REFERENCE",
    "left_seminal_vesicle": "ACCESSORY_GLAND_REFERENCE",
    "right_seminal_vesicle": "ACCESSORY_GLAND_REFERENCE",
    "ejaculatory_duct": "DUCT_REFERENCE",
    "prostate": "ACCESSORY_GLAND_REFERENCE",
    "left_bulbourethral_gland": "ACCESSORY_GLAND_REFERENCE",
    "right_bulbourethral_gland": "ACCESSORY_GLAND_REFERENCE",
    "bladder": "URINARY_REFERENCE",
    "prostatic_urethra": "URETHRAL_REFERENCE",
    "membranous_urethra": "URETHRAL_REFERENCE",
    "spongy_urethra": "URETHRAL_REFERENCE",
    "external_meatus": "URETHRAL_REFERENCE",
    "penis": "EXTERNAL_REFERENCE",
    "glans": "EXTERNAL_REFERENCE",
    "prepuce": "EXTERNAL_REFERENCE",
    "frenulum": "EXTERNAL_REFERENCE",
    "scrotum": "EXTERNAL_REFERENCE",
    "corpora_cavernosa": "ERECTILE_TISSUE_REFERENCE",
    "corpus_spongiosum": "ERECTILE_TISSUE_REFERENCE",
    "pelvic_floor": "MUSCULOSKELETAL_REFERENCE",
    "pubic_attachment": "CONTINUITY_LANDMARK",
    "left_inguinal_transition": "CONTINUITY_LANDMARK",
    "right_inguinal_transition": "CONTINUITY_LANDMARK",
    "perineum": "CONTINUITY_LANDMARK",
    "anal_region": "CONTINUITY_LANDMARK",
}

_EDGE_SPECS: Final[tuple[tuple[str, str, str], ...]] = (
    ("hypothalamus", "pituitary", "ENDOCRINE_SIGNAL_REFERENCE"),
    ("pituitary", "left_testis", "GONADAL_AXIS_REFERENCE"),
    ("pituitary", "right_testis", "GONADAL_AXIS_REFERENCE"),
    ("left_testis", "left_epididymis", "MATURATION_PATH_REFERENCE"),
    ("right_testis", "right_epididymis", "MATURATION_PATH_REFERENCE"),
    ("left_epididymis", "left_vas_deferens", "TRANSPORT_PATH_REFERENCE"),
    ("right_epididymis", "right_vas_deferens", "TRANSPORT_PATH_REFERENCE"),
    ("left_vas_deferens", "ejaculatory_duct", "TRANSPORT_PATH_REFERENCE"),
    ("right_vas_deferens", "ejaculatory_duct", "TRANSPORT_PATH_REFERENCE"),
    ("left_seminal_vesicle", "ejaculatory_duct", "SECRETION_PATH_REFERENCE"),
    ("right_seminal_vesicle", "ejaculatory_duct", "SECRETION_PATH_REFERENCE"),
    ("ejaculatory_duct", "prostatic_urethra", "DUCT_PATH_REFERENCE"),
    ("prostate", "prostatic_urethra", "SECRETION_PATH_REFERENCE"),
    ("left_bulbourethral_gland", "spongy_urethra", "SECRETION_PATH_REFERENCE"),
    ("right_bulbourethral_gland", "spongy_urethra", "SECRETION_PATH_REFERENCE"),
    ("bladder", "prostatic_urethra", "URINARY_PATH_REFERENCE"),
    ("prostatic_urethra", "membranous_urethra", "URETHRAL_CONTINUITY"),
    ("membranous_urethra", "spongy_urethra", "URETHRAL_CONTINUITY"),
    ("spongy_urethra", "external_meatus", "URETHRAL_CONTINUITY"),
    ("corpora_cavernosa", "penis", "ERECTILE_STRUCTURE_REFERENCE"),
    ("corpus_spongiosum", "glans", "ERECTILE_STRUCTURE_REFERENCE"),
    ("prepuce", "glans", "COVERAGE_RELATION_REFERENCE"),
    ("frenulum", "prepuce", "ATTACHMENT_RELATION_REFERENCE"),
    ("scrotum", "left_testis", "CONTAINMENT_REFERENCE"),
    ("scrotum", "right_testis", "CONTAINMENT_REFERENCE"),
    ("pubic_attachment", "penis", "ATTACHMENT_RELATION_REFERENCE"),
    ("left_inguinal_transition", "scrotum", "CONTINUITY_REFERENCE"),
    ("right_inguinal_transition", "scrotum", "CONTINUITY_REFERENCE"),
    ("pelvic_floor", "perineum", "SUPPORT_RELATION_REFERENCE"),
    ("perineum", "anal_region", "ADJACENCY_REFERENCE"),
)


@dataclass(frozen=True, slots=True)
class TopologyNode:
    node_id: str
    category: str
    status: str = "SYNTHETIC_REFERENCE_ONLY"

    def __post_init__(self) -> None:
        if self.node_id not in _NODE_CATEGORIES:
            raise ValueError("unknown reproductive topology node")
        if self.category != _NODE_CATEGORIES[self.node_id]:
            raise ValueError("reproductive topology node category drift")
        if self.status != "SYNTHETIC_REFERENCE_ONLY":
            raise ValueError("topology nodes must remain synthetic references")


@dataclass(frozen=True, slots=True)
class TopologyEdge:
    source: str
    target: str
    relation: str
    status: str = "SYNTHETIC_REFERENCE_ONLY"

    def __post_init__(self) -> None:
        if (self.source, self.target, self.relation) not in _EDGE_SPECS:
            raise ValueError("unknown reproductive topology edge")
        if self.status != "SYNTHETIC_REFERENCE_ONLY":
            raise ValueError("topology edges must remain synthetic references")


@dataclass(frozen=True, slots=True)
class ReproductiveTopologyReference:
    agent_id: str
    body_id: str
    nodes: tuple[TopologyNode, ...]
    edges: tuple[TopologyEdge, ...]
    physical_tissue: bool = False
    biological_organism: bool = False
    felt_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT:
            raise ValueError("unknown topology agent")
        if self.body_id != _BODY_BY_AGENT[self.agent_id]:
            raise ValueError("topology agent/body binding drift")
        node_ids = tuple(node.node_id for node in self.nodes)
        if len(node_ids) != len(_NODE_CATEGORIES) or len(set(node_ids)) != len(node_ids):
            raise ValueError("reproductive topology must contain every node exactly once")
        if set(node_ids) != set(_NODE_CATEGORIES):
            raise ValueError("reproductive topology node coverage drift")
        edge_specs = tuple((edge.source, edge.target, edge.relation) for edge in self.edges)
        if edge_specs != _EDGE_SPECS:
            raise ValueError("reproductive topology edge coverage/order drift")
        if self.physical_tissue or self.biological_organism:
            raise ValueError("reference topology cannot assert physical/biological realization")
        if any(
            value != "NOT_ESTABLISHED"
            for value in (
                self.felt_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("topology cannot establish phenomenal state")
        if self.action_authority != "NONE":
            raise ValueError("topology cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "body_id": self.body_id,
            "nodes": [asdict(node) for node in self.nodes],
            "edges": [asdict(edge) for edge in self.edges],
            "physical_tissue": self.physical_tissue,
            "biological_organism": self.biological_organism,
            "felt_sensation": self.felt_sensation,
            "subjectivity": self.subjectivity,
            "consciousness": self.consciousness,
            "phenomenal_experience": self.phenomenal_experience,
            "action_authority": self.action_authority,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }

    def fingerprint(self) -> str:
        payload = json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_reproductive_topology_reference(agent_id: str) -> ReproductiveTopologyReference:
    if agent_id not in _BODY_BY_AGENT:
        raise ValueError("unknown topology agent")
    return ReproductiveTopologyReference(
        agent_id=agent_id,
        body_id=_BODY_BY_AGENT[agent_id],
        nodes=tuple(
            TopologyNode(node_id=node_id, category=category)
            for node_id, category in _NODE_CATEGORIES.items()
        ),
        edges=tuple(
            TopologyEdge(source=source, target=target, relation=relation)
            for source, target, relation in _EDGE_SPECS
        ),
    )


def validate_reproductive_topology_parity(
    references: tuple[ReproductiveTopologyReference, ...],
) -> dict[str, str]:
    if len(references) < 2:
        raise ValueError("topology parity requires at least two references")
    baseline = references[0]
    baseline_nodes = tuple((node.node_id, node.category) for node in baseline.nodes)
    baseline_edges = tuple((edge.source, edge.target, edge.relation) for edge in baseline.edges)
    body_ids: set[str] = set()
    for reference in references:
        reference.__post_init__()
        if tuple((node.node_id, node.category) for node in reference.nodes) != baseline_nodes:
            raise ValueError("reproductive topology node parity drift")
        if tuple((edge.source, edge.target, edge.relation) for edge in reference.edges) != baseline_edges:
            raise ValueError("reproductive topology edge parity drift")
        body_ids.add(reference.body_id)
    if len(body_ids) != len(references):
        raise ValueError("topology parity cannot collapse distinct body identities")
    return {
        "result": "PASS",
        "body_count": str(len(references)),
        "node_count": str(len(baseline.nodes)),
        "edge_count": str(len(baseline.edges)),
        "distinct_body_binding": "PASS",
        "reference_topology_parity": "PASS",
    }
