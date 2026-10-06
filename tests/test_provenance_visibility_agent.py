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
    report_from_c2pa_manifest_store,
)


def test_local_c2pa_manifest_is_made_visible() -> None:
    report = report_from_c2pa_manifest_store(
        {
            "active_manifest": "urn:c2pa:test",
            "manifests": {
                "urn:c2pa:test": {
                    "issuer": "Example Issuer",
                    "model": "Example Model",
                    "generated_at": "2026-10-06T00:00:00Z",
                    "validation_status": ["valid"],
                }
            },
        },
        media_kind=MediaKind.IMAGE,
    )
    assert report.verdict == "C2PA_MANIFEST_DETECTED"
    assert report.local_only is True
    assert report.network_required is False
    assert report.signals[0].signal_type is SignalType.C2PA
    assert report.signals[0].outcome is SignalOutcome.DETECTED
    assert report.signals[0].issuer == "Example Issuer"


def test_c2pa_warning_is_not_misrepresented_as_trusted() -> None:
    report = report_from_c2pa_manifest_store(
        {
            "active_manifest": "urn:c2pa:test",
            "manifests": {
                "urn:c2pa:test": {
                    "validation_status": ["signingCredential.untrusted"],
                }
            },
        },
        media_kind=MediaKind.IMAGE,
    )
    assert report.signals[0].validation_state == "PRESENT_WITH_VALIDATION_WARNING"
    assert "不能標成可信來源" in report.visible_label_zh_tw


def test_no_c2pa_is_unknown_not_human_proof() -> None:
    report = report_from_c2pa_manifest_store(
        {"active_manifest": None, "manifests": {}},
        media_kind=MediaKind.IMAGE,
    )
    assert report.verdict == "NO_C2PA_MANIFEST_DETECTED"
    assert report.not_detected_is_not_human_proof is True
    assert "不代表" in report.visible_label_zh_tw


def test_textgrain_without_secret_key_fails_to_unknown() -> None:
    report = ProvenanceVisibilityAgent().textgrain_without_secret_key()
    assert report.verdict == "TEXTGRAIN_NOT_LOCALLY_VERIFIABLE_WITHOUT_KEY"
    assert report.signals[0].signal_type is SignalType.TEXTGRAIN
    assert report.signals[0].outcome is SignalOutcome.KEY_REQUIRED
    assert report.network_required is False


def test_local_text_detector_interface_never_requires_api() -> None:
    report = ProvenanceVisibilityAgent().text_with_local_keyed_detector(
        "sample text",
        detector=lambda _text: True,
        signal_type=SignalType.SYNTHID_TEXT,
    )
    assert report.verdict == "SUPPORTED_LOCAL_TEXT_SIGNAL_DETECTED"
    assert report.local_only is True
    assert report.network_required is False


def test_local_text_no_hit_is_not_human_proof() -> None:
    report = ProvenanceVisibilityAgent().text_with_local_keyed_detector(
        "sample text",
        detector=lambda _text: False,
        signal_type=SignalType.TEXTGRAIN,
    )
    assert report.verdict == "NO_SUPPORTED_LOCAL_TEXT_SIGNAL_DETECTED"
    assert report.not_detected_is_not_human_proof is True


def test_invalid_text_detector_signal_type_is_rejected() -> None:
    with pytest.raises(ValueError):
        ProvenanceVisibilityAgent().text_with_local_keyed_detector(
            "sample",
            detector=lambda _text: True,
            signal_type=SignalType.C2PA,
        )


def test_synthid_media_without_public_local_verifier_is_explicit() -> None:
    report = ProvenanceVisibilityAgent().synthid_media_local_capability(
        MediaKind.AUDIO
    )
    assert report.verdict == "SYNTHID_LOCAL_VERIFIER_NOT_PUBLIC"
    assert report.signals[0].outcome is SignalOutcome.LOCAL_VERIFIER_NOT_PUBLIC
    assert report.network_required is False


def test_markdown_discloses_local_processing_and_limits() -> None:
    report = ProvenanceVisibilityAgent().textgrain_without_secret_key()
    rendered = render_markdown(report)
    assert "本機處理：是" in rendered
    assert "需要網路：否" in rendered
    assert "不等於證明作者" in rendered
    assert "不提供浮水印移除" in rendered
