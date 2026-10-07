"""v0.3 visibility controls / 顯影正例、合法控制與來源安全測試。"""
import codecs
import hashlib
import json
from pathlib import Path
import sys
import unicodedata

import pytest

SRC = Path(__file__).resolve().parents[1] / 'research-labs/provenance-visibility-agent_v0.1.0/src'
sys.path.insert(0, str(SRC))
from aion_provenance_visibility_agent import text_reveal as tr  # noqa: E402


@pytest.mark.parametrize('encoding,bom', [('utf-8',b''),('utf-8',codecs.BOM_UTF8),('utf-16-le',codecs.BOM_UTF16_LE),('utf-16-be',codecs.BOM_UTF16_BE),('utf-32-le',codecs.BOM_UTF32_LE),('utf-32-be',codecs.BOM_UTF32_BE)])
def test_exact_offsets_and_binding(encoding, bom):
    text = '中😀\r\nx\r\ny\n\u200b'
    data = bom + text.encode(encoding)
    report = tr.reveal_hidden_text_bytes(data)
    item = next(i for i in report.exact_cues if i.codepoint == 'U+200B')
    assert (item.codepoint_index, item.line, item.column) == (9,4,1)
    assert item.byte_offset == len(bom) + len(text[:9].encode(encoding))
    assert bytes.fromhex(item.source_hex) == '\u200b'.encode(encoding)
    assert item.input_sha256 == hashlib.sha256(data).hexdigest()
    assert report.source_text_modified is False
    assert all(r.input_sha256 == report.raw_profile.sha256 for r in report.evidence_ledger)


@pytest.mark.parametrize('cp', [0x200B,0x200C,0x200D,0x2060,0xFEFF,0x200E,0x200F,*range(0x202A,0x202F),*range(0x2066,0x206A),0xFE00,0xFE0F,0xE0100,0xE01EF,0xE0061,0xE007F,0xA0,0x202F,0x3000,0x0301,0x034F,0x115F,0x3164,0x1B])
def test_inventory(cp):
    report = tr.reveal_hidden_text_signal('a'+chr(cp)+'b')
    item = next(i for i in report.exact_cues if i.codepoint_index == 1)
    assert item.codepoint == f'U+{cp:04X}'
    assert item.unicode_name == unicodedata.name(chr(cp),'UNNAMED')
    assert item.category == unicodedata.category(chr(cp))
    assert item.counter_explanations
    assert report.watermark_verdict == 'NOT_ESTABLISHED'


@pytest.mark.parametrize('text', ['👩\u200d💻','می\u200cروم','שלום\u200f','العربية\u200e','漢\U000e0100','1\u00a0000','cafe\u0301','English 中文 Ελληνικά'])
def test_legitimate_controls(text):
    report = tr.reveal_hidden_text_signal(text)
    assert report.watermark_verdict == 'NOT_ESTABLISHED'
    assert report.heuristic_score_is_probability is False
    assert report.statistical_p_value is None
    assert all(c.counter_explanations for c in report.exact_cues)


def test_four_normalizations_and_tags():
    report = tr.reveal_hidden_text_signal('Ａe\u0301\U000e0061')
    assert {v.form for v in report.normalization_views} == {'NFC','NFD','NFKC','NFKD'}
    assert any(v.changed for v in report.normalization_views)
    tag = next(c for c in report.exact_cues if c.codepoint == 'U+E0061')
    assert tag.tag_representation == 'a'
    assert report.analysis_environment['grapheme_cluster_index'] == 'NOT_IMPLEMENTED'
    assert report.analysis_environment['unicode_database_version'] == unicodedata.unidata_version


def test_confusable_table_and_script():
    report = tr.reveal_hidden_text_signal('p\u0430ypal \u0391')
    cyr = next(c for c in report.exact_cues if c.codepoint == 'U+0430')
    assert cyr.script == 'Cyrillic'
    assert cyr.confusable_with == ('U+0061',)
    assert 'CONFUSABLE_TABLE_MAPPING' in cyr.classifications


def test_safe_render_and_determinism():
    text = '~~~\n<script>alert(1)</script>\n```\n\u202ex\u202c\x1b[2J'
    a = tr.reveal_hidden_text_signal(text)
    assert a.as_dict() == tr.reveal_hidden_text_signal(text).as_dict()
    md = tr.render_text_reveal_markdown(a)
    assert '\u202e' not in md and '\x1b' not in md
    assert '\n~~~~text\n~~~\n<script>' in md  # Longer outer fence keeps HTML inside code / 外層長圍欄保護來源
    assert 'U+202E RIGHT-TO-LEFT OVERRIDE' in md
    parsed = json.loads(tr.render_text_reveal_json(a))
    assert parsed['raw_profile']['sha256'] == hashlib.sha256(text.encode()).hexdigest()
    assert parsed['exact_cues'] and 'coverage' in parsed


