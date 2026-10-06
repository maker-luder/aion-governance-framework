from __future__ import annotations

import codecs
import difflib
import hashlib
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


class EvidenceFamily(StrEnum):
    RAW_LAYOUT = "RAW_LAYOUT"
    UNICODE_ENCODING = "UNICODE_ENCODING"
    NORMALIZATION = "NORMALIZATION"
    SCRIPT = "SCRIPT"
    POSITIONAL = "POSITIONAL"
    CONTEXT = "CONTEXT"


@dataclass(frozen=True, slots=True)
class RawTextProfile:
    sha256: str
    byte_count: int
    encoding: str
    bom: str | None
    crlf_count: int
    lf_only_count: int
    cr_only_count: int
    trailing_space_lines: int
    trailing_tab_lines: int
    raw_bytes_preserved: bool = True


@dataclass(frozen=True, slots=True)
class TextCue:
    cue_type: str
    kind: CueKind
    family: EvidenceFamily
    char_index: int | None
    byte_offset: int | None
    detail: str
    alternative_explanation: str


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    observation: str
    evidence_kind: CueKind
    family: EvidenceFamily
    char_index: int | None
    byte_offset: int | None
    method: str
    method_origin: str
    supports: str
    does_not_establish: tuple[str, ...]
    counter_explanations: tuple[str, ...]


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
    raw_profile: RawTextProfile
    cues: tuple[TextCue, ...]
    evidence_ledger: tuple[EvidenceRecord, ...]
    panels: tuple[MontagePanel, ...]
    periodic_scan: tuple[PeriodicCue, ...]
    candidate_period: int | None
    independent_families: tuple[EvidenceFamily, ...]
    hypotheses: tuple[str, ...]
    reasoning_modes: tuple[str, ...]
    null_model_status: str
    statistical_p_value: float | None
    visible_label_zh_tw: str
    watermark_verdict: str = "NOT_ESTABLISHED"
    heuristic_score_is_probability: bool = False
    local_only: bool = True
    network_required: bool = False
    api_required: bool = False
    source_text_modified: bool = False
    removal_or_evasion: str = "OUT_OF_SCOPE"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _decode_source(data: bytes) -> tuple[str, str, str | None, int]:
    candidates: tuple[tuple[bytes, str, str], ...] = (
        (codecs.BOM_UTF32_BE, "utf-32-be", "UTF-32-BE"),
        (codecs.BOM_UTF32_LE, "utf-32-le", "UTF-32-LE"),
        (codecs.BOM_UTF8, "utf-8", "UTF-8"),
        (codecs.BOM_UTF16_BE, "utf-16-be", "UTF-16-BE"),
        (codecs.BOM_UTF16_LE, "utf-16-le", "UTF-16-LE"),
    )
    for marker, encoding, label in candidates:
        if data.startswith(marker):
            payload = data[len(marker) :]
            return payload.decode(encoding, errors="strict"), encoding, label, len(marker)

    return data.decode("utf-8", errors="strict"), "utf-8", None, 0


def _byte_offsets(text: str, encoding: str, bom_size: int) -> tuple[int, ...]:
    offsets: list[int] = []
    position = bom_size
    for character in text:
        offsets.append(position)
        position += len(character.encode(encoding))
    return tuple(offsets)


def _raw_profile(data: bytes, text: str, encoding: str, bom: str | None) -> RawTextProfile:
    crlf_count = text.count("\r\n")
    lf_only_count = text.count("\n") - crlf_count
    cr_only_count = text.count("\r") - crlf_count
    lines = text.splitlines()
    trailing_space_lines = sum(1 for line in lines if line.endswith(" "))
    trailing_tab_lines = sum(1 for line in lines if line.endswith("\t"))
    return RawTextProfile(
        sha256=hashlib.sha256(data).hexdigest(),
        byte_count=len(data),
        encoding=encoding,
        bom=bom,
        crlf_count=crlf_count,
        lf_only_count=lf_only_count,
        cr_only_count=cr_only_count,
        trailing_space_lines=trailing_space_lines,
        trailing_tab_lines=trailing_tab_lines,
    )


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


