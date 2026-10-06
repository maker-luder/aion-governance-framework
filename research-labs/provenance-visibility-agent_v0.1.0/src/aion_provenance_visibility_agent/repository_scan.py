from __future__ import annotations

import codecs
import hashlib
import json
import os
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .text_reveal import CueKind, EvidenceFamily, TextRevealReport, reveal_hidden_text_bytes


DEFAULT_IGNORED_DIRECTORIES: tuple[str, ...] = (
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
)
DEFAULT_MAX_FILE_BYTES = 1_048_576


class ScanStatus(StrEnum):
    ANALYZED = "ANALYZED"
    EMPTY = "EMPTY"
    SKIPPED_TOO_LARGE = "SKIPPED_TOO_LARGE"
    SKIPPED_BINARY = "SKIPPED_BINARY"
    DECODE_ERROR = "DECODE_ERROR"
    READ_ERROR = "READ_ERROR"


@dataclass(frozen=True, slots=True)
class ScanPolicy:
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    ignored_directories: tuple[str, ...] = DEFAULT_IGNORED_DIRECTORIES

    def __post_init__(self) -> None:
        if self.max_file_bytes <= 0:
            raise ValueError("max_file_bytes must be positive")
        if any(not item or "/" in item or "\\" in item for item in self.ignored_directories):
            raise ValueError("ignored_directories must contain simple directory names")


@dataclass(frozen=True, slots=True)
class RepositoryFileResult:
    path: str
    status: ScanStatus
    byte_count: int
    sha256: str | None
    exact_evidence_count: int
    heuristic_evidence_count: int
    evidence_families: tuple[EvidenceFamily, ...]
    observations: tuple[str, ...]
    hypotheses: tuple[str, ...]
    watermark_verdict: str
    note_zh_tw: str


@dataclass(frozen=True, slots=True)
class FamilyAggregate:
    family: EvidenceFamily
    file_count: int
    evidence_record_count: int


@dataclass(frozen=True, slots=True)
class RepositoryScanReport:
    method: str
    root_label: str
    policy: ScanPolicy
    files: tuple[RepositoryFileResult, ...]
    family_aggregates: tuple[FamilyAggregate, ...]
    analyzed_files: int
    skipped_files: int
    files_with_exact_evidence: int
    files_with_heuristic_candidates: int
    watermark_verdict: str = "NOT_ESTABLISHED"
    authorship_inference: str = "PROHIBITED"
    vendor_attribution: str = "NOT_ESTABLISHED"
    source_files_modified: bool = False
    network_required: bool = False
    hosted_api_required: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _has_supported_unicode_bom(data: bytes) -> bool:
    return any(
        data.startswith(marker)
        for marker in (
            codecs.BOM_UTF8,
            codecs.BOM_UTF16_LE,
            codecs.BOM_UTF16_BE,
            codecs.BOM_UTF32_LE,
            codecs.BOM_UTF32_BE,
        )
    )


def _looks_binary(data: bytes) -> bool:
    if _has_supported_unicode_bom(data):
        return False
    return b"\x00" in data


def _relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _file_result_from_report(path: str, report: TextRevealReport) -> RepositoryFileResult:
    exact_count = sum(
        1 for item in report.evidence_ledger if item.evidence_kind is CueKind.EXACT
    )
    heuristic_count = sum(
        1 for item in report.evidence_ledger if item.evidence_kind is CueKind.HEURISTIC
    )
    observations = tuple(item.observation for item in report.evidence_ledger)

    if exact_count:
        note = (
            "存在可直接由來源 bytes／Unicode 結構確認的 machine-visible 特徵；"
            "這些特徵已轉成人類可讀證據，但不等於浮水印。"
        )
    elif heuristic_count:
        note = (
            "沒有 exact 隱藏特徵，但存在值得人工複核的 heuristic pattern candidate；"
            "不得把候選規律當成浮水印偵測。"
        )
    else:
        note = "目前本地視角沒有建立隱藏文字訊號；沒有結果也不證明不存在 keyed watermark。"

    return RepositoryFileResult(
        path=path,
        status=ScanStatus.ANALYZED,
        byte_count=report.raw_profile.byte_count,
        sha256=report.raw_profile.sha256,
        exact_evidence_count=exact_count,
        heuristic_evidence_count=heuristic_count,
        evidence_families=report.independent_families,
        observations=observations,
        hypotheses=report.hypotheses,
        watermark_verdict=report.watermark_verdict,
        note_zh_tw=note,
    )


