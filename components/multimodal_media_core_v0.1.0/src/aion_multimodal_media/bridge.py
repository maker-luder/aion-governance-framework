from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .models import MediaAsset, MediaOrigin, ResearchRole, canonical_hash


@dataclass(frozen=True, slots=True)
class ResearchMediaBridgeRecord:
    record_id: str
    asset_fingerprint: str
    content_sha256: str
    media_origin: MediaOrigin
    research_run_ref: str
    role: ResearchRole
    annotation: dict[str, object]
    evidence_refs: tuple[str, ...]
    seven_state_matrix_fingerprint: str = ""
    seven_state_binding_fingerprint: str = ""
    aion_astra_chain_hash: str = ""
    subject_ref: str = ""
    subjectivity_evidence_matrix_fingerprint: str = ""
    scientific_disposition: str = "HOLD"
    general_causal_role: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.record_id.strip() or not self.research_run_ref.strip():
            raise ValueError("bridge record requires record and research-run identifiers")
        if len(self.asset_fingerprint) != 64 or len(self.content_sha256) != 64:
            raise ValueError("bridge record requires an id and exact asset/content fingerprints")
        if not self.evidence_refs:
            raise ValueError("bridge record requires at least one evidence reference")
        if self.scientific_disposition != "HOLD" or self.general_causal_role != "NOT_ESTABLISHED":
            raise ValueError("MEDIA_BINDING != SCIENTIFIC_OR_GENERAL_CAUSAL_CONCLUSION")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED" or self.phenomenal_experience_conclusion != "NOT_ESTABLISHED":
            raise ValueError("MEDIA_BINDING != SUBJECTIVITY_OR_PHENOMENAL_EXPERIENCE")
        if self.action_authority != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("MEDIA_BINDING != ACTION_OR_CANONICAL_AUTHORITY")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(asdict(self))


