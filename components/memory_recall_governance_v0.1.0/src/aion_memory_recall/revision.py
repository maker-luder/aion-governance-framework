"""Opt-in, bounded claim revision in the existing local memory database.

Relations and review decisions are supplied by a caller, not inferred from text.
RECORDED means eligible for the existing recall gate, never established truth.
No model, scheduler, network, repository writer or canonical-state writer runs here.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
import hashlib
import json
import re

from .models import RecallRequest
from .store import MemoryWriteDenied, SQLiteMemoryStore, StoredMemory


MAX_VERSIONS = 256
MAX_EVENTS = 2048
MAX_EVIDENCE = 1024


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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

    def __post_init__(self) -> None:
        for name in ("evidence_id", "target_memory_id", "source_id", "locator", "rationale"):
            _text(getattr(self, name), name)
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

    def __post_init__(self) -> None:
        _text(self.claim_id, "claim_id", 200)
        _text(self.memory_id, "memory_id")
        if type(self.version) is not int or self.version < 1 or not isinstance(self.status, ClaimStatus):
            raise ValueError("revision request requires a positive version and typed status")
        if not re.fullmatch(r"[0-9a-f]{64}", self.expected_event_hash):
            raise ValueError("revision request requires an exact event hash")
        for refs in (self.evidence_refs, self.dependency_refs):
            if not isinstance(refs, tuple) or len(refs) != len(set(refs)):
                raise ValueError("revision references must be distinct tuples")
            for ref in refs:
                _text(ref, "revision reference")
        if self.canonical_effect != "NONE":
            raise ValueError("revision requests cannot create canonical effects")


class ClaimRevisionService:
    """One identity/namespace view over SQLiteMemoryStore, not a second memory store.

    The request is a caller-supplied scope, not authentication. The caller must
    enforce identity and write approval before using this local library.
    """

    def __init__(self, store: SQLiteMemoryStore, request: RecallRequest, *, namespace: str) -> None:
        _text(namespace, "namespace", 200)
        self.store = store
        self.request = request
        self.namespace = namespace
        self.scope = _hash([request.user_id, request.agent_id, namespace])
        with self.store._session() as db:
            db.executescript("""
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

    @contextmanager
    def _transaction(self, approved: bool):
        if approved is not True:
            raise MemoryWriteDenied("explicit local writeback approval is required")
        db = self.store._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _memory(self, db, memory_id: str) -> StoredMemory:
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
        previous = self._head(db)
        digest = _hash({"sequence": count + 1, "previous_hash": previous, "payload": payload})
        db.execute("INSERT INTO claim_revision_events VALUES(?,?,?,?,?)", (self.scope, count + 1, previous, _json(payload), digest))

    def _dependencies(self, db, ids: tuple[str, ...], item: StoredMemory, claim_id: str) -> None:
        if not isinstance(ids, tuple) or len(ids) > 16 or len(ids) != len(set(ids)):
            raise ValueError("dependencies must be a tuple of at most 16 distinct version IDs")
        for mid in ids:
            parent = self._version(db, mid)
            memory = self._memory(db, mid)
            if parent["status"] != ClaimStatus.RECORDED or memory.conflict or memory.superseded or memory.tombstoned:
                raise ValueError("dependencies must be active, unchallenged recorded versions")
            if not memory.access_scope.issubset(item.access_scope):
                raise MemoryWriteDenied("derived claim cannot broaden dependency access")
        # Version references form a DAG, and logical claim cycles across versions
        # are also prohibited. Only existing, same-scope versions are traversed.
        seen: set[str] = set()
        pending = list(ids)
        while pending:
            mid = pending.pop()
            if mid in seen:
                continue
            seen.add(mid)
            parent = self._version(db, mid)
            if parent["claim_id"] == claim_id:
                raise ValueError("logical claim dependency cycle")
            pending.extend(json.loads(parent["dependencies_json"]))

    def _insert(self, db, memory_id: str, claim_id: str, version: int, inference_type: InferenceType,
                assumptions: tuple[str, ...], dependencies: tuple[str, ...], supersedes: str | None) -> None:
        _text(claim_id, "claim_id", 200)
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
        rows = db.execute("SELECT * FROM claim_versions WHERE scope=?", (self.scope,)).fetchall()
        affected = {memory_id}
        changed = True
        while changed:
            changed = False
            for row in rows:
                if row["status"] in {ClaimStatus.SUPERSEDED, ClaimStatus.WITHDRAWN}:
                    continue
                if row["memory_id"] not in affected and affected.intersection(json.loads(row["dependencies_json"])):
                    affected.add(row["memory_id"])
                    changed = True
        for mid in sorted(affected):
            current = self._version(db, mid)
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
                if existing[0] != _json(payload):
                    raise ValueError("evidence ID collision")
                return False
            if target["status"] in {ClaimStatus.SUPERSEDED, ClaimStatus.WITHDRAWN}:
                raise ValueError("stale target version; explicitly assess relevance to its successor")
            if db.execute("SELECT count(*) FROM claim_evidence WHERE scope=?", (self.scope,)).fetchone()[0] >= MAX_EVIDENCE:
                raise ValueError("evidence budget exhausted")
            db.execute("INSERT INTO claim_evidence VALUES(?,?,?,?)", (self.scope, link.evidence_id, link.target_memory_id, _json(payload)))
            affected = self._hold(db, link.target_memory_id, ClaimStatus.CHALLENGED) if link.relation is EvidenceRelation.CONTRADICTS else []
            self._append(db, {"kind": "EVIDENCE", "link": payload, "affected": affected})
            return True

    def pending_reviews(self, *, limit: int = 8) -> tuple[RevisionRequest, ...]:
        if type(limit) is not int or not 1 <= limit <= 64:
            raise ValueError("pending review limit must be an integer between 1 and 64")
        with self.store._session() as db:
            db.execute("BEGIN")
            rows = db.execute("SELECT * FROM claim_versions WHERE scope=? AND status IN ('CHALLENGED','DEPENDENCY_HOLD') ORDER BY memory_id", (self.scope,)).fetchall()
            result = []
            for row in rows:
                try:
                    item = self._memory(db, row["memory_id"])
                except MemoryWriteDenied:
                    continue
                if item.tombstoned or item.superseded:
                    continue
                refs = tuple(r[0] for r in db.execute("SELECT evidence_id FROM claim_evidence WHERE scope=? AND target_memory_id=? ORDER BY evidence_id", (self.scope, row["memory_id"])))
                result.append(RevisionRequest(row["claim_id"], row["memory_id"], row["version"], ClaimStatus(row["status"]), refs,
                                              tuple(json.loads(row["dependencies_json"])), self._head(db)))
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
        if datetime.fromisoformat(recorded_at).tzinfo is None:
            raise ValueError("review timestamp requires an explicit timezone")
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
            lineage = {memory_id}
            todo = list(json.loads(old["dependencies_json"]))
            while todo:
                mid = todo.pop()
                if mid not in lineage:
                    lineage.add(mid)
                    todo.extend(json.loads(self._version(db, mid)["dependencies_json"]))
            visible = {r["evidence_id"]: json.loads(r["payload_json"]) for r in db.execute("SELECT * FROM claim_evidence WHERE scope=?", (self.scope,)) if r["target_memory_id"] in lineage}
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
            versions = [dict(r) for r in db.execute("SELECT * FROM claim_versions WHERE scope=? ORDER BY claim_id,version", (self.scope,))]
            for row in versions:
                self._memory(db, row["memory_id"])
            links = [json.loads(r[0]) for r in db.execute("SELECT payload_json FROM claim_evidence WHERE scope=? ORDER BY evidence_id", (self.scope,))]
            events = [dict(r) for r in db.execute("SELECT * FROM claim_revision_events WHERE scope=? ORDER BY sequence", (self.scope,))]
            return {"versions": versions, "evidence": links, "events": events,
                    "event_head": self._head(db), "canonical_effect": "NONE", "deployment": False,
                    "subjectivity": "NOT_ESTABLISHED", "semantic_contradiction_detection": False,
                    "automatic_review": False, "independent_support_count": "NOT_ESTABLISHED",
                    "distinct_source_labels": len({e["source_id"] for e in links}),
                    "distinct_content_digests": len({e["content_sha256"] for e in links})}


def verify_revision_history(snapshot: dict) -> bool:
    """Check event-chain integrity only, not truth or resistance to database-owner tampering."""
    previous = "GENESIS"
    try:
        for number, event in enumerate(snapshot["events"], 1):
            expected = _hash({"sequence": number, "previous_hash": previous, "payload": json.loads(event["payload_json"])})
            if event["sequence"] != number or event["previous_hash"] != previous or event["event_hash"] != expected:
                return False
            previous = expected
        return snapshot["event_head"] == previous
    except (KeyError, TypeError, ValueError):
        return False
