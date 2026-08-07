"""Versioned materialized-fact serialization and storage integrity checks."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import unicodedata
from decimal import Decimal
from typing import Any


SERIALIZATION_SCHEMA_VERSION = "BAZI_MATERIALIZED_FACTS_V1"
CATEGORY_ORDER = (
    "bazi_pillars",
    "bazi_hidden_stems",
    "bazi_ten_gods",
    "bazi_relations",
    "bazi_luck_cycles",
)
_CATEGORY_QUERIES: dict[str, tuple[str, tuple[str, ...]]] = {
    "bazi_pillars": (
        """SELECT pillar_name, stem, branch, fact_json
           FROM bazi_pillars WHERE natal_profile_id=?
           ORDER BY CASE pillar_name
             WHEN 'YEAR' THEN 0 WHEN 'MONTH' THEN 1
             WHEN 'DAY' THEN 2 WHEN 'HOUR' THEN 3 ELSE 99 END,
             pillar_name""",
        ("pillar_name", "stem", "branch", "fact_json"),
    ),
    "bazi_hidden_stems": (
        """SELECT pillar_name, sequence, hidden_stem
           FROM bazi_hidden_stems WHERE natal_profile_id=?
           ORDER BY CASE pillar_name
             WHEN 'YEAR' THEN 0 WHEN 'MONTH' THEN 1
             WHEN 'DAY' THEN 2 WHEN 'HOUR' THEN 3 ELSE 99 END,
             pillar_name, sequence""",
        ("pillar_name", "sequence", "hidden_stem"),
    ),
    "bazi_ten_gods": (
        """SELECT pillar_name, sequence, ten_god
           FROM bazi_ten_gods WHERE natal_profile_id=?
           ORDER BY CASE pillar_name
             WHEN 'YEAR' THEN 0 WHEN 'MONTH' THEN 1
             WHEN 'DAY' THEN 2 WHEN 'HOUR' THEN 3 ELSE 99 END,
             pillar_name, sequence""",
        ("pillar_name", "sequence", "ten_god"),
    ),
    "bazi_relations": (
        """SELECT sequence, relation_type, relation_json
           FROM bazi_relations WHERE natal_profile_id=?
           ORDER BY sequence, relation_type, relation_json""",
        ("sequence", "relation_type", "relation_json"),
    ),
    "bazi_luck_cycles": (
        """SELECT sequence, pillar, start_age_years, end_age_years, direction
           FROM bazi_luck_cycles WHERE natal_profile_id=?
           ORDER BY sequence, pillar, direction""",
        ("sequence", "pillar", "start_age_years", "end_age_years", "direction"),
    ),
}


def _normalize(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        decimal = Decimal(str(value)).normalize()
        return {"$decimal": format(decimal, "f")}
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, tuple):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        return {
            unicodedata.normalize("NFC", str(key)): _normalize(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    raise TypeError(f"unsupported canonical materialization value: {type(value)!r}")


def canonical_materialized_json(value: Any) -> str:
    """Serialize with fixed Unicode, null, decimal and JSON-key semantics."""
    return json.dumps(
        _normalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _json_field(name: str, value: Any) -> Any:
    if name.endswith("_json"):
        return json.loads(str(value))
    return value


def materialized_payload(
    connection: sqlite3.Connection,
    natal_profile_id: str,
) -> dict[str, Any]:
    identity = connection.execute(
        """SELECT n.natal_profile_id, n.calculation_run_id,
                  r.algorithm_version, r.ephemeris_version
           FROM bazi_natal_profiles n
           JOIN bazi_calculation_runs r
             ON r.calculation_run_id=n.calculation_run_id
           WHERE n.natal_profile_id=?""",
        (natal_profile_id,),
    ).fetchone()
    if identity is None:
        raise ValueError("natal profile does not exist")
    categories: list[dict[str, Any]] = []
    for category in CATEGORY_ORDER:
        query, columns = _CATEGORY_QUERIES[category]
        rows = connection.execute(query, (natal_profile_id,)).fetchall()
        categories.append(
            {
                "category": category,
                "rows": [
                    {
                        column: _json_field(column, row[index])
                        for index, column in enumerate(columns)
                    }
                    for row in rows
                ],
            }
        )
    return {
        "serialization_schema_version": SERIALIZATION_SCHEMA_VERSION,
        "identity": {
            "natal_profile_id": identity["natal_profile_id"],
            "calculation_run_id": identity["calculation_run_id"],
            "algorithm_version": identity["algorithm_version"],
            "ephemeris_version": identity["ephemeris_version"],
        },
        "category_order": list(CATEGORY_ORDER),
        "categories": categories,
    }


def materialized_facts_hash(
    connection: sqlite3.Connection,
    natal_profile_id: str,
) -> str:
    serialized = canonical_materialized_json(
        materialized_payload(connection, natal_profile_id)
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def materialized_category_counts(
    connection: sqlite3.Connection,
    natal_profile_id: str,
) -> dict[str, int]:
    payload = materialized_payload(connection, natal_profile_id)
    return {
        str(category["category"]): len(category["rows"])
        for category in payload["categories"]
    }