def _exact_cues(
    text: str,
    offsets: tuple[int, ...],
    profile: RawTextProfile,
) -> tuple[TextCue, ...]:
    cues: list[TextCue] = []

    if profile.bom is not None:
        cues.append(
            TextCue(
                cue_type="BYTE_ORDER_MARK",
                kind=CueKind.EXACT,
                family=EvidenceFamily.RAW_LAYOUT,
                char_index=None,
                byte_offset=0,
                detail=f"BOM={profile.bom}",
                alternative_explanation="可能是正常編碼標記；存在本身不是浮水印證據。",
            )
        )

    if profile.crlf_count and (profile.lf_only_count or profile.cr_only_count):
        cues.append(
            TextCue(
                cue_type="MIXED_LINE_ENDINGS",
                kind=CueKind.EXACT,
                family=EvidenceFamily.RAW_LAYOUT,
                char_index=None,
                byte_offset=None,
                detail=(
                    f"CRLF={profile.crlf_count}; LF={profile.lf_only_count}; "
                    f"CR={profile.cr_only_count}"
                ),
                alternative_explanation="可能由不同編輯器、作業系統或複製貼上造成。",
            )
        )

    if profile.trailing_space_lines:
        cues.append(
            TextCue(
                cue_type="TRAILING_SPACE_LINES",
                kind=CueKind.EXACT,
                family=EvidenceFamily.RAW_LAYOUT,
                char_index=None,
                byte_offset=None,
                detail=f"lines={profile.trailing_space_lines}",
                alternative_explanation="可能是正常編輯殘留或格式化工具造成。",
            )
        )

    if profile.trailing_tab_lines:
        cues.append(
            TextCue(
                cue_type="TRAILING_TAB_LINES",
                kind=CueKind.EXACT,
                family=EvidenceFamily.RAW_LAYOUT,
                char_index=None,
                byte_offset=None,
                detail=f"lines={profile.trailing_tab_lines}",
                alternative_explanation="可能是正常縮排或編輯器行尾殘留。",
            )
        )

    for index, character in enumerate(text):
        byte_offset = offsets[index]
        if unicodedata.category(character) == "Cf":
            cues.append(
                TextCue(
                    "UNICODE_FORMAT_CONTROL",
                    CueKind.EXACT,
                    EvidenceFamily.UNICODE_ENCODING,
                    index,
                    byte_offset,
                    _label(character),
                    "可能是合法雙向文字、排版或複製貼上殘留。",
                )
            )
        elif _variation_selector(character):
            cues.append(
                TextCue(
                    "UNICODE_VARIATION_SELECTOR",
                    CueKind.EXACT,
                    EvidenceFamily.UNICODE_ENCODING,
                    index,
                    byte_offset,
                    _label(character),
                    "可能只是合法字形選擇或 emoji/CJK 變體。",
                )
            )
        elif _nonstandard_space(character):
            cues.append(
                TextCue(
                    "NONSTANDARD_WHITESPACE",
                    CueKind.EXACT,
                    EvidenceFamily.UNICODE_ENCODING,
                    index,
                    byte_offset,
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
                    EvidenceFamily.SCRIPT,
                    match.start(),
                    offsets[match.start()],
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


def _counterfactual_panel(text: str) -> str:
    original_tokens = tuple(TOKEN_RE.findall(text))
    nfkc_tokens = tuple(TOKEN_RE.findall(unicodedata.normalize("NFKC", text)))
    stripped_text = "".join(
        character for character in text if unicodedata.category(character) != "Cf"
    )
    stripped_tokens = tuple(TOKEN_RE.findall(stripped_text))

    def candidate(tokens: tuple[str, ...]) -> int | None:
        return _choose_period(tuple(_periodic_cue(tokens, period) for period in PERIODS))

    return (
        f"original_period={candidate(original_tokens)}\n"
        f"nfkc_period={candidate(nfkc_tokens)}\n"
        f"format_control_stripped_period={candidate(stripped_tokens)}\n"
        "用途：觀察候選位置規律是否在不改原始檔的分析副本轉換後仍存在。"
    )


def _evidence_ledger(
    cues: tuple[TextCue, ...],
    normalization_changed: bool,
    candidate_period: int | None,
    repeated: tuple[tuple[str, int], ...],
) -> tuple[EvidenceRecord, ...]:
    records: list[EvidenceRecord] = []
    for cue in cues:
        records.append(
            EvidenceRecord(
                observation=cue.cue_type,
                evidence_kind=cue.kind,
                family=cue.family,
                char_index=cue.char_index,
                byte_offset=cue.byte_offset,
                method="SOURCE_PRESERVING_REVEAL",
                method_origin="STANDARD_OR_DIRECT_OBSERVATION",
                supports="文字中存在可被機器精確觀察並轉成人類可讀表示的特徵。",
                does_not_establish=("watermark", "vendor", "author", "model"),
                counter_explanations=(cue.alternative_explanation,),
            )
        )

    if normalization_changed:
        records.append(
            EvidenceRecord(
                observation="NFKC_NORMALIZATION_DIFFERENCE",
                evidence_kind=CueKind.EXACT,
                family=EvidenceFamily.NORMALIZATION,
                char_index=None,
                byte_offset=None,
                method="UNICODE_NFKC_CONTRAST",
                method_origin="UNICODE_STANDARD_BASED",
                supports="原始表示與相容正規化表示不同。",
                does_not_establish=("watermark", "vendor", "intent"),
                counter_explanations=("正常全形/相容字", "輸入法或排版差異"),
            )
        )

    if candidate_period is not None:
        records.append(
            EvidenceRecord(
                observation=f"POSITIONAL_PERIOD_{candidate_period}",
                evidence_kind=CueKind.HEURISTIC,
                family=EvidenceFamily.POSITIONAL,
                char_index=None,
                byte_offset=None,
                method="MODULO_POSITION_MONTAGE",
                method_origin="PROJECT_ORIGIN_ENGINEERING_HEURISTIC",
                supports="存在值得人工檢查的位置分組規律。",
                does_not_establish=("watermark", "probability", "vendor"),
                counter_explanations=("自然文體節奏", "模板", "清單格式", "句法規律"),
            )
        )

    if repeated:
        records.append(
            EvidenceRecord(
                observation="REPEATED_BIGRAM_CONTEXT",
                evidence_kind=CueKind.HEURISTIC,
                family=EvidenceFamily.CONTEXT,
                char_index=None,
                byte_offset=None,
                method="REPEATED_CONTEXT_VIEW",
                method_origin="PROJECT_ORIGIN_REVIEW_AID",
                supports="存在可重複檢視的 context 結構。",
                does_not_establish=("watermark", "vendor", "authorship"),
                counter_explanations=("自然重複", "術語重現", "模板化文字"),
            )
        )

    return tuple(records)


def reveal_hidden_text_bytes(data: bytes) -> TextRevealReport:
    if not data:
        raise ValueError("data must not be empty")

    text, encoding, bom, bom_size = _decode_source(data)
    if not text:
        raise ValueError("decoded text must not be empty")

    offsets = _byte_offsets(text, encoding, bom_size)
    profile = _raw_profile(data, text, encoding, bom)
    tokens = tuple(TOKEN_RE.findall(text))
    cues = _exact_cues(text, offsets, profile)
    normalization, normalization_changed = _normalization_contrast(text)
    periodic_scan = tuple(_periodic_cue(tokens, period) for period in PERIODS)
    candidate_period = _choose_period(periodic_scan)
    repeated = _repeated_bigrams(tokens)
    ledger = _evidence_ledger(cues, normalization_changed, candidate_period, repeated)
    independent_families = tuple(sorted({item.family for item in ledger}, key=str))

    panels: list[MontagePanel] = [
        MontagePanel(
            "raw_profile",
            (
                f"sha256={profile.sha256}\n"
                f"bytes={profile.byte_count}\n"
                f"encoding={profile.encoding}\n"
                f"bom={profile.bom}\n"
                f"CRLF={profile.crlf_count}; LF={profile.lf_only_count}; CR={profile.cr_only_count}\n"
                f"trailing_space_lines={profile.trailing_space_lines}\n"
                f"trailing_tab_lines={profile.trailing_tab_lines}"
            ),
            CueKind.EXACT,
            "先固定原始 bytes 的 hash、encoding 與換行／行尾結構，再進入文字推理。",
        ),
        MontagePanel("original", text, CueKind.EXACT, "解碼後原始文字；不改寫來源 bytes。"),
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
            "同 modulo 位置並置；montage 是專案自創的人類證據排列介面，不是 detector。",
        ),
        MontagePanel(
            "repeated_context",
            (
                "\n".join(f"{count}× {gram}" for gram, count in repeated)
                if repeated
                else "沒有重複 bigram 達到顯示條件。"
            ),
            CueKind.HEURISTIC,
            "顯示重複 context；重複本身不是浮水印證據。",
        ),
        MontagePanel(
            "counterfactual_stability",
            _counterfactual_panel(text),
            CueKind.HEURISTIC,
            "在分析副本上比較 NFKC／移除 format-control 後候選是否仍存在；不修改來源。",
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
            f"本機已把 {len(cues)} 個 exact 文字／bytes 特徵轉成人類可讀證據；"
            "是否屬於浮水印仍未建立。"
        )
    elif candidate_period is not None:
        label = (
            f"未找到 exact 隱藏文字特徵，但 period={candidate_period} 出現啟發式位置規律；"
            "只列為候選。"
        )
    else:
        label = (
            "本機多視角顯影沒有建立文字浮水印；若方案依賴秘密 key/tokenizer，"
            "沒有對應材料時維持 UNKNOWN。"
        )

    return TextRevealReport(
        method="AION_TEXT_VISIBILITY_V0_2",
        character_count=len(text),
        token_count=len(tokens),
        raw_profile=profile,
        cues=cues,
        evidence_ledger=ledger,
        panels=tuple(panels),
        periodic_scan=periodic_scan,
        candidate_period=candidate_period,
        independent_families=independent_families,
        hypotheses=tuple(hypotheses),
        reasoning_modes=(
            "RAW_BYTE_PRESERVATION",
            "DETERMINISTIC_REVEAL",
            "CONTRASTIVE_REASONING",
            "MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR",
            "ABDUCTIVE_REASONING",
            "ANALOGICAL_REASONING_WHEN_REFERENCE_EXISTS",
            "DEFEASIBLE_REASONING_WITH_COUNTER_EXPLANATIONS",
            "COUNTERFACTUAL_STABILITY_CHECK",
            "EVIDENCE_FAMILY_INDEPENDENCE_CHECK",
            "MULTI_VIEW_TRIANGULATION",
        ),
        null_model_status="UNDEFINED_FOR_GENERIC_HEURISTIC",
        statistical_p_value=None,
        visible_label_zh_tw=label,
    )


def reveal_hidden_text_signal(text: str) -> TextRevealReport:
    if not text:
        raise ValueError("text must not be empty")
    return reveal_hidden_text_bytes(text.encode("utf-8"))


def render_text_reveal_markdown(report: TextRevealReport) -> str:
    lines = [
        "# 文字隱藏訊號顯現報告",
        "",
        f"- 方法：{report.method}",
        f"- SHA-256：{report.raw_profile.sha256}",
        f"- encoding：{report.raw_profile.encoding}",
        f"- bytes：{report.raw_profile.byte_count}",
        f"- 字元數：{report.character_count}",
        f"- token 數：{report.token_count}",
        f"- 浮水印判定：{report.watermark_verdict}",
        f"- null model：{report.null_model_status}",
        f"- p-value：{report.statistical_p_value}",
        f"- 獨立 evidence families：{', '.join(item.value for item in report.independent_families) or '無'}",
        f"- 明示標籤：{report.visible_label_zh_tw}",
        "",
        "## Evidence ledger",
    ]

    if report.evidence_ledger:
        for item in report.evidence_ledger:
            lines.extend(
                [
                    f"### {item.observation}",
                    f"- 類型：{item.evidence_kind.value}",
                    f"- family：{item.family.value}",
                    f"- char index：{item.char_index}",
                    f"- byte offset：{item.byte_offset}",
                    f"- method：{item.method}",
                    f"- method origin：{item.method_origin}",
                    f"- supports：{item.supports}",
                    f"- does not establish：{', '.join(item.does_not_establish)}",
                    f"- counter explanations：{'; '.join(item.counter_explanations)}",
                ]
            )
    else:
        lines.append("- 無。")

    lines.extend(["", "## Montage / human-readable panels"])
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
            "- RAW_BYTE_PRESERVATION 先固定來源 bytes，再進行任何文字推理。",
            "- MONTAGE_JUXTAPOSITION 是本專案借用 montage 並置概念的自創研究介面，不冒充標準形式邏輯。",
            "- HUMAN_ORIGIN 依樣畫葫蘆在形式化上對應 analogical / case-based pattern transfer；類比只提高可疑性。",
            "- ABDUCTION 只產生候選解釋，必須保留 competing explanations。",
            "- 同一 evidence family 的多個 cue 不重複計票成多條獨立證據。",
            "- MULTI_VIEW_TRIANGULATION 可提高可檢查性，但不等於 vendor watermark proof。",
            "- NO_DEFINED_NULL_MODEL = NO_VALID_P_VALUE。",
            "- HEURISTIC_CUE != WATERMARK_DETECTION。",
            "- HEURISTIC_SCORE != PROBABILITY。",
            "- EXACT_UNICODE_CUE != WATERMARK_PROOF。",
            "- WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN。",
            "- 不連接 hosted provenance API。",
            "- 不提供浮水印移除、破壞或規避。",
        ]
    )
    return "\n".join(lines) + "\n"
