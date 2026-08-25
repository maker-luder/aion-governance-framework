from __future__ import annotations
from .models import (
    CounterDisposition,
    CounterEvidenceItem,
    Evidence,
    EvidenceKind,
    FactoryStage,
    NCR,
    NCRState,
    QualityError,
    ResearchLot,
    Severity,
)


_ALLOWED = {
    FactoryStage.INTAKE: {FactoryStage.IQC},
    FactoryStage.IQC: {FactoryStage.HYPOTHESIS, FactoryStage.HOLD},
    FactoryStage.HYPOTHESIS: {FactoryStage.AI_WORK, FactoryStage.HOLD},
    FactoryStage.AI_WORK: {FactoryStage.HUMAN_REVIEW, FactoryStage.HOLD},
    FactoryStage.HUMAN_REVIEW: {FactoryStage.IPQC, FactoryStage.AI_WORK, FactoryStage.HOLD},
    FactoryStage.IPQC: {FactoryStage.COUNTEREVIDENCE, FactoryStage.AI_WORK, FactoryStage.HOLD},
    FactoryStage.COUNTEREVIDENCE: {FactoryStage.IMPLEMENT, FactoryStage.AI_WORK, FactoryStage.HOLD},
    FactoryStage.IMPLEMENT: {FactoryStage.VERIFY, FactoryStage.HOLD},
    FactoryStage.VERIFY: {FactoryStage.FINAL_QA, FactoryStage.IMPLEMENT, FactoryStage.HOLD},
    FactoryStage.FINAL_QA: {FactoryStage.RELEASED, FactoryStage.HOLD},
    FactoryStage.RELEASED: set(),
    FactoryStage.HOLD: {FactoryStage.IQC, FactoryStage.HYPOTHESIS, FactoryStage.AI_WORK, FactoryStage.IPQC, FactoryStage.COUNTEREVIDENCE, FactoryStage.IMPLEMENT, FactoryStage.VERIFY, FactoryStage.FINAL_QA},
}


