import pytest

from tokenizer_contract import ReferenceTokenizer, TokenizerContractError, TokenizerMetadata


def tokenizer(max_length=20):
    return ReferenceTokenizer(TokenizerMetadata("reference.zh", 100000, max_length))


def test_unicode_and_cjk_offsets_are_deterministic():
    result = tokenizer().tokenize("AION 台灣 2026")
    assert result.tokens == ("AION", "台", "灣", "2026")
    assert result.offsets == ((0, 4), (5, 6), (6, 7), (8, 12))
    assert result.token_ids == tokenizer().tokenize("AION 台灣 2026").token_ids
    assert result.truncated is False


def test_special_tokens_and_truncation_are_explicit():
    result = tokenizer(max_length=3).tokenize("甲乙丙丁", add_special_tokens=True)
    assert result.special_tokens_added is True
    assert result.tokens == ("<bos>", "甲", "乙")
    assert result.truncated is True
    assert result.offsets[0] == (0, 0)


def test_metadata_is_serializable_and_bounded():
    instance = tokenizer()
    assert '"tokenizer_id":"reference.zh"' in instance.metadata_json()
    assert instance.metadata.canonical_effect == "NONE"
    assert instance.metadata.deployment is False


def test_invalid_metadata_fails_closed():
    with pytest.raises(TokenizerContractError, match="invalid tokenizer metadata"):
        TokenizerMetadata("", 0, 0).validate()
    with pytest.raises(TokenizerContractError, match="special tokens"):
        TokenizerMetadata("bad", 10, 10, ("<x>", "<x>")).validate()
    with pytest.raises(TokenizerContractError, match="canonical_effect"):
        TokenizerMetadata("bad", 10, 10, canonical_effect="WRITE").validate()
