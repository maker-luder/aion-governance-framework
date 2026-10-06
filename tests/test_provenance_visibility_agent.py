from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "provenance-visibility-agent_v0.1.0" / "src"
sys.path.insert(0, str(SRC))

from aion_provenance_visibility_agent import (  # noqa: E402
    MediaKind,
    ProvenanceVisibilityAgent,
    SignalOutcome,
    SignalType,
    render_markdown,
)


def test_image_c2pa_and_synthid_are_made_visible() -> None:
    payload = {
        "results": [
            {
                "type": "c2pa",
                "outcome": "detected",
                "validation_state": "trusted",
                "issuer": "OpenAI OpCo, LLC",
                "model": "gpt-image",
                "generated_at": "2026-07-27T18:34:12Z",
            },
            {
                "type": "synthid",
                "outcome": "detected",
                "model": None,
                "generated_at": None,
            },
        ]
    }
    report = ProvenanceVisibilityAgent().from_openai_payload(
        MediaKind.IMAGE,
        payload,
    )
    assert report.verdict == "SUPPORTED_PROVENANCE_SIGNAL_DETECTED"
    assert "C2PA" in report.visible_label_zh_tw
    assert "SYNTHID" in report.visible_label_zh_tw
    assert report.signals[0].signal_type is SignalType.C2PA
    assert report.signals[0].outcome is SignalOutcome.DETECTED


def test_not_detected_never_becomes_human_created_claim() -> None:
    report = ProvenanceVisibilityAgent().from_openai_payload(
        MediaKind.AUDIO,
        {"results": [{"type": "synthid", "outcome": "not_detected"}]},
    )
    assert report.verdict == "NO_SUPPORTED_SIGNAL_DETECTED"
    assert report.not_detected_is_not_human_proof is True
    assert "不代表" in report.visible_label_zh_tw


def test_text_without_approved_detector_fails_to_unknown_not_guess() -> None:
    report = ProvenanceVisibilityAgent().text_without_detector()
    assert report.verdict == "VERIFICATION_ACCESS_REQUIRED"
    assert report.signals[0].signal_type is SignalType.TEXTGRAIN
    assert report.signals[0].outcome is SignalOutcome.ACCESS_REQUIRED


def test_approved_text_detector_result_can_be_rendered() -> None:
    agent = ProvenanceVisibilityAgent()
    detected = agent.text_with_approved_detector(
        "sample text",
        detector=lambda _text: True,
    )
    not_detected = agent.text_with_approved_detector(
        "sample text",
        detector=lambda _text: False,
    )
    assert detected.verdict == "SUPPORTED_PROVENANCE_SIGNAL_DETECTED"
    assert not_detected.verdict == "NO_SUPPORTED_SIGNAL_DETECTED"


def test_empty_text_is_rejected() -> None:
    with pytest.raises(ValueError):
        ProvenanceVisibilityAgent().text_with_approved_detector(
            "   ",
            detector=lambda _text: False,
        )


def test_invalid_c2pa_cannot_be_called_detected() -> None:
    with pytest.raises(ValueError, match="detected C2PA"):
        ProvenanceVisibilityAgent().from_openai_payload(
            MediaKind.IMAGE,
            {
                "results": [
                    {
                        "type": "c2pa",
                        "outcome": "detected",
                        "validation_state": "invalid",
                    }
                ]
            },
        )


def test_signal_type_must_match_media_kind() -> None:
    with pytest.raises(ValueError, match="not applicable"):
        ProvenanceVisibilityAgent().from_openai_payload(
            MediaKind.AUDIO,
            {
                "results": [
                    {
                        "type": "c2pa",
                        "outcome": "not_detected",
                        "validation_state": "not_present",
                    }
                ]
            },
        )


def test_markdown_is_explicit_and_non_inferential() -> None:
    report = ProvenanceVisibilityAgent().from_openai_payload(
        MediaKind.IMAGE,
        {
            "results": [
                {
                    "type": "c2pa",
                    "outcome": "detected",
                    "validation_state": "valid",
                    "issuer": "OpenAI OpCo, LLC",
                }
            ]
        },
    )
    rendered = render_markdown(report)
    assert "來源訊號可視化報告" in rendered
    assert "issuer=OpenAI OpCo, LLC" in rendered
    assert "不等於證明作者" in rendered
    assert "不提供浮水印移除" in rendered
