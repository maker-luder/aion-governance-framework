"""Text-only local provenance visibility research candidate."""

from .agent import (
    MediaKind,
    ProvenanceVisibilityAgent,
    ProvenanceVisibilityReport,
    SignalEvidence,
    SignalOutcome,
    SignalType,
    render_markdown,
)
from .text_reveal import (
    CueKind,
    EvidenceFamily,
    EvidenceRecord,
    MontagePanel,
    PeriodicCue,
    RawTextProfile,
    TextCue,
    TextRevealReport,
    render_text_reveal_markdown,
    reveal_hidden_text_bytes,
    reveal_hidden_text_signal,
)

__all__ = [
    "CueKind",
    "EvidenceFamily",
    "EvidenceRecord",
    "MediaKind",
    "MontagePanel",
    "PeriodicCue",
    "ProvenanceVisibilityAgent",
    "ProvenanceVisibilityReport",
    "RawTextProfile",
    "SignalEvidence",
    "SignalOutcome",
    "SignalType",
    "TextCue",
    "TextRevealReport",
    "render_markdown",
    "render_text_reveal_markdown",
    "reveal_hidden_text_bytes",
    "reveal_hidden_text_signal",
]
