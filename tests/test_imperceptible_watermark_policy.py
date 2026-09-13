from __future__ import annotations

import importlib.util

import pytest
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


def test_unregistered_source_marker_fails_closed(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "docs" / "research" / "sources" / "external.txt"
    target.parent.mkdir(parents=True)
    target.write_text("source" + chr(0x200B) + "text\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "U+200B" in errors[0]
    assert retained_signals == []


def test_unregistered_qa_patch_marker_fails_closed(tmp_path: Path) -> None:
    scanner = load_scanner()
    target = tmp_path / "qa" / "historical" / "snapshot.patch"
    target.parent.mkdir(parents=True)
    target.write_text("+source" + chr(0x200B) + "text\n", encoding="utf-8")

    errors, retained_signals = scanner.scan_root_detailed(tmp_path)

    assert len(errors) == 1
    assert "qa/historical/snapshot.patch" in errors[0]
    assert "U+200B" in errors[0]
    assert retained_signals == []


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


@pytest.mark.parametrize("relative", list(load_scanner().RETAINED_MARKER_EVIDENCE))
def test_exact_historical_bytes_retained_without_rewriting(tmp_path, relative):
    scanner = load_scanner()
    original = (ROOT / relative).read_bytes()
    target = tmp_path / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(original)
    errors, signals = scanner.scan_root_detailed(tmp_path)
    assert errors == []
    assert signals and all("retained imperceptible marker signal:" in s for s in signals)
    assert target.read_bytes() == original


@pytest.mark.parametrize("change", ["append", "rename", "newline"])
def test_retention_cannot_survive_byte_or_path_change(tmp_path, change):
    scanner = load_scanner()
    relative = next(iter(scanner.RETAINED_MARKER_EVIDENCE))
    original = (ROOT / relative).read_bytes()
    target = tmp_path / relative
    if change == "rename":
        target = target.with_name("copied.patch")
    elif change == "append":
        original += ("new" + chr(0x200B)).encode("utf-8")
    else:
        original = original.replace(b"\n", b"\r\n")
    target.parent.mkdir(parents=True)
    target.write_bytes(original)
    errors, signals = scanner.scan_root_detailed(tmp_path)
    assert errors and any("imperceptible marker:" in e for e in errors)
    assert signals == []


@pytest.mark.parametrize("relative", [
    "scripts/scan_public_tree.py", "src/sources/owned.py",
    "docs/incident-originals/new.md", "qa/new.patch",
])
def test_self_and_directory_names_do_not_bypass_markers(tmp_path, relative):
    target = tmp_path / relative
    target.parent.mkdir(parents=True)
    target.write_text("owned" + chr(0x200B), encoding="utf-8")
    errors, signals = load_scanner().scan_root_detailed(tmp_path)
    assert len(errors) == 1
    assert "U+200B" in errors[0]
    assert signals == []


def test_crlf_line_positions_and_repeated_bom(tmp_path):
    (tmp_path / "text.md").write_bytes(
        (chr(0xFEFF) + "first\r\n" + chr(0xFEFF)).encode("utf-8")
    )
    errors = load_scanner().scan_root(tmp_path)
    assert len(errors) == 1
    assert "text.md:2:1 U+FEFF" in errors[0]
