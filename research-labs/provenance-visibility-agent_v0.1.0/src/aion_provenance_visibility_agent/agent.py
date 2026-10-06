from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any


class MediaKind(StrEnum):
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    TEXT = "TEXT"


class SignalType(StrEnum):
    C2PA = "C2PA"
    SYNTHID = "SYNTHID"
    TEXTGRAIN = "TEXTGRAIN"


class SignalOutcome(StrEnum):
    DETECTED = "DETECTED"
    NOT_DETECTED = "NOT_DETECTED"
    ACCESS_REQUIRED = "ACCESS_REQUIRED"
    NOT_CHECKED = "NOT_CHECKED"


@dataclass(frozen=True, slots=True)
class SignalEvidence:
    signal_type: SignalType
    outcome: SignalOutcome
    validation_state: str | None = None
    issuer: str | None = None
    model: str | None = None
    generated_at: str | None = None
    source: str = "OPENAI_CONTENT_PROVENANCE"

    def __post_init__(self) -> None:
        if self.signal_type is SignalType.C2PA and self.outcome is SignalOutcome.DETECTED:
            if self.validation_state not in {"trusted", "valid"}:
                raise ValueError("detected C2PA requires trusted or valid validation state")


@dataclass(frozen=True, slots=True)
class ProvenanceVisibilityReport:
    media_kind: MediaKind
    signals: tuple[SignalEvidence, ...]
    verdict: str
    visible_label_zh_tw: str
    not_detected_is_not_human_proof: bool = True
    detected_is_not_authorship_proof: bool = True
    personal_identity_inference: str = "PROHIBITED"
    prompt_inference: str = "PROHIBITED"
    watermark_removal_or_evasion: str = "OUT_OF_SCOPE"
    canonical_effect: str = "NONE"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _signal_type(raw: str) -> SignalType:
    normalized = raw.strip().lower()
    if normalized == "c2pa":
        return SignalType.C2PA
    if normalized == "synthid":
        return SignalType.SYNTHID
    if normalized == "textgrain":
        return SignalType.TEXTGRAIN
    raise ValueError(f"unsupported provenance signal type: {raw}")


def _signal_outcome(raw: str) -> SignalOutcome:
    normalized = raw.strip().lower()
    if normalized == "detected":
        return SignalOutcome.DETECTED
    if normalized == "not_detected":
        return SignalOutcome.NOT_DETECTED
    raise ValueError(f"unsupported provenance signal outcome: {raw}")


def normalize_openai_provenance_payload(
    media_kind: MediaKind,
    payload: Mapping[str, Any],
) -> tuple[SignalEvidence, ...]:
    raw_results = payload.get("results", ())
    if not isinstance(raw_results, Sequence) or isinstance(raw_results, (str, bytes)):
        raise ValueError("provider payload results must be a sequence")

    signals: list[SignalEvidence] = []
    for raw in raw_results:
        if not isinstance(raw, Mapping):
            raise ValueError("each provider result must be a mapping")
        signal_type = _signal_type(str(raw.get("type", "")))
        outcome = _signal_outcome(str(raw.get("outcome", "")))
        signals.append(
            SignalEvidence(
                signal_type=signal_type,
                outcome=outcome,
                validation_state=(
                    str(raw["validation_state"])
                    if raw.get("validation_state") is not None
                    else None
                ),
                issuer=str(raw["issuer"]) if raw.get("issuer") is not None else None,
                model=str(raw["model"]) if raw.get("model") is not None else None,
                generated_at=(
                    str(raw["generated_at"])
                    if raw.get("generated_at") is not None
                    else None
                ),
            )
        )

    allowed = {
        MediaKind.IMAGE: {SignalType.C2PA, SignalType.SYNTHID},
        MediaKind.AUDIO: {SignalType.SYNTHID},
        MediaKind.TEXT: {SignalType.TEXTGRAIN},
    }[media_kind]
    if any(item.signal_type not in allowed for item in signals):
        raise ValueError("provider payload contains a signal not applicable to media kind")
    return tuple(signals)


