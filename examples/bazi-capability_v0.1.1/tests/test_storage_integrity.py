from __future__ import annotations

import sqlite3
from typing import Any

import pytest

from aion_astra_bazi_core.enums import LuckDirection
from aion_astra_bazi_core.integrity import (
    SERIALIZATION_SCHEMA_VERSION,
    canonical_materialized_json,
    materialized_facts_hash,
    materialized_payload,
)


IMMUTABLE_CASES = (
    ("bazi_pillars", "bazi_pillars_immutable_update", "stem='甲'"),
    (
        "bazi_hidden_stems",
        "bazi_hidden_stems_immutable_update",
        "hidden_stem='甲'",
    ),
    ("bazi_ten_gods", "bazi_ten_gods_immutable_update", "ten_god='比肩'"),
    (
        "bazi_relations",
        "bazi_relations_immutable_update",
        "relation_type='TAMPERED'",
    ),
)


@pytest.mark.parametrize(
    ("table", "trigger", "assignment"),
    IMMUTABLE_CASES,
    ids=(
        "BAZI_PILLAR_UPDATE_REJECTED_001",
        "BAZI_HIDDEN_STEM_UPDATE_REJECTED_001",
        "BAZI_TEN_GOD_UPDATE_REJECTED_001",
        "BAZI_RELATION_UPDATE_REJECTED_001",
    ),
)
def test_materialized_fact_update_rejected_001(
    persisted_profile: tuple[Any, Any],
    core: Any,
    table: str,
    trigger: str,
    assignment: str,
) -> None:
    _, profile = persisted_profile
    connection = core.database.connection
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            f"UPDATE {table} SET {assignment} WHERE natal_profile_id=?",
            (profile.natal_profile_id,),
        )
    assert trigger in {
        str(row[0])
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger'"
        ).fetchall()
    }


@pytest.mark.parametrize(
    ("table", "trigger"),
    (
        ("bazi_pillars", "bazi_pillars_immutable_delete"),
        ("bazi_hidden_stems", "bazi_hidden_stems_immutable_delete"),
        ("bazi_ten_gods", "bazi_ten_gods_immutable_delete"),
        ("bazi_relations", "bazi_relations_immutable_delete"),
    ),
    ids=(
        "BAZI_PILLAR_DELETE_REJECTED_001",
        "BAZI_HIDDEN_STEM_DELETE_REJECTED_001",
        "BAZI_TEN_GOD_DELETE_REJECTED_001",
        "BAZI_RELATION_DELETE_REJECTED_001",
    ),
)
def test_materialized_fact_delete_rejected_001(
    persisted_profile: tuple[Any, Any],
    core: Any,
    table: str,
    trigger: str,
) -> None:
    _, profile = persisted_profile
    connection = core.database.connection
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            f"DELETE FROM {table} WHERE natal_profile_id=?",
            (profile.natal_profile_id,),
        )
    assert trigger in {
        str(row[0])
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger'"
        ).fetchall()
    }


def test_bazi_luck_cycle_update_rejected_001(persisted_profile: tuple[Any, Any], core: Any) -> None:
    _, profile = persisted_profile
    core.calculate_luck_cycles(profile.natal_profile_id, LuckDirection.FORWARD, 3.0)
    with pytest.raises(sqlite3.IntegrityError):
        core.database.connection.execute(
            """UPDATE bazi_luck_cycles SET pillar='甲子'
               WHERE natal_profile_id=?""",
            (profile.natal_profile_id,),
        )


def test_bazi_luck_cycle_delete_rejected_001(persisted_profile: tuple[Any, Any], core: Any) -> None:
    _, profile = persisted_profile
    core.calculate_luck_cycles(profile.natal_profile_id, LuckDirection.FORWARD, 3.0)
    with pytest.raises(sqlite3.IntegrityError):
        core.database.connection.execute(
            "DELETE FROM bazi_luck_cycles WHERE natal_profile_id=?",
            (profile.natal_profile_id,),
        )


def _drop(connection: sqlite3.Connection, trigger: str) -> None:
    connection.execute(f"DROP TRIGGER {trigger}")


