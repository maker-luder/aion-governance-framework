import hashlib
import json
from pathlib import Path
import shutil

import pytest

from scripts import fetch_quality_method_sources as sources


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def copy_root(tmp_path):
    shutil.copytree(ROOT / sources.SOURCE_DIR, tmp_path / sources.SOURCE_DIR)
    (tmp_path / "schemas").mkdir()
    shutil.copyfile(
        ROOT / "schemas/governed_knowledge_source_v0.1.0.schema.json",
        tmp_path / "schemas/governed_knowledge_source_v0.1.0.schema.json",
    )
    return tmp_path


def update_manifest(root, mutate):
    path = root / sources.SOURCE_DIR / "DOWNLOAD_MANIFEST.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_reviewed_quality_cards_verify_offline(monkeypatch):
    monkeypatch.setattr(sources, "fetch", lambda *_: pytest.fail("offline validation performed network access"))
    manifest = sources.validate(ROOT)
    assert len(manifest["sources"]) == 3
    assert all(row["intake_scope"] == "DERIVATIVE_CARD_ONLY" for row in manifest["sources"])


def test_manifest_binds_exact_official_payload_receipts():
    manifest = sources.validate(ROOT)
    assert {row["source_id"] for row in manifest["sources"]} == {
        "nist-ai-rmf-1.0",
        "nist-ai-600-1",
        "fda-capa-qsit-1999",
    }
    assert all(len(row["sha256"]) == 64 and row["bytes"] > 0 for row in manifest["sources"])


def test_tampered_card_fails_closed(copy_root):
    path = copy_root / sources.SOURCE_DIR / "nist-ai-rmf-1.0.md"
    path.write_text("tampered", encoding="utf-8")
    with pytest.raises(ValueError, match="card digest mismatch"):
        sources.validate(copy_root)


@pytest.mark.parametrize("name", ["../escape.md", "/escape.md", "C:/escape.md", "nested/card.md"])
def test_card_path_escape_fails(copy_root, name):
    update_manifest(copy_root, lambda data: data["sources"][0].update(card=name))
    with pytest.raises(ValueError, match="filename"):
        sources.validate(copy_root)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda data: data.update(canonical_effect="WRITE"),
        lambda data: data.update(deployment=0),
        lambda data: data.update(subjectivity="ESTABLISHED"),
        lambda data: data["sources"][0].update(url="http://nvlpubs.nist.gov/file.pdf"),
        lambda data: data["sources"][0].update(sha256="unverified"),
        lambda data: data["sources"][0].update(intake_scope="FULL_TEXT"),
    ],
)
def test_invalid_manifest_cannot_promote_quality_sources(copy_root, mutate):
    update_manifest(copy_root, mutate)
    with pytest.raises(ValueError):
        sources.validate(copy_root)


def test_governed_record_uses_existing_schema_and_remains_candidate(copy_root):
    path = copy_root / sources.SOURCE_DIR / "GOVERNED_SOURCES.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data[0]["registry_status"] = "ACTIVE_REFERENCE"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="admission"):
        sources.validate(copy_root)


def test_download_rejects_repository_destination_before_network(copy_root, monkeypatch):
    monkeypatch.setattr(sources, "fetch", lambda *_: pytest.fail("unexpected network"))
    with pytest.raises(ValueError, match="outside"):
        sources.download_cache(copy_root, copy_root / "cache", sources.validate(copy_root))


def test_existing_wrong_cache_is_not_overwritten(copy_root, tmp_path, monkeypatch):
    cache = tmp_path.parent / (tmp_path.name + "-cache")
    cache.mkdir()
    target = cache / "nist-ai-rmf-1.0.source"
    target.write_bytes(b"keep this")
    before = hashlib.sha256(target.read_bytes()).hexdigest()
    monkeypatch.setattr(sources, "fetch", lambda *_: pytest.fail("unexpected network"))
    with pytest.raises(ValueError, match="no overwrite"):
        sources.download_cache(copy_root, cache, sources.validate(copy_root))
    assert hashlib.sha256(target.read_bytes()).hexdigest() == before