def _visible_label(
    media_kind: MediaKind,
    signals: tuple[SignalEvidence, ...],
) -> tuple[str, str]:
    detected = tuple(item for item in signals if item.outcome is SignalOutcome.DETECTED)
    access_required = tuple(
        item for item in signals if item.outcome is SignalOutcome.ACCESS_REQUIRED
    )

    if detected:
        names = "、".join(item.signal_type.value for item in detected)
        return (
            "SUPPORTED_PROVENANCE_SIGNAL_DETECTED",
            f"已偵測到受支援的隱藏來源訊號：{names}。",
        )
    if access_required:
        names = "、".join(item.signal_type.value for item in access_required)
        return (
            "VERIFICATION_ACCESS_REQUIRED",
            f"此內容的來源訊號需要額外驗證權限：{names}；目前不能判定。",
        )
    if signals and all(
        item.outcome is SignalOutcome.NOT_DETECTED for item in signals
    ):
        return (
            "NO_SUPPORTED_SIGNAL_DETECTED",
            "未偵測到受支援的來源訊號；這不代表內容一定是人類創作。",
        )
    return (
        "VERIFICATION_NOT_ESTABLISHED",
        f"{media_kind.value} 的來源訊號目前沒有足夠證據可判定。",
    )


class ProvenanceVisibilityAgent:
    """Turn supported hidden provenance signals into explicit, human-visible reports."""

    def from_openai_payload(
        self,
        media_kind: MediaKind,
        payload: Mapping[str, Any],
    ) -> ProvenanceVisibilityReport:
        signals = normalize_openai_provenance_payload(media_kind, payload)
        verdict, label = _visible_label(media_kind, signals)
        return ProvenanceVisibilityReport(
            media_kind=media_kind,
            signals=signals,
            verdict=verdict,
            visible_label_zh_tw=label,
        )

    def text_without_detector(self) -> ProvenanceVisibilityReport:
        signals = (
            SignalEvidence(
                signal_type=SignalType.TEXTGRAIN,
                outcome=SignalOutcome.ACCESS_REQUIRED,
                source="OPENAI_TEXT_DETECTOR_ACCESS_REQUIRED",
            ),
        )
        verdict, label = _visible_label(MediaKind.TEXT, signals)
        return ProvenanceVisibilityReport(
            media_kind=MediaKind.TEXT,
            signals=signals,
            verdict=verdict,
            visible_label_zh_tw=label,
        )

    def text_with_approved_detector(
        self,
        text: str,
        detector: Callable[[str], bool],
    ) -> ProvenanceVisibilityReport:
        if not text.strip():
            raise ValueError("text must not be empty")
        detected = bool(detector(text))
        signals = (
            SignalEvidence(
                signal_type=SignalType.TEXTGRAIN,
                outcome=(
                    SignalOutcome.DETECTED
                    if detected
                    else SignalOutcome.NOT_DETECTED
                ),
                source="APPROVED_TEXT_DETECTOR",
            ),
        )
        verdict, label = _visible_label(MediaKind.TEXT, signals)
        return ProvenanceVisibilityReport(
            media_kind=MediaKind.TEXT,
            signals=signals,
            verdict=verdict,
            visible_label_zh_tw=label,
        )

    def verify_file_with_openai(
        self,
        path: str | Path,
        media_kind: MediaKind,
    ) -> ProvenanceVisibilityReport:
        if media_kind not in {MediaKind.IMAGE, MediaKind.AUDIO}:
            raise ValueError("public Content Provenance API currently supports image/audio")
        file_path = Path(path)
        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI SDK is required for live provenance verification"
            ) from exc

        client = OpenAI()
        with file_path.open("rb") as handle:
            response = client.content_provenance_checks.create(file=handle)

        if hasattr(response, "model_dump"):
            payload = response.model_dump(mode="json")
        elif isinstance(response, Mapping):
            payload = dict(response)
        else:
            raise RuntimeError("unsupported OpenAI SDK provenance response type")
        return self.from_openai_payload(media_kind, payload)


def render_markdown(report: ProvenanceVisibilityReport) -> str:
    lines = [
        "# 來源訊號可視化報告",
        "",
        f"- 媒體類型：{report.media_kind.value}",
        f"- 判定：{report.verdict}",
        f"- 明示標籤：{report.visible_label_zh_tw}",
        "",
        "## 訊號",
    ]
    if not report.signals:
        lines.append("- 無可用訊號。")
    for item in report.signals:
        detail = [item.signal_type.value, item.outcome.value]
        if item.validation_state:
            detail.append(f"validation={item.validation_state}")
        if item.issuer:
            detail.append(f"issuer={item.issuer}")
        if item.model:
            detail.append(f"model={item.model}")
        if item.generated_at:
            detail.append(f"generated_at={item.generated_at}")
        lines.append("- " + " | ".join(detail))

    lines.extend(
        [
            "",
            "## 必要限制",
            "- 未偵測到訊號，不等於證明內容由人類創作。",
            "- 偵測到訊號，不等於證明作者、所有權或人類參與比例。",
            "- 不推論使用者身分、帳號或 prompt。",
            "- 本 agent 不提供浮水印移除、破壞或規避功能。",
        ]
    )
    return "\n".join(lines) + "\n"
