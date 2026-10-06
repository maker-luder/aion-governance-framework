from __future__ import annotations

import importlib
import json
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .heuristic_reveal import HeuristicRevealReport, reveal_hidden_image_file


class MediaKind(StrEnum):
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    TEXT = "TEXT"
    OTHER = "OTHER"


class SignalType(StrEnum):
    C2PA = "C2PA"
    SYNTHID = "SYNTHID"
    TEXTGRAIN = "TEXTGRAIN"
    SYNTHID_TEXT = "SYNTHID_TEXT"


class SignalOutcome(StrEnum):
    DETECTED = "DETECTED"
    NOT_DETECTED = "NOT_DETECTED"
    KEY_REQUIRED = "KEY_REQUIRED"
    LOCAL_VERIFIER_NOT_PUBLIC = "LOCAL_VERIFIER_NOT_PUBLIC"
    DEPENDENCY_REQUIRED = "DEPENDENCY_REQUIRED"
    NOT_CHECKED = "NOT_CHECKED"


@dataclass(frozen=True, slots=True)
class SignalEvidence:
    signal_type: SignalType
    outcome: SignalOutcome
    validation_state: str | None = None
    issuer: str | None = None
    model: str | None = None
    generated_at: str | None = None
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


def _nested_strings(value: Any) -> tuple[str, ...]:
    found: list[str] = []
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, Mapping):
        for item in value.values():
            found.extend(_nested_strings(item))
    elif isinstance(value, list | tuple):
        for item in value:
            found.extend(_nested_strings(item))
    return tuple(found)


def _first_string(
    mapping: Mapping[str, Any],
    keys: tuple[str, ...],
) -> str | None:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def report_from_c2pa_manifest_store(
    manifest_store: Mapping[str, Any],
    *,
    media_kind: MediaKind,
) -> ProvenanceVisibilityReport:
    active_label = manifest_store.get("active_manifest")
    manifests = manifest_store.get("manifests")

    if not isinstance(active_label, str) or not active_label:
        evidence = SignalEvidence(
            signal_type=SignalType.C2PA,
            outcome=SignalOutcome.NOT_DETECTED,
            source="LOCAL_C2PA_READER",
            detail="No active C2PA manifest was present in the local reader output.",
        )
        return ProvenanceVisibilityReport(
            media_kind=media_kind,
            signals=(evidence,),
            verdict="NO_C2PA_MANIFEST_DETECTED",
            visible_label_zh_tw=(
                "本機未讀到 C2PA Content Credentials；"
                "這不代表內容一定不是 AI 產生或處理。"
            ),
        )

    if not isinstance(manifests, Mapping):
        raise ValueError("C2PA manifest store has active_manifest but no manifests mapping")

    raw_manifest = manifests.get(active_label)
    if not isinstance(raw_manifest, Mapping):
        raise ValueError("active C2PA manifest is missing from manifests mapping")

    strings = _nested_strings(raw_manifest)
    lowered = tuple(item.lower() for item in strings)
    invalid_markers = ("invalid", "mismatch", "untrusted", "failure", "error")
    has_validation_problem = any(
        marker in item for item in lowered for marker in invalid_markers
    )
    validation_state = (
        "PRESENT_WITH_VALIDATION_WARNING"
        if has_validation_problem
        else "PRESENT_NO_WARNING_FOUND_IN_READER_REPORT"
    )

    issuer = _first_string(
        raw_manifest,
        ("issuer", "claim_generator", "claim_generator_info"),
    )
    model = _first_string(
        raw_manifest,
        ("model", "generator_model", "model_name"),
    )
    generated_at = _first_string(
        raw_manifest,
        ("generated_at", "date", "timestamp", "time"),
    )

    evidence = SignalEvidence(
        signal_type=SignalType.C2PA,
        outcome=SignalOutcome.DETECTED,
        validation_state=validation_state,
        issuer=issuer,
        model=model,
        generated_at=generated_at,
        source="LOCAL_C2PA_READER",
        detail=f"active_manifest={active_label}",
    )
    label = "本機已讀到 C2PA Content Credentials。"
    if has_validation_problem:
        label += " 驗證報告同時出現警告／不信任／錯誤訊號，不能標成可信來源。"

    return ProvenanceVisibilityReport(
        media_kind=media_kind,
        signals=(evidence,),
        verdict="C2PA_MANIFEST_DETECTED",
        visible_label_zh_tw=label,
    )


