from __future__ import annotations

from pathlib import Path
from typing import Any

from .enums import ApprovalStatus, QAStatus, VerificationResult
from .errors import ConflictError, ValidationError
from .models import SystemStateRecord
from .storage import load_json, write_new_json


class StateLineageLedger:
    def __init__(self, root: Path) -> None:
        self.root = root

    def append(self, state: SystemStateRecord) -> Path:
        sealed = state.sealed()
        target = self.root / f"{sealed.sequence_number:06d}_{sealed.state_id}.json"
        if any(self.root.glob(f"*_{sealed.state_id}.json")):
            raise ConflictError(f"state_id already exists: {sealed.state_id}")
        if sealed.sequence_number > 0:
            parent = self.find(sealed.previous_state_id or "")
            if parent is None:
                raise ConflictError("parent state is missing")
            if parent.get("state_hash") != sealed.previous_state_hash:
                raise ConflictError("parent state hash does not match")
            if int(parent.get("sequence_number", -1)) + 1 != sealed.sequence_number:
                raise ConflictError("sequence number must increment by one")
        elif any(self.root.glob("*.json")):
            raise ConflictError("ledger already has a genesis state")
        return write_new_json(target, sealed)

    def find(self, state_id: str) -> dict[str, Any] | None:
        matches = list(self.root.glob(f"*_{state_id}.json")) if self.root.exists() else []
        return dict(load_json(matches[0])) if len(matches) == 1 else None

    def states(self) -> list[dict[str, Any]]:
        return [dict(load_json(path)) for path in sorted(self.root.glob("*.json"))]

    def verify(self, known_artifacts: set[str] | None = None) -> VerificationResult:
        states = self.states()
        if not states:
            return VerificationResult.MISSING_PARENT
        previous: dict[str, Any] | None = None
        for index, raw in enumerate(states):
            try:
                expected = SystemStateRecord(**raw).expected_hash()
            except ValidationError:
                return VerificationResult.INVALID_HASH
            if raw.get("state_hash") != expected:
                return VerificationResult.INVALID_HASH
            if int(raw.get("sequence_number", -1)) != index:
                return VerificationResult.BROKEN_CHAIN
            if previous is not None:
                if raw.get("previous_state_id") != previous.get("state_id"):
                    return VerificationResult.MISSING_PARENT
                if raw.get("previous_state_hash") != previous.get("state_hash"):
                    return VerificationResult.BROKEN_CHAIN
            if known_artifacts is not None:
                artifact_ids = raw.get("artifact_ids", [])
                if isinstance(artifact_ids, list) and any(item not in known_artifacts for item in artifact_ids):
                    return VerificationResult.UNKNOWN_ARTIFACT
            previous = raw
        last = states[-1]
        if (
            last.get("qa_status") != QAStatus.APPROVED.value
            or last.get("approval_status") != ApprovalStatus.APPROVED.value
        ):
            return VerificationResult.QA_HOLD
        return VerificationResult.VALID
