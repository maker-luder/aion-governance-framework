"""Verify reviewed quality-method cards; optionally verify exact raw bytes in an external cache."""
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
SOURCE_DIR = Path("docs/research/sources/quality")
MAX_BYTES = 10 * 1024 * 1024
HOSTS = {"nvlpubs.nist.gov", "www.fda.gov"}
BOUNDARIES = {
    "purpose": "RESEARCH_QUALITY_METHOD_CROSSWALK",
    "subjectivity": "NOT_ESTABLISHED",
    "canonical_effect": "NONE",
    "deployment": False,
    "runtime_network_required": False,
}


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def local_card(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9.-]*\.md", name):
        raise ValueError("invalid quality source card filename")
    directory = root / SOURCE_DIR
    path = directory / name
    if (
        path.is_symlink()
        or not path.is_file()
        or path.resolve().parent != directory.resolve()
        or root.resolve() not in path.resolve().parents
    ):
        raise ValueError("quality source card is missing or outside source directory")
    return path


def validate(root: Path = ROOT) -> dict[str, object]:
    import jsonschema

    directory = root / SOURCE_DIR
    manifest = json.loads((directory / "DOWNLOAD_MANIFEST.json").read_text(encoding="utf-8"))
    for name, value in BOUNDARIES.items():
        if type(manifest.get(name)) is not type(value) or manifest[name] != value:
            raise ValueError(f"boundary changed: {name}")
    sources = manifest.get("sources")
    if not isinstance(sources, list) or len(sources) != 3:
        raise ValueError("reviewed quality source set must contain exactly three records")

    identifiers: set[str] = set()
    for source in sources:
        identifier = source["source_id"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]+", identifier) or identifier in identifiers:
            raise ValueError("invalid or duplicate source identifier")
        identifiers.add(identifier)
        parsed = urlparse(source["url"])
        if parsed.scheme != "https" or parsed.hostname not in HOSTS or parsed.username or parsed.password or parsed.port:
            raise ValueError("source URL is not an allowed official HTTPS endpoint")
        if not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
            raise ValueError("missing exact upstream digest")
        if type(source["bytes"]) is not int or not 0 < source["bytes"] <= MAX_BYTES:
            raise ValueError("source byte count outside acquisition cap")
        if source["status"] != "PASS" or source["intake_scope"] != "DERIVATIVE_CARD_ONLY":
            raise ValueError("source has no bounded successful acquisition receipt")
        payload = local_card(root, source["card"]).read_bytes()
        if len(payload) != source["card_bytes"] or digest(payload) != source["card_sha256"]:
            raise ValueError(f"quality source card digest mismatch: {identifier}")

    records = json.loads((directory / "GOVERNED_SOURCES.json").read_text(encoding="utf-8"))
    schema = json.loads((root / "schemas/governed_knowledge_source_v0.1.0.schema.json").read_text(encoding="utf-8"))
    if len(records) != len(sources) or {record["source_id"] for record in records} != identifiers:
        raise ValueError("governed registry and quality download manifest differ")
    for record in records:
        try:
            jsonschema.validate(record, schema)
        except jsonschema.ValidationError as exc:
            raise ValueError("governed quality source fails the existing schema") from exc
        if record["registry_status"] != "CANDIDATE" or record["authority_level"] != "REFERENCE_ONLY":
            raise ValueError("quality reference admission or authority changed")
        locator = record["provenance"]["locator"]
        expected_prefix = SOURCE_DIR.as_posix() + "/"
        if record["provenance"]["kind"] != "REPOSITORY_FILE" or not locator.startswith(expected_prefix):
            raise ValueError("governed quality source locator mismatch")
        path = local_card(root, locator[len(expected_prefix) :])
        if record["content_hash"] != "sha256:" + digest(path.read_bytes()):
            raise ValueError("governed quality source content binding mismatch")
    return manifest


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "AION-quality-method-review/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            final_url = urlparse(response.url)
            if final_url.scheme != "https" or final_url.hostname not in HOSTS:
                raise ValueError("unexpected source redirect")
            payload = response.read(MAX_BYTES + 1)
    except OSError:
        result = subprocess.run(
            [
                "curl",
                "--proto",
                "=https",
                "--proto-redir",
                "=https",
                "--location",
                "--fail",
                "--silent",
                "--show-error",
                "--max-time",
                "90",
                "--max-filesize",
                str(MAX_BYTES),
                url,
            ],
            capture_output=True,
            check=True,
            timeout=100,
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
    parser.add_argument("--download-cache", type=Path, help="explicit acquisition; external directory only")
    args = parser.parse_args(argv)
    try:
        manifest = validate()
        verified = download_cache(ROOT, args.download_cache, manifest) if args.download_cache else 0
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "sources": len(manifest["sources"]),
                    "downloaded_or_verified_cache": verified,
                    "mode": "DOWNLOAD" if args.download_cache else "OFFLINE_VERIFY",
                    **BOUNDARIES,
                },
                indent=2,
            )
        )
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "HOLD", "error_type": type(exc).__name__, "message": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
