"""Fetch the exact allowlisted Western-astrology and Bazi research sources.

Redistributable text/license snapshots are retained in the component. Sources
whose redistribution terms were not established are downloaded, hashed, and
discarded; their URL/hash/size still become auditable evidence in the manifest.
"""

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
USER_AGENT = "aion-governance-source-audit/0.2 (+https://github.com/maker-luder/aion-governance-framework)"


@dataclass(frozen=True)
class Source:
    component: str
    source_id: str
    url: str
    license: str
    policy: str
    local_name: str | None = None
    expected_sha256: str | None = None
    note: str = ""


SOURCES = (
    Source("western", "PTOLEMY_TETRABIBLOS_GUTENBERG_70850", "https://www.gutenberg.org/cache/epub/70850/pg70850.txt", "PUBLIC_DOMAIN_US", "VENDOR", "ptolemy-tetrabiblos-pg70850.txt"),
    Source("western", "SEPHARIAL_ASTROLOGY_GUTENBERG_46963", "https://www.gutenberg.org/cache/epub/46963/pg46963.txt", "PUBLIC_DOMAIN_US", "VENDOR", "sepharial-astrology-pg46963.txt"),
    Source("western", "SWISS_EPHEMERIS_PROGRAMMER_DOC_2_10", "https://www.astro.com/swisseph-download/doc/swisseph.pdf", "AGPL_OR_PROFESSIONAL_DUAL_LICENSE", "HASH_ONLY", note="Provider candidate only; no code/data vendored and no dependency added."),
    Source("western", "JPL_HORIZONS_MANUAL", "https://ssd.jpl.nasa.gov/horizons/manual.html", "US_GOVERNMENT_SITE_TERMS", "HASH_ONLY", note="Independent astronomical provider reference."),
    Source("western", "ASTRODIENST_MODERN_RULERS", "https://www.astro.com/astrowiki/en/Rulers", "COPYRIGHTED_REFERENCE", "HASH_ONLY"),
    Source("western", "ASTRODIENST_ASPECTS", "https://www.astro.com/astrowiki/en/Aspect", "COPYRIGHTED_REFERENCE", "HASH_ONLY"),
    Source("bazi", "LUNAR_PYTHON_LICENSE_1_4_8", "https://raw.githubusercontent.com/6tail/lunar-python/000c8a3d74eed098d6256a28fdd51b869324c559/LICENSE", "MIT", "VENDOR", "lunar-python-1.4.8-LICENSE.txt"),
    Source("bazi", "LUNAR_PYTHON_README_1_4_8", "https://raw.githubusercontent.com/6tail/lunar-python/000c8a3d74eed098d6256a28fdd51b869324c559/README_EN.md", "MIT_REPOSITORY_DOCUMENT", "VENDOR", "lunar-python-1.4.8-README_EN.md"),
    Source("bazi", "LUNAR_PYTHON_SDIST_1_4_8", "https://files.pythonhosted.org/packages/source/l/lunar_python/lunar_python-1.4.8.tar.gz", "MIT", "HASH_ONLY", expected_sha256="3aa11cc73c25e70ddf0ba5bdac7398c03acc9491a3aa512a91c9642973b669d6"),
    Source("bazi", "WIKISOURCE_DI_TIAN_SUI", "https://zh.wikisource.org/w/index.php?title=%E6%BB%B4%E5%A4%A9%E9%AB%93&action=raw", "PUBLIC_DOMAIN_TEXT_CC_BY_SA_SITE_LAYER", "VENDOR", "wikisource-di-tian-sui.txt"),
    Source("bazi", "WIKISOURCE_YUAN_HAI_ZI_PING", "https://zh.wikisource.org/w/index.php?title=%E6%B7%B5%E6%B5%B7%E5%AD%90%E5%B9%B3&action=raw", "PUBLIC_DOMAIN_TEXT_CC_BY_SA_SITE_LAYER", "VENDOR", "wikisource-yuan-hai-zi-ping.txt", note="Source page itself reports completeness/provenance concerns; use as comparison evidence only."),
    Source("bazi", "WIKISOURCE_SAN_MING_TONG_HUI_INDEX", "https://zh.wikisource.org/w/index.php?title=%E4%B8%89%E5%91%BD%E9%80%9A%E6%9C%83_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)&action=raw", "PUBLIC_DOMAIN_TEXT_CC_BY_SA_SITE_LAYER", "VENDOR", "wikisource-san-ming-tong-hui-index.txt", note="Index/provenance snapshot; edition variation must remain explicit."),
    Source("bazi", "HKO_24_SOLAR_TERMS", "https://www.hko.gov.hk/en/gts/time/24solarterms.htm", "OFFICIAL_REFERENCE_REDISTRIBUTION_NOT_ESTABLISHED", "HASH_ONLY"),
    Source("bazi", "TAIWAN_CWA_24_SOLAR_TERMS_PDF", "https://www.cwa.gov.tw/Data/knowledge/announce/astronomy3.pdf", "OFFICIAL_REFERENCE_REDISTRIBUTION_NOT_ESTABLISHED", "HASH_ONLY"),
)