def test_full_exact_coverage_after_display_limit():
    report = tr.reveal_hidden_text_signal('word '*4200 + '\u200b')
    assert report.coverage['exact_codepoints'] == report.character_count
    assert report.coverage['analysis_partial'] is True
    assert report.coverage['heuristic_tokens_analyzed'] == 4096
    assert any(c.codepoint_index == 21000 for c in report.exact_cues)
    assert all(len(p.content) < 300000 for p in report.panels)
    assert set(report.sensitivity) == {'original','NFC','NFD','NFKC','NFKD','format_control_stripped'}
    assert all(hasattr(p,'eligible') and p.threshold == 0.18 for p in report.periodic_scan)


@pytest.mark.parametrize('data', [b'',codecs.BOM_UTF8,b'\xff',codecs.BOM_UTF16_LE+b'x',b'\xed\xa0\x80'])
def test_decode_fail_closed(data):
    with pytest.raises((ValueError,UnicodeDecodeError)):
        tr.reveal_hidden_text_bytes(data)


def test_compare_sources_and_positions():
    from aion_provenance_visibility_agent import compare_hidden_text_bytes
    a, b = b'ab\r\n', codecs.BOM_UTF8 + 'a\u200bb\n'.encode()
    result = compare_hidden_text_bytes(a,b)
    assert result.source_a.sha256 == hashlib.sha256(a).hexdigest()
    assert result.source_b.sha256 == hashlib.sha256(b).hexdigest()
    assert result.byte_differences and result.codepoint_differences
    assert result.invisible_differences and result.line_ending_difference
    assert result.bom_difference
    assert result.source_modified is False
    assert result.watermark_verdict == 'NOT_ESTABLISHED'


@pytest.mark.parametrize('form,text,expected', [('NFC','e\u0301','é'),('NFD','é','e\u0301'),('NFKC','Ａ','A'),('NFKD','①','1')])
def test_normalization_spans_reconstruct(form,text,expected):
    report = tr.reveal_hidden_text_signal(text)
    view = next(v for v in report.normalization_views if v.form == form)
    restored = text
    for span in reversed(view.changes):
        restored = restored[:span.original_start] + expected[span.transformed_start:span.transformed_end] + restored[span.original_end:]
        assert span.original_codepoints
    assert restored == expected
    assert report.raw_profile.sha256 == hashlib.sha256(text.encode()).hexdigest()


def test_source_binding_rejects_mixed_receipts_and_wrong_bytes():
    from dataclasses import replace
    a = tr.reveal_hidden_text_signal('a\u200bb')
    b = tr.reveal_hidden_text_signal('c\u200bd')
    assert tr.verify_text_reveal_source(a, 'a\u200bb'.encode())
    assert not tr.verify_text_reveal_source(a, 'c\u200bd'.encode())
    with pytest.raises(ValueError,match='SOURCE_BINDING_MISMATCH'):
        tr.render_text_reveal_json(replace(a,raw_profile=b.raw_profile))
    with pytest.raises(ValueError,match='SOURCE_BINDING_MISMATCH'):
        tr.render_text_reveal_markdown(replace(a,evidence_ledger=b.evidence_ledger))


@pytest.mark.parametrize('a,b', [(b'abc',b'abcx'),(b'abc',b'ab'),(b'ab',b'axb'),(b'a\r',b'a\n'),(b'a',codecs.BOM_UTF8+b'a'),('é'.encode(),'e\u0301'.encode()),(b'x'*10000,b'x'*5000+b'y'+b'x'*5000)])
def test_comparison_exact_reconstruction(a,b):
    from aion_provenance_visibility_agent import compare_hidden_text_bytes
    report = compare_hidden_text_bytes(a,b)
    rebuilt = a
    for span in reversed(report.byte_differences):
        rebuilt = rebuilt[:span.a_start]+b[span.b_start:span.b_end]+rebuilt[span.a_end:]
    assert rebuilt == b
    ta,ea,_,ba = tr._decode_source(a)
    tb,eb,_,bb = tr._decode_source(b)
    rebuilt_text = ta
    for span in reversed(report.codepoint_differences):
        i,j,k,l = span.a_start.codepoint_index,span.a_end.codepoint_index,span.b_start.codepoint_index,span.b_end.codepoint_index
        assert span.a_start.byte_offset == ba+len(ta[:i].encode(ea))
        assert span.b_end.byte_offset == bb+len(tb[:l].encode(eb))
        rebuilt_text=rebuilt_text[:i]+tb[k:l]+rebuilt_text[j:]
    assert rebuilt_text == tb
    assert json.loads(report.to_json())['source_b']['byte_count'] == len(b)


