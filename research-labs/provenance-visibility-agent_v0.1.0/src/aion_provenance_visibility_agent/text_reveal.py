from __future__ import annotations

import difflib
import re
import unicodedata
from dataclasses import asdict, dataclass
from enum import StrEnum
from math import sqrt
from typing import Any

TOKEN_RE = re.compile(r"\S+")
PERIODS: tuple[int, ...] = (2, 3, 4, 5, 8)
PERIODIC_CUE_THRESHOLD = 0.18


class CueKind(StrEnum):
    EXACT = "EXACT"
    HEURISTIC = "HEURISTIC"


@dataclass(frozen=True, slots=True)
class TextCue:
    cue_type: str
    kind: CueKind
    index: int | None
    detail: str
    alternative_explanation: str


@dataclass(frozen=True, slots=True)
class MontagePanel:
    name: str
    content: str
    kind: CueKind
    explanation_zh_tw: str


@dataclass(frozen=True, slots=True)
class PeriodicCue:
    period: int
    score: float


@dataclass(frozen=True, slots=True)
class TextRevealReport:
    method: str
    character_count: int
    token_count: int
    cues: tuple[TextCue, ...]
    panels: tuple[MontagePanel, ...]
    periodic_scan: tuple[PeriodicCue, ...]
    candidate_period: int | None
    hypotheses: tuple[str, ...]
    reasoning_modes: tuple[str, ...]
    visible_label_zh_tw: str
    watermark_verdict: str = "NOT_ESTABLISHED"
    heuristic_score_is_probability: bool = False
    local_only: bool = True
    network_required: bool = False
    api_required: bool = False
    removal_or_evasion: str = "OUT_OF_SCOPE"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _variation_selector(character: str) -> bool:
    codepoint = ord(character)
    return 0xFE00 <= codepoint <= 0xFE0F or 0xE0100 <= codepoint <= 0xE01EF


def _nonstandard_space(character: str) -> bool:
    return character.isspace() and character not in {" ", "\t", "\r", "\n"}


def _special(character: str) -> bool:
    return (
        unicodedata.category(character) == "Cf"
        or _variation_selector(character)
        or _nonstandard_space(character)
    )


def _label(character: str) -> str:
    return f"U+{ord(character):04X} {unicodedata.name(character, 'UNNAMED')}"


def _script(character: str) -> str | None:
    name = unicodedata.name(character, "")
    for script in ("LATIN", "CYRILLIC", "GREEK"):
        if script in name:
            return script
    return None


def _exact_cues(text: str) -> tuple[TextCue, ...]:
    cues: list[TextCue] = []
    for index, character in enumerate(text):
        if unicodedata.category(character) == "Cf":
            cues.append(
                TextCue(
                    "UNICODE_FORMAT_CONTROL",
                    CueKind.EXACT,
                    index,
                    _label(character),
                    "可能是合法雙向文字、排版或複製貼上殘留。",
                )
            )
        elif _variation_selector(character):
            cues.append(
                TextCue(
                    "UNICODE_VARIATION_SELECTOR",
                    CueKind.EXACT,
                    index,
                    _label(character),
                    "可能只是合法字形選擇或 emoji/CJK 變體。",
                )
            )
        elif _nonstandard_space(character):
            cues.append(
                TextCue(
                    "NONSTANDARD_WHITESPACE",
                    CueKind.EXACT,
                    index,
                    _label(character),
                    "可能由正常排版、網頁或編輯器產生。",
                )
            )

    for match in TOKEN_RE.finditer(text):
        token = match.group(0)
        scripts = {
            script
            for character in token
            if (script := _script(character)) is not None
        }
        if len(scripts) >= 2:
            cues.append(
                TextCue(
                    "MIXED_LATIN_CYRILLIC_GREEK_TOKEN",
                    CueKind.EXACT,
                    match.start(),
                    f"token={token!r}; scripts={','.join(sorted(scripts))}",
                    "可能是正常多語混寫，也可能包含人眼近似字形。",
                )
            )
    return tuple(cues)


def _machine_visible(text: str) -> str:
    return "".join(
        f"⟦{_label(character)}⟧" if _special(character) else character
        for character in text
    )


def _whitespace_visible(text: str) -> str:
    output: list[str] = []
    for character in text:
        if character == " ":
            output.append("·")
        elif character == "\t":
            output.append("⇥")
        elif character == "\n":
            output.append("⏎\n")
        elif character == "\r":
            output.append("␍")
        elif _nonstandard_space(character):
            output.append(f"⟦{_label(character)}⟧")
        else:
            output.append(character)
    return "".join(output)


def _normalization_contrast(text: str) -> tuple[str, bool]:
    normalized = unicodedata.normalize("NFKC", text)
    if normalized == text:
        return "NFKC：無差異", False
    diff = "".join(
        difflib.unified_diff(
            text.splitlines(keepends=True) or [text],
            normalized.splitlines(keepends=True) or [normalized],
            fromfile="original",
            tofile="NFKC",
            lineterm="",
        )
    )
    return diff or f"original={text!r}\nNFKC={normalized!r}", True


