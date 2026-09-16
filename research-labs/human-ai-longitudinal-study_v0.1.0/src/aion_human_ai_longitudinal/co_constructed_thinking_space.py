from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


class ThinkingSpaceProfile(StrEnum):
    CORE_INTERACTION = "CORE_INTERACTION"
    LONGITUDINAL_REPOSITORY_RESEARCH = "LONGITUDINAL_REPOSITORY_RESEARCH"


class ContributionRole(StrEnum):
    HUMAN_OWNER = "HUMAN_OWNER"
    AI_COLLABORATOR = "AI_COLLABORATOR"
    EXTERNAL_EVIDENCE = "EXTERNAL_EVIDENCE"
    REPOSITORY_ARTIFACT = "REPOSITORY_ARTIFACT"
    IMPLEMENTATION_EVIDENCE = "IMPLEMENTATION_EVIDENCE"


class RevisionRelation(StrEnum):
    REVISES = "REVISES"
    CHALLENGES = "CHALLENGES"
    CLARIFIES = "CLARIFIES"


class GroundingDisposition(StrEnum):
    SUFFICIENT_FOR_CURRENT_PURPOSE = "SUFFICIENT_FOR_CURRENT_PURPOSE"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"


_SUBSTANTIVE_RECIPROCITY_RELATIONS = frozenset(
    {RevisionRelation.REVISES, RevisionRelation.CHALLENGES}
)


def _validate_digest(name: str, digest: str) -> None:
    if type(digest) is not str or len(digest) != 64 or any(
        char not in "0123456789abcdef" for char in digest
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _revision_graph_is_connected(
    contribution_ids: set[str],
    revision_edges: tuple[RevisionEdge, ...],
) -> bool:
    adjacency: dict[str, set[str]] = {
        contribution_id: set() for contribution_id in contribution_ids
    }
    for edge in revision_edges:
        adjacency[edge.source_id].add(edge.target_id)
        adjacency[edge.target_id].add(edge.source_id)
    pending = [next(iter(contribution_ids))]
    visited: set[str] = set()
    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)
        pending.extend(adjacency[current] - visited)
    return visited == contribution_ids


@dataclass(frozen=True, slots=True)
class EpistemicContribution:
    contribution_id: str
    role: ContributionRole
    payload_sha256: str

    def __post_init__(self) -> None:
        if type(self.contribution_id) is not str or not self.contribution_id.strip():
            raise StudyError("contribution_id must be non-empty text")
        if type(self.role) is not ContributionRole:
            raise StudyError("role must be an exact ContributionRole")
        _validate_digest("payload_sha256", self.payload_sha256)


@dataclass(frozen=True, slots=True)
class RevisionEdge:
    source_id: str
    target_id: str
    relation: RevisionRelation

    def __post_init__(self) -> None:
        if type(self.source_id) is not str or not self.source_id.strip():
            raise StudyError("source_id must be non-empty text")
        if type(self.target_id) is not str or not self.target_id.strip():
            raise StudyError("target_id must be non-empty text")
        if type(self.relation) is not RevisionRelation:
            raise StudyError("relation must be an exact RevisionRelation")
        if self.source_id == self.target_id:
            raise StudyError("revision edge cannot target itself")


@dataclass(frozen=True, slots=True)
class GroundingCheckpoint:
    problem_representation_sha256: str
    human_contribution_id: str
    ai_contribution_id: str
    disposition: GroundingDisposition
    unresolved_mismatch: bool

    def __post_init__(self) -> None:
        _validate_digest(
            "grounding_checkpoint.problem_representation_sha256",
            self.problem_representation_sha256,
        )
        if type(self.human_contribution_id) is not str or not self.human_contribution_id.strip():
            raise StudyError("grounding human_contribution_id must be non-empty text")
        if type(self.ai_contribution_id) is not str or not self.ai_contribution_id.strip():
            raise StudyError("grounding ai_contribution_id must be non-empty text")
        if type(self.disposition) is not GroundingDisposition:
            raise StudyError("grounding disposition must be an exact GroundingDisposition")
        if type(self.unresolved_mismatch) is not bool:
            raise StudyError("grounding unresolved_mismatch must be an exact bool")
        if self.human_contribution_id == self.ai_contribution_id:
            raise StudyError("grounding checkpoint must reference distinct Human and AI contributions")