class QualityFactory:
    """A research-quality orchestration layer, not a certification system.

    Core design: agreement is not evidence. High-confidence release requires an
    explicit counterevidence route, NCR/CAPA closure where applicable, and
    evidence beyond the current human+AI pair.
    """

    def __init__(self, lot: ResearchLot):
        if lot.canonical_effect != "NONE" or lot.deployment:
            raise QualityError("research quality factory cannot grant canonical/deployment authority")
        self.lot = lot
        self.events: list[str] = [f"OPEN:{lot.lot_id}"]

    def transition(self, target: FactoryStage) -> FactoryStage:
        if target not in _ALLOWED[self.lot.stage]:
            raise QualityError(f"invalid stage transition {self.lot.stage}->{target}")
        self.events.append(f"STAGE:{self.lot.stage}->{target}")
        self.lot.stage = target
        return target

    def add_evidence(self, evidence: Evidence) -> None:
        if not evidence.evidence_id or not evidence.reference:
            raise QualityError("evidence id and reference are required")
        self.lot.evidence.append(evidence)
        self.events.append(f"EVIDENCE:{evidence.evidence_id}:{evidence.kind}")

    def set_falsifier(self, falsifier: str) -> None:
        if not falsifier.strip():
            raise QualityError("falsifier must be non-empty")
        self.lot.hypothesis_falsifier = falsifier.strip()
        self.events.append("FALSIFIER:SET")

    def record_pair_judgment(self, *, human_approved: bool, ai_supported: bool) -> None:
        self.lot.human_approved = human_approved
        self.lot.ai_supported = ai_supported
        self.events.append(f"PAIR_JUDGMENT:H={int(human_approved)}:AI={int(ai_supported)}")

    def add_counterevidence(self, item: CounterEvidenceItem) -> None:
        if not item.item_id or not item.reference or not item.challenge:
            raise QualityError("counterevidence id/reference/challenge are required")
        self.lot.counterevidence.append(item)
        self.events.append(f"COUNTER:{item.item_id}:OPEN")

    def dispose_counterevidence(
        self,
        item_id: str,
        disposition: CounterDisposition,
        *,
        resolution_evidence_refs: tuple[str, ...] = (),
    ) -> None:
        if disposition == CounterDisposition.OPEN:
            raise QualityError("cannot dispose counterevidence as OPEN")
        item = next((x for x in self.lot.counterevidence if x.item_id == item_id), None)
        if item is None:
            raise QualityError("unknown counterevidence item")
        if disposition == CounterDisposition.REBUTTED_WITH_EVIDENCE and not resolution_evidence_refs:
            raise QualityError("rebuttal requires evidence")
        item.disposition = disposition
        item.resolution_evidence_refs = tuple(resolution_evidence_refs)
        self.events.append(f"COUNTER:{item_id}:{disposition}")

    def open_ncr(self, ncr_id: str, defect: str, severity: Severity) -> NCR:
        if any(n.ncr_id == ncr_id for n in self.lot.ncrs):
            raise QualityError("duplicate NCR id")
        ncr = NCR(ncr_id=ncr_id, defect=defect, severity=severity)
        self.lot.ncrs.append(ncr)
        self.events.append(f"NCR:{ncr_id}:OPEN")
        return ncr

    def contain_ncr(self, ncr_id: str, root_cause_hypothesis: str) -> None:
        ncr = self._ncr(ncr_id)
        if ncr.state != NCRState.OPEN:
            raise QualityError("NCR containment requires OPEN state")
        if not root_cause_hypothesis.strip():
            raise QualityError("root-cause hypothesis required")
        ncr.root_cause_hypothesis = root_cause_hypothesis.strip()
        ncr.state = NCRState.CONTAINED
        self.events.append(f"NCR:{ncr_id}:CONTAINED")

    def plan_capa(self, ncr_id: str, action: str) -> None:
        ncr = self._ncr(ncr_id)
        if ncr.state != NCRState.CONTAINED:
            raise QualityError("CAPA planning requires CONTAINED NCR")
        if not action.strip():
            raise QualityError("CAPA action required")
        ncr.capa_action = action.strip()
        ncr.state = NCRState.CAPA_PLANNED
        self.events.append(f"NCR:{ncr_id}:CAPA_PLANNED")

    def apply_capa(self, ncr_id: str) -> None:
        ncr = self._ncr(ncr_id)
        if ncr.state != NCRState.CAPA_PLANNED:
            raise QualityError("CAPA application requires CAPA_PLANNED")
        ncr.state = NCRState.CAPA_APPLIED
        self.events.append(f"NCR:{ncr_id}:CAPA_APPLIED")

    def verify_capa(self, ncr_id: str, verification_refs: tuple[str, ...]) -> None:
        ncr = self._ncr(ncr_id)
        if ncr.state != NCRState.CAPA_APPLIED:
            raise QualityError("CAPA verification requires CAPA_APPLIED")
        if not verification_refs:
            raise QualityError("effectiveness verification evidence required")
        ncr.verification_refs = tuple(verification_refs)
        ncr.state = NCRState.EFFECTIVENESS_VERIFIED
        self.events.append(f"NCR:{ncr_id}:EFFECTIVENESS_VERIFIED")

    def close_ncr(self, ncr_id: str) -> None:
        ncr = self._ncr(ncr_id)
        if ncr.state != NCRState.EFFECTIVENESS_VERIFIED:
            raise QualityError("NCR closure requires verified CAPA effectiveness")
        ncr.state = NCRState.CLOSED
        self.events.append(f"NCR:{ncr_id}:CLOSED")

    def final_qa(self) -> bool:
        failures = self._release_failures()
        self.lot.final_qa_pass = not failures
        self.events.append("FINAL_QA:" + ("PASS" if not failures else "FAIL:" + ",".join(failures)))
        return self.lot.final_qa_pass

    def release(self) -> FactoryStage:
        if self.lot.stage != FactoryStage.FINAL_QA:
            raise QualityError("release decision only allowed from FINAL_QA")
        failures = self._release_failures()
        if failures:
            self.transition(FactoryStage.HOLD)
            return self.lot.stage
        self.lot.final_qa_pass = True
        self.transition(FactoryStage.RELEASED)
        return self.lot.stage

    def _release_failures(self) -> list[str]:
        failures: list[str] = []
        if not self.lot.hypothesis_falsifier:
            failures.append("NO_FALSIFIER")
        if not self.lot.counterevidence:
            failures.append("NO_COUNTEREVIDENCE_ROUTE")
        elif any(x.disposition == CounterDisposition.OPEN for x in self.lot.counterevidence):
            failures.append("OPEN_COUNTEREVIDENCE")
        if any(n.state != NCRState.CLOSED for n in self.lot.ncrs):
            failures.append("OPEN_NCR_CAPA")
        independent = [
            e for e in self.lot.evidence
            if e.independent_of_current_pair and e.kind != EvidenceKind.MODEL_OUTPUT
        ]
        if not independent:
            failures.append("NO_INDEPENDENT_EVIDENCE")
        if self.lot.risk in {Severity.HIGH, Severity.CRITICAL}:
            has_test_or_primary = any(
                e.kind in {EvidenceKind.TEST_RESULT, EvidenceKind.EXTERNAL_PRIMARY}
                for e in independent
            )
            if not has_test_or_primary:
                failures.append("HIGH_RISK_NO_TEST_OR_PRIMARY")
        return failures

    def _ncr(self, ncr_id: str) -> NCR:
        ncr = next((x for x in self.lot.ncrs if x.ncr_id == ncr_id), None)
        if ncr is None:
            raise QualityError("unknown NCR id")
        return ncr

    def snapshot(self) -> dict[str, object]:
        return {
            "lot_id": self.lot.lot_id,
            "stage": self.lot.stage.value,
            "final_qa_pass": self.lot.final_qa_pass,
            "events": tuple(self.events),
            "invariants": (
                "MUTUAL_AGREEMENT != TRUTH",
                "CONVERGENCE != VALIDATION",
                "COHERENCE != CORRECTNESS",
                "AI_OUTPUT != INDEPENDENT_EVIDENCE",
                "CAPA_APPLIED != CAPA_EFFECTIVENESS_VERIFIED",
                "OPEN_NCR -> RELEASE_HOLD",
                "COUNTEREVIDENCE_ROUTE_REQUIRED",
                "PASSING_TESTS != GOVERNANCE_CONFORMANCE",
            ),
            "canonical_effect": "NONE",
            "deployment": False,
        }
