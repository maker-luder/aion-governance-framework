import codecs
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "provenance-visibility-agent_v0.1.0" / "src"
sys.path.insert(0, str(SRC))

from aion_provenance_visibility_agent import (  # noqa: E402
    EvidenceFamily,
    MediaKind,
    ProvenanceVisibilityAgent,
    SignalOutcome,
    SignalType,
    render_markdown,
    render_text_reveal_markdown,
    reveal_hidden_text_bytes,
    reveal_hidden_text_signal,
)


def test_textgrain_without_secret_key_fails_to_unknown() -> None:
    report = ProvenanceVisibilityAgent().textgrain_without_secret_key()
    assert report.media_kind is MediaKind.TEXT
    assert report.verdict == "TEXTGRAIN_NOT_LOCALLY_VERIFIABLE_WITHOUT_KEY"
    assert report.signals[0].signal_type is SignalType.TEXTGRAIN
    assert report.signals[0].outcome is SignalOutcome.KEY_REQUIRED
    assert report.network_required is False
    assert "不能冒充正式 detector" in report.visible_label_zh_tw


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


def test_markdown_discloses_local_processing_and_limits() -> None:
    report = ProvenanceVisibilityAgent().textgrain_without_secret_key()
    rendered = render_markdown(report)
    assert "本機處理：是" in rendered
    assert "需要網路：否" in rendered
    assert "不等於證明作者" in rendered
    assert "不連接 hosted provenance API" in rendered
    assert "不提供浮水印移除" in rendered


def test_raw_utf8_bom_and_byte_offset_are_preserved() -> None:
    data = codecs.BOM_UTF8 + "a\u200bb".encode("utf-8")
    report = reveal_hidden_text_bytes(data)

    assert report.method == "AION_TEXT_VISIBILITY_V0_2"
    assert report.raw_profile.bom == "UTF-8"
    assert report.raw_profile.byte_count == len(data)

    cue = next(
        item for item in report.cues
        if item.cue_type == "UNICODE_FORMAT_CONTROL"
    )
    assert cue.char_index == 1
    assert cue.byte_offset == 4
    assert cue.family is EvidenceFamily.UNICODE_ENCODING


def test_raw_profile_surfaces_mixed_line_endings_and_trailing_whitespace() -> None:
    data = b"alpha  \r\nbeta\ncharlie\t\r\n"
    report = reveal_hidden_text_bytes(data)

    assert report.raw_profile.crlf_count == 2
    assert report.raw_profile.lf_only_count == 1
    assert report.raw_profile.trailing_space_lines == 1
    assert report.raw_profile.trailing_tab_lines == 1
    cue_types = {cue.cue_type for cue in report.cues}
    assert "MIXED_LINE_ENDINGS" in cue_types
    assert "TRAILING_SPACE_LINES" in cue_types
    assert "TRAILING_TAB_LINES" in cue_types


def test_text_reveal_makes_zero_width_control_human_visible() -> None:
    report = reveal_hidden_text_signal("alpha\u200bbeta")

    assert report.watermark_verdict == "NOT_ESTABLISHED"
    assert any(cue.cue_type == "UNICODE_FORMAT_CONTROL" for cue in report.cues)

    panel = next(
        item for item in report.panels if item.name == "machine_visible_unicode"
    )
    assert "U+200B ZERO WIDTH SPACE" in panel.content


def test_text_reveal_surfaces_mixed_script_without_calling_it_watermark() -> None:
    report = reveal_hidden_text_signal("pаypal example")

    assert any(
        cue.cue_type == "MIXED_LATIN_CYRILLIC_GREEK_TOKEN"
        for cue in report.cues
    )
    assert "HOMOGLYPH_OR_MIXED_SCRIPT_CHANNEL" in report.hypotheses
    assert report.watermark_verdict == "NOT_ESTABLISHED"


def test_text_reveal_surfaces_normalization_contrast() -> None:
    report = reveal_hidden_text_signal("ＡION provenance")

    assert "COMPATIBILITY_ENCODING_CHANNEL" in report.hypotheses
    panel = next(
        item for item in report.panels if item.name == "normalization_contrast"
    )
    assert "NFKC" in panel.content
    assert EvidenceFamily.NORMALIZATION in report.independent_families