def test_analysis_no_network_and_file_immutable(tmp_path,monkeypatch):
    import socket
    from aion_provenance_visibility_agent import ProvenanceVisibilityAgent
    def forbidden(*args,**kwargs):
        raise AssertionError('network called')
    monkeypatch.setattr(socket,'socket',forbidden)
    path = tmp_path/'source.txt'
    data='👩\u200d💻 cafe\u0301\r\n'.encode()
    path.write_bytes(data)
    report=ProvenanceVisibilityAgent().reveal_hidden_text_file_local(path)
    assert path.read_bytes() == data
    assert report.analysis_environment['network_used'] is False


def test_single_large_token_render_is_bounded():
    report=tr.reveal_hidden_text_signal('x'*20000+'\u200b')
    assert all(len(p.content)<300000 for p in report.panels)
    assert report.coverage['display_partial'] is True
    assert report.exact_cues[-1].codepoint_index == 20000


def test_cr_lf_without_crlf_is_mixed():
    report=tr.reveal_hidden_text_signal('a\rb\n')
    assert any(c.cue_type=='MIXED_LINE_ENDINGS' for c in report.cues)


def test_bidi_logical_order_and_metadata():
    report=tr.reveal_hidden_text_signal('abc\u202exyz\u202c')
    p=next(p for p in report.panels if p.name=='bidi_logical_order')
    assert 'abc⟦U+202E RIGHT-TO-LEFT OVERRIDE⟧xyz⟦U+202C POP DIRECTIONAL FORMATTING⟧'==p.content
    assert next(c for c in report.exact_cues if c.codepoint=='U+202E').bidi_class=='RLO'


def test_official_table_digest_and_limits():
    from aion_provenance_visibility_agent.unicode_evidence import tables,TABLE_SHA256
    raw=(SRC/'aion_provenance_visibility_agent/unicode_tables.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==TABLE_SHA256
    table=tables()
    assert table['version']=='15.0.0' and len(table['confusables'])==6311
    assert all(len(s['sha256'])==64 and s['url'].startswith('https://www.unicode.org/') for s in table['sources'].values())


def test_whole_report_binding_rejects_spliced_views_and_as_dict():
    from dataclasses import replace
    a = tr.reveal_hidden_text_signal('Ａ\u200b')
    b = tr.reveal_hidden_text_signal('é\u202e')
    for field in ('panels','normalization_views','cues','exact_cues','evidence_ledger','sensitivity','coverage'):
        altered=replace(a,**{field:getattr(b,field)})
        # 若值本來相同，不是內容被替換；只驗證確實不同的欄位。
        if getattr(a,field)==getattr(b,field): continue
        for render in (lambda r:r.as_dict(),tr.render_text_reveal_json,tr.render_text_reveal_markdown):
            with pytest.raises(ValueError,match='SOURCE_BINDING_MISMATCH'):
                render(altered)


def test_comparison_receipt_environment_and_binding():
    from dataclasses import replace
    from aion_provenance_visibility_agent import compare_hidden_text_bytes
    result=compare_hidden_text_bytes(b'ab','a\u200bb'.encode())
    assert result.analysis_environment['unicode_database_version']==unicodedata.unidata_version
    assert result.analysis_environment['unicode_table_sha256']
    assert result.analysis_environment['source_a_sha256']==result.source_a.sha256
    with pytest.raises(ValueError,match='SOURCE_BINDING_MISMATCH'):
        replace(result,codepoint_differences=()).as_dict()


def test_expanded_panel_truncation_is_in_coverage():
    report=tr.reveal_hidden_text_signal('\u200b'*200)
    assert report.coverage['display_partial'] is True
    assert report.coverage['panel_truncations']


def test_new_inventory_is_not_reported_as_no_observation():
    report=tr.reveal_hidden_text_signal('\x1b')
    assert 'NO_LOCAL_HUMAN_VISIBLE_CUE_ESTABLISHED' not in report.hypotheses
    assert '精確' in report.visible_label_zh_tw
