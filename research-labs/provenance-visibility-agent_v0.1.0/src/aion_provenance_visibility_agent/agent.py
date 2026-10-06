from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .text_reveal import (
    TextRevealReport,
    reveal_hidden_text_bytes,
    reveal_hidden_text_signal,
)


class MediaKind(StrEnum):
    TEXT = "TEXT"


class SignalType(StrEnum):
    TEXTGRAIN = "TEXTGRAIN"
    SYNTHID_TEXT = "SYNTHID_TEXT"


class SignalOutcome(StrEnum):
    DETECTED = "DETECTED"
    NOT_DETECTED = "NOT_DETECTED"
    KEY_REQUIRED = "KEY_REQUIRED"


@dataclass(frozen=True, slots=True)
class SignalEvidence:
    signal_type: SignalType
    outcome: SignalOutcome
    source: str = "LOCAL_VERIFICATION"
    detail: str | None = None


@dataclass(frozen=True, slots=True)
class ProvenanceVisibilityReport:
    media_kind: MediaKind
    signals: tuple[SignalEvidence, ...]
    verdict: str
    visible_label_zh_tw: str
    local_only: bool = True
    network_required: bool = False
    not_detected_is_not_human_proof: bool = True
    detected_is_not_authorship_proof: bool = True
    personal_identity_inference: str = "PROHIBITED"
    prompt_inference: str = "PROHIBITED"
    watermark_removal_or_evasion: str = "OUT_OF_SCOPE"
    canonical_effect: str = "NONE"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProvenanceVisibilityAgent:
    """Text-only local provenance visibility and human-readable reveal surface."""

    def reveal_hidden_text_signal_local(self, text: str) -> TextRevealReport:
        """Reveal machine-visible text structure from an in-memory string."""

        return reveal_hidden_text_signal(text)

    def reveal_hidden_text_bytes_local(self, data: bytes) -> TextRevealReport:
        """Reveal text structure while preserving byte-level source evidence."""

        return reveal_hidden_text_bytes(data)

    def reveal_hidden_text_file_local(self, path: str | Path) -> TextRevealReport:
        """Read a local text file as bytes and preserve source evidence before decoding."""

        file_path = Path(path)
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        return reveal_hidden_text_bytes(file_path.read_bytes())

    def textgrain_without_secret_key(self) -> ProvenanceVisibilityReport:
        evidence = SignalEvidence(
            signal_type=SignalType.TEXTGRAIN,
            outcome=SignalOutcome.KEY_REQUIRED,
            source="OPENAI_TEXTGRAIN_TECHNICAL_REPORT",
            detail=(
                "The published detection procedure requires the secret key plus "
                "matching tokenizer/configuration. Those required materials are "
                "not available to this generic local verifier."
            ),
        )
        return ProvenanceVisibilityReport(
            media_kind=MediaKind.TEXT,
            signals=(evidence,),
            verdict="TEXTGRAIN_NOT_LOCALLY_VERIFIABLE_WITHOUT_KEY",
            visible_label_zh_tw=(
                "textGrain 的精確檢測需要秘密金鑰與相符 tokenizer／設定；"
                "目前缺少必要材料，所以只能顯現可觀察文字證據，不能冒充正式 detector。"
            ),
        )

    def text_with_local_keyed_detector(
        self,
        text: str,
        detector: Callable[[str], bool],
        *,
        signal_type: SignalType,
    ) -> ProvenanceVisibilityReport:
        if not text.strip():
            raise ValueError("text must not be empty")

        detected = bool(detector(text))
        evidence = SignalEvidence(
            signal_type=signal_type,
            outcome=(
                SignalOutcome.DETECTED
                if detected
                else SignalOutcome.NOT_DETECTED
            ),
            source="LOCAL_KEYED_TEXT_DETECTOR",
        )
        if detected:
            verdict = "SUPPORTED_LOCAL_TEXT_SIGNAL_DETECTED"
            label = f"本機 keyed detector 偵測到 {signal_type.value} 訊號。"
        else:
            verdict = "NO_SUPPORTED_LOCAL_TEXT_SIGNAL_DETECTED"
            label = (
                f"本機 keyed detector 未偵測到 {signal_type.value} 訊號；"
                "這不代表文字一定由人類撰寫。"
            )

        return ProvenanceVisibilityReport(
            media_kind=MediaKind.TEXT,
            signals=(evidence,),
            verdict=verdict,
            visible_label_zh_tw=label,
        )


def render_markdown(report: ProvenanceVisibilityReport) -> str:
    lines = [
        "# 文字來源訊號可視化報告",
        "",
        f"- 媒體類型：{report.media_kind.value}",
        f"- 判定：{report.verdict}",
        f"- 本機處理：{'是' if report.local_only else '否'}",
        f"- 需要網路：{'是' if report.network_required else '否'}",
        f"- 明示標籤：{report.visible_label_zh_tw}",
        "",
        "## 訊號",
    ]
    for item in report.signals:
        detail = [item.signal_type.value, item.outcome.value]
        if item.detail:
            detail.append(f"detail={item.detail}")
        lines.append("- " + " | ".join(detail))

    lines.extend(
        [
            "",
            "## 解讀邊界",
            "- 未偵測到訊號，不等於證明內容由人類創作。",
            "- 偵測到訊號，不等於證明作者、所有權或人類參與比例。",
            "- 不推論使用者身分、帳號或 prompt。",
            "- 不用一般 AI classifier 冒充 text watermark detector。",
            "- 不連接 hosted provenance API。",
            "- 不提供浮水印移除、破壞或規避功能。",
        ]
    )
    return "\n".join(lines) + "\n"