@dataclass(frozen=True, slots=True)
class CoConstructedThinkingSpaceManifest:
    space_id: str
    profile: ThinkingSpaceProfile
    problem_representation_sha256: str
    grounding_checkpoint: GroundingCheckpoint
    contributions: tuple[EpistemicContribution, ...]
    revision_edges: tuple[RevisionEdge, ...]
    provenance_manifest_sha256: str
    claim_boundary_sha256: str
    authority_policy_sha256: str
    rejected_branch_manifest_sha256: str
    persistent_artifact_sha256: str | None = None
    reentry_binding_sha256: str | None = None
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False
    asserts_shared_mind: bool = False
    asserts_shared_consciousness: bool = False
    asserts_ai_subjectivity_from_structure: bool = False

    def __post_init__(self) -> None:
        if type(self.space_id) is not str or not self.space_id.strip():
            raise StudyError("space_id must be non-empty text")
        if type(self.profile) is not ThinkingSpaceProfile:
            raise StudyError("profile must be an exact ThinkingSpaceProfile")
        if type(self.grounding_checkpoint) is not GroundingCheckpoint:
            raise StudyError("grounding_checkpoint must be an exact GroundingCheckpoint")
        if type(self.contributions) is not tuple or not self.contributions:
            raise StudyError("contributions must be a non-empty tuple")
        if any(type(item) is not EpistemicContribution for item in self.contributions):
            raise StudyError("contributions must contain exact EpistemicContribution values")
        contribution_ids = [item.contribution_id for item in self.contributions]
        if len(contribution_ids) != len(set(contribution_ids)):
            raise StudyError("contribution ids must be unique")
        if type(self.revision_edges) is not tuple or not self.revision_edges:
            raise StudyError("revision_edges must be a non-empty tuple")
        if any(type(item) is not RevisionEdge for item in self.revision_edges):
            raise StudyError("revision_edges must contain exact RevisionEdge values")
        known_ids = set(contribution_ids)
        for edge in self.revision_edges:
            if edge.source_id not in known_ids or edge.target_id not in known_ids:
                raise StudyError("revision edge must reference known contributions")

        structural_digests = (
            self.problem_representation_sha256,
            self.provenance_manifest_sha256,
            self.claim_boundary_sha256,
            self.authority_policy_sha256,
            self.rejected_branch_manifest_sha256,
        )
        for name, digest in (
            ("problem_representation_sha256", self.problem_representation_sha256),
            ("provenance_manifest_sha256", self.provenance_manifest_sha256),
            ("claim_boundary_sha256", self.claim_boundary_sha256),
            ("authority_policy_sha256", self.authority_policy_sha256),
            ("rejected_branch_manifest_sha256", self.rejected_branch_manifest_sha256),
        ):
            _validate_digest(name, digest)
        if len(set(structural_digests)) != len(structural_digests):
            raise StudyError("core structural bindings must be content-distinct")

        role_by_id = {item.contribution_id: item.role for item in self.contributions}
        checkpoint = self.grounding_checkpoint
        if checkpoint.problem_representation_sha256 != self.problem_representation_sha256:
            raise StudyError(
                "grounding checkpoint must bind the manifest problem representation"
            )
        if (
            checkpoint.human_contribution_id not in known_ids
            or checkpoint.ai_contribution_id not in known_ids
        ):
            raise StudyError("grounding checkpoint must reference known contributions")
        if role_by_id[checkpoint.human_contribution_id] is not ContributionRole.HUMAN_OWNER:
            raise StudyError("grounding human contribution must have HUMAN_OWNER role")
        if role_by_id[checkpoint.ai_contribution_id] is not ContributionRole.AI_COLLABORATOR:
            raise StudyError("grounding AI contribution must have AI_COLLABORATOR role")

        optional_digests: list[str] = []
        for name in ("persistent_artifact_sha256", "reentry_binding_sha256"):
            digest = getattr(self, name)
            if digest is not None:
                _validate_digest(name, digest)
                optional_digests.append(digest)
        all_structural_digests = structural_digests + tuple(optional_digests)
        if len(set(all_structural_digests)) != len(all_structural_digests):
            raise StudyError(
                "longitudinal bindings must be distinct from core bindings and each other"
            )

        for name in (
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_human_identity",
            "contains_private_material",
            "asserts_shared_mind",
            "asserts_shared_consciousness",
            "asserts_ai_subjectivity_from_structure",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")

        if not self.synthetic:
            raise StudyError("v0.1.0 formalization accepts synthetic structural manifests only")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError("structural formalization cannot contain model or human observations")
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")
        if (
            self.asserts_shared_mind
            or self.asserts_shared_consciousness
            or self.asserts_ai_subjectivity_from_structure
        ):
            raise StudyError(
                "thinking-space structure cannot establish shared mind, consciousness, or AI subjectivity"
            )


@dataclass(frozen=True, slots=True)
class ThinkingSpaceAudit:
    profile: ThinkingSpaceProfile
    roles_present: tuple[ContributionRole, ...]
    grounding_adequate_for_current_purpose: bool
    reciprocal_human_ai_revision: bool
    revision_graph_connected: bool
    external_evidence_present: bool
    repository_artifact_present: bool
    implementation_evidence_present: bool
    longitudinal_bindings_present: bool
    research_profile_complete: bool
    mode: str = "DETERMINISTIC_SYNTHETIC_STRUCTURE"
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    grounding_evidence_scope: str = "STRUCTURAL_DECLARATION_ONLY"
    mutual_understanding: str = "NOT_ESTABLISHED"
    epistemic_co_agency: str = "NOT_ESTABLISHED"
    distributed_cognition_mechanism: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    shared_mind: str = "NOT_ESTABLISHED"
    shared_consciousness: str = "NOT_ESTABLISHED"
    ai_subjectivity: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_co_constructed_thinking_space(
    manifest: CoConstructedThinkingSpaceManifest,
) -> ThinkingSpaceAudit:
    if type(manifest) is not CoConstructedThinkingSpaceManifest:
        raise StudyError("manifest must be an exact CoConstructedThinkingSpaceManifest")

    roles = {item.role for item in manifest.contributions}
    if ContributionRole.HUMAN_OWNER not in roles or ContributionRole.AI_COLLABORATOR not in roles:
        raise StudyError("co-constructed space requires both human and AI contribution roles")

    checkpoint = manifest.grounding_checkpoint
    if checkpoint.disposition is not GroundingDisposition.SUFFICIENT_FOR_CURRENT_PURPOSE:
        raise StudyError(
            "CCTS admission requires grounding sufficient for the current purpose"
        )
    if checkpoint.unresolved_mismatch:
        raise StudyError("CCTS admission cannot retain an unresolved grounding mismatch")

    role_by_id = {item.contribution_id: item.role for item in manifest.contributions}
    human_to_ai = any(
        role_by_id[edge.source_id] is ContributionRole.HUMAN_OWNER
        and role_by_id[edge.target_id] is ContributionRole.AI_COLLABORATOR
        and edge.relation in _SUBSTANTIVE_RECIPROCITY_RELATIONS
        for edge in manifest.revision_edges
    )
    ai_to_human = any(
        role_by_id[edge.source_id] is ContributionRole.AI_COLLABORATOR
        and role_by_id[edge.target_id] is ContributionRole.HUMAN_OWNER
        and edge.relation in _SUBSTANTIVE_RECIPROCITY_RELATIONS
        for edge in manifest.revision_edges
    )
    if not (human_to_ai and ai_to_human):
        raise StudyError(
            "co-construction requires reciprocal Human<->AI REVISES or CHALLENGES edges"
        )

    contribution_ids = set(role_by_id)
    graph_connected = _revision_graph_is_connected(contribution_ids, manifest.revision_edges)
    if not graph_connected:
        raise StudyError("all declared contributions must participate in one connected revision graph")

    external_evidence = ContributionRole.EXTERNAL_EVIDENCE in roles
    repository_artifact = ContributionRole.REPOSITORY_ARTIFACT in roles
    implementation_evidence = ContributionRole.IMPLEMENTATION_EVIDENCE in roles

    repository_artifact_payloads = {
        item.payload_sha256
        for item in manifest.contributions
        if item.role is ContributionRole.REPOSITORY_ARTIFACT
    }
    persistent_artifact_bound = (
        manifest.persistent_artifact_sha256 is not None
        and manifest.persistent_artifact_sha256 in repository_artifact_payloads
    )
    reentry_binding_bound = (
        manifest.reentry_binding_sha256 is not None
        and manifest.reentry_binding_sha256 in repository_artifact_payloads
    )
    longitudinal_bindings = persistent_artifact_bound and reentry_binding_bound

    research_profile_complete = False
    if manifest.profile is ThinkingSpaceProfile.LONGITUDINAL_REPOSITORY_RESEARCH:
        if not external_evidence:
            raise StudyError("longitudinal repository research profile requires external evidence")
        if not repository_artifact:
            raise StudyError(
                "longitudinal repository research profile requires repository artifact mediation"
            )
        if not implementation_evidence:
            raise StudyError(
                "longitudinal repository research profile requires implementation evidence"
            )
        if manifest.persistent_artifact_sha256 is None or manifest.reentry_binding_sha256 is None:
            raise StudyError(
                "longitudinal repository research profile requires persistent artifact and re-entry bindings"
            )
        if not persistent_artifact_bound:
            raise StudyError(
                "persistent artifact binding must match a declared REPOSITORY_ARTIFACT payload"
            )
        if not reentry_binding_bound:
            raise StudyError(
                "re-entry binding must match a declared REPOSITORY_ARTIFACT payload"
            )
        research_profile_complete = True

    return ThinkingSpaceAudit(
        profile=manifest.profile,
        roles_present=tuple(sorted(roles, key=str)),
        grounding_adequate_for_current_purpose=True,
        reciprocal_human_ai_revision=True,
        revision_graph_connected=True,
        external_evidence_present=external_evidence,
        repository_artifact_present=repository_artifact,
        implementation_evidence_present=implementation_evidence,
        longitudinal_bindings_present=longitudinal_bindings,
        research_profile_complete=research_profile_complete,
    )