def test_text_reveal_montage_finds_synthetic_period_two_candidate() -> None:
    tokens: list[str] = []
    for _ in range(12):
        tokens.extend(["a", "veryverylong,"])
    report = reveal_hidden_text_signal(" ".join(tokens))

    assert report.candidate_period == 2
    assert "POSITIONAL_PATTERN_CANDIDATE" in report.hypotheses
    montage = next(
        item for item in report.panels if item.name == "positional_montage"
    )
    assert "period=2" in montage.content
    assert report.heuristic_score_is_probability is False
    assert EvidenceFamily.POSITIONAL in report.independent_families


def test_same_family_cues_do_not_become_independent_votes() -> None:
    report = reveal_hidden_text_signal("a\u200bb\u200cc")

    assert sum(
        1 for cue in report.cues
        if cue.family is EvidenceFamily.UNICODE_ENCODING
    ) == 2
    assert report.independent_families.count(
        EvidenceFamily.UNICODE_ENCODING
    ) == 1


def test_evidence_ledger_separates_support_from_claims() -> None:
    report = reveal_hidden_text_signal("a\u200bb")
    record = next(
        item for item in report.evidence_ledger
        if item.observation == "UNICODE_FORMAT_CONTROL"
    )

    assert record.evidence_kind.value == "EXACT"
    assert "watermark" in record.does_not_establish
    assert "vendor" in record.does_not_establish
    assert record.method == "SOURCE_PRESERVING_REVEAL"


def test_generic_heuristic_never_invents_p_value() -> None:
    tokens: list[str] = []
    for _ in range(12):
        tokens.extend(["a", "veryverylong,"])
    report = reveal_hidden_text_signal(" ".join(tokens))

    assert report.null_model_status == "UNDEFINED_FOR_GENERIC_HEURISTIC"
    assert report.statistical_p_value is None
    assert report.heuristic_score_is_probability is False


def test_counterfactual_panel_does_not_modify_source_hash() -> None:
    data = "ＡION\u200b alpha beta".encode("utf-8")
    report = reveal_hidden_text_bytes(data)

    panel = next(
        item for item in report.panels
        if item.name == "counterfactual_stability"
    )
    assert "original_period=" in panel.content
    assert "nfkc_period=" in panel.content
    assert "format_control_stripped_period=" in panel.content
    assert report.raw_profile.sha256
    assert report.source_text_modified is False


def test_plain_short_text_remains_unknown() -> None:
    report = reveal_hidden_text_signal("ordinary transparent repository text")

    assert report.candidate_period is None
    assert report.watermark_verdict == "NOT_ESTABLISHED"
    assert report.network_required is False
    assert report.api_required is False


def test_agent_exposes_raw_byte_text_reveal() -> None:
    data = codecs.BOM_UTF8 + "visible\u200binvisible".encode("utf-8")
    report = ProvenanceVisibilityAgent().reveal_hidden_text_bytes_local(data)

    assert report.raw_profile.bom == "UTF-8"
    assert any(cue.cue_type == "UNICODE_FORMAT_CONTROL" for cue in report.cues)
    assert report.local_only is True


def test_agent_reads_local_file_as_raw_bytes(tmp_path: Path) -> None:
    source = tmp_path / "sample.txt"
    data = codecs.BOM_UTF8 + "alpha\u200bbeta\r\n".encode("utf-8")
    source.write_bytes(data)

    report = ProvenanceVisibilityAgent().reveal_hidden_text_file_local(source)

    assert report.raw_profile.sha256
    assert report.raw_profile.byte_count == len(data)
    assert report.raw_profile.bom == "UTF-8"
    assert any(cue.cue_type == "UNICODE_FORMAT_CONTROL" for cue in report.cues)


def test_text_reveal_markdown_discloses_v0_2_limits() -> None:
    report = reveal_hidden_text_signal("alpha\u200bbeta")
    rendered = render_text_reveal_markdown(report)

    assert "Evidence ledger" in rendered
    assert "byte offset" in rendered
    assert "MONTAGE_JUXTAPOSITION" in rendered
    assert "NO_DEFINED_NULL_MODEL = NO_VALID_P_VALUE" in rendered
    assert "同一 evidence family" in rendered
    assert "WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN" in rendered
    assert "不連接 hosted provenance API" in rendered
    assert "不提供浮水印移除" in rendered
