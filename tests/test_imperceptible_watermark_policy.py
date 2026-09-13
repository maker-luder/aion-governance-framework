from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_scanner():
    path = ROOT / "scripts" / "scan_public_tree.py"
    spec = importlib.util.spec_from_file_location("aion_test_scan_public_tree_watermark", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_project_owned_zero_width_marker_fails_closed(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "docs" / "owned.md"
    target.parent.mkdir(parents=True)
    target.write_text("visible" + chr(0x200B) + "text\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "imperceptible marker: docs/owned.md:1:8 U+200B" in errors[0]
    assert retained_signals == []


def test_project_owned_unicode_tag_character_fails_closed(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "artifact.txt"
    target.write_text("A" + chr(0xE0061) + "B\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "U+E0061" in errors[0]
    assert retained_signals == []


def test_supplementary_variation_selector_fails_closed(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "artifact.txt"
    target.write_text("A" + chr(0xE0100) + "B\n", encoding="utf-8")

    errors, _ = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "U+E0100 VARIATION SELECTOR SUPPLEMENT" in errors[0]


def test_common_visible_emoji_variation_selector_is_not_blanket_banned(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "artifact.txt"
    target.write_text(chr(0x2764) + chr(0xFE0F) + "\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert errors == []
    assert retained_signals == []


def test_leading_utf8_bom_is_encoding_metadata_not_content_marker(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "vectors.csv"
    target.write_text(chr(0xFEFF) + "a,b\n1,2\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert errors == []
    assert retained_signals == []


def test_embedded_feff_still_fails_closed(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "artifact.txt"
    target.write_text("A" + chr(0xFEFF) + "B\n", encoding="utf-8")

    errors, _ = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "U+FEFF" in errors[0]


def test_external_source_marker_is_retained_signal_not_project_failure(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "docs" / "research" / "sources" / "external.txt"
    target.parent.mkdir(parents=True)
    target.write_text("source" + chr(0x200B) + "text\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert errors == []
    assert len(retained_signals) == 1
    assert retained_signals[0].startswith("retained imperceptible marker signal:")
    assert "U+200B" in retained_signals[0]


def test_qa_patch_marker_is_retained_signal_to_preserve_evidence_bytes(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "qa" / "historical" / "snapshot.patch"
    target.parent.mkdir(parents=True)
    target.write_text("+source" + chr(0x200B) + "text\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert errors == []
    assert len(retained_signals) == 1
    assert "qa/historical/snapshot.patch" in retained_signals[0]
    assert "U+200B" in retained_signals[0]


def test_patch_outside_qa_remains_project_owned_and_fails_closed(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "docs" / "candidate.patch"
    target.parent.mkdir(parents=True)
    target.write_text("+owned" + chr(0x200B) + "text\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "imperceptible marker: docs/candidate.patch" in errors[0]
    assert retained_signals == []


def test_plain_project_text_passes(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "docs" / "plain.md"
    target.parent.mkdir(parents=True)
    target.write_text("transparent provenance only\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert errors == []
    assert retained_signals == []
