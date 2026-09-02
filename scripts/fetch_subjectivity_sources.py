"""Offline verification by default; explicit, digest-pinned acquisition to external cache."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path("docs/research/sources/subjectivity")
MAX_BYTES = 20 * 1024 * 1024
HOSTS = {"arxiv.org", "www.ncbi.nlm.nih.gov", "api.crossref.org"}
BOUNDARIES = {
    "central_research_question": "AI_SUBJECTIVITY_POSSIBILITY",
    "subjectivity": "NOT_ESTABLISHED",
    "canonical_effect": "NONE",
    "deployment": False,
    "runtime_network_required": False,
}


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def local_file(root: Path, name: str) -> Path:
    # All retained artifacts are direct children, never arbitrary repository paths.
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9.-]*\.(txt|md)", name):
        raise ValueError("invalid source filename")
    directory = root / SOURCE_DIR
    path = directory / name
    if (path.is_symlink() or not path.is_file() or path.resolve().parent != directory.resolve()
            or root.resolve() not in path.resolve().parents):
        raise ValueError("source is missing or outside source directory")
    return path


def validate(root: Path = ROOT) -> dict[str, object]:
    import jsonschema

    directory = root / SOURCE_DIR
    manifest = json.loads((directory / "DOWNLOAD_MANIFEST.json").read_text(encoding="utf-8"))
    for name, value in BOUNDARIES.items():
        if type(manifest.get(name)) is not type(value) or manifest[name] != value:
            raise ValueError(f"boundary changed: {name}")
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("source set must be nonempty")
    identifiers = set()
    for source in sources:
        identifier = source["source_id"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]+", identifier) or identifier in identifiers:
            raise ValueError("invalid or duplicate source identifier")
        identifiers.add(identifier)
        parsed = urlparse(source["url"])
        if parsed.scheme != "https" or parsed.hostname not in HOSTS or parsed.username or parsed.password or parsed.port:
            raise ValueError("source URL is not an allowed public HTTPS endpoint")
        if not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
            raise ValueError("missing exact upstream digest")
        if type(source["bytes"]) is not int or not 0 < source["bytes"] <= MAX_BYTES:
            raise ValueError("source byte count outside acquisition cap")
        if source["status"] != "PASS":
            raise ValueError("source has no successful acquisition receipt")
        if source["retained_text"] is not None:
            if source["license"] != "CC-BY-4.0":
                raise ValueError("full-text retention requires the reviewed CC-BY profile")
            payload = local_file(root, source["retained_text"]).read_bytes()
            if len(payload) != source["retained_bytes"] or digest(payload) != source["retained_sha256"]:
                raise ValueError(f"retained source digest mismatch: {identifier}")
    records = json.loads((directory / "GOVERNED_SOURCES.json").read_text(encoding="utf-8"))
    schema = json.loads((root / "schemas/governed_knowledge_source_v0.1.0.schema.json").read_text(encoding="utf-8"))
    if len(records) != len(sources) or {r["source_id"] for r in records} != identifiers:
        raise ValueError("governed registry and download manifest differ")
    for record in records:
        try:
            jsonschema.validate(record, schema)
        except jsonschema.ValidationError as exc:
            raise ValueError("governed source fails the existing schema") from exc
        if record["registry_status"] != "CANDIDATE" or record["authority_level"] != "REFERENCE_ONLY":
            raise ValueError("reference admission or authority changed")
        locator = record["provenance"]["locator"]
        expected_prefix = SOURCE_DIR.as_posix() + "/"
        if record["provenance"]["kind"] != "REPOSITORY_FILE" or not locator.startswith(expected_prefix):
            raise ValueError("governed source locator mismatch")
        path = local_file(root, locator[len(expected_prefix):])
        if record["content_hash"] != "sha256:" + digest(path.read_bytes()):
            raise ValueError("governed source content binding mismatch")
    return manifest


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "AION-bounded-research-source-review/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            final_url = urlparse(response.url)
            if final_url.scheme != "https" or final_url.hostname not in HOSTS:
                raise ValueError("unexpected source redirect")
            payload = response.read(MAX_BYTES + 1)
    except OSError:
        # System TLS fallback, never disable certificate checks or permit HTTP redirects.
        result = subprocess.run(
            ["curl", "--proto", "=https", "--proto-redir", "=https", "--location", "--fail",
             "--silent", "--show-error", "--max-time", "90", "--max-filesize", str(MAX_BYTES), url],
            capture_output=True, check=True, timeout=100,
        )
        payload = result.stdout
    if len(payload) > MAX_BYTES:
        raise ValueError("download exceeded byte cap")
    return payload


def download_cache(root: Path, cache: Path, manifest: dict[str, object]) -> int:
    cache = cache.resolve()
    root = root.resolve()
    if cache == root or root in cache.parents:
        raise ValueError("raw acquisition cache must be outside the repository")
    cache.mkdir(parents=True, exist_ok=True)
    count = 0
    for source in manifest["sources"]:
        path = cache / (source["source_id"] + ".source")
        if path.is_symlink():
            raise ValueError("cache target must not be a symlink")
        payload = path.read_bytes() if path.exists() else fetch(source["url"])
        if len(payload) != source["bytes"] or digest(payload) != source["sha256"]:
            raise ValueError(f"upstream/cache changed; no overwrite: {source['source_id']}")
        if not path.exists():
            with path.open("xb") as stream:
                stream.write(payload)
        count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download-cache", type=Path, help="explicit network acquisition; external directory only")
    args = parser.parse_args(argv)
    try:
        manifest = validate()
        downloaded = download_cache(ROOT, args.download_cache, manifest) if args.download_cache else 0
        print(json.dumps({"status": "PASS", "sources": len(manifest["sources"]),
                          "downloaded_or_verified_cache": downloaded,
                          "mode": "DOWNLOAD" if args.download_cache else "OFFLINE_VERIFY", **BOUNDARIES}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "HOLD", "error_type": type(exc).__name__, "message": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
