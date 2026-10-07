# Provenance Visibility Agent — text-only local research specification

Date: 2026-10-06  
Status: `TEXT-ONLY V0.3 CANDIDATE / HUMAN_REVIEW_REQUIRED`

v0.2 was merged via PR #282. The dated v0.2 sections below are historical design context;
the following v0.3 section defines this candidate.

## v0.3 升級規格、操作與證據邊界（2026-10-07）

本輪從 `main=70d89e0942e3cbf28e3e0590be0f7773d9dcd4fd` 延伸既有實作。
沒有另外建立來源權威、浮水印分類器或具身功能。方法識別更新為
`AION_TEXT_VISIBILITY_V0_3`；原有 public Python 函式、cue_type 與報告欄位保留，新增欄位為加法擴充。
直接手動建構 TextRevealReport 的呼叫端需提供新增欄位；建議使用既有工廠函式。

### 來源與差異的精確意義

- 原始 bytes 先取 SHA-256，BOM 判斷在 strict decode（嚴格解碼）之前；不猜測無 BOM 的 UTF-16/32。
- UTF-8、BOM UTF-8/16LE/16BE/32LE/32BE 受支援；非法編碼、空 bytes、只有 BOM 均拒絕。
- `byte_offset`／`codepoint_index` 從 0 計，`line`／`column` 從 1 計；欄是碼點數，不是螢幕寬度。
  CRLF 算一次換行，CR 與 LF 仍各自有碼點位置；只有 CR 或 LF 也換行。BOM 不計入文字碼點。
- `grapheme_cluster_index=NOT_IMPLEMENTED`：沒有冒充完整 Unicode 字素叢集演算法。
- 每個 inventory 項目列正式英文名稱、中文工程解說、category、script、bidi class、座標、原始 hex、
  前後至多 8 bytes 的 context、tag 表示、confusable 表映射與替代解釋。
- 正規化對整串分析副本做 NFC/NFD/NFKC/NFKD；差異區間分別使用來源與轉換後的碼點座標。
- 較小字串提供 SequenceMatcher 區間；兩側合計大於 8192 碼點時，用共同前後綴得到單一精確包覆區間。
  它可由原文重建結果，但不主張最小 edit script（編輯操作序列）。每側 preview 最多 256 碼點，明示截斷。
- 雙來源比較同時提供兩側 SHA256、bytes、encoding、BOM、byte/codepoint 差異、不可見性質清單、
  四種正規化等價、換行與空白位置差異，以及兩側摘要、工具/runtime/UCD/table 版本與全內容摘要。byte 差異也是共同前後綴的精確區間，hex preview 至多 64 bytes。
  不可見清單包含一般控制字元與 combining mark；不等於「全部在人眼下永遠不可見」。

### 固定資料與版本

`unicode_tables.json` 是 Unicode **15.0.0** 官方 `DerivedCoreProperties.txt` 的
Default_Ignorable_Code_Point、`Scripts.txt`、`confusables.txt` 的 ASCII 衍生表，包含 6311 筆映射。
選用固定版本供重現，不宣稱是最新 Unicode。原檔 URL/SHA256 在表內；衍生表自身 SHA256 在程式固定，
每次程序首次載入即驗證。附 `UNICODE_LICENSE.txt`；執行時不連網、不安裝額外 detector。

Python runtime 的 `unicodedata.unidata_version` 與固定 property table 版本分別揭露；
Python 3.11/3.12 的 UCD 可能不同。未收錄於 runtime UCD 的正式名稱可能為 UNNAMED，
不因此否認固定表性質。重現條件是相同來源、設定、工具、資料表與 Python/UCD 環境。
無 timestamp，避免相同環境重跑序列化結果改變。

Script 使用官方 Script property；不冒充 Script_Extensions。confusable 表映射是精確查表結果，
但「實際看起來相同」取決於字型、上下文；沒有實作完整 UTS #39 skeleton 或攻擊判定。
bidi 視圖是安全的 logical order（邏輯順序），方向控制轉成標籤；沒有實作完整 UAX #9 視覺重排。

可重建衍生表（使用已明示取得的官方原檔目錄；此命令不連網、不覆寫既有檔）：

