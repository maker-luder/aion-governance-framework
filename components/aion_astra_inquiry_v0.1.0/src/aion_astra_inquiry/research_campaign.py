from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re

from .automation import AutonomousInquiryCampaign, InquiryCampaignReport
from .core import EvidenceSource
from .external import ExternalWebEvidenceSource, ExternalWebPolicy
from .research_closure import (
    BoundedResearchClosure,
    ResearchClosureReport,
    closure_to_dict,
    closure_to_markdown,
    verify_research_closure,
)


@dataclass(frozen=True)
class ResearchCycle:
    cycle_index: int
    seed_questions: tuple[str, ...]
    inquiry_campaign: InquiryCampaignReport
    closures: tuple[ResearchClosureReport, ...]


@dataclass(frozen=True)
class BoundedResearchCampaignReport:
    repository_root_name: str
    repository_ref: str
    cycles: tuple[ResearchCycle, ...]
    campaign_hash: str
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    repository_mutation: bool = False
    network_access: bool = False
    external_network_mode: str = "DISABLED"
    deployment: bool = False
    autonomous_merge: bool = False
    full_automation: bool = True
    full_authority: bool = False


class BoundedAutonomousResearchCampaign:
    """Compose inquiry, executed evidence-plane probes, statistics and bounded follow-up.

    Each cycle runs the existing AION/Astra inquiry unchanged, closes every inquiry
    report with deterministic intervention/ablation/replay/counterfactual operations,
    then uses unresolved closure questions as the next bounded cycle's agenda.
    """

    def __init__(
        self,
        root: Path,
        *,
        max_cycles: int = 2,
        max_questions_per_cycle: int = 2,
        max_rounds: int = 3,
        evidence_limit: int = 4,
        repository_ref: str = "UNSPECIFIED",
        external_web: bool = False,
        external_policy: ExternalWebPolicy | None = None,
        external_evidence_source: EvidenceSource | None = None,
    ) -> None:
        resolved = root.resolve()
        if not resolved.is_dir():
            raise ValueError("research campaign root must be an existing directory")
        if not 1 <= max_cycles <= 6:
            raise ValueError("max_cycles must be between 1 and 6")
        if not 1 <= max_questions_per_cycle <= 4:
            raise ValueError("max_questions_per_cycle must be between 1 and 4")
        if not 1 <= max_rounds <= 12:
            raise ValueError("max_rounds must be between 1 and 12")
        if not 1 <= evidence_limit <= 20:
            raise ValueError("evidence_limit must be between 1 and 20")

        self._root = resolved
        self._max_cycles = max_cycles
        self._max_questions_per_cycle = max_questions_per_cycle
        self._max_rounds = max_rounds
        self._evidence_limit = evidence_limit
        self._repository_ref = repository_ref.strip() or "UNSPECIFIED"
        if external_evidence_source is not None:
            self._external_source = external_evidence_source
        elif external_web:
            self._external_source = ExternalWebEvidenceSource(policy=external_policy)
        else:
            self._external_source = None
        self._external_enabled = self._external_source is not None
        self._closure = BoundedResearchClosure()

    def run(self, seed_questions: tuple[str, ...] = ()) -> BoundedResearchCampaignReport:
        normalized_seeds = tuple(
            question.strip() for question in seed_questions if question.strip()
        )
        next_questions = normalized_seeds
        seen: set[str] = {_question_key(question) for question in normalized_seeds}
        cycles: list[ResearchCycle] = []

        for cycle_index in range(1, self._max_cycles + 1):
            inquiry = AutonomousInquiryCampaign(
                self._root,
                max_questions=self._max_questions_per_cycle,
                max_rounds=self._max_rounds,
                evidence_limit=self._evidence_limit,
                repository_ref=self._repository_ref,
                external_evidence_source=self._external_source,
            ).run(next_questions)
            closures = tuple(self._closure.close(report) for report in inquiry.reports)
            if not all(verify_research_closure(item) for item in closures):
                raise RuntimeError("research closure integrity verification failed")

            cycles.append(
                ResearchCycle(
                    cycle_index=cycle_index,
                    seed_questions=next_questions,
                    inquiry_campaign=inquiry,
                    closures=closures,
                )
            )

            follow_ups: list[str] = []
            for closure in closures:
                candidate = closure.follow_up_question.strip()
                key = _question_key(candidate)
                if not candidate or not key or key in seen:
                    continue
                seen.add(key)
                follow_ups.append(candidate)
                if len(follow_ups) >= self._max_questions_per_cycle:
                    break
            if not follow_ups:
                break
            next_questions = tuple(follow_ups)

        campaign_hash = _campaign_hash(tuple(cycles), self._repository_ref)
        return BoundedResearchCampaignReport(
            repository_root_name=self._root.name,
            repository_ref=self._repository_ref,
            cycles=tuple(cycles),
            campaign_hash=campaign_hash,
            network_access=self._external_enabled,
            external_network_mode="GOVERNED_READ_ONLY" if self._external_enabled else "DISABLED",
        )


