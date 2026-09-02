"""Fetch the exact allowlisted Zi Wei Dou Shu research sources."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "examples" / "zi-wei-dou-shu_v0.1.0"
SNAPSHOTS = COMPONENT / "sources" / "reviewed-snapshots"
USER_AGENT = "aion-governance-source-audit/0.1 (+https://github.com/maker-luder/aion-governance-framework)"


@dataclass(frozen=True)
class Source:
    source_id: str
    url: str
    terms: str
    policy: str
    local_name: str | None = None
    expected_sha256: str | None = None
    note: str = ""
    normalize_utf8_text: bool = False


COMMIT = "80dcedfdeab8df9130d1088db4510f43c0cf2d78"
SOURCES = (
    Source(
        "ZI_WEI_DOU_SHU_QUAN_SHU_WIKISOURCE_REV_850734",
        "https://zh.wikisource.org/w/index.php?title=%E7%B4%AB%E5%BE%AE%E6%96%97%E6%95%B8%E5%85%A8%E6%9B%B8%2F%E5%85%A8%E8%A6%BD&oldid=850734&printable=yes",
        "PUBLIC_DOMAIN_TEXT_CC_BY_SA_SITE_LAYER",
        "VENDOR",
        "wikisource-zi-wei-dou-shu-quan-shu-rev850734.html",
        note="Pinned rendered transcription; attribution and edition history remain disputed.",
        normalize_utf8_text=True,
    ),
    Source(
        "IZTRO_LICENSE_2_6_0",
        f"https://raw.githubusercontent.com/SylarLong/iztro/{COMMIT}/LICENSE",
        "MIT",
        "VENDOR",
        "iztro-2.6.0-LICENSE.txt",
    ),
    Source(
        "IZTRO_README_2_6_0",
        f"https://raw.githubusercontent.com/SylarLong/iztro/{COMMIT}/README.md",
        "MIT_REPOSITORY_DOCUMENT",
        "VENDOR",
        "iztro-2.6.0-README.md",
    ),
    Source(
        "IZTRO_NPM_TARBALL_2_6_0",
        "https://registry.npmjs.org/iztro/-/iztro-2.6.0.tgz",
        "MIT",
        "HASH_ONLY",
        expected_sha256="df7013db5260d548ed1359f5173089eab6a925d90e15b327235b10a1e0b0abb9",
    ),
    Source(
        "HKO_CALENDAR_2000",
        "https://www.hko.gov.hk/tc/gts/time/calendar/pdf/files/2000.pdf",
        "OFFICIAL_REFERENCE_REDISTRIBUTION_NOT_ESTABLISHED",
        "HASH_ONLY",
    ),
    Source(
        "HKO_CALENDAR_2026",
        "https://www.hko.gov.hk/tc/gts/time/calendar/pdf/files/2026.pdf",
        "OFFICIAL_REFERENCE_REDISTRIBUTION_NOT_ESTABLISHED",
        "HASH_ONLY",
    ),
    Source(
        "HKO_24_SOLAR_TERMS",
        "https://www.hko.gov.hk/tc/gts/time/24solarterms.htm",
        "OFFICIAL_REFERENCE_REDISTRIBUTION_NOT_ESTABLISHED",
        "HASH_ONLY",
    ),
)


def fetch(source: Source) -> tuple[bytes, str]:
    request = urllib.request.Request(source.url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return response.read(), "PYTHON_URLLIB_SYSTEM_TLS"
    except Exception as primary_error:
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            path = Path(handle.name)
        try:
            completed = subprocess.run(
                ["curl", "-L", "--fail", "--silent", "--show-error", "--user-agent", USER_AGENT,
                 "--output", str(path), source.url],
                check=False, capture_output=True, text=True, timeout=120,
            )
            if completed.returncode:
                raise RuntimeError(
                    f"urllib={type(primary_error).__name__}: {primary_error}; "
                    f"curl_exit={completed.returncode}: {completed.stderr.strip()}"
                )
            return path.read_bytes(), "CURL_SYSTEM_TLS_FALLBACK"
        finally:
            path.unlink(missing_ok=True)


def main() -> int:
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    errors = 0
    for source in SOURCES:
        record: dict[str, object] = {
            "source_id": source.source_id,
            "url": source.url,
            "license_or_terms": source.terms,
            "retention_policy": source.policy,
            "note": source.note,
        }
        try:
            payload, transport = fetch(source)
            digest = hashlib.sha256(payload).hexdigest()
            record.update({"download_status": "PASS", "transport": transport, "bytes": len(payload), "sha256": digest})
            if source.expected_sha256:
                record["expected_sha256"] = source.expected_sha256
                record["expected_sha256_match"] = digest == source.expected_sha256
                if digest != source.expected_sha256:
                    raise ValueError(f"expected SHA-256 mismatch for {source.source_id}")
            if source.policy == "VENDOR":
                target = SNAPSHOTS / str(source.local_name)
                repository_payload = payload
                if source.normalize_utf8_text:
                    text = payload.decode("utf-8")
                    repository_payload = (
                        "\n".join(line.rstrip(" \t") for line in text.splitlines()) + "\n"
                    ).encode("utf-8")
                    record["repository_normalization"] = "UTF8_LF_REMOVE_TRAILING_HORIZONTAL_WHITESPACE_V1"
                target.write_bytes(repository_payload)
                record["repository_path"] = target.relative_to(ROOT).as_posix()
                record["repository_sha256"] = hashlib.sha256(repository_payload).hexdigest()
                record["repository_bytes"] = len(repository_payload)
            else:
                record["repository_path"] = None
                record["discarded_after_hash"] = True
        except Exception as exc:
            errors += 1
            record.update({"download_status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
        results.append(record)
    manifest = {
        "schema_version": "1.0",
        "generated_on": date.today().isoformat(),
        "component": "zi-wei-dou-shu",
        "network_required_at_runtime": False,
        "source_count": len(results),
        "sources": results,
    }
    target = COMPONENT / "sources" / "SOURCE_FETCH_MANIFEST.json"
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