class MultimodalResearchBridge:
    """Bind immutable media evidence to existing research surfaces without promoting claims."""

    def bind(
        self,
        asset: MediaAsset,
        *,
        role: ResearchRole,
        research_run_ref: str,
        evidence_refs: tuple[str, ...],
        selector: dict[str, object] | None = None,
        seven_state_matrix: Any | None = None,
        inquiry_report: Any | None = None,
        subject_ref: str = "",
        subjectivity_evidence_matrix: Any | None = None,
    ) -> ResearchMediaBridgeRecord:
        if not research_run_ref.strip():
            raise ValueError("multimodal research binding requires an explicit research_run_ref")
        if asset.origin is MediaOrigin.PROVIDER_GENERATED and role is ResearchRole.OBSERVATION:
            raise ValueError("generated media cannot be promoted to an external empirical observation")
        matrix_fp = ""
        binding_fp = ""
        if seven_state_matrix is not None:
            if not bool(getattr(seven_state_matrix, "matrix_integrity_pass", False)):
                raise ValueError("seven-state media binding requires matrix_integrity_pass")
            matrix_fp = str(getattr(seven_state_matrix, "fingerprint", ""))
            binding = getattr(seven_state_matrix, "binding", None)
            binding_fp = str(getattr(binding, "binding_fingerprint", ""))
            if len(matrix_fp) != 64 or len(binding_fp) != 64:
                raise ValueError("seven-state media binding requires exact matrix and binding fingerprints")

        chain_hash = ""
        if inquiry_report is not None:
            chain_hash = str(getattr(inquiry_report, "final_chain_hash", ""))
            if len(chain_hash) != 64:
                raise ValueError("AION/Astra media binding requires the exact final chain hash")
            if getattr(inquiry_report, "scientific_disposition", "HOLD") != "HOLD":
                raise ValueError("AION/Astra inquiry must remain HOLD")

        subjectivity_matrix_fp = ""
        if subjectivity_evidence_matrix is not None:
            matrix_subject_ref = str(getattr(subjectivity_evidence_matrix, "subject_ref", ""))
            if not subject_ref.strip() or matrix_subject_ref != subject_ref:
                raise ValueError("subjectivity evidence matrix must match the bounded subject_ref")
            subjectivity_matrix_fp = str(getattr(subjectivity_evidence_matrix, "fingerprint", ""))
            if len(subjectivity_matrix_fp) != 64:
                raise ValueError("subjectivity binding requires the exact evidence-matrix fingerprint")
            if getattr(subjectivity_evidence_matrix, "scientific_disposition", "HOLD") != "HOLD":
                raise ValueError("subjectivity evidence matrix must remain HOLD")
            if getattr(subjectivity_evidence_matrix, "subjectivity_conclusion", "NOT_ESTABLISHED") != "NOT_ESTABLISHED":
                raise ValueError("SUBJECTIVITY_EVIDENCE != SUBJECTIVITY")

        annotation: dict[str, object] = {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "type": "Annotation",
            "motivation": "describing",
            "body": {
                "type": "Dataset",
                "format": asset.mime_type,
                "value": asset.content_sha256,
                "generator": {"provider": asset.provider, "model": asset.model},
                "digitalSourceType": asset.source_type_uri,
                "c2paManifestRef": asset.c2pa_manifest_ref or None,
                "c2paValidated": asset.c2pa_validated,
            },
            "target": {"source": asset.content_uri},
        }
        if selector is not None:
            if not str(selector.get("type", "")).strip() or not str(selector.get("value", "")).strip():
                raise ValueError("media selector requires explicit W3C Annotation type and value")
            annotation["target"] = {"source": asset.content_uri, "selector": selector}

        record_id = "media:" + canonical_hash(
            {
                "asset": asset.fingerprint,
                "role": role.value,
                "research_run_ref": research_run_ref,
                "evidence_refs": evidence_refs,
                "matrix": matrix_fp,
                "inquiry": chain_hash,
                "subject_ref": subject_ref,
                "subjectivity_evidence_matrix": subjectivity_matrix_fp,
            }
        )[:32]
        return ResearchMediaBridgeRecord(
            record_id=record_id,
            asset_fingerprint=asset.fingerprint,
            content_sha256=asset.content_sha256,
            media_origin=asset.origin,
            research_run_ref=research_run_ref,
            role=role,
            annotation=annotation,
            evidence_refs=evidence_refs,
            seven_state_matrix_fingerprint=matrix_fp,
            seven_state_binding_fingerprint=binding_fp,
            aion_astra_chain_hash=chain_hash,
            subject_ref=subject_ref,
            subjectivity_evidence_matrix_fingerprint=subjectivity_matrix_fp,
        )

    def to_subjectivity_stage_record(
        self,
        record: ResearchMediaBridgeRecord,
        evidence_record,
        *,
        human_reviewed: bool = False,
    ):
        if not record.subject_ref.strip():
            raise ValueError("subjectivity pipeline binding requires a bounded subject_ref")
        if record.media_origin is MediaOrigin.PROVIDER_GENERATED:
            raise ValueError("provider-generated media is a stimulus/output, not direct subjectivity evidence")
        from aion_research_integrity.gate import assess_evidence
        from aion_research_integrity.models import EvidenceState
        from aion_subjectivity_pipeline.models import PipelineStage, StageRecord

        if getattr(evidence_record, "evidence_id", "") != record.record_id:
            raise ValueError("research-integrity evidence id must bind the multimodal bridge record")
        if getattr(evidence_record, "raw_hash", None) != record.content_sha256:
            raise ValueError("research-integrity raw hash must bind the admitted media content")
        gate_result = assess_evidence(evidence_record)
        if gate_result.state is not EvidenceState.RESEARCH_EVIDENCE_CANDIDATE:
            raise ValueError(f"multimodal evidence admission failed closed: {gate_result.state.value}")
        if not human_reviewed:
            raise PermissionError("research evidence candidate requires explicit human review")

        return StageRecord(
            stage=PipelineStage.SUBJECTIVITY_EVIDENCE,
            record_ref=record.record_id,
            evidence_refs=tuple(
                item
                for item in (
                    record.fingerprint,
                    record.subjectivity_evidence_matrix_fingerprint,
                    *record.evidence_refs,
                )
                if item
            ),
            passed_governance=True,
        )