class ProvenanceVisibilityAgent:
    """Local-first provenance verifier and disclosure renderer."""

    def verify_c2pa_local(
        self,
        path: str | Path,
        media_kind: MediaKind,
        *,
        trust_anchors_pem: str | None = None,
    ) -> ProvenanceVisibilityReport:
        file_path = Path(path)
        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        try:
            c2pa = importlib.import_module("c2pa")
        except ImportError:
            evidence = SignalEvidence(
                signal_type=SignalType.C2PA,
                outcome=SignalOutcome.DEPENDENCY_REQUIRED,
                source="LOCAL_C2PA_READER",
                detail="Install the optional c2pa-python dependency.",
            )
            return ProvenanceVisibilityReport(
                media_kind=media_kind,
                signals=(evidence,),
                verdict="LOCAL_C2PA_DEPENDENCY_REQUIRED",
                visible_label_zh_tw=(
                    "本機 C2PA 驗證元件尚未安裝；未上傳檔案，也未呼叫遠端 API。"
                ),
            )

        settings: dict[str, Any] = {
            "verify": {
                "verify_after_reading": True,
                "verify_trust": True,
                "verify_timestamp_trust": True,
                "remote_manifest_fetch": False,
            }
        }
        if trust_anchors_pem:
            settings["trust"] = {"user_anchors": trust_anchors_pem}

        context = c2pa.Context.from_dict(settings)
        with c2pa.Reader(str(file_path), context=context) as reader:
            raw = reader.json()

        parsed = json.loads(raw)
        if not isinstance(parsed, Mapping):
            raise ValueError("C2PA reader returned a non-object manifest store")

        return report_from_c2pa_manifest_store(parsed, media_kind=media_kind)

    def reveal_hidden_image_signal_local(
        self,
        path: str | Path,
        *,
        output_dir: str | Path | None = None,
    ) -> HeuristicRevealReport:
        """Surface local image residual/bit-plane/periodic cues without a detector claim."""

        return reveal_hidden_image_file(path, output_dir=output_dir)

    def textgrain_without_secret_key(self) -> ProvenanceVisibilityReport:
        evidence = SignalEvidence(
            signal_type=SignalType.TEXTGRAIN,
            outcome=SignalOutcome.KEY_REQUIRED,
            source="OPENAI_TEXTGRAIN_TECHNICAL_REPORT",
            detail=(
                "The published detection procedure requires the secret key plus "
                "matching tokenizer/configuration. The deployed OpenAI key is not public."
            ),
        )
        return ProvenanceVisibilityReport(
            media_kind=MediaKind.TEXT,
            signals=(evidence,),
            verdict="TEXTGRAIN_NOT_LOCALLY_VERIFIABLE_WITHOUT_KEY",
            visible_label_zh_tw=(
                "textGrain 的檢測程序需要秘密金鑰與相符設定；"
                "目前沒有這些必要材料，因此不能本機判定。"
            ),
        )

    def text_with_local_keyed_detector(
        self,
        text: str,
        detector: Callable[[str], bool],
        *,
        signal_type: SignalType,
    ) -> ProvenanceVisibilityReport:
        if signal_type not in {SignalType.TEXTGRAIN, SignalType.SYNTHID_TEXT}:
            raise ValueError("local keyed text detector must be a text watermark detector")
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

    def synthid_media_local_capability(
        self,
        media_kind: MediaKind,
    ) -> ProvenanceVisibilityReport:
        if media_kind not in {MediaKind.IMAGE, MediaKind.AUDIO}:
            raise ValueError("media SynthID capability applies only to image/audio")
        evidence = SignalEvidence(
            signal_type=SignalType.SYNTHID,
            outcome=SignalOutcome.LOCAL_VERIFIER_NOT_PUBLIC,
            source="PUBLIC_TECHNOLOGY_AUDIT",
            detail=(
                "No public general-purpose local verifier was found for the "
                "OpenAI-used image/audio SynthID signal."
            ),
        )
        return ProvenanceVisibilityReport(
            media_kind=media_kind,
            signals=(evidence,),
            verdict="SYNTHID_LOCAL_VERIFIER_NOT_PUBLIC",
            visible_label_zh_tw=(
                "目前沒有找到可獨立驗證 OpenAI 圖片／音訊 SynthID 的"
                "公開泛用本機 detector；本 agent 不會用分類器冒充浮水印驗證。"
            ),
        )


def render_markdown(report: ProvenanceVisibilityReport) -> str:
    lines = [
        "# 來源訊號可視化報告",
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
        if item.validation_state:
            detail.append(f"validation={item.validation_state}")
        if item.issuer:
            detail.append(f"issuer={item.issuer}")
        if item.model:
            detail.append(f"model={item.model}")
        if item.generated_at:
            detail.append(f"generated_at={item.generated_at}")
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
            "- 不用一般 AI classifier 冒充 watermark detector。",
            "- 不提供浮水印移除、破壞或規避功能。",
        ]
    )
    return "\n".join(lines) + "\n"
