"""Explicit two-source local comparison / 明示兩份來源的本機比較；無路徑搜尋或網路。"""
from __future__ import annotations
from dataclasses import asdict, dataclass, replace
import json
from typing import Any
import unicodedata
from .normalization_views import FORMS, contrast_spans
from .unicode_evidence import SourcePosition, evidence_digest, source_positions
from .text_reveal import RawTextProfile, _decode_source, reveal_hidden_text_bytes


@dataclass(frozen=True, slots=True)
class ByteDifference:
    a_start: int
    a_end: int
    b_start: int
    b_end: int
    a_hex: str
    b_hex: str
    preview_partial: bool


@dataclass(frozen=True, slots=True)
class CodepointDifference:
    operation: str
    a_start: SourcePosition
    a_end: SourcePosition
    b_start: SourcePosition
    b_end: SourcePosition
    a_representation: str
    b_representation: str
    preview_partial: bool


@dataclass(frozen=True, slots=True)
class TextComparisonReport:
    source_a: RawTextProfile
    source_b: RawTextProfile
    byte_differences: tuple[ByteDifference, ...]
    codepoint_differences: tuple[CodepointDifference, ...]
    invisible_differences: dict[str, Any]
    normalization_equivalence: dict[str, bool]
    line_ending_difference: bool
    whitespace_difference: bool
    bom_difference: bool
    analysis_environment: dict[str, Any]
    evidence_sha256: str = ""
    source_modified: bool = False
    network_used: bool = False
    watermark_verdict: str = 'NOT_ESTABLISHED'
    difference_semantics: str = 'EXACT_REPLACEMENT_SPANS_NOT_MINIMAL_EDIT_SCRIPT'

    def as_dict(self) -> dict[str, Any]:
        if self.evidence_sha256 != evidence_digest(asdict(self)):
            raise ValueError("SOURCE_BINDING_MISMATCH")
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=True, sort_keys=True)+'\n'


def compare_hidden_text_bytes(a: bytes, b: bytes) -> TextComparisonReport:
    """Bind both byte strings before comparison / 先固定兩側來源，不使用未授權的外部基線。"""
    ra, rb = reveal_hidden_text_bytes(a), reveal_hidden_text_bytes(b)
    ta, ea, _, ba = _decode_source(a)
    tb, eb, _, bb = _decode_source(b)
    pa, pb = source_positions(ta,ea,ba), source_positions(tb,eb,bb)
    byte_diffs: tuple[ByteDifference, ...] = ()
    if a != b:
        start = 0
        while start < min(len(a),len(b)) and a[start] == b[start]: start += 1
        tail = 0
        while tail < min(len(a),len(b))-start and a[len(a)-tail-1] == b[len(b)-tail-1]: tail += 1
        end_a, end_b = len(a)-tail, len(b)-tail
        byte_diffs = (ByteDifference(start,end_a,start,end_b,a[start:min(end_a,start+64)].hex(' '),
                       b[start:min(end_b,start+64)].hex(' '),end_a-start>64 or end_b-start>64),)
    cp_diffs = tuple(CodepointDifference(s.operation,pa[s.original_start],pa[s.original_end],
        pb[s.transformed_start],pb[s.transformed_end],s.original_representation,
        s.transformed_representation,s.representation_partial) for s in contrast_spans(ta,tb))
    ia = [asdict(c) for c in ra.exact_cues if set(c.classifications)-{'CONFUSABLE_TABLE_MAPPING'}]
    ib = [asdict(c) for c in rb.exact_cues if set(c.classifications)-{'CONFUSABLE_TABLE_MAPPING'}]
    # 保留雙側完整位置，變更旗標只比較序列及座標，不把不同來源 hash 本身當字元差異。
    invisible_changed = [(c['codepoint'],c['codepoint_index'],c['byte_offset']) for c in ia] != [
        (c['codepoint'],c['codepoint_index'],c['byte_offset']) for c in ib]
    report = TextComparisonReport(ra.raw_profile,rb.raw_profile,byte_diffs,cp_diffs,
        {'changed':invisible_changed,'source_a':ia,'source_b':ib},
        {f:unicodedata.normalize(f,ta)==unicodedata.normalize(f,tb) for f in FORMS},
        [(i,c) for i,c in enumerate(ta) if c in '\r\n'] != [(i,c) for i,c in enumerate(tb) if c in '\r\n'],
        [(i,c) for i,c in enumerate(ta) if c.isspace()] != [(i,c) for i,c in enumerate(tb) if c.isspace()],
        ra.raw_profile.bom != rb.raw_profile.bom,
        {key:value for key,value in ra.analysis_environment.items() if key not in ('input_sha256','byte_count','encoding')} |
        {'source_a_sha256':ra.raw_profile.sha256,'source_b_sha256':rb.raw_profile.sha256,
         'comparison_method_version':'AION_TEXT_COMPARISON_V0_3'})
    return replace(report,evidence_sha256=evidence_digest(asdict(report)))
