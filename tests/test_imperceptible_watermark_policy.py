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

    errors, external_signals = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "imperceptible marker: docs/owned.md:1:8 U+200B" in errors[0]
    assert external_signals == []


def test_project_owned_unicode_tag_character_fails_closed(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "artifact.txt"
    target.write_text("A" + chr(0xE0061) + "B\n", encoding="utf-8")

    errors, external_signals = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "U+E0061" in errors[0]
    assert external_signals == []


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

    errors, external_signals = scanner.scan_root_detailed(tmp_path)

    assert errors == []
    assert external_signals == []


def test_external_source_marker_is_signal_not_project_owned_failure(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "docs" / "research" / "sources" / "external.txt"
    target.parent.mkdir(parents=True)
    target.write_text("source" + chr(0x200B) + "text\n", encoding="utf-8")

    errors, external_signals = scanner.scan_root_detailed(tmp_path)

    assert errors == []
    assert len(external_signals) == 1
    assert external_signals[0].startswith("external imperceptible marker signal:")
    assert "U+200B" in external_signals[0]


def test_plain_project_text_passes(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "docs" / "plain.md"
    target.parent.mkdir(parents=True)
    target.write_text("transparent provenance only\n", encoding="utf-8")

    errors, external_signals = scanner.scan_root_detailed(tmp_path)

    assert errors == []
    assert external_signals == []