def _stddev(values: tuple[float, ...]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def _ends_punctuation(token: str) -> bool:
    return bool(token) and unicodedata.category(token[-1]).startswith("P")


def _periodic_cue(tokens: tuple[str, ...], period: int) -> PeriodicCue:
    if len(tokens) < period * 4:
        return PeriodicCue(period, 0.0)

    overall_mean = sum(len(token) for token in tokens) / len(tokens)
    length_means: list[float] = []
    punctuation_rates: list[float] = []

    for offset in range(period):
        group = tuple(
            token for index, token in enumerate(tokens) if index % period == offset
        )
        length_means.append(sum(len(token) for token in group) / len(group))
        punctuation_rates.append(
            sum(1 for token in group if _ends_punctuation(token)) / len(group)
        )

    length_dispersion = _stddev(tuple(length_means)) / (overall_mean + 1.0)
    punctuation_dispersion = max(punctuation_rates) - min(punctuation_rates)
    return PeriodicCue(
        period,
        min(1.0, 0.5 * length_dispersion + 0.5 * punctuation_dispersion),
    )


def _choose_period(cues: tuple[PeriodicCue, ...]) -> int | None:
    eligible = tuple(cue for cue in cues if cue.score >= PERIODIC_CUE_THRESHOLD)
    if not eligible:
        return None
    best = max(cue.score for cue in eligible)
    return min(cue.period for cue in eligible if cue.score >= best - 0.03)


def _token_index(tokens: tuple[str, ...], limit: int = 160) -> str:
    shown = tokens[:limit]
    rendered = " ".join(
        f"[{index:04d}] {token}" for index, token in enumerate(shown)
    )
    if len(tokens) > limit:
        rendered += f" … ⟦TRUNCATED {len(tokens) - limit} TOKENS⟧"
    return rendered


def _montage(tokens: tuple[str, ...], period: int, limit: int = 160) -> str:
    shown = tokens[:limit]
    lines = [f"period={period}"]
    for offset in range(period):
        row = [
            f"[{index:04d}]{token}"
            for index, token in enumerate(shown)
            if index % period == offset
        ]
        lines.append(f"offset {offset}: " + " | ".join(row))
    return "\n".join(lines)


def _repeated_bigrams(tokens: tuple[str, ...]) -> tuple[tuple[str, int], ...]:
    counts: dict[tuple[str, str], int] = {}
    for index in range(len(tokens) - 1):
        gram = (tokens[index], tokens[index + 1])
        counts[gram] = counts.get(gram, 0) + 1
    result = [
        (" ".join(gram), count)
        for gram, count in counts.items()
        if count > 1
    ]
    result.sort(key=lambda item: (-item[1], item[0]))
    return tuple(result[:20])


def reveal_hidden_text_signal(text: str) -> TextRevealReport:
    if not text:
        raise ValueError("text must not be empty")

    tokens = tuple(TOKEN_RE.findall(text))
    cues = _exact_cues(text)
    normalization, normalization_changed = _normalization_contrast(text)
    periodic_scan = tuple(_periodic_cue(tokens, period) for period in PERIODS)
    candidate_period = _choose_period(periodic_scan)
    repeated = _repeated_bigrams(tokens)

    panels: list[MontagePanel] = [
        MontagePanel("original", text, CueKind.EXACT, "原始文字，不改寫來源。"),
        MontagePanel(
            "machine_visible_unicode",
            _machine_visible(text),
            CueKind.EXACT,
            "把機器可見而人眼通常看不見的 Unicode 特徵轉成人類可讀 code point。",
        ),
        MontagePanel(
            "whitespace_visible",
            _whitespace_visible(text),
            CueKind.EXACT,
            "把空白、tab、換行與特殊空白顯式化。",
        ),
        MontagePanel(
            "normalization_contrast",
            normalization,
            CueKind.EXACT,
            "把原文與 NFKC normalization 並置，找出相容字表示差異。",
        ),
        MontagePanel(
            "token_index",
            _token_index(tokens),
            CueKind.EXACT,
            "替 token 加位置索引，讓位置規律可被人眼追蹤。",
        ),
        MontagePanel(
            "positional_montage",
            (
                _montage(tokens, candidate_period)
                if candidate_period is not None
                else "未建立達工程門檻的候選週期。"
            ),
            CueKind.HEURISTIC,
            "把同一 modulo 位置的 token 並置；借用 montage/juxtaposition 概念，不是正式 detector。",
        ),
        MontagePanel(
            "repeated_context",
            (
                "\n".join(f"{count}× {gram}" for gram, count in repeated)
                if repeated
                else "沒有重複 bigram 達到顯示條件。"
            ),
            CueKind.HEURISTIC,
            "把重複 context 顯示給人看；重複本身不是浮水印證據。",
        ),
    ]

    hypotheses: list[str] = []
    cue_types = {cue.cue_type for cue in cues}
    if "UNICODE_FORMAT_CONTROL" in cue_types:
        hypotheses.append("HIDDEN_UNICODE_CONTROL_CHANNEL")
    if "UNICODE_VARIATION_SELECTOR" in cue_types:
        hypotheses.append("VARIATION_SELECTOR_CHANNEL")
    if "MIXED_LATIN_CYRILLIC_GREEK_TOKEN" in cue_types:
        hypotheses.append("HOMOGLYPH_OR_MIXED_SCRIPT_CHANNEL")
    if normalization_changed:
        hypotheses.append("COMPATIBILITY_ENCODING_CHANNEL")
    if candidate_period is not None:
        hypotheses.append("POSITIONAL_PATTERN_CANDIDATE")
    if repeated:
        hypotheses.append("REPEATED_CONTEXT_STRUCTURE")
    if not hypotheses:
        hypotheses.append("NO_LOCAL_HUMAN_VISIBLE_CUE_ESTABLISHED")

    if cues:
        label = (
            f"本機已把 {len(cues)} 個可確定的機器可見文字特徵轉成人類可讀標記；"
            "是否屬於浮水印仍未建立。"
        )
    elif candidate_period is not None:
        label = (
            f"沒有找到明確隱藏 Unicode 特徵，但 period={candidate_period} "
            "出現啟發式位置規律；只列為候選。"
        )
    else:
        label = (
            "本機多視角顯影沒有建立文字浮水印；若方案依賴秘密 key/tokenizer，"
            "沒有對應材料時維持 UNKNOWN。"
        )

    return TextRevealReport(
        method="AION_TEXT_MONTAGE_REVEAL_V0_1",
        character_count=len(text),
        token_count=len(tokens),
        cues=cues,
        panels=tuple(panels),
        periodic_scan=periodic_scan,
        candidate_period=candidate_period,
        hypotheses=tuple(hypotheses),
        reasoning_modes=(
            "DETERMINISTIC_REVEAL",
            "CONTRASTIVE_REASONING",
            "MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR",
            "ABDUCTIVE_REASONING",
            "ANALOGICAL_REASONING_WHEN_REFERENCE_EXISTS",
            "MULTI_VIEW_TRIANGULATION",
        ),
        visible_label_zh_tw=label,
    )


def render_text_reveal_markdown(report: TextRevealReport) -> str:
    lines = [
        "# 文字隱藏訊號顯現報告",
        "",
        f"- 方法：{report.method}",
        f"- 字元數：{report.character_count}",
        f"- token 數：{report.token_count}",
        (
            "- 候選週期："
            f"{report.candidate_period if report.candidate_period is not None else '未建立'}"
        ),
        f"- 浮水印判定：{report.watermark_verdict}",
        f"- 明示標籤：{report.visible_label_zh_tw}",
        "",
        "## 可確定訊號",
    ]
    if report.cues:
        for cue in report.cues:
            lines.append(
                f"- {cue.cue_type} | index={cue.index} | {cue.detail} | "
                f"替代解釋：{cue.alternative_explanation}"
            )
    else:
        lines.append("- 無。")

    lines.extend(["", "## Montage / juxtaposition panels"])
    for panel in report.panels:
        lines.extend(
            [
                f"### {panel.name}",
                f"- 類型：{panel.kind.value}",
                f"- 說明：{panel.explanation_zh_tw}",
                "",
                "~~~text",
                panel.content,
                "~~~",
            ]
        )

    lines.extend(["", "## 競爭假設"])
    for hypothesis in report.hypotheses:
        lines.append(f"- {hypothesis} [CANDIDATE]")

    lines.extend(
        [
            "",
            "## 推理與證據邊界",
            "- MONTAGE_JUXTAPOSITION 是本專案借用 montage 並置概念的自創研究介面，不冒充標準形式邏輯。",
            "- HUMAN_ORIGIN 依樣畫葫蘆在形式化上對應 analogical / case-based pattern transfer；類比只提高可疑性。",
            "- ABDUCTION 只產生候選解釋，必須保留 competing explanations。",
            "- MULTI_VIEW_TRIANGULATION 可提高可檢查性，但不等於 vendor watermark proof。",
            "- HEURISTIC_CUE != WATERMARK_DETECTION。",
            "- HEURISTIC_SCORE != PROBABILITY。",
            "- EXACT_UNICODE_CUE != WATERMARK_PROOF。",
            "- WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN。",
            "- 不連接 hosted provenance API。",
            "- 不提供浮水印移除、破壞或規避。",
        ]
    )
    return "\n".join(lines) + "\n"