~~~sh
python scripts/build_text_visibility_unicode_tables.py \
  --source-directory /path/to/unicode-15-sources \
  --manifest research-labs/provenance-visibility-agent_v0.1.0/src/aion_provenance_visibility_agent/unicode_tables.json \
  --output /path/to/new-table.json
~~~

### 報告、來源綁定與輸出安全

JSON 與 Markdown 都由同一 `TextRevealReport` 產生；JSON 轉義非 ASCII 字元。
既有 `cues` 保留 v0.2 相容語義，`exact_cues` 是更完整的逐碼點 inventory。
每個 inventory/ledger 項目綁同一 input SHA256，report receipt 記錄 byte count、encoding、
方法、Python/UCD/table version，以及本機無網路、無 API、來源未修改。
報告另有涵蓋全欄位的 `evidence_sha256` 內容摘要；`as_dict` 與兩種 renderer 均驗證，
拒絕混入其他 SHA 的 receipt 或事後替換 panel/cue/normalization/coverage；`verify_text_reveal_source(report, data)` 以明示 bytes
重算整份報告以驗證。這是可重算來源綁定，**不是數位簽章、作者證明或抵抗蓄意整份偽造的認證**。

Markdown 將 bidi／ESC／其他控制與組合符號顯式化，使用比內容更長的動態圍欄，
防止來源關閉程式碼區後注入 HTML。`original` 面板是安全顯示副本，不冒充未轉義的原始 bytes。
原始 bytes 請用來源 digest + byte view 核對。所有檔案讀取仍走既有唯讀本機介面。

### 覆蓋範圍與限制

全來源 hash、精確碼點掃描、四種正規化均涵蓋全檔；目前是記憶體內處理，**沒有 streaming 保證**。
大型輸入與大量 exact observations 會增加記憶體/JSON 體積；不宣稱資源消耗恆定。

位置與重複 context 啟發式最多取前 4096 tokens，`analysis_partial` 與 `[start,end)` 範圍揭露。
六種敏感度（原文、四種正規化、format-control-stripped 副本）各自列覆蓋與完整 period scan。
展示最多 160 tokens、每個面板 4096 個輸入碼點；控制字元標籤展開後長度可較大。
Markdown ledger、inventory、每種正規化差異最多 160 列；完整列在 JSON；重複 context 最多 20 筆。
`panel_truncations` 記錄字元標籤展開後仍超過顯示上限的面板；
顯示截斷與分析截斷分開揭露；命中摘要不是完整文字檢視。

`independent_families` 保留舊欄位，但其意義僅是依機制去重分組，沒有證明統計獨立。
自然節奏、模板、清單、標點、token 長度與小樣本皆是位置規律的競爭解釋。
無 null model（虛無模型），無 p-value，無總浮水印機率；合法 Unicode 不被自動標惡意。

### 使用例

~~~python
from aion_provenance_visibility_agent import (
    reveal_hidden_text_bytes, render_text_reveal_json,
    render_text_reveal_markdown, compare_hidden_text_bytes,
    verify_text_reveal_source,
)
data = b"alpha" + chr(0x200B).encode("utf-8") + b"beta"
report = reveal_hidden_text_bytes(data)
assert verify_text_reveal_source(report, data)
assert report.watermark_verdict == "NOT_ESTABLISHED"
print(render_text_reveal_markdown(report))
json_report = render_text_reveal_json(report)
comparison = compare_hidden_text_bytes(b"alphabeta", data)
~~~

中文：先固定 `alpha + U+200B + beta` 的來源，顯示 U+200B 的 byte/codepoint 位置；
仍不判定為浮水印。比較函式僅接收呼叫者明示的兩份 bytes，無 URL、遞迴目錄或追蹤功能。
`CLI=DEFERRED`：既有 Python/file 介面可完成任務，不增加檔案寫入或掃描介面。

### 本輪查證與來源分工

