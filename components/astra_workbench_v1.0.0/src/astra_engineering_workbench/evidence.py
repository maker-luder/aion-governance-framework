"""Evidence fingerprints and JSON persistence."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from .models import EvidenceReference


def environment_fingerprint(values: dict[str, str]) -> str:
    return hashlib.sha256(
        json.dumps(values, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def save_evidence(reference: EvidenceReference, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(reference), ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )


def load_evidence(path: Path) -> EvidenceReference:
    from .enums import EvidenceValidity

    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["test_scope"] = tuple(raw["test_scope"])
    raw["dependency_scope"] = tuple(raw["dependency_scope"])
    raw["invalidation_conditions"] = tuple(raw["invalidation_conditions"])
    raw["reused_by_versions"] = tuple(raw.get("reused_by_versions", ()))
    raw["validity_status"] = EvidenceValidity(raw["validity_status"])
    return EvidenceReference(**raw)