def _skipped_result(
    path: str,
    status: ScanStatus,
    data: bytes | None,
    note: str,
) -> RepositoryFileResult:
    digest = hashlib.sha256(data).hexdigest() if data is not None else None
    return RepositoryFileResult(
        path=path,
        status=status,
        byte_count=len(data) if data is not None else 0,
        sha256=digest,
        exact_evidence_count=0,
        heuristic_evidence_count=0,
        evidence_families=(),
        observations=(),
        hypotheses=(),
        watermark_verdict="NOT_EVALUATED",
        note_zh_tw=note,
    )


def _candidate_paths(root: Path, policy: ScanPolicy) -> tuple[Path, ...]:
    paths: list[Path] = []
    for current_root, directory_names, file_names in os.walk(root):
        directory_names[:] = sorted(
            name for name in directory_names if name not in policy.ignored_directories
        )
        current = Path(current_root)
        for file_name in sorted(file_names):
            paths.append(current / file_name)
    return tuple(paths)


def scan_text_repository(
    root: str | Path,
    *,
    policy: ScanPolicy | None = None,
) -> RepositoryScanReport:
    """Scan local repository files without changing them or using network services."""

    root_path = Path(root)
    if not root_path.is_dir():
        raise NotADirectoryError(root_path)
    active_policy = policy or ScanPolicy()

    results: list[RepositoryFileResult] = []
    for path in _candidate_paths(root_path, active_policy):
        relative = _relative_path(root_path, path)
        try:
            size = path.stat().st_size
        except OSError as exc:
            results.append(
                _skipped_result(
                    relative,
                    ScanStatus.READ_ERROR,
                    None,
                    f"無法讀取檔案 metadata：{type(exc).__name__}",
                )
            )
            continue

        if size > active_policy.max_file_bytes:
            results.append(
                _skipped_result(
                    relative,
                    ScanStatus.SKIPPED_TOO_LARGE,
                    None,
                    (
                        f"檔案大小 {size} bytes 超過本次上限 "
                        f"{active_policy.max_file_bytes} bytes；未讀取內容。"
                    ),
                )
            )
            continue

        try:
            data = path.read_bytes()
        except OSError as exc:
            results.append(
                _skipped_result(
                    relative,
                    ScanStatus.READ_ERROR,
                    None,
                    f"無法讀取檔案：{type(exc).__name__}",
                )
            )
            continue

        if not data:
            results.append(
                _skipped_result(
                    relative,
                    ScanStatus.EMPTY,
                    data,
                    "空檔案；沒有可分析文字內容。",
                )
            )
            continue

        if _looks_binary(data):
            results.append(
                _skipped_result(
                    relative,
                    ScanStatus.SKIPPED_BINARY,
                    data,
                    "偵測到 NUL byte 且沒有支援的 Unicode BOM；以 binary 候選跳過。",
                )
            )
            continue

        try:
            report = reveal_hidden_text_bytes(data)
        except (UnicodeDecodeError, ValueError) as exc:
            results.append(
                _skipped_result(
                    relative,
                    ScanStatus.DECODE_ERROR,
                    data,
                    f"嚴格文字解碼失敗：{type(exc).__name__}；沒有使用 replacement characters。",
                )
            )
            continue

        results.append(_file_result_from_report(relative, report))

    results.sort(key=lambda item: item.path)
    analyzed = tuple(item for item in results if item.status is ScanStatus.ANALYZED)

    family_file_counts: dict[EvidenceFamily, int] = {}
    family_record_counts: dict[EvidenceFamily, int] = {}
    for item in analyzed:
        for family in item.evidence_families:
            family_file_counts[family] = family_file_counts.get(family, 0) + 1
        for observation in item.observations:
            del observation
        # The file summary intentionally counts independent family presence once per file.
        # Exact record totals are reconstructed conservatively from the available family set.
        for family in item.evidence_families:
            family_record_counts[family] = family_record_counts.get(family, 0) + 1

    family_aggregates = tuple(
        FamilyAggregate(
            family=family,
            file_count=family_file_counts[family],
            evidence_record_count=family_record_counts[family],
        )
        for family in sorted(family_file_counts, key=str)
    )

    return RepositoryScanReport(
        method="AION_REPOSITORY_TEXT_VISIBILITY_V0_3",
        root_label=root_path.name or ".",
        policy=active_policy,
        files=tuple(results),
        family_aggregates=family_aggregates,
        analyzed_files=len(analyzed),
        skipped_files=len(results) - len(analyzed),
        files_with_exact_evidence=sum(
            1 for item in analyzed if item.exact_evidence_count > 0
        ),
        files_with_heuristic_candidates=sum(
            1 for item in analyzed if item.heuristic_evidence_count > 0
        ),
    )


