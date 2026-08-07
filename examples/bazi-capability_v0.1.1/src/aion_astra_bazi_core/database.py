"""SQLite persistence boundary with foreign keys and transactions."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from importlib.resources import files
from pathlib import Path

from .errors import RepositoryError


class Database:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self._connection = sqlite3.connect(str(path), isolation_level=None)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")

    @property
    def connection(self) -> sqlite3.Connection:
        """Advanced access remains schema-constrained and cannot bypass invariants."""
        return self._connection

    def initialize(self) -> None:
        schema = files("aion_astra_bazi_core").joinpath("schema.sql").read_text(encoding="utf-8")
        try:
            self._connection.executescript(schema)
            self._connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES(?, ?)",
                (1, "2026-07-30T00:00:00+08:00"),
            )
            self._connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES(?, ?)",
                (2, "2026-07-30T06:20:00+08:00"),
            )
        except sqlite3.DatabaseError as exc:
            raise RepositoryError("Bazi schema initialization failed") from exc

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            yield self._connection
            self._connection.execute("COMMIT")
        except sqlite3.DatabaseError as exc:
            self._connection.execute("ROLLBACK")
            raise RepositoryError("Bazi transaction rolled back") from exc
        except BaseException:
            self._connection.execute("ROLLBACK")
            raise

    def close(self) -> None:
        self._connection.close()
