"""Exact contrast spans / 精確差異區間；不覆寫来源，也不聲稱最小編輯距離。"""
from __future__ import annotations
from dataclasses import dataclass
import difflib
import unicodedata
from typing import Literal
from .unicode_evidence import safe_text

FORMS: tuple[Literal['NFC','NFD','NFKC','NFKD'], ...] = ('NFC', 'NFD', 'NFKC', 'NFKD')


@dataclass(frozen=True, slots=True)
class ContrastSpan:
    operation: str
    original_start: int
    original_end: int
    transformed_start: int
    transformed_end: int
    original_representation: str
    transformed_representation: str
    representation_partial: bool
    original_codepoints: tuple[str, ...]
    transformed_codepoints: tuple[str, ...]


def contrast_spans(a: str, b: str) -> tuple[ContrastSpan, ...]:
    """Small input opcodes; large input exact enclosure / 小檔分段，大檔共同前後綴界定精確包覆區間。"""
    if a == b: return ()
    if len(a)+len(b) <= 8192:
        ops = difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes()
    else:
        start = 0
        while start < min(len(a),len(b)) and a[start] == b[start]: start += 1
        tail = 0
        while tail < min(len(a),len(b))-start and a[len(a)-tail-1] == b[len(b)-tail-1]: tail += 1
        ops = [('replace',start,len(a)-tail,start,len(b)-tail)]
    return tuple(ContrastSpan(op,i,j,k,l,safe_text(a[i:min(j,i+256)]),safe_text(b[k:min(l,k+256)]),
                              j-i>256 or l-k>256, tuple(f'U+{ord(c):04X}' for c in a[i:min(j,i+256)]),
                              tuple(f'U+{ord(c):04X}' for c in b[k:min(l,k+256)])) for op,i,j,k,l in ops if op != 'equal')


@dataclass(frozen=True, slots=True)
class NormalizationView:
    form: str
    changed: bool
    changes: tuple[ContrastSpan, ...]
    source_modified: bool = False
    index_unit: str = 'CODEPOINT / 碼點；各自座標系統'
    difference_semantics: str = 'EXACT_REPLACEMENT_SPANS_NOT_MINIMAL_EDIT_SCRIPT'


def normalization_views(text: str) -> tuple[NormalizationView, ...]:
    """Compare whole strings; per-character normalization is incorrect / 對整串正規化，避免組合字逐字轉換錯誤。"""
    return tuple(NormalizationView(form, normalized != text, contrast_spans(text,normalized))
                 for form in FORMS for normalized in [unicodedata.normalize(form,text)])