def render_repository_scan_markdown(report: RepositoryScanReport) -> str:
    lines = [
        "# Repository 文字隱藏訊號透明化報告",
        "",
        f"- 方法：{report.method}",
        f"- root label：{report.root_label}",
        f"- 已分析檔案：{report.analyzed_files}",
        f"- 跳過／無法分析：{report.skipped_files}",
        f"- 含 exact evidence 的檔案：{report.files_with_exact_evidence}",
        f"- 含 heuristic candidate 的檔案：{report.files_with_heuristic_candidates}",
        f"- 浮水印總判定：{report.watermark_verdict}",
        "- 來源檔案被修改：否",
        "- 需要網路：否",
        "- hosted API：否",
        "",
        "## Evidence-family matrix",
        "",
        "| family | files | independent family records |",
        "| --- | ---: | ---: |",
    ]
    if report.family_aggregates:
        for item in report.family_aggregates:
            lines.append(
                f"| {item.family.value} | {item.file_count} | {item.evidence_record_count} |"
            )
    else:
        lines.append("| 無 | 0 | 0 |")

    lines.extend(
        [
            "",
            "## 檔案摘要",
            "",
            "| path | status | exact | heuristic | families | verdict |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for item in report.files:
        families = ", ".join(family.value for family in item.evidence_families) or "—"
        lines.append(
            f"| {item.path} | {item.status.value} | {item.exact_evidence_count} | "
            f"{item.heuristic_evidence_count} | {families} | {item.watermark_verdict} |"
        )

    lines.extend(["", "## 有訊號檔案的可讀證據"])
    signaled = tuple(
        item
        for item in report.files
        if item.exact_evidence_count or item.heuristic_evidence_count
    )
    if not signaled:
        lines.append("- 無。")
    for item in signaled:
        lines.extend(
            [
                "",
                f"### {item.path}",
                f"- SHA-256：{item.sha256}",
                f"- observations：{', '.join(item.observations) or '無'}",
                f"- hypotheses：{', '.join(item.hypotheses) or '無'}",
                f"- 說明：{item.note_zh_tw}",
            ]
        )

    lines.extend(
        [
            "",
            "## 解讀邊界",
            "- REPOSITORY_SCAN = DISCOVERY_AND_VISIBILITY，不是作者或 vendor 判定器。",
            "- EXACT_TEXT_PROPERTY != WATERMARK_PROOF。",
            "- HEURISTIC_CANDIDATE != WATERMARK_DETECTION。",
            "- CUE_COUNT != INDEPENDENT_EVIDENCE_COUNT。",
            "- SAME_FAMILY_CUES 不重複計票成多條獨立證據。",
            "- NO_DEFINED_WATERMARK_NULL_MODEL = NO_VALID_WATERMARK_P_VALUE。",
            "- WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN。",
            "- NOT_DETECTED != HUMAN_CREATED。",
            "- 不推論作者、帳號、prompt 或模型身分。",
            "- 不修改來源檔案，也不提供浮水印移除、破壞或規避。",
        ]
    )
    return "\n".join(lines) + "\n"


def render_repository_scan_json(report: RepositoryScanReport) -> str:
    return json.dumps(report.as_dict(), ensure_ascii=False, indent=2) + "\n"