def test_bazi_stored_pillar_tampering_detected_001(
    persisted_profile: tuple[Any, Any], core: Any
) -> None:
    _, profile = persisted_profile
    connection = core.database.connection
    _drop(connection, "bazi_pillars_immutable_update")
    connection.execute(
        """UPDATE bazi_pillars SET stem='甲'
           WHERE natal_profile_id=? AND pillar_name='YEAR'""",
        (profile.natal_profile_id,),
    )
    assert core.verify_derivation_identity(profile.natal_profile_id)
    assert not core.verify_materialized_facts_integrity(profile.natal_profile_id)
    assert not core.verify_complete_calculation_integrity(profile.natal_profile_id)


def test_bazi_stored_relation_tampering_detected_001(
    persisted_profile: tuple[Any, Any], core: Any
) -> None:
    _, profile = persisted_profile
    connection = core.database.connection
    _drop(connection, "bazi_relations_immutable_update")
    connection.execute(
        """UPDATE bazi_relations SET relation_type='TAMPERED'
           WHERE natal_profile_id=? AND sequence=0""",
        (profile.natal_profile_id,),
    )
    assert not core.verify_materialized_facts_integrity(profile.natal_profile_id)


def test_bazi_stored_luck_cycle_tampering_detected_001(
    persisted_profile: tuple[Any, Any], core: Any
) -> None:
    _, profile = persisted_profile
    core.calculate_luck_cycles(profile.natal_profile_id, LuckDirection.FORWARD, 3.0)
    connection = core.database.connection
    _drop(connection, "bazi_luck_cycles_immutable_update")
    connection.execute(
        """UPDATE bazi_luck_cycles SET pillar='甲子'
           WHERE natal_profile_id=? AND sequence=1""",
        (profile.natal_profile_id,),
    )
    assert not core.verify_materialized_facts_integrity(profile.natal_profile_id)


def test_bazi_missing_materialized_row_detected_001(
    persisted_profile: tuple[Any, Any], core: Any
) -> None:
    _, profile = persisted_profile
    connection = core.database.connection
    _drop(connection, "bazi_hidden_stems_immutable_delete")
    connection.execute(
        """DELETE FROM bazi_hidden_stems
           WHERE natal_profile_id=? AND pillar_name='YEAR' AND sequence=0""",
        (profile.natal_profile_id,),
    )
    assert not core.verify_materialized_facts_integrity(profile.natal_profile_id)


def test_bazi_extra_materialized_row_detected_001(
    persisted_profile: tuple[Any, Any], core: Any
) -> None:
    _, profile = persisted_profile
    core.database.connection.execute(
        """INSERT INTO bazi_relations(
           natal_profile_id, sequence, relation_type, relation_json
        ) VALUES (?, 999, 'UNTRACED', '{"type":"UNTRACED"}')""",
        (profile.natal_profile_id,),
    )
    assert not core.verify_materialized_facts_integrity(profile.natal_profile_id)


def test_bazi_complete_integrity_pass_001(
    persisted_profile: tuple[Any, Any], core: Any
) -> None:
    _, profile = persisted_profile
    assert core.verify_derivation_identity(profile.natal_profile_id)
    assert core.verify_materialized_facts_integrity(profile.natal_profile_id)
    assert core.verify_complete_calculation_integrity(profile.natal_profile_id)
    core.calculate_luck_cycles(profile.natal_profile_id, LuckDirection.FORWARD, 3.0)
    assert core.verify_complete_calculation_integrity(profile.natal_profile_id)


def test_bazi_canonical_serialization_deterministic_001(
    persisted_profile: tuple[Any, Any], core: Any
) -> None:
    _, profile = persisted_profile
    connection = core.database.connection
    payload = materialized_payload(connection, profile.natal_profile_id)
    assert payload["serialization_schema_version"] == SERIALIZATION_SCHEMA_VERSION
    assert canonical_materialized_json(payload) == canonical_materialized_json(payload)
    assert materialized_facts_hash(
        connection, profile.natal_profile_id
    ) == materialized_facts_hash(connection, profile.natal_profile_id)


def test_snapshot_is_append_only_001(
    persisted_profile: tuple[Any, Any], core: Any
) -> None:
    _, profile = persisted_profile
    with pytest.raises(sqlite3.IntegrityError):
        core.database.connection.execute(
            """UPDATE bazi_materialization_snapshots
               SET materialized_facts_hash='tampered'
               WHERE natal_profile_id=?""",
            (profile.natal_profile_id,),
        )


def test_schema_migration_v2_recorded_001(core: Any) -> None:
    versions = [
        int(row[0])
        for row in core.database.connection.execute(
            "SELECT version FROM schema_migrations ORDER BY version"
        ).fetchall()
    ]
    assert versions == [1, 2]
