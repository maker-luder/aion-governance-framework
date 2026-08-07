
from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from ..errors import AuditDatabaseError, SchemaVersionError

SCHEMA_VERSION = "1"

@contextmanager
def open_database(db_path: str) -> Iterator[sqlite3.Connection]:
    connection = None
    try:
        connection = sqlite3.connect(db_path, timeout=5)
        connection.row_factory = sqlite3.Row
        yield connection
    except sqlite3.Error as exc:
        raise AuditDatabaseError("database operation failed") from exc
    finally:
        if connection is not None:
            connection.close()

def init_schema(connection: sqlite3.Connection) -> None:
    try:
        connection.execute("CREATE TABLE IF NOT EXISTS schema_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        row = connection.execute("SELECT value FROM schema_metadata WHERE key='schema_version'").fetchone()
        if row is not None and row["value"] != SCHEMA_VERSION:
            raise SchemaVersionError("unsupported audit schema version")
        connection.execute("INSERT OR IGNORE INTO schema_metadata(key,value) VALUES('schema_version',?)", (SCHEMA_VERSION,))
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT NOT NULL,
                stage TEXT NOT NULL,
                decision TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                status TEXT NOT NULL,
                policy_version TEXT NOT NULL,
                rule_ids TEXT NOT NULL,
                source_type TEXT NOT NULL,
                action TEXT NOT NULL,
                target_class TEXT NOT NULL,
                environment TEXT NOT NULL,
                authorization_state TEXT NOT NULL,
                input_hash TEXT NOT NULL,
                reason_code TEXT NOT NULL,
                error_code TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    except SchemaVersionError:
        raise
    except sqlite3.Error as exc:
        raise AuditDatabaseError("audit schema initialization failed") from exc