def fetch(source: Source) -> tuple[bytes, str]:
    request = urllib.request.Request(source.url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return response.read(), "PYTHON_URLLIB_SYSTEM_TLS"
    except Exception as primary_error:
        # Windows Python installations sometimes lack the enterprise/system CA
        # chain while curl.exe can use it. This is a transport fallback only;
        # certificate verification remains enabled.
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            temp_path = Path(handle.name)
        try:
            completed = subprocess.run(
                ["curl", "-L", "--fail", "--silent", "--show-error", "--user-agent", USER_AGENT,
                 "--output", str(temp_path), source.url],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    f"urllib={type(primary_error).__name__}: {primary_error}; "
                    f"curl_exit={completed.returncode}: {completed.stderr.strip()}"
                )
            return temp_path.read_bytes(), "CURL_SYSTEM_TLS_FALLBACK"
        finally:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    results: dict[str, list[dict[str, object]]] = {"western": [], "bazi": []}
    errors = 0
    for source in SOURCES:
        record: dict[str, object] = {
            "source_id": source.source_id,
            "url": source.url,
            "license_or_terms": source.license,
            "retention_policy": source.policy,
            "note": source.note,
        }
        try:
            payload, transport = fetch(source)
            digest = hashlib.sha256(payload).hexdigest()
            record.update({
                "download_status": "PASS", "transport": transport,
                "bytes": len(payload), "sha256": digest,
            })
            if source.expected_sha256:
                record["expected_sha256"] = source.expected_sha256
                record["expected_sha256_match"] = digest == source.expected_sha256
                if digest != source.expected_sha256:
                    raise ValueError(f"expected SHA-256 mismatch for {source.source_id}")
            if source.policy == "VENDOR":
                component_dir = (
                    ROOT / "examples" / "classical-western-astrology_v0.1.0" / "sources" / "public-domain"
                    if source.component == "western"
                    else ROOT / "examples" / "bazi-capability_v0.1.1" / "sources" / "reviewed-snapshots"
                )
                component_dir.mkdir(parents=True, exist_ok=True)
                target = component_dir / str(source.local_name)
                target.write_bytes(payload)
                record["repository_path"] = target.relative_to(ROOT).as_posix()
            else:
                record["repository_path"] = None
                record["discarded_after_hash"] = True
        except Exception as exc:  # audited failure is retained in the manifest
            errors += 1
            record.update({"download_status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
        results[source.component].append(record)

    manifests = {
        "western": ROOT / "examples" / "classical-western-astrology_v0.1.0" / "sources" / "SOURCE_FETCH_MANIFEST.json",
        "bazi": ROOT / "examples" / "bazi-capability_v0.1.1" / "sources" / "SOURCE_FETCH_MANIFEST.json",
    }
    for component, path in manifests.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        document = {
            "schema_version": "1.0",
            "generated_on": date.today().isoformat(),
            "component": component,
            "network_required_at_runtime": False,
            "source_count": len(results[component]),
            "sources": results[component],
        }
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(path)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
