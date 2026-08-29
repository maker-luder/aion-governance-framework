from __future__ import annotations

from .models import AgendaEntry, AgendaKind, AgendaScore
from aion_triadic_state import canonical_hash


_SCORE_BY_KIND = {
    AgendaKind.UNRESOLVED_GAP: AgendaScore(9, 8, 8, 3, 2),
    AgendaKind.CONTRADICTION: AgendaScore(9, 9, 9, 4, 3),
    AgendaKind.FAILED_REPLICATION: AgendaScore(8, 9, 8, 4, 2),
    AgendaKind.UNTESTED_FALSIFIER: AgendaScore(8, 10, 9, 3, 2),
    AgendaKind.CONFOUND: AgendaScore(8, 9, 8, 3, 2),
    AgendaKind.FOLLOW_UP: AgendaScore(7, 8, 7, 3, 2),
}


def build_agenda(questions: tuple[str, ...], *, default_question: str | None = None) -> tuple[AgendaEntry, ...]:
    normalized: list[str] = []
    seen: set[str] = set()
    candidates = questions if questions else ((default_question,) if default_question else ())
    for question in candidates:
        clean = " ".join(question.split()).strip()
        key = clean.casefold()
        if not clean or key in seen:
            continue
        seen.add(key)
        normalized.append(clean)
    entries = [
        AgendaEntry(
            question_id=f"Q-{canonical_hash(question)[:16]}",
            question=question,
            kind=AgendaKind.UNRESOLVED_GAP if index == 0 else AgendaKind.FOLLOW_UP,
            score=_SCORE_BY_KIND[AgendaKind.UNRESOLVED_GAP if index == 0 else AgendaKind.FOLLOW_UP],
            source_refs=("AUTONOMOUS_RESEARCH_LOOP_CONCEPT_SOURCE:USER_GIVEN",),
        )
        for index, question in enumerate(normalized)
    ]
    return tuple(sorted(entries, key=lambda entry: (-entry.score.exact, entry.question_id)))


def select_questions(agenda: tuple[AgendaEntry, ...], limit: int) -> tuple[AgendaEntry, ...]:
    if limit < 1:
        raise ValueError("question selection limit must be positive")
    return agenda[:limit]
