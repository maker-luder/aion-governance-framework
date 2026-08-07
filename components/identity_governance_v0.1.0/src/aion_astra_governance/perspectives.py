from __future__ import annotations

from .models import PerspectiveEventRecord


def compare_channels(record: PerspectiveEventRecord) -> dict[str, object]:
    return {
        "event_id": record.event_id,
        "channel_count": len(record.analysis_channels),
        "agreements": list(record.agreements),
        "disagreements": list(record.disagreements),
        "unresolved_questions": list(record.unresolved_questions),
        "merge_status": record.merge_status,
        "original_channels_preserved": True,
        "canonical_effect": record.canonical_effect.value,
    }