def research_campaign_to_dict(
    campaign: BoundedResearchCampaignReport,
) -> dict[str, object]:
    return {
        "repository_root_name": campaign.repository_root_name,
        "repository_ref": campaign.repository_ref,
        "scientific_disposition": campaign.scientific_disposition,
        "canonical_effect": campaign.canonical_effect,
        "repository_mutation": campaign.repository_mutation,
        "network_access": campaign.network_access,
        "external_network_mode": campaign.external_network_mode,
        "deployment": campaign.deployment,
        "autonomous_merge": campaign.autonomous_merge,
        "full_automation": campaign.full_automation,
        "full_authority": campaign.full_authority,
        "campaign_hash": campaign.campaign_hash,
        "cycles": [
            {
                "cycle_index": cycle.cycle_index,
                "seed_questions": list(cycle.seed_questions),
                "inquiry_campaign_hash": cycle.inquiry_campaign.campaign_hash,
                "closures": [closure_to_dict(item) for item in cycle.closures],
            }
            for cycle in campaign.cycles
        ],
    }


def research_campaign_to_markdown(campaign: BoundedResearchCampaignReport) -> str:
    lines = [
        "# AION / Astra bounded autonomous research closure",
        "",
        f"- repository ref: `{campaign.repository_ref}`",
        f"- cycles executed: `{len(campaign.cycles)}`",
        f"- external network mode: `{campaign.external_network_mode}`",
        f"- scientific disposition: `{campaign.scientific_disposition}`",
        f"- canonical effect: `{campaign.canonical_effect}`",
        f"- campaign hash: `{campaign.campaign_hash}`",
        "",
    ]
    for cycle in campaign.cycles:
        lines.extend(
            [
                f"## Cycle {cycle.cycle_index}",
                "",
                f"- inquiry campaign hash: `{cycle.inquiry_campaign.campaign_hash}`",
                f"- inquiry count: `{len(cycle.inquiry_campaign.reports)}`",
                f"- closure count: `{len(cycle.closures)}`",
                "",
            ]
        )
        for closure in cycle.closures:
            lines.extend([closure_to_markdown(closure), ""])

    lines.extend(
        [
            "## Locked authority boundary",
            "",
            "`FULL_AUTOMATION != FULL_AUTHORITY`",
            "",
            "`NORMATIVE_STATE != AUTHORITY`",
            "",
            "`RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH`",
            "",
            "`ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY`",
            "",
            "`ENGINEERING_INTERVENTION != REAL_WORLD_CAUSAL_IDENTIFICATION`",
            "",
            "`AUTONOMOUS_REPOSITORY_MUTATION = NO`",
            "",
            "`AUTONOMOUS_SECRET_ACCESS = NO`",
            "",
            "`AUTONOMOUS_DEPLOYMENT = NO`",
            "",
            "`AUTONOMOUS_MERGE = NO`",
            "",
            "`CANONICAL_EFFECT = NONE`",
            "",
        ]
    )
    return "\n".join(lines)


def write_research_campaign_report(
    campaign: BoundedResearchCampaignReport,
    output_dir: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "research_campaign.json"
    markdown_path = output_dir / "research_campaign.md"
    json_path.write_text(
        json.dumps(research_campaign_to_dict(campaign), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        research_campaign_to_markdown(campaign) + "\n",
        encoding="utf-8",
    )
    return json_path, markdown_path


def _campaign_hash(cycles: tuple[ResearchCycle, ...], repository_ref: str) -> str:
    payload = {
        "repository_ref": repository_ref,
        "cycles": [
            {
                "cycle_index": cycle.cycle_index,
                "inquiry_campaign_hash": cycle.inquiry_campaign.campaign_hash,
                "closure_hashes": [item.closure_hash for item in cycle.closures],
            }
            for cycle in cycles
        ],
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _question_key(question: str) -> str:
    return re.sub(r"\W+", " ", question.lower(), flags=re.UNICODE).strip()
