from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re

from .core import AgentId, BoundedInquiryLoop, InquiryReport, RepositoryTextEvidenceSource
from .reasoning import EvidenceDrivenReasoningProvider, ProviderBackedPeer


@dataclass(frozen=True)
class QuestionCandidate:
    question: str
    source_ref: str
    priority: int


@dataclass(frozen=True)
class InquiryCampaignReport:
    repository_root_name: str
    repository_ref: str
    questions_considered: tuple[QuestionCandidate, ...]
    reports: tuple[InquiryReport, ...]
    campaign_hash: str
    run_mode: str = "LOCAL_EVIDENCE_DRIVEN"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    repository_mutation: bool = False
    network_access: bool = False
    deployment: bool = False
    autonomous_merge: bool = False


class RepositoryQuestionGenerator:
    """Discover bounded research questions from unresolved repository surfaces."""

    _ALLOWED_SUFFIXES = {".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
    _EXCLUDED_PARTS = {".git", ".mypy_cache", ".pytest_cache", ".venv", "__pycache__", "node_modules"}
    _MARKERS = (
        "research question",
        "open question",
        "not_established",
        "not established",
        "scientific disposition: `hold`",
        "scientific disposition = hold",
        "falsifier",
        "falsification",
        "todo",
    )

    def __init__(
        self,
        root: Path,
        *,
        max_file_bytes: int = 131_072,
        max_files_scanned: int = 800,
    ) -> None:
        resolved = root.resolve()
        if not resolved.is_dir():
            raise ValueError("repository question root must be an existing directory")
        if max_file_bytes <= 0 or max_files_scanned <= 0:
            raise ValueError("question discovery limits must be positive")
        self._root = resolved
        self._max_file_bytes = max_file_bytes
        self._max_files_scanned = max_files_scanned

    def discover(self, *, limit: int = 4) -> tuple[QuestionCandidate, ...]:
        if not 1 <= limit <= 20:
            raise ValueError("question discovery limit must be between 1 and 20")
        ranked: list[tuple[int, str, int, QuestionCandidate]] = []
        scanned = 0
        for path in sorted(self._root.rglob("*")):
            if scanned >= self._max_files_scanned:
                break
            if not path.is_file() or path.is_symlink():
                continue
            try:
                relative = path.resolve().relative_to(self._root)
            except ValueError:
                continue
            if any(part in self._EXCLUDED_PARTS for part in relative.parts):
                continue
            if path.suffix.lower() not in self._ALLOWED_SUFFIXES:
                continue
            try:
                if path.stat().st_size > self._max_file_bytes:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            scanned += 1
            lines = text.splitlines()
            for line_index, line in enumerate(lines, start=1):
                normalized = " ".join(line.strip().split())
                if not 18 <= len(normalized) <= 260:
                    continue
                lowered = normalized.lower()
                source_ref = f"{relative.as_posix()}#L{line_index}"
                if "?" in normalized or "？" in normalized:
                    question = _clean_question(normalized)
                    if question:
                        candidate = QuestionCandidate(question=question, source_ref=source_ref, priority=0)
                        ranked.append((0, relative.as_posix(), line_index, candidate))
                        continue
                marker = next((item for item in self._MARKERS if item in lowered), None)
                if marker is None:
                    continue
                snippet = _clip(_strip_markup(normalized), 180)
                if not snippet:
                    continue
                question = (
                    "What bounded repository evidence would most directly resolve or falsify this unresolved point: "
                    f"{snippet}?"
                )
                priority = 1 if "research question" in lowered or "open question" in lowered else 2
                candidate = QuestionCandidate(question=question, source_ref=source_ref, priority=priority)
                ranked.append((priority, relative.as_posix(), line_index, candidate))

        ranked.sort(key=lambda item: (item[0], item[1], item[2], item[3].question))
        unique: list[QuestionCandidate] = []
        seen: set[str] = set()
        for _, _, _, candidate in ranked:
            key = _question_key(candidate.question)
            if not key or key in seen:
                continue
            seen.add(key)
            unique.append(candidate)
            if len(unique) >= limit:
                break
        if unique:
            return tuple(unique)
        return (
            QuestionCandidate(
                question=(
                    "Which current repository claim has the strongest unresolved evidence gap, and what bounded "
                    "read-only check would reduce that uncertainty?"
                ),
                source_ref="REPOSITORY_FALLBACK",
                priority=9,
            ),
        )


class AutonomousInquiryCampaign:
    """Run a bounded AION/Astra research campaign over read-only repository evidence."""

    def __init__(
        self,
        root: Path,
        *,
        max_questions: int = 3,
        max_rounds: int = 3,
        evidence_limit: int = 4,
        repository_ref: str = "UNSPECIFIED",
    ) -> None:
        resolved = root.resolve()
        if not resolved.is_dir():
            raise ValueError("campaign root must be an existing directory")
        if not 1 <= max_questions <= 8:
            raise ValueError("max_questions must be between 1 and 8")
        self._root = resolved
        self._max_questions = max_questions
        self._max_rounds = max_rounds
        self._evidence_limit = evidence_limit
        self._repository_ref = repository_ref.strip() or "UNSPECIFIED"
        self._evidence_source = RepositoryTextEvidenceSource(resolved)
        self._question_generator = RepositoryQuestionGenerator(resolved)
        self._aion = ProviderBackedPeer(EvidenceDrivenReasoningProvider(AgentId.AION))
        self._astra = ProviderBackedPeer(EvidenceDrivenReasoningProvider(AgentId.ASTRA))

    @property
    def aion_private_notes(self) -> tuple[str, ...]:
        return self._aion.private_notes

    @property
    def astra_private_notes(self) -> tuple[str, ...]:
        return self._astra.private_notes

    def run(self, seed_questions: tuple[str, ...] = ()) -> InquiryCampaignReport:
        queue: list[QuestionCandidate] = []
        for index, question in enumerate(seed_questions):
            normalized = question.strip()
            if normalized:
                queue.append(
                    QuestionCandidate(
                        question=normalized,
                        source_ref=f"OWNER_SEED_{index + 1}",
                        priority=-1,
                    )
                )
        if not queue:
            queue.extend(self._question_generator.discover(limit=self._max_questions))

        reports: list[InquiryReport] = []
        considered: list[QuestionCandidate] = []
        seen: set[str] = set()
        while queue and len(reports) < self._max_questions:
            candidate = queue.pop(0)
            key = _question_key(candidate.question)
            if not key or key in seen:
                continue
            seen.add(key)
            considered.append(candidate)
            report = BoundedInquiryLoop(
                self._evidence_source,
                max_rounds=self._max_rounds,
                evidence_limit=self._evidence_limit,
            ).run(candidate.question, aion=self._aion, astra=self._astra)
            reports.append(report)
            if len(reports) >= self._max_questions:
                continue
            follow_up = _derive_follow_up(report)
            follow_key = _question_key(follow_up)
            if follow_up and follow_key and follow_key not in seen:
                queue.append(
                    QuestionCandidate(
                        question=follow_up,
                        source_ref=f"DERIVED_FROM_REPORT_{len(reports)}",
                        priority=3,
                    )
                )

        campaign_hash = _campaign_hash(tuple(reports), self._repository_ref)
        return InquiryCampaignReport(
            repository_root_name=self._root.name,
            repository_ref=self._repository_ref,
            questions_considered=tuple(considered),
            reports=tuple(reports),
            campaign_hash=campaign_hash,
        )


def campaign_to_dict(campaign: InquiryCampaignReport) -> dict[str, object]:
    return {
        "repository_root_name": campaign.repository_root_name,
        "repository_ref": campaign.repository_ref,
        "run_mode": campaign.run_mode,
        "scientific_disposition": campaign.scientific_disposition,
        "canonical_effect": campaign.canonical_effect,
        "repository_mutation": campaign.repository_mutation,
        "network_access": campaign.network_access,
        "deployment": campaign.deployment,
        "autonomous_merge": campaign.autonomous_merge,
        "campaign_hash": campaign.campaign_hash,
        "questions_considered": [
            {
                "question": item.question,
                "source_ref": item.source_ref,
                "priority": item.priority,
            }
            for item in campaign.questions_considered
        ],
        "reports": [_report_to_dict(report) for report in campaign.reports],
    }


def campaign_to_markdown(campaign: InquiryCampaignReport) -> str:
    lines = [
        "# AION / Astra bounded inquiry report",
        "",
        f"- repository ref: `{campaign.repository_ref}`",
        f"- mode: `{campaign.run_mode}`",
        f"- scientific disposition: `{campaign.scientific_disposition}`",
        f"- canonical effect: `{campaign.canonical_effect}`",
        f"- campaign hash: `{campaign.campaign_hash}`",
        "",
    ]
    for index, report in enumerate(campaign.reports, start=1):
        source_ref = campaign.questions_considered[index - 1].source_ref
        lines.extend(
            [
                f"## Inquiry {index}",
                "",
                f"Question: {report.question}",
                "",
                f"Source: `{source_ref}`",
                "",
                f"Stop reason: `{report.stop_reason.value}`",
                "",
                "Candidate findings:",
            ]
        )
        for finding in report.candidate_findings:
            lines.append(f"- {_clip(finding, 500)}")
        if not report.candidate_findings:
            lines.append("- none")
        lines.extend(["", "Evidence refs:"])
        if report.evidence:
            for item in report.evidence:
                lines.append(f"- `{item.ref}` (`{item.content_sha256[:12]}…`)")
        else:
            lines.append("- none retrieved")
        lines.extend(["", f"Dialogue chain: `{report.final_chain_hash}`", ""])
    lines.extend(
        [
            "## Authority and epistemic boundary",
            "",
            "`AUTONOMOUS_INQUIRY = BOUNDED`",
            "",
            "`AUTONOMOUS_REPOSITORY_MUTATION = NO`",
            "",
            "`AUTONOMOUS_NETWORK_ACCESS = NO`",
            "",
            "`AUTONOMOUS_MERGE = NO`",
            "",
            "`PEER_CONSENSUS != SCIENTIFIC_TRUTH`",
            "",
            "`ENGINEERING_BEHAVIOR != SUBJECTIVITY_EVIDENCE`",
            "",
        ]
    )
    return "\n".join(lines)


def write_campaign_report(campaign: InquiryCampaignReport, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "campaign.json"
    markdown_path = output_dir / "campaign.md"
    json_path.write_text(json.dumps(campaign_to_dict(campaign), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(campaign_to_markdown(campaign) + "\n", encoding="utf-8")
    return json_path, markdown_path


def _report_to_dict(report: InquiryReport) -> dict[str, object]:
    return {
        "question": report.question,
        "stop_reason": report.stop_reason.value,
        "candidate_findings": list(report.candidate_findings),
        "final_chain_hash": report.final_chain_hash,
        "scientific_disposition": report.scientific_disposition,
        "canonical_effect": report.canonical_effect,
        "deployment": report.deployment,
        "autonomous_merge": report.autonomous_merge,
        "evidence": [
            {
                "ref": item.ref,
                "excerpt": item.excerpt,
                "content_sha256": item.content_sha256,
            }
            for item in report.evidence
        ],
        "transcript": [
            {
                "sequence": event.sequence,
                "round_index": event.round_index,
                "speaker": event.speaker.value,
                "claim": event.claim,
                "challenge": event.challenge,
                "evidence_query": event.evidence_query,
                "evidence_refs": list(event.evidence_refs),
                "probe_kind": event.probe_kind.value if event.probe_kind else None,
                "probe_description": event.probe_description,
                "stop_vote": event.stop_vote,
                "previous_hash": event.previous_hash,
                "event_hash": event.event_hash,
            }
            for event in report.transcript
        ],
    }


def _derive_follow_up(report: InquiryReport) -> str:
    challenge = next((event.challenge for event in reversed(report.transcript) if event.challenge.strip()), "")
    if challenge:
        return _clip(
            "Which repository evidence or bounded counterexample most directly resolves this peer challenge: " + challenge,
            360,
        )
    if not report.evidence:
        return _clip(
            "Which repository artifact can directly support or falsify the unresolved question: " + report.question,
            360,
        )
    return ""


def _campaign_hash(reports: tuple[InquiryReport, ...], repository_ref: str) -> str:
    payload = {
        "repository_ref": repository_ref,
        "reports": [
            {
                "question": report.question,
                "final_chain_hash": report.final_chain_hash,
                "evidence": [(item.ref, item.content_sha256) for item in report.evidence],
            }
            for report in reports
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256(encoded).hexdigest()


def _clean_question(line: str) -> str:
    cleaned = _strip_markup(line)
    if "?" in cleaned:
        cleaned = cleaned[: cleaned.find("?") + 1]
    elif "？" in cleaned:
        cleaned = cleaned[: cleaned.find("？") + 1]
    cleaned = cleaned.strip(" -#*>`\t")
    if len(cleaned) < 18:
        return ""
    return _clip(cleaned, 300)


def _strip_markup(text: str) -> str:
    value = re.sub(r"[`*_#>|]", " ", text)
    value = re.sub(r"\[[^\]]+\]\([^\)]+\)", " ", value)
    return " ".join(value.split()).strip()


def _question_key(question: str) -> str:
    return re.sub(r"\W+", " ", question.lower(), flags=re.UNICODE).strip()


def _clip(text: str, limit: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"
