"""Offline Unicode evidence / 離線 Unicode 性質、來源位置與安全文字表示。"""
from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from functools import lru_cache
import hashlib
from importlib.resources import files
import json
from typing import Any
import unicodedata

TABLE_SHA256 = 'e20d65ba3fd0a194f7014659b1f4b454a64beca7b42d672e6f2418683cbd05d6'
BIDI_CONTROLS = frozenset([0x061C, 0x200E, 0x200F, *range(0x202A, 0x202F), *range(0x2066, 0x206A)])


@lru_cache(maxsize=1)
def tables() -> dict[str, Any]:
    """Verify the bundled table / 校驗內附資料；失配時不繼續分析。"""
    raw = files(__package__).joinpath('unicode_tables.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != TABLE_SHA256:
        raise ValueError('Unicode table digest mismatch / Unicode 資料摘要不符')
    value: dict[str, Any] = json.loads(raw)
    return value


@lru_cache(maxsize=1)
def _script_ranges() -> tuple[tuple[int, ...], tuple[tuple[int, int, str], ...]]:
    ranges = tuple((int(a), int(b), str(s)) for a, b, s in tables()['scripts'])
    return tuple(r[0] for r in ranges), ranges


def script_of(cp: int) -> str:
    """Script, not Script_Extensions / 主文字系統，不冒充延伸文字系統。"""
    starts, ranges = _script_ranges()
    i = bisect_right(starts, cp) - 1
    return ranges[i][2] if i >= 0 and cp <= ranges[i][1] else 'Unknown'


def default_ignorable(cp: int) -> bool:
    return any(a <= cp <= b for a, b in tables()['default_ignorable'])


@dataclass(frozen=True, slots=True)
class SourcePosition:
    """Byte/codepoint zero-based, line/column one-based / 位元組與碼點從零計，行欄從一計。"""
    byte_offset: int
    codepoint_index: int
    line: int
    column: int


def source_positions(text: str, encoding: str, bom_size: int) -> tuple[SourcePosition, ...]:
    """Include EOF; CRLF is one break / 包含檔尾；CRLF 算一次換行，CR/LF 各有座標。"""
    result: list[SourcePosition] = []
    byte, line, col = bom_size, 1, 1
    for i, ch in enumerate(text):
        result.append(SourcePosition(byte, i, line, col))
        byte += len(ch.encode(encoding, errors='strict'))
        if ch == '\n' or (ch == '\r' and (i+1 == len(text) or text[i+1] != '\n')):
            line, col = line+1, 1
        else:
            col += 1
    result.append(SourcePosition(byte, len(text), line, col))
    return tuple(result)


def label(ch: str) -> str:
    return f"U+{ord(ch):04X} {unicodedata.name(ch, 'UNNAMED')}"


def safe_text(text: str) -> str:
    """Escape display controls without editing source / 僅轉義顯示副本，來源不改。"""
    return ''.join(
        f'⟦{label(ch)}⟧' if ((unicodedata.category(ch).startswith('C') and ch != '\n')
        or default_ignorable(ord(ch)) or unicodedata.category(ch).startswith('M')
        or ch in '\u2028\u2029') else ch for ch in text
    )


@dataclass(frozen=True, slots=True)
class UnicodeObservation:
    input_sha256: str
    codepoint: str
    unicode_name: str
    category: str
    script: str
    bidi_class: str
    byte_offset: int
    codepoint_index: int
    line: int
    column: int
    classifications: tuple[str, ...]
    source_hex: str
    context_start: int
    context_hex: str
    tag_representation: str | None
    confusable_with: tuple[str, ...]
    explanation_zh_tw: str
    counter_explanations: tuple[str, ...]
    evidence_kind: str = 'EXACT'
    evidence_family: str = 'UNICODE_ENCODING'


def classifications(ch: str) -> tuple[str, ...]:
    cp, cat = ord(ch), unicodedata.category(ch)
    kinds: list[str] = []
    if cat == 'Cf': kinds.append('FORMAT_CONTROL')
    if cat == 'Cc': kinds.append('CONTROL_CHARACTER')
    if cp in (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF): kinds.append('ZERO_WIDTH_OR_JOIN_CONTROL')
    if cp in BIDI_CONTROLS: kinds.append('BIDI_CONTROL')
    if 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF: kinds.append('VARIATION_SELECTOR')
    if 0xE0000 <= cp <= 0xE007F: kinds.append('TAG_BLOCK')
    if ch.isspace() and ch not in ' \t\r\n': kinds.append('NONSTANDARD_WHITESPACE')
    if cat.startswith('M'): kinds.append('COMBINING_MARK')
    if default_ignorable(cp): kinds.append('DEFAULT_IGNORABLE')
    if str(cp) in tables()['confusables']: kinds.append('CONFUSABLE_TABLE_MAPPING')
    return tuple(kinds)


def character_inventory(text: str, data: bytes, positions: tuple[SourcePosition, ...]) -> tuple[UnicodeObservation, ...]:
    """One row per observed codepoint / 每個碼點一列，多屬性不冒充多份獨立證據。"""
    digest = hashlib.sha256(data).hexdigest()
    result: list[UnicodeObservation] = []
    for i, ch in enumerate(text):
        kinds = classifications(ch)
        if not kinds: continue
        cp, pos = ord(ch), positions[i]
        end = positions[i+1].byte_offset
        start = max(0, pos.byte_offset-8)
        tag = chr(cp-0xE0000) if 0xE0020 <= cp <= 0xE007E else ('CANCEL TAG' if cp == 0xE007F else None)
        result.append(UnicodeObservation(
            digest, f'U+{cp:04X}', unicodedata.name(ch, 'UNNAMED'), unicodedata.category(ch),
            script_of(cp), unicodedata.bidirectional(ch), pos.byte_offset, i, pos.line, pos.column,
            kinds, data[pos.byte_offset:end].hex(' '), start, data[start:min(len(data),end+8)].hex(' '),
            tag, tuple(f'U+{n:04X}' for n in tables()['confusables'].get(str(cp), [])),
            '正式英文名稱及 Unicode 性質；中文為工程解說，字形相似取決於字型與上下文。',
            ('合法文字塑形、emoji 或 CJK 字形選擇', '合法雙向排版、組合重音或一般字形對照',
             '編輯器、輸入法或複製貼上差異；不證明惡意或浮水印'),
        ))
    return tuple(result)


def evidence_digest(payload: dict[str, Any]) -> str:
    """Content-integrity receipt, not a signature / 全報告內容一致性摘要，不是認證簽章。"""
    body = {key:value for key,value in payload.items() if key != 'evidence_sha256'}
    return hashlib.sha256(json.dumps(body, ensure_ascii=True, sort_keys=True,
        separators=(',',':'),allow_nan=False).encode('ascii')).hexdigest()
