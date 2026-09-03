"""Opt-in, bounded claim revision in the existing local memory database.

Relations and review decisions are supplied by a caller, not inferred from text.
RECORDED means eligible for the existing recall gate, never established truth.
No model, scheduler, network, repository writer or canonical-state writer runs here.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
import re

from .revision_integrity import bounded_dag, canonical_payload, identifier, strict_json, timestamp
from .models import RecallRequest
from .store import MemoryWriteDenied, SQLiteMemoryStore, StoredMemory


MAX_VERSIONS = 256
MAX_EVENTS = 2048
MAX_EVIDENCE = 1024
MAX_DEPTH = 64
MAX_EDGES = 1024
MAX_PARENTS = 16
MAX_AFFECTED = 256
MAX_EVENT_BYTES = 196608
MAX_HISTORY_BYTES = 8 * 1024 * 1024
MAX_SOURCE_NODES = 2048
MAX_LINEAGE_PARENTS = 8


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash(value: object) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _text(value: str, name: str, limit: int = 4000) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{name} must be nonblank and at most {limit} characters")


class InferenceType(str, Enum):
    OBSERVATION = "OBSERVATION"
    ANALOGY = "ANALOGY"
    INFERENCE = "INFERENCE"


class ClaimStatus(str, Enum):
    RECORDED = "RECORDED"
    CHALLENGED = "CHALLENGED"
    DEPENDENCY_HOLD = "DEPENDENCY_HOLD"
    SUPERSEDED = "SUPERSEDED"
    WITHDRAWN = "WITHDRAWN"


class EvidenceRelation(str, Enum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    IRRELEVANT = "IRRELEVANT"


class ReviewDecision(str, Enum):
    RETAIN = "RETAIN"
    REVISE = "REVISE"
    WITHDRAW = "WITHDRAW"


@dataclass(frozen=True, slots=True)
class EvidenceLink:
    evidence_id: str
    target_memory_id: str
    source_id: str
    locator: str
    content_sha256: str
    relation: EvidenceRelation
    rationale: str
    provenance_verified: bool
    derived_from: tuple[str, ...] = ()
    publisher: str | None = None
    retrieval_agent: str | None = None
    retrieval_event_id: str | None = None

    def __post_init__(self) -> None:
        for name in ("evidence_id", "target_memory_id", "source_id", "locator", "rationale"):
            _text(getattr(self, name), name)
        for name in ("evidence_id", "target_memory_id", "source_id"):
            identifier(getattr(self, name), name)
        if not isinstance(self.derived_from, tuple) or len(self.derived_from) > MAX_LINEAGE_PARENTS or len(set(self.derived_from)) != len(self.derived_from):
            raise ValueError("source lineage parent budget or duplicate")
        for parent in self.derived_from:
            identifier(parent, "derived_from")
            if parent == self.source_id:
                raise ValueError("source lineage cycle")
        object.__setattr__(self, "derived_from", tuple(sorted(self.derived_from)))
        for name in ("retrieval_agent", "retrieval_event_id"):
            if getattr(self, name) is not None:
                identifier(getattr(self, name), name)
        if self.publisher is not None:
            _text(self.publisher, "publisher", 200)
        if not isinstance(self.relation, EvidenceRelation):
            raise ValueError("relation must be an EvidenceRelation")
        if not re.fullmatch(r"[0-9a-f]{64}", self.content_sha256):
            raise ValueError("content_sha256 must be a lowercase SHA-256 digest")
        if self.provenance_verified is not True:
            raise MemoryWriteDenied("verified provenance is required; it does not establish correctness")


@dataclass(frozen=True, slots=True)
class RevisionRequest:
    claim_id: str
    memory_id: str
    version: int
    status: ClaimStatus
    evidence_refs: tuple[str, ...]
    dependency_refs: tuple[str, ...]
    expected_event_hash: str
    canonical_effect: str = "NONE"
    counterevidence_refs: tuple[str, ...] = ()
    affected_by: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        identifier(self.claim_id, "claim_id")
        identifier(self.memory_id, "memory_id")
        if type(self.version) is not int or self.version < 1 or not isinstance(self.status, ClaimStatus):
            raise ValueError("revision request requires a positive version and typed status")
        if not re.fullmatch(r"[0-9a-f]{64}", self.expected_event_hash):
            raise ValueError("revision request requires an exact event hash")
        for refs in (self.evidence_refs, self.dependency_refs, self.counterevidence_refs, self.affected_by):
            if not isinstance(refs, tuple) or len(refs) > MAX_EVIDENCE or len(refs) != len(set(refs)):
                raise ValueError("revision references must be distinct tuples")
            for ref in refs:
                identifier(ref, "revision reference")
        if self.canonical_effect != "NONE":
            raise ValueError("revision requests cannot create canonical effects")


class ClaimRevisionService:
    """One identity/namespace view over SQLiteMemoryStore, not a second memory store.

    The request is a caller-supplied scope, not authentication. The caller must
    enforce identity and write approval before using this local library.
    """

    def __init__(self, store: SQLiteMemoryStore, request: RecallRequest, *, namespace: str) -> None:
        identifier(namespace, "namespace")
        identifier(request.user_id, "user_id")
        identifier(request.agent_id, "agent_id")
        self.store = store
        self.request = request
        self.namespace = namespace
        self.scope = _hash([request.user_id, request.agent_id, namespace])
        with self.store._session() as db:
            db.executescript("""BEGIN IMMEDIATE;
                CREATE TABLE IF NOT EXISTS claim_versions (
                    memory_id TEXT PRIMARY KEY REFERENCES memory_records(memory_id),
                    scope TEXT NOT NULL, claim_id TEXT NOT NULL, version INTEGER NOT NULL,
                    status TEXT NOT NULL CHECK(status IN
                        ('RECORDED','CHALLENGED','DEPENDENCY_HOLD','SUPERSEDED','WITHDRAWN')),
                    inference_type TEXT NOT NULL, assumptions_json TEXT NOT NULL,
                    dependencies_json TEXT NOT NULL, supersedes TEXT,
                    UNIQUE(scope, claim_id, version)
                );
                CREATE TABLE IF NOT EXISTS claim_evidence (
                    scope TEXT NOT NULL, evidence_id TEXT NOT NULL, target_memory_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL, PRIMARY KEY(scope, evidence_id)
                );
                CREATE TABLE IF NOT EXISTS claim_revision_events (
                    scope TEXT NOT NULL, sequence INTEGER NOT NULL,
                    previous_hash TEXT NOT NULL, payload_json TEXT NOT NULL, event_hash TEXT NOT NULL,
                    PRIMARY KEY(scope, sequence)
                );
                CREATE TRIGGER IF NOT EXISTS claim_hold_guard BEFORE UPDATE OF conflict ON memory_records
                WHEN NEW.conflict=0 AND EXISTS (
                    SELECT 1 FROM claim_versions WHERE memory_id=OLD.memory_id AND status!='RECORDED'
                ) BEGIN SELECT RAISE(ABORT, 'managed claim hold requires explicit versioned review'); END;
                CREATE TRIGGER IF NOT EXISTS claim_content_guard BEFORE UPDATE ON memory_records
                WHEN EXISTS (SELECT 1 FROM claim_versions WHERE memory_id=OLD.memory_id) AND
                    (NEW.content!=OLD.content OR NEW.namespace!=OLD.namespace OR NEW.user_id!=OLD.user_id OR
                     NEW.agent_id!=OLD.agent_id OR NEW.provenance_source!=OLD.provenance_source OR
                     NEW.provenance_verified!=OLD.provenance_verified OR NEW.access_scope_json!=OLD.access_scope_json OR
                     NEW.recorded_at!=OLD.recorded_at OR NEW.entities_json!=OLD.entities_json OR
                     NEW.topics_json!=OLD.topics_json OR NEW.memory_id!=OLD.memory_id)
                BEGIN SELECT RAISE(ABORT, 'managed claim content is immutable'); END;
            """)
            self._validate_state(db)

    @staticmethod
    def _evidence_payload(raw: str) -> dict:
        data = strict_json(raw)
        if not isinstance(data, dict):
            raise ValueError("corrupt evidence object")
        data["relation"] = EvidenceRelation(data["relation"])
        data["derived_from"] = tuple(data.get("derived_from", ()))
        return asdict(EvidenceLink(**data))

    @staticmethod
    def _duplicates(links: list[dict]) -> list[dict]:
        groups: dict[str, list[str]] = {}
        for link in links:
            groups.setdefault(link["content_sha256"], []).append(link["evidence_id"])
        return [{"content_sha256": key, "evidence_ids": sorted(ids)}
                for key, ids in sorted(groups.items()) if len(ids) > 1]

    @staticmethod
    def _source_lineage(links: list[dict]) -> dict[str, list[str]]:
        graph: dict[str, tuple[str, ...]] = {}
        for link in links:
            source = link["source_id"]
            parents = tuple(link.get("derived_from", ()))
            if graph.get(source) and parents and graph[source] != parents:
                raise ValueError("conflicting declared source lineage")
            graph[source] = parents or graph.get(source, ())
        for parents in tuple(graph.values()):
            for parent in parents:
                graph.setdefault(parent, ())
        order = bounded_dag(graph, max_nodes=MAX_SOURCE_NODES, max_edges=MAX_EVIDENCE * MAX_LINEAGE_PARENTS,
                            max_depth=MAX_DEPTH, max_parents=MAX_LINEAGE_PARENTS)
        roots: dict[str, list[str]] = {}
        for source in order:
            roots[source] = sorted(set().union(*(set(roots[parent]) for parent in graph[source]))) if graph[source] else [source]
        return {key: roots[key] for key in sorted(roots)}

    def _graph(self, db) -> tuple[dict, dict]:
        count = db.execute("SELECT count(*) FROM claim_versions WHERE scope=?", (self.scope,)).fetchone()[0]
        if count > MAX_VERSIONS:
            raise ValueError("claim version budget exceeded")
        if db.execute("SELECT 1 FROM claim_versions WHERE scope=? AND (length(dependencies_json)>4000 OR length(assumptions_json)>160000 OR length(memory_id)>200 OR length(claim_id)>200) LIMIT 1", (self.scope,)).fetchone():
            raise ValueError("stored version text budget exceeded")
        rows = {r["memory_id"]: r for r in db.execute("SELECT * FROM claim_versions WHERE scope=? ORDER BY memory_id", (self.scope,))}
        graph = {}
        for mid, row in rows.items():
            identifier(mid, "memory_id")
            identifier(row["claim_id"], "claim_id")
            if len(row["dependencies_json"]) > 4000:
                raise ValueError("dependency payload budget exceeded")
            refs = strict_json(row["dependencies_json"])
            if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
                raise ValueError("corrupt dependencies")
            graph[mid] = tuple(refs)
        bounded_dag(graph, max_nodes=MAX_VERSIONS, max_edges=MAX_EDGES, max_depth=MAX_DEPTH,
                    max_parents=MAX_PARENTS, labels={mid: r["claim_id"] for mid, r in rows.items()})
        return rows, graph

    def _lineage(self, db, memory_id: str) -> set[str]:
        _, graph = self._graph(db)
        result = set()
        todo = [memory_id]
        while todo:
            mid = todo.pop()
            if mid not in result:
                self._version(db, mid)
                result.add(mid)
                todo.extend(graph[mid])
        return result

    def _validate_state(self, db) -> None:
        """Fail closed on bounded structural corruption; no repair or truth judgment."""
        expected = {
            "claim_versions": ("memory_id", "scope", "claim_id", "version", "status", "inference_type", "assumptions_json", "dependencies_json", "supersedes"),
            "claim_evidence": ("scope", "evidence_id", "target_memory_id", "payload_json"),
            "claim_revision_events": ("scope", "sequence", "previous_hash", "payload_json", "event_hash"),
        }
        for table, columns in expected.items():
            if tuple(r["name"] for r in db.execute(f"PRAGMA table_info({table})")) != columns:
                raise ValueError("unsupported revision database schema")
        counts = {table: db.execute(f"SELECT count(*) FROM {table} WHERE scope=?", (self.scope,)).fetchone()[0]
                  for table in expected}
        if counts["claim_evidence"] > MAX_EVIDENCE or counts["claim_revision_events"] > MAX_EVENTS:
            raise ValueError("stored evidence/event budget exceeded")
        if db.execute("SELECT 1 FROM claim_evidence WHERE scope=? AND length(payload_json)>40000 LIMIT 1", (self.scope,)).fetchone():
            raise ValueError("stored evidence payload budget exceeded")
        size = db.execute("SELECT coalesce(sum(length(cast(payload_json AS BLOB))),0), coalesce(max(length(cast(payload_json AS BLOB))),0) FROM claim_revision_events WHERE scope=?", (self.scope,)).fetchone()
        if size[0] > MAX_HISTORY_BYTES or size[1] > MAX_EVENT_BYTES:
            raise ValueError("event byte budget exceeded")
        rows, graph = self._graph(db)
        claims: dict[str, list[int]] = {}
        for mid, row in rows.items():
            if type(row["version"]) is not int or row["version"] < 1:
                raise ValueError("corrupt claim version")
            claims.setdefault(row["claim_id"], []).append(row["version"])
            status = ClaimStatus(row["status"])
            InferenceType(row["inference_type"])
            assumptions = strict_json(row["assumptions_json"])
            if not isinstance(assumptions, list) or len(assumptions) > 32:
                raise ValueError("corrupt assumptions")
            for assumption in assumptions:
                _text(assumption, "assumption")
            memory = db.execute("SELECT * FROM memory_records WHERE memory_id=?", (mid,)).fetchone()
            if memory is None or (memory["user_id"], memory["agent_id"], memory["namespace"]) != (
                self.request.user_id, self.request.agent_id, self.namespace
            ) or memory["canonical_effect"] != "NONE" or memory["provenance_verified"] != 1:
                raise ValueError("corrupt claim identity or provenance")
            flags = tuple(memory[key] for key in ("conflict", "superseded", "tombstoned"))
            required = (0, 0, 0) if status is ClaimStatus.RECORDED else (
                (1, 1, 0) if status in {ClaimStatus.SUPERSEDED, ClaimStatus.WITHDRAWN} else (1, 0, 0))
            if flags != required:
                raise ValueError("corrupt claim flag/status binding")
            if status is ClaimStatus.RECORDED and any(rows[parent]["status"] != ClaimStatus.RECORDED for parent in graph[mid]):
                raise ValueError("recorded dependent has inactive premise")
            if row["version"] == 1:
                if row["supersedes"] is not None:
                    raise ValueError("invalid first-version supersession")
            else:
                previous = rows.get(row["supersedes"])
                if previous is None or previous["claim_id"] != row["claim_id"] or previous["version"] != row["version"] - 1 or previous["status"] != ClaimStatus.SUPERSEDED:
                    raise ValueError("invalid supersession lineage")
        if any(sorted(versions) != list(range(1, len(versions) + 1)) for versions in claims.values()):
            raise ValueError("nonlinear claim version sequence")
        links = []
        for row in db.execute("SELECT * FROM claim_evidence WHERE scope=? ORDER BY evidence_id", (self.scope,)):
            if len(row["payload_json"]) > 40000:
                raise ValueError("evidence payload budget exceeded")
            link = self._evidence_payload(row["payload_json"])
            if link["evidence_id"] != row["evidence_id"] or link["target_memory_id"] != row["target_memory_id"] or link["target_memory_id"] not in rows:
                raise ValueError("corrupt evidence binding")
            links.append(link)
        self._source_lineage(links)
        events = [dict(r) for r in db.execute("SELECT * FROM claim_revision_events WHERE scope=? ORDER BY sequence", (self.scope,))]
        if not verify_revision_history({"events": events, "event_head": self._head(db)}):
            raise ValueError("revision event chain damaged")
        self._validate_projection(rows, links, events)

    @staticmethod
    def _validate_projection(rows: dict, links: list[dict], events: list[dict]) -> None:
        """Cross-check bounded event effects, not authenticity of a rewritten database."""
        statuses: dict[str, str] = {}
        dependencies: dict[str, tuple] = {}
        seen_evidence: dict[str, dict] = {}
        retired = {ClaimStatus.SUPERSEDED, ClaimStatus.WITHDRAWN}

        def insert(mid, claim_id, version, parents, previous):
            row = rows.get(mid)
            if mid in statuses or row is None or (row['claim_id'], row['version'], row['supersedes']) != (claim_id, version, previous):
                raise ValueError("event/version projection mismatch")
            if list(parents) != strict_json(row['dependencies_json']) or any(statuses.get(p) != ClaimStatus.RECORDED for p in parents):
                raise ValueError("event/dependency projection mismatch")
            statuses[mid] = ClaimStatus.RECORDED
            dependencies[mid] = tuple(parents)

        def hold(mid, status, declared):
            affected = {mid}
            for node in bounded_dag(dependencies, max_nodes=MAX_VERSIONS, max_edges=MAX_EDGES,
                                    max_depth=MAX_DEPTH, max_parents=MAX_PARENTS):
                if 'canonicalization' not in p and statuses[node] in retired:
                    continue  # Preserve the pre-hardening V1 event interpretation.
                if affected.intersection(dependencies[node]):
                    affected.add(node)
            if sorted(affected) != declared:
                raise ValueError("event/affected projection mismatch")
            for node in sorted(affected):
                if node == mid:
                    statuses[node] = status
                elif statuses[node] not in retired and statuses[node] != ClaimStatus.CHALLENGED:
                    statuses[node] = ClaimStatus.DEPENDENCY_HOLD

        try:
            for event in events:
                p = strict_json(event['payload_json'])
                if p['kind'] == 'REGISTER':
                    insert(p['memory']['memory_id'], p['claim_id'], 1, p['dependencies'], None)
                elif p['kind'] == 'EVIDENCE':
                    link = ClaimRevisionService._evidence_payload(_json(p['link']))
                    mid, eid = link['target_memory_id'], link['evidence_id']
                    if eid in seen_evidence or mid not in statuses or statuses[mid] in retired:
                        raise ValueError("event/evidence projection mismatch")
                    seen_evidence[eid] = link
                    if link['relation'] == EvidenceRelation.CONTRADICTS:
                        hold(mid, ClaimStatus.CHALLENGED, p['affected'])
                    elif p['affected'] != []:
                        raise ValueError("non-counterevidence affected claims")
                elif p['kind'] == 'REVIEW':
                    mid = p['memory_id']
                    if statuses.get(mid) not in {ClaimStatus.CHALLENGED, ClaimStatus.DEPENDENCY_HOLD}:
                        raise ValueError("event/review projection mismatch")
                    decision = ReviewDecision(p['decision'])
                    if decision == ReviewDecision.WITHDRAW:
                        if p['successor'] is not None:
                            raise ValueError("withdrawal created successor")
                        hold(mid, ClaimStatus.WITHDRAWN, p['affected'])
                    else:
                        insert(p['successor'], rows[mid]['claim_id'], rows[mid]['version'] + 1, p['dependencies'], mid)
                        hold(mid, ClaimStatus.SUPERSEDED, p['affected'])
                else:
                    raise ValueError("unknown revision event kind")
            if statuses != {mid: row['status'] for mid, row in rows.items()}:
                raise ValueError("event/status projection mismatch")
            # New events normalize human text; V1 events and stored payloads remain untouched.
            def normalize(link):
                return canonical_payload({'link': link})
            if {k: normalize(v) for k, v in seen_evidence.items()} != {v['evidence_id']: normalize(v) for v in links}:
                raise ValueError("event/evidence projection mismatch")
        except (KeyError, TypeError) as exc:
            raise ValueError("malformed revision event projection") from exc

    @contextmanager
    def _transaction(self, approved: bool):
        if approved is not True:
            raise MemoryWriteDenied("explicit local writeback approval is required")
        db = self.store._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            self._validate_state(db)
            yield db
            self._validate_state(db)
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _memory(self, db, memory_id: str) -> StoredMemory:
        identifier(memory_id, "memory_id")
        if db.execute("SELECT 1 FROM memory_records WHERE memory_id=? AND (length(content)>4000 OR length(provenance_source)>4000 OR length(entities_json)>16000 OR length(topics_json)>16000 OR length(access_scope_json)>16000) LIMIT 1", (memory_id,)).fetchone():
            raise ValueError("memory text budget exceeded")
        row = db.execute("SELECT * FROM memory_records WHERE memory_id=?", (memory_id,)).fetchone()
        if row is None:
            raise KeyError(memory_id)
        item = self.store._decode(row)
        if (item.user_id, item.agent_id, item.namespace) != (
            self.request.user_id, self.request.agent_id, self.namespace
        ) or not item.access_scope.issubset(self.request.requester_scopes):
            raise MemoryWriteDenied("claim identity, namespace or access scope mismatch")
        if not item.provenance_verified or item.canonical_effect != "NONE":
            raise MemoryWriteDenied("claim provenance or canonical boundary invalid")
        _text(item.content, "memory content")
        _text(item.provenance_source, "memory provenance")
        timestamp(item.recorded_at)
        for refs in (item.entities, item.topics, item.access_scope):
            if len(refs) > 64:
                raise ValueError("memory reference budget exceeded")
            for ref in refs:
                identifier(ref, "memory reference")
        return item

    def _version(self, db, memory_id: str):
        self._memory(db, memory_id)
        row = db.execute("SELECT * FROM claim_versions WHERE memory_id=? AND scope=?", (memory_id, self.scope)).fetchone()
        if row is None:
            raise KeyError(memory_id)
        return row

    def _head(self, db) -> str:
        row = db.execute("SELECT event_hash FROM claim_revision_events WHERE scope=? ORDER BY sequence DESC LIMIT 1", (self.scope,)).fetchone()
        return "GENESIS" if row is None else row[0]

    def _append(self, db, payload: dict) -> None:
        count = db.execute("SELECT count(*) FROM claim_revision_events WHERE scope=?", (self.scope,)).fetchone()[0]
        if count >= MAX_EVENTS:
            raise ValueError("revision event budget exhausted")
        payload = canonical_payload(payload)
        encoded = _json(payload)
        size = len(encoded.encode("utf-8"))
        used = db.execute("SELECT coalesce(sum(length(cast(payload_json AS BLOB))),0) FROM claim_revision_events WHERE scope=?", (self.scope,)).fetchone()[0]
        if size > MAX_EVENT_BYTES or used + size > MAX_HISTORY_BYTES:
            raise ValueError("event byte budget exceeded")
        previous = self._head(db)
        digest = _hash({"sequence": count + 1, "previous_hash": previous, "payload": payload})
        db.execute("INSERT INTO claim_revision_events VALUES(?,?,?,?,?)", (self.scope, count + 1, previous, _json(payload), digest))

    def _dependencies(self, db, ids: tuple[str, ...], item: StoredMemory, claim_id: str) -> None:
        if not isinstance(ids, tuple) or len(ids) > MAX_PARENTS or len(ids) != len(set(ids)):
            raise ValueError("dependencies must be a tuple of at most 16 distinct version IDs")
        for mid in ids:
            parent = self._version(db, mid)
            memory = self._memory(db, mid)
            if parent["status"] != ClaimStatus.RECORDED or memory.conflict or memory.superseded or memory.tombstoned:
                raise ValueError("dependencies must be active, unchallenged recorded versions")
            if not memory.access_scope.issubset(item.access_scope):
                raise MemoryWriteDenied("derived claim cannot broaden dependency access")
        rows, graph = self._graph(db)
        graph[item.memory_id] = ids
        labels = {mid: row["claim_id"] for mid, row in rows.items()}
        labels[item.memory_id] = claim_id
        bounded_dag(graph, max_nodes=MAX_VERSIONS, max_edges=MAX_EDGES, max_depth=MAX_DEPTH,
                    max_parents=MAX_PARENTS, labels=labels)

    def _insert(self, db, memory_id: str, claim_id: str, version: int, inference_type: InferenceType,
                assumptions: tuple[str, ...], dependencies: tuple[str, ...], supersedes: str | None) -> None:
        identifier(claim_id, "claim_id")
        if not isinstance(inference_type, InferenceType):
            raise ValueError("inference_type must be an InferenceType")
        if not isinstance(assumptions, tuple) or len(assumptions) > 32:
            raise ValueError("assumptions must be a tuple of at most 32 entries")
        for assumption in assumptions:
            _text(assumption, "assumption")
        count = db.execute("SELECT count(*) FROM claim_versions WHERE scope=?", (self.scope,)).fetchone()[0]
        if count >= MAX_VERSIONS:
            raise ValueError("claim version budget exhausted")
        self._dependencies(db, dependencies, self._memory(db, memory_id), claim_id)
        db.execute("INSERT INTO claim_versions VALUES(?,?,?,?,?,?,?,?,?)", (
            memory_id, self.scope, claim_id, version, ClaimStatus.RECORDED.value,
            inference_type.value, _json(assumptions), _json(sorted(dependencies)), supersedes,
        ))

    def register(self, memory_id: str, *, claim_id: str, inference_type: InferenceType,
                 assumptions: tuple[str, ...] = (), dependencies: tuple[str, ...] = (),
                 writeback_approved: bool = False) -> None:
        """Enroll an existing approved memory; enrollment itself is not evidence of truth."""
        with self._transaction(writeback_approved) as db:
            item = self._memory(db, memory_id)
            if item.conflict or item.tombstoned or item.superseded:
                raise ValueError("only active memory can be enrolled")
            if db.execute("SELECT 1 FROM claim_versions WHERE scope=? AND claim_id=?", (self.scope, claim_id)).fetchone():
                raise ValueError("claim already exists; use versioned review")
            self._insert(db, memory_id, claim_id, 1, inference_type, assumptions, dependencies, None)
            self._append(db, {"kind": "REGISTER", "memory": asdict(item) | {
                "entities": sorted(item.entities), "topics": sorted(item.topics), "access_scope": sorted(item.access_scope)},
                "claim_id": claim_id, "inference_type": inference_type.value,
                "assumptions": assumptions, "dependencies": sorted(dependencies)})

    def _hold(self, db, memory_id: str, status: ClaimStatus) -> list[str]:
        rows, graph = self._graph(db)
        affected = {memory_id}
        # Include retired nodes while traversing historical version-bound edges.
        for mid in bounded_dag(graph, max_nodes=MAX_VERSIONS, max_edges=MAX_EDGES,
                               max_depth=MAX_DEPTH, max_parents=MAX_PARENTS):
            if affected.intersection(graph[mid]):
                affected.add(mid)
        if len(affected) > MAX_AFFECTED:
            raise ValueError("affected downstream budget exceeded")
        for mid in sorted(affected):
            current = self._version(db, mid)
            if mid != memory_id and current["status"] in {ClaimStatus.SUPERSEDED, ClaimStatus.WITHDRAWN}:
                continue
            next_status = status if mid == memory_id else (
                ClaimStatus.CHALLENGED if current["status"] == ClaimStatus.CHALLENGED else ClaimStatus.DEPENDENCY_HOLD)
            db.execute("UPDATE claim_versions SET status=? WHERE memory_id=?", (next_status.value, mid))
            db.execute("UPDATE memory_records SET conflict=1 WHERE memory_id=?", (mid,))
        return sorted(affected)

    def add_evidence(self, link: EvidenceLink, *, writeback_approved: bool = False) -> bool:
        """Append a typed, caller-verified relation; identical delivery is idempotent."""
        if not isinstance(link, EvidenceLink):
            raise TypeError("expected EvidenceLink")
        with self._transaction(writeback_approved) as db:
            target = self._version(db, link.target_memory_id)
            payload = asdict(link)
            existing = db.execute("SELECT payload_json FROM claim_evidence WHERE scope=? AND evidence_id=?", (self.scope, link.evidence_id)).fetchone()
            if existing:
                if self._evidence_payload(existing[0]) != payload:
                    raise ValueError("evidence ID collision")
                return False
            if target["status"] in {ClaimStatus.SUPERSEDED, ClaimStatus.WITHDRAWN}:
                raise ValueError("stale target version; explicitly assess relevance to its successor")
            if db.execute("SELECT count(*) FROM claim_evidence WHERE scope=?", (self.scope,)).fetchone()[0] >= MAX_EVIDENCE:
                raise ValueError("evidence budget exhausted")
            self._source_lineage([self._evidence_payload(r[0]) for r in db.execute("SELECT payload_json FROM claim_evidence WHERE scope=? ORDER BY evidence_id", (self.scope,))] + [payload])
            db.execute("INSERT INTO claim_evidence VALUES(?,?,?,?)", (self.scope, link.evidence_id, link.target_memory_id, _json(payload)))
            affected = self._hold(db, link.target_memory_id, ClaimStatus.CHALLENGED) if link.relation is EvidenceRelation.CONTRADICTS else []
            self._append(db, {"kind": "EVIDENCE", "link": payload, "affected": affected})
            return True

    def pending_reviews(self, *, limit: int = 8) -> tuple[RevisionRequest, ...]:
        if type(limit) is not int or not 1 <= limit <= 64:
            raise ValueError("pending review limit must be an integer between 1 and 64")
        with self.store._session() as db:
            db.execute("BEGIN")
            self._validate_state(db)
            rows = db.execute("SELECT * FROM claim_versions WHERE scope=? AND status IN ('CHALLENGED','DEPENDENCY_HOLD') ORDER BY memory_id", (self.scope,)).fetchall()
            result = []
            for row in rows:
                try:
                    item = self._memory(db, row["memory_id"])
                except MemoryWriteDenied:
                    continue
                if item.tombstoned or item.superseded:
                    continue
                lineage = self._lineage(db, row["memory_id"])
                links = [self._evidence_payload(r[0]) for r in db.execute("SELECT payload_json FROM claim_evidence WHERE scope=? ORDER BY evidence_id", (self.scope,))]
                refs = tuple(link["evidence_id"] for link in links if link["target_memory_id"] in lineage)
                counter = tuple(link["evidence_id"] for link in links if link["target_memory_id"] in lineage and link["relation"] == EvidenceRelation.CONTRADICTS)
                causes = tuple(sorted({link["target_memory_id"] for link in links if link["evidence_id"] in counter}))
                result.append(RevisionRequest(row["claim_id"], row["memory_id"], row["version"], ClaimStatus(row["status"]), refs,
                                              tuple(strict_json(row["dependencies_json"])), self._head(db),
                                              counterevidence_refs=counter, affected_by=causes))
            return tuple(result[:limit])

    def resolve(self, memory_id: str, *, decision: ReviewDecision, reason: str, reviewer_ref: str,
                evidence_refs: tuple[str, ...], expected_event_hash: str, recorded_at: str,
                replacement_content: str | None = None, dependencies: tuple[str, ...] = (),
                assumptions: tuple[str, ...] = (), inference_type: InferenceType | None = None,
                writeback_approved: bool = False) -> str | None:
        """Record a caller's review, never adjudicate truth or auto-release dependents.

        RETAIN and REVISE create a fresh immutable memory version. A caller must
        explicitly supply the successor's assumptions and dependency version IDs.
        """
        if not isinstance(decision, ReviewDecision):
            raise ValueError("decision must be a ReviewDecision")
        for name, value in (("reason", reason), ("reviewer_ref", reviewer_ref), ("recorded_at", recorded_at)):
            _text(value, name)
        recorded_at = timestamp(recorded_at)
        identifier(memory_id, "memory_id")
        if inference_type is not None and not isinstance(inference_type, InferenceType):
            raise ValueError("inference_type must be an InferenceType")
        if not isinstance(evidence_refs, tuple) or not evidence_refs or len(evidence_refs) > MAX_EVIDENCE or len(set(evidence_refs)) != len(evidence_refs):
            raise ValueError(f"review requires 1..{MAX_EVIDENCE} distinct evidence references")
        with self._transaction(writeback_approved) as db:
            old = self._version(db, memory_id)
            item = self._memory(db, memory_id)
            if expected_event_hash != self._head(db):
                raise ValueError("stale review; reload after new evidence or revisions")
            if old["status"] not in {ClaimStatus.CHALLENGED, ClaimStatus.DEPENDENCY_HOLD} or item.tombstoned or item.superseded:
                raise ValueError("review requires an active pending version")
            # Evidence may address this version or one of its transitive premises.
            lineage = self._lineage(db, memory_id)
            visible = {r["evidence_id"]: self._evidence_payload(r["payload_json"]) for r in db.execute("SELECT * FROM claim_evidence WHERE scope=?", (self.scope,)) if r["target_memory_id"] in lineage}
            if any(ref not in visible or visible[ref]["relation"] == EvidenceRelation.IRRELEVANT for ref in evidence_refs):
                raise ValueError("review evidence must be relevant to the claim or its premises")
            required = {key for key, value in visible.items() if value["relation"] == EvidenceRelation.CONTRADICTS}
            if not required.issubset(evidence_refs):
                raise ValueError("review must explicitly address all recorded counterevidence in its lineage")
            successor = None
            if decision is ReviewDecision.WITHDRAW:
                if replacement_content is not None or dependencies or assumptions or inference_type is not None:
                    raise ValueError("withdrawal cannot supply successor fields")
                affected = self._hold(db, memory_id, ClaimStatus.WITHDRAWN)
                db.execute("UPDATE memory_records SET superseded=1 WHERE memory_id=?", (memory_id,))
            else:
                content = item.content if decision is ReviewDecision.RETAIN else replacement_content
                _text(content, "replacement_content")
                if decision is ReviewDecision.RETAIN and replacement_content is not None:
                    raise ValueError("retain uses the existing content")
                if decision is ReviewDecision.REVISE and content == item.content:
                    raise ValueError("revision must change content; use retain otherwise")
                version = old["version"] + 1
                successor = "claim-version:" + _hash([self.scope, old["claim_id"], version])
                db.execute("""INSERT INTO memory_records
                    SELECT ?,namespace,user_id,agent_id,?,entities_json,topics_json,access_scope_json,?,1,?,0,0,0,'NONE'
                    FROM memory_records WHERE memory_id=?""", (successor, content, f"review:{reviewer_ref}; prior:{memory_id}", recorded_at, memory_id))
                self._insert(db, successor, old["claim_id"], version, inference_type or InferenceType(old["inference_type"]), assumptions, dependencies, memory_id)
                affected = self._hold(db, memory_id, ClaimStatus.SUPERSEDED)
                db.execute("UPDATE memory_records SET superseded=1 WHERE memory_id=?", (memory_id,))
            self._append(db, {"kind": "REVIEW", "memory_id": memory_id, "decision": decision.value,
                              "reason": reason, "reviewer_ref": reviewer_ref, "evidence_refs": sorted(evidence_refs),
                              "recorded_at": recorded_at, "successor": successor, "replacement_content": replacement_content,
                              "dependencies": sorted(dependencies), "assumptions": assumptions,
                              "inference_type": None if inference_type is None else inference_type.value,
                              "affected": affected})
            return successor

    def snapshot(self) -> dict:
        """Inspection-only export with complete version, evidence and event history.

        Same-namespace export requires access to every enrolled memory, rather
        than silently leaking restricted dependent claims through the event log.
        """
        with self.store._session() as db:
            db.execute("BEGIN")
            self._validate_state(db)
            versions = [dict(r) for r in db.execute("SELECT * FROM claim_versions WHERE scope=? ORDER BY claim_id,version", (self.scope,))]
            for row in versions:
                self._memory(db, row["memory_id"])
            links = [self._evidence_payload(r[0]) for r in db.execute("SELECT payload_json FROM claim_evidence WHERE scope=? ORDER BY evidence_id", (self.scope,))]
            events = [dict(r) for r in db.execute("SELECT * FROM claim_revision_events WHERE scope=? ORDER BY sequence", (self.scope,))]
            return {"versions": versions, "evidence": links, "events": events,
                    "event_head": self._head(db), "canonical_effect": "NONE", "deployment": False,
                    "subjectivity": "NOT_ESTABLISHED", "semantic_contradiction_detection": False,
                    "automatic_review": False, "independent_support_count": "NOT_ESTABLISHED",
                    "consciousness": "NOT_ESTABLISHED", "identity_continuity": "NOT_ESTABLISHED",
                    "canonicalization": "CLAIM_REVISION_V2_NEW_EVENTS_ONLY",
                    "content_dedup_implemented": True, "logical_dedup_implemented": False,
                    "source_lineage_tracking": True, "automatic_source_independence_judgment": False,
                    "declared_source_lineage_roots": self._source_lineage(links),
                    "content_duplicate_groups": self._duplicates(links),
                    "distinct_source_labels": len({e["source_id"] for e in links}),
                    "distinct_content_digests": len({e["content_sha256"] for e in links})}


def verify_revision_history(snapshot: dict) -> bool:
    """Check event-chain integrity only, not truth or resistance to database-owner tampering."""
    previous = "GENESIS"
    try:
        if not isinstance(snapshot, dict) or not isinstance(snapshot["events"], list) or len(snapshot["events"]) > MAX_EVENTS:
            return False
        for number, event in enumerate(snapshot["events"], 1):
            if not isinstance(event, dict) or type(event["sequence"]) is not int or not isinstance(event["payload_json"], str) or len(event["payload_json"].encode("utf-8")) > MAX_EVENT_BYTES:
                return False
            payload = strict_json(event["payload_json"])
            if not isinstance(payload, dict):
                return False
            expected = _hash({"sequence": number, "previous_hash": previous, "payload": payload})
            if event["sequence"] != number or event["previous_hash"] != previous or event["event_hash"] != expected:
                return False
            previous = expected
        return snapshot["event_head"] == previous
    except (KeyError, TypeError, ValueError):
        return False
