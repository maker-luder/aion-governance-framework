from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json

from .models import MeaningProjection


class MeaningRelationKind(str, Enum):
    SUPPORTS = "SUPPORTS"
    CONSTRAINS = "CONSTRAINS"
    PRIORITIZES = "PRIORITIZES"
    IN_TENSION_WITH = "IN_TENSION_WITH"
    DERIVED_FROM = "DERIVED_FROM"
    REFINES = "REFINES"


@dataclass(frozen=True, slots=True)
class MeaningRelation:
    relation_id: str
    subject_id: str
    namespace: str
    source_claim_id: str
    target_claim_id: str
    kind: MeaningRelationKind
    provenance_refs: tuple[str, ...]
    confidence: float = 1.0

    def __post_init__(self) -> None:
        for name, value in (
            ("relation_id", self.relation_id),
            ("subject_id", self.subject_id),
            ("namespace", self.namespace),
            ("source_claim_id", self.source_claim_id),
            ("target_claim_id", self.target_claim_id),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if self.source_claim_id == self.target_claim_id:
            raise ValueError("a meaning relation cannot target itself")
        if not self.provenance_refs:
            raise ValueError("provenance_refs are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class MeaningStructureSnapshot:
    subject_id: str
    namespace: str
    claim_ids: tuple[str, ...]
    claim_fingerprints: tuple[tuple[str, str], ...]
    relation_ids: tuple[str, ...]
    relation_fingerprints: tuple[tuple[str, str], ...]
    structure_fingerprint: str
    canonical_effect: str = "NONE"
    runtime_effect: str = "NONE"
    identity_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


@dataclass(frozen=True, slots=True)
class MeaningStructureDrift:
    subject_id: str
    namespace: str
    before_fingerprint: str
    after_fingerprint: str
    added_claim_ids: tuple[str, ...]
    removed_claim_ids: tuple[str, ...]
    changed_claim_ids: tuple[str, ...]
    added_relation_ids: tuple[str, ...]
    removed_relation_ids: tuple[str, ...]
    changed_relation_ids: tuple[str, ...]
    changed: bool
    canonical_effect: str = "NONE"
    runtime_effect: str = "NONE"


class MeaningStructureAnalyzer:
    """Pure research analyzer for explicit claim/relation structure.

    This class does not infer latent relations, grant authority, write state, or decide
    whether a proposition is true. It fingerprints only the explicit research material
    supplied by the caller.
    """

    @staticmethod
    def _digest(payload: object) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def _claim_fingerprint(cls, claim: object) -> str:
        provenance = tuple(
            sorted(
                (
                    ref.source_id,
                    ref.source_kind.value,
                    ref.locator,
                    ref.content_sha256,
                )
                for ref in claim.provenance
            )
        )
        return cls._digest(
            {
                "claim_id": claim.claim_id,
                "subject_id": claim.subject_id,
                "namespace": claim.namespace,
                "kind": claim.kind.value,
                "proposition": claim.proposition,
                "importance": claim.importance,
                "confidence": claim.confidence,
                "provenance": provenance,
                "recorded_at": claim.recorded_at,
                "revision_of": claim.revision_of,
            }
        )

    @classmethod
    def _relation_fingerprint(cls, relation: MeaningRelation) -> str:
        return cls._digest(
            {
                "relation_id": relation.relation_id,
                "subject_id": relation.subject_id,
                "namespace": relation.namespace,
                "source_claim_id": relation.source_claim_id,
                "target_claim_id": relation.target_claim_id,
                "kind": relation.kind.value,
                "provenance_refs": sorted(relation.provenance_refs),
                "confidence": relation.confidence,
            }
        )

    def snapshot(
        self,
        projection: MeaningProjection,
        relations: tuple[MeaningRelation, ...] = (),
    ) -> MeaningStructureSnapshot:
        claims = tuple(projection.current_candidate_claims)
        claim_ids = [claim.claim_id for claim in claims]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("duplicate claim_id in projection")

        claim_by_id = {claim.claim_id: claim for claim in claims}
        relation_ids: set[str] = set()
        for relation in relations:
            if relation.relation_id in relation_ids:
                raise ValueError("duplicate relation_id")
            relation_ids.add(relation.relation_id)
            if relation.subject_id != projection.subject_id or relation.namespace != projection.namespace:
                raise ValueError("relation subject and namespace must match projection")
            if relation.source_claim_id not in claim_by_id or relation.target_claim_id not in claim_by_id:
                raise ValueError("relation endpoints must exist in the current projection")

        claim_fingerprints = tuple(
            sorted((claim.claim_id, self._claim_fingerprint(claim)) for claim in claims)
        )
        relation_fingerprints = tuple(
            sorted((relation.relation_id, self._relation_fingerprint(relation)) for relation in relations)
        )
        structure_fingerprint = self._digest(
            {
                "subject_id": projection.subject_id,
                "namespace": projection.namespace,
                "claims": claim_fingerprints,
                "relations": relation_fingerprints,
            }
        )
        return MeaningStructureSnapshot(
            subject_id=projection.subject_id,
            namespace=projection.namespace,
            claim_ids=tuple(item[0] for item in claim_fingerprints),
            claim_fingerprints=claim_fingerprints,
            relation_ids=tuple(item[0] for item in relation_fingerprints),
            relation_fingerprints=relation_fingerprints,
            structure_fingerprint=structure_fingerprint,
        )

    def compare(
        self,
        before: MeaningStructureSnapshot,
        after: MeaningStructureSnapshot,
    ) -> MeaningStructureDrift:
        if before.subject_id != after.subject_id or before.namespace != after.namespace:
            raise ValueError("cross-subject or cross-namespace structure comparison is prohibited")

        before_claims = dict(before.claim_fingerprints)
        after_claims = dict(after.claim_fingerprints)
        before_relations = dict(before.relation_fingerprints)
        after_relations = dict(after.relation_fingerprints)

        added_claims = tuple(sorted(after_claims.keys() - before_claims.keys()))
        removed_claims = tuple(sorted(before_claims.keys() - after_claims.keys()))
        changed_claims = tuple(
            sorted(
                claim_id
                for claim_id in before_claims.keys() & after_claims.keys()
                if before_claims[claim_id] != after_claims[claim_id]
            )
        )
        added_relations = tuple(sorted(after_relations.keys() - before_relations.keys()))
        removed_relations = tuple(sorted(before_relations.keys() - after_relations.keys()))
        changed_relations = tuple(
            sorted(
                relation_id
                for relation_id in before_relations.keys() & after_relations.keys()
                if before_relations[relation_id] != after_relations[relation_id]
            )
        )
        return MeaningStructureDrift(
            subject_id=before.subject_id,
            namespace=before.namespace,
            before_fingerprint=before.structure_fingerprint,
            after_fingerprint=after.structure_fingerprint,
            added_claim_ids=added_claims,
            removed_claim_ids=removed_claims,
            changed_claim_ids=changed_claims,
            added_relation_ids=added_relations,
            removed_relation_ids=removed_relations,
            changed_relation_ids=changed_relations,
            changed=before.structure_fingerprint != after.structure_fingerprint,
        )
