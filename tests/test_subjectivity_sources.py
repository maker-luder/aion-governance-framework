import json
from pathlib import Path
import shutil

import pytest

from scripts import fetch_subjectivity_sources as sources

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def copy_root(tmp_path):
    shutil.copytree(ROOT / sources.SOURCE_DIR, tmp_path / sources.SOURCE_DIR)
    (tmp_path / "schemas").mkdir()
    shutil.copyfile(ROOT / "schemas/governed_knowledge_source_v0.1.0.schema.json",
                    tmp_path / "schemas/governed_knowledge_source_v0.1.0.schema.json")
    return tmp_path


def update_manifest(root, mutate):
    path = root / sources.SOURCE_DIR / "DOWNLOAD_MANIFEST.json"
    data = json.loads(path.read_text())
    mutate(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_real_sources_verify_without_network(monkeypatch):
    monkeypatch.setattr(sources, "fetch", lambda *_: pytest.fail("offline validation performed network access"))
    manifest = sources.validate(ROOT)
    assert len(manifest["sources"]) == 4
    assert sum(bool(r["retained_text"]) for r in manifest["sources"]) == 2


def test_tampered_reference_fails_closed(copy_root):
    path = copy_root / sources.SOURCE_DIR / "cogitate-2025.txt"
    path.write_text("tampered", encoding="utf-8")
    with pytest.raises(ValueError, match="digest mismatch"):
        sources.validate(copy_root)


@pytest.mark.parametrize("name", ["../escape.txt", "/escape.txt", "C:/escape.txt", "nested/file.txt"])
def test_source_path_escape_fails(copy_root, name):
    update_manifest(copy_root, lambda d: d["sources"][1].update(retained_text=name))
    with pytest.raises(ValueError, match="filename"):
        sources.validate(copy_root)


@pytest.mark.parametrize("mutate", [
    lambda d: d.update(canonical_effect="WRITE"),
    lambda d: d.update(deployment=0),
    lambda d: d.update(sources=[]),
    lambda d: d["sources"].append(d["sources"][0]),
    lambda d: d["sources"][0].update(url="http://arxiv.org/pdf/2308.08708v3"),
    lambda d: d["sources"][0].update(sha256="unverified"),
    lambda d: d["sources"][1].update(license="UNREVIEWED"),
])
def test_invalid_manifest_cannot_promote_sources(copy_root, mutate):
    update_manifest(copy_root, mutate)
    with pytest.raises(ValueError):
        sources.validate(copy_root)


def test_governed_record_uses_existing_schema_and_remains_candidate(copy_root):
    path = copy_root / sources.SOURCE_DIR / "GOVERNED_SOURCES.json"
    data = json.loads(path.read_text())
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
    target = cache / "butlin-2023-v3.source"
    target.write_bytes(b"keep this")
    monkeypatch.setattr(sources, "fetch", lambda *_: pytest.fail("unexpected network"))
    with pytest.raises(ValueError, match="no overwrite"):
        sources.download_cache(copy_root, cache, sources.validate(copy_root))
    assert target.read_bytes() == b"keep this"
