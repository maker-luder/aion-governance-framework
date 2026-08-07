"""Local-only blocked-task review packet construction."""

from __future__ import annotations

import hashlib
from pathlib import Path

from .models import ExternalTeacherInput, ReviewPacket
from .redaction import redact_text


def create_review_packet(
    *,
    packet_id: str,
    task_id: str,
    blocking_issue: str,
    current_state: str,
    expected_result: str,
    actual_result: str,
    attempts_made: tuple[str, ...],
    relevant_files: tuple[Path, ...],
    minimal_code_excerpt: str,
    logs: str,
    environment: dict[str, str],
    questions_for_reviewer: tuple[str, ...],
) -> ReviewPacket:
    safe_excerpt, redactions_a = redact_text(minimal_code_excerpt)
    safe_logs, redactions_b = redact_text(logs)
    hashes = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in relevant_files
        if path.is_file()
    }
    return ReviewPacket(
        packet_id=packet_id,
        task_id=task_id,
        blocking_issue=blocking_issue,
        current_state=current_state,
        expected_result=expected_result,
        actual_result=actual_result,
        attempts_made=attempts_made,
        relevant_files=tuple(path.name for path in relevant_files),
        minimal_code_excerpt=safe_excerpt,
        logs=safe_logs,
        environment=environment,
        privacy_classification="REDACTED_LOCAL_REVIEW",
        redactions_applied=tuple(sorted(set((*redactions_a, *redactions_b)))),
        questions_for_reviewer=questions_for_reviewer,
        excluded_material=("credentials", "private conversations", "unrelated files"),
        manifest=tuple(sorted(hashes)),
        hashes=hashes,
        owner_submission_status="NOT_SUBMITTED_MANUAL_OWNER_ACTION_REQUIRED",
    )


def record_external_response(
    *, task_id: str, source_actor_id: str, response: str, received_at: str
) -> ExternalTeacherInput:
    from .enums import SourceType
    from .reasoning_provider import external_input_hash

    return ExternalTeacherInput(
        input_id=f"EXT-{external_input_hash(response)[:12]}",
        task_id=task_id,
        source_type=SourceType.EXTERNAL_MODEL_OR_TEACHER_INPUT,
        source_actor_id=source_actor_id,
        content_hash=external_input_hash(response),
        received_at=received_at,
    )