- HUMAN_ORIGIN：機器可見性應能讓人類查閱；附件升級需求與邊界。
- JOINT_SYNTHESIS / PROJECT_ORIGIN：既有 montage、context 與反事實候選檢視。
- AI_FORMALIZATION：資料型別、差異區間、來源綁定、測試與顯示防護。
- EXTERNAL_SOURCE：Unicode 官方資料、[UAX #15](https://www.unicode.org/reports/tr15/)、
  [UAX #9](https://www.unicode.org/reports/tr9/)、[UTS #39](https://www.unicode.org/reports/tr39/)、
  [Python unicodedata](https://docs.python.org/3.12/library/unicodedata.html)。
- REPOSITORY_STATE：本輪重新讀回 main、10 個分支、無 open PR、最近 merge 與既有 v0.2。
- IMPLEMENTATION_EVIDENCE：本 PR 實際測試與 exact-head CI；UNKNOWN：浮水印、作者、模型歸屬。

本輪外掛：GitHub 現況、Personal Context 回顧流程、Superpowers 工程流程、Context7 查 stdlib、
Web + 官方原檔交叉核對。沒有新增統計或模型主張，故未觸發 Wolfram、HF、Consensus、Scite；
官方規範直接足以裁定 API/Unicode 行為，未為湊數再跑 Exa/Firecrawl。工具未觸發不表示證據不存在。
下面歷史區塊的外掛失敗描述只屬當時紀錄，不是本輪工具可用性判定。

MERGE_TO_MAIN = NO；CANONICAL_EFFECT = NONE；HUMAN_GATE_REQUIRED = YES。

## Research question

Can this public, text-centered repository make machine-visible textual provenance cues
human-visible through local, inspectable transforms without using a hosted provenance
API, while preserving source evidence and keeping heuristic claims below a valid
statistical detector?

~~~text
TEXT_ONLY = TRUE
LOCAL_FIRST = TRUE
SOURCE_BYTES_PRESERVED = TRUE
HOSTED_API_REQUIRED = FALSE
SOURCE_TEXT_MODIFIED = FALSE
~~~

## Recovery provenance

v0.2 is a fresh bounded implementation from current `main` after PR #281 was
merged. It preserves the v0.1 human-visible text reveal and extends it with raw-byte,
evidence-ledger, counterfactual, and evidence-family controls.

~~~text
SOURCE_HISTORY = PR_281
PR_281_STATE = MERGED
REUSE_TYPE = FORWARD_ITERATION_ON_MERGED_BASE
PR_281_MERGE != V0_2_VALIDATION
~~~

## Human origin / formalization

~~~text
HUMAN_ORIGIN
- 反向推理
- 蒙太奇式並置
- 依樣畫葫蘆
- 機器看得到的訊號，也應讓人類公平地看得到
- 本地自創、慢慢學，不接 hosted API

AI_FORMALIZATION
- 反向推理 -> abductive / retroductive hypothesis generation
- 蒙太奇 -> MONTAGE_JUXTAPOSITION_PROJECT_METAPHOR
- 依樣畫葫蘆 -> analogical / case-based pattern transfer
- 公平顯現 -> source-preserving multi-view disclosure
~~~

`montage reasoning` was not found as a standard formal-logic term. The project uses
montage only as an explicit project-origin metaphor for assemblage / juxtaposition of
evidence views.

## Layer 0 — raw byte preservation

The analysis starts before normal text parsing:

~~~text
SOURCE BYTES
  -> SHA-256
  -> BOM / encoding
  -> CRLF / LF / CR counts
  -> trailing-space / trailing-tab counts
  -> byte offset map
  -> decoded Unicode text
~~~

Reason:

~~~text
PARSER_NORMALIZATION_CAN_DESTROY_EVIDENCE = TRUE
RAW_BYTES_FIRST = REQUIRED_FOR_EXACT_TRACEABILITY
~~~

The implementation currently supports strict local decoding of UTF-8 and BOM-marked
UTF-8 / UTF-16 / UTF-32 variants. Unsupported or malformed input fails closed rather
than silently replacing bytes.

## Layer 1 — deterministic reveal

The exact layer surfaces properties actually present in the source:

1. Unicode format controls;
2. Unicode variation selectors;
3. non-standard whitespace;
4. mixed Latin/Cyrillic/Greek tokens;
5. NFKC normalization differences;
6. BOM and mixed line-ending structure;
7. trailing spaces/tabs;
8. character and byte offsets.

~~~text
EXACT_CUE = DIRECTLY_OBSERVED_PROPERTY
EXACT_CUE != WATERMARK_PROOF
~~~

Unicode UTS #39 supports the security relevance of mixed-script/confusable analysis.
This implementation is a bounded cue surface, not a claim of full UTS #39 conformance.

## Layer 2 — montage / juxtaposition

The same source is rendered through several views:

~~~text
RAW_PROFILE
ORIGINAL
MACHINE_VISIBLE_UNICODE
WHITESPACE_VISIBLE
NORMALIZATION_CONTRAST
TOKEN_INDEX
POSITIONAL_MONTAGE
REPEATED_CONTEXT
COUNTERFACTUAL_STABILITY
~~~

The goal is evidence arrangement, not attribution. A relation that is difficult to
notice in continuous prose can become inspectable after indexing, grouping or
juxtaposition.

## Layer 3 — reverse / abductive reasoning

Abduction is used only to generate candidate explanations:

~~~text
OBSERVED_CUE
  -> CANDIDATE_A
  -> COUNTER_EXPLANATION_B
  -> COUNTER_EXPLANATION_C
  -> FURTHER_TEST_OR_UNKNOWN
~~~

A candidate can be rebutted by later evidence or undercut by a better explanation.

## Layer 4 — analogical transfer

The HUMAN_ORIGIN phrase "依樣畫葫蘆" is formalized as analogical / case-based pattern
transfer.

~~~text
KNOWN_PATTERN
  -> derive inspection strategy
  -> apply to target
  -> compare similarities and differences

ANALOGICAL_MATCH = PLAUSIBILITY_CUE
ANALOGICAL_MATCH != PROOF
~~~

The source pattern and target identity must remain separate.

## Layer 5 — counterfactual stability

Heuristic positional structure is checked on analysis copies after:

- NFKC normalization;
- removal of Unicode format-control characters.

This does not edit the source. It asks whether a candidate depends entirely on a
specific representational artifact.

~~~text
COUNTERFACTUAL_COPY != SOURCE_MUTATION
CANDIDATE_SURVIVES_TRANSFORM != WATERMARK_PROOF
CANDIDATE_DISAPPEARS != WATERMARK_DISPROOF
~~~

## Layer 6 — evidence ledger

Every surfaced item records:

~~~text
OBSERVATION
EVIDENCE_KIND = EXACT | HEURISTIC
EVIDENCE_FAMILY
CHAR_INDEX
BYTE_OFFSET
METHOD
METHOD_ORIGIN
SUPPORTS
DOES_NOT_ESTABLISH
COUNTER_EXPLANATIONS
~~~

The ledger is designed so a human reviewer can inspect not only the result, but also
how the result was produced and what it cannot support.

## Layer 7 — evidence-family independence

Multiple cues from one underlying mechanism are not counted as multiple independent
evidence lines.

Current families:

~~~text
RAW_LAYOUT
UNICODE_ENCODING
NORMALIZATION
SCRIPT
POSITIONAL
CONTEXT
~~~

For example, multiple format-control characters remain one `UNICODE_ENCODING`
family, not many independent votes.

~~~text
CUE_COUNT != INDEPENDENT_EVIDENCE_COUNT
MULTI_VIEW_AGREEMENT != PROOF
~~~

## Layer 8 — statistical claim ceiling

Peer-reviewed LLM-watermark work treats exact statistical detection as a hypothesis
test. Valid false-positive control requires a defined null model / pivotal statistic,
detector rule and threshold, and many schemes also require a key/configuration.

Kirchenbauer et al. (ICML 2023) demonstrate a green-list statistical detector.
Li et al. (Annals of Statistics 2025; arXiv:2404.01245) develop a broader hypothesis-
testing framework using pivotal statistics and secret-key-dependent verification to
control Type-I error.

Therefore the generic local heuristic layer explicitly returns:

~~~text
NULL_MODEL_STATUS = UNDEFINED_FOR_GENERIC_HEURISTIC
STATISTICAL_P_VALUE = NONE

NO_DEFINED_NULL_MODEL = NO_VALID_P_VALUE
HEURISTIC_SCORE != PROBABILITY
HEURISTIC_CUE != WATERMARK_DETECTION
~~~

No percentage confidence or p-value is manufactured.

## Pattern analysis

Sequence-pattern literature, including Sabeti et al. (Entropy 2022), shows that pattern
dictionaries and compression-based approaches can support interpretable anomaly
analysis. v0.2 uses this literature only as support for the general idea that repeated
sequence structure can be made inspectable.

~~~text
SEQUENCE_ANOMALY_METHOD != WATERMARK_VALIDATION
PATTERN_REGULARITY != VENDOR_ATTRIBUTION
~~~

The current implementation deliberately stays simpler than a trained pattern dictionary
because the repository does not yet have a justified training corpus / null baseline.

## Architecture

~~~text
RAW LOCAL TEXT BYTES
  |
  +--> hash / encoding / BOM / newline profile
  |
  +--> exact Unicode / script / normalization views
  |
  +--> token position index
  |
  +--> positional montage
  |
  +--> repeated context
  |
  +--> counterfactual stability
  |
  +--> evidence ledger
  |
  +--> evidence-family independence check
  |
  +--> human review
  |
  +--> exact keyed detector only when matching detector material exists
~~~

No new image, audio, video, C2PA, or media-watermark path is retained in this package.

## Claim ceiling

~~~text
HEURISTIC_CUE != WATERMARK_DETECTION
HEURISTIC_SCORE != PROBABILITY
EXACT_UNICODE_CUE != WATERMARK_PROOF
MONTAGE_VISIBILITY != VENDOR_ATTRIBUTION
ANALOGICAL_MATCH != PROOF
MULTI_VIEW_AGREEMENT != PROOF
NO_DEFINED_NULL_MODEL = NO_VALID_P_VALUE
WITHOUT_REQUIRED_KEY_OR_CONFIGURATION = UNKNOWN
DETECTED != AUTHORSHIP
NOT_DETECTED != HUMAN_CREATED
WATERMARK_VERDICT = NOT_ESTABLISHED
NO_WATERMARK_REMOVAL_OR_EVASION
~~~

## Sources checked

- Unicode Technical Standard #39, Unicode Security Mechanisms:
  https://www.unicode.org/reports/tr39/
- Kirchenbauer et al., *A Watermark for Large Language Models*, ICML 2023:
  https://proceedings.mlr.press/v202/kirchenbauer23a.html
- Kirchenbauer et al., *On the Reliability of Watermarks for Large Language Models*,
  ICLR 2024 / arXiv:2306.04634.
- Li et al., *A Statistical Framework of Watermarks for Large Language Models:
  Pivot, Detection Efficiency and Optimal Rules*, Annals of Statistics 53(1), 2025,
  arXiv:2404.01245.
- Sabeti et al., *A Pattern Dictionary Method for Anomaly Detection*, Entropy 24(8),
  2022, DOI 10.3390/e24081095.
- Stanford Encyclopedia of Philosophy entries on analogy and abduction.
- Montage literature was checked only for assemblage / juxtaposition as the metaphor
  source.

Tool availability note: Consensus quota was already exhausted in this session; Scite
required paid/trial access; Hugging Face paper search was unavailable. These tool
limitations are not evidence that relevant literature does not exist.

## v0.3 對抗審查紀錄

獨立上下文 reviewer 檢查首個候選 `27853bb0fe011b0f62d91e37342d162d05e3b2b8`，
發現兩項重要問題：完整視圖移植可繞過局部 digest 檢查，以及比較報告遺漏環境版本。
新增失敗測試後修正為全報告摘要與所有公開序列化出口驗證、比較環境收據。
另將顯示截斷旗標及新控制字元「無觀察」摘要矛盾視為規格完整性問題一併修正。
四項 regression tests 均先 FAIL 再 PASS；113 項 targeted tests 通過。
reviewer 沒有重新審查修補後版本；修補由原實作者測試驗證，不冒充二次獨立審查。

限制仍包括：無字素索引、非完整 UTS #39/UAX #9、無串流、固定 15.0.0 表與 runtime UCD 分離、
較大差異是精確包覆區間而非最小差異；摘要不是認證。這些不被測試通過消除。
