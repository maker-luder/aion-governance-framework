# Human–AI Epistemic Workflow：clean dossier 與 salvage review

Document-Class: RESEARCH_REFERENCE  
Document-Type: Research  
Status: CANDIDATE / SCIENTIFIC_HOLD  
Authority: INFORMATIONAL  
Last-Reviewed: 2026-09-10

來源是事故精確 HEAD `58ce7c3dae7ac3eefbe89cb659e00dc2f5846b21` 的四份文件。這是本輪新整理的繁體中文 review dossier，不是找回原始對話或原始 AION 白皮書；也沒有把原 branch merge、rewrite 或抹除。

## 1. 保留與修正決策

| 原內容 | 決策與理由 |
|---|---|
| IECW 暫名、非固定序列 | 保留為 AI_FORMALIZATION 候選；不主張新穎 construct |
| 直覺／暫定答案可先於 decomposition | 保留為研究取樣與 coding 的候選區分，不假定所有人都如此 |
| 認識能動性、Knowledge Building、AIR、SRL、vigilance 等 crosswalk | 保留為 D1 source concepts；相關／相似不等於效應、trait 或機制認證 |
| 語義 branch mis-selection 的案例 | 降為原 dossier 的 SOURCE_REPORT；本輪未取得原對話、user correction 時間戳或代表性抽樣 |
| H1–H5、ambiguity/salience/reasoning 操弄、mainline/side-branch 分離 | 保留假說與設計；H5 是規範治理命題，不能與 empirical causal hypothesis 混計 |
| `OBSERVATIONAL_PATTERN = SUPPORTED_BY_DIALOGUE_HISTORY` | 不沿用此強結論；改 `PATTERN_SOURCE = PRIOR_DOSSIER_REPORT; ORIGINAL_DIALOGUE_REVALIDATION = NOT_PERFORMED` |
| 「最接近」「unusually well」「strongest evidence」等評價 | 改成概念鄰近程度的 provisional assessment，沒有比較所有 framework 的證據 |
| SOURCES.md | 只剩一行 Sources placeholder，無獨立 bibliography 證據；由此 review 的來源表取代候選用途，原件保存 |
| IMPLEMENTATION_HANDOFF.md | 原本 3 行延期敘述不足以 operationalize；以本 review 與 KNOWLEDGE_AND_CAPA_DESIGN 的明確 gates 補充設計，不宣布已修改原件 |
| DRAFT_SCOPE.md | documentation-only boundary 值得保留，不擴張成 implementation authority |

13 個 temporary files 已從 incident tip 刪除，但其 creation/deletion commits 保留。研究文本內容價值與 execution-history conformity 是分開評估，不以一方掩蓋另一方。

## 2. 工作流候選（不是人的固定特質）

起點可以是 QUESTION／PROVISIONAL MODEL／INTUITION，經 externalization、資料與反例擴展、定義與前提分解、來源歸屬檢查、branch exploration、mainline/goal review、revision，再進入 transfer/new question。各階段可缺省、重訪或重新排序。

必須分開量測：使用者選定的 mainline 是否保留、AI side branch 是否有後續價值、來源歸屬是否正確、無 AI 時能否重建或遷移。對話更長、更順、雙方更同意都不是學習效果。

```text
OBSERVED INTERACTION != STABLE TRAIT
CONCEPTUAL FIT != PSYCHOLOGICAL VALIDATION
PROVENANCE != TRUTH
HUMAN_AI_CONSENSUS != EVIDENCE
OFF-INTENT VALUE != PERMISSION TO OVERRIDE USER INTENT
DOCUMENTATION != IMPLEMENTATION
```

## 3. Provenance：沿用既有五類與 parent 規則

本輪 handoff 本身是 direct user statement 的來源；它對舊對話的記述仍是 source report，不是當日逐字稿。

| Proposition | Origin／layer | 可追溯限制 |
|---|---|---|
| 需要像圖書館一樣讓文件可找到 | HUMAN_ORIGIN／DIRECT_STATEMENT | 本輪 handoff §18 明文，不回溯猜最初日期 |
| Governance Knowledge Discoverability / Retrieval Gap | AI_FORMALIZATION／HYPOTHESIS | handoff 明標 candidate，非已 approved architecture |
| anomaly 先停再回上位審視 | 本輪要求 HUMAN_ORIGIN／DIRECT_STATEMENT | 舊對話共同形成的 parent 未取得，因此不追認舊 JOINT_SYNTHESIS |
| ASEG | AI_FORMALIZATION／HYPOTHESIS | EARLY CANDIDATE / NOT APPROVED |
| 原 dossier 的人類觀察與 correction 歸屬 | UNKNOWN／SOURCE_REPORT 待原資料核對 | 不把原 dossier 的標記直接當本輪 independently verified attribution |
| 本輪 gap table、測試設計與此 review | AI_FORMALIZATION／ANALYSIS 或 HYPOTHESIS | 依目前 repo 與 handoff 形成，未自動轉 JOINT_SYNTHESIS |
| 公開論文的作者主張 | EXTERNAL_SOURCE／SOURCE_REPORT | metadata／abstract／論述層級分開；不繼承為個案結論 |

若稍後要入 ledger，直接用 `ContributionRecord`、`ContributionOrigin`、`ClaimLayer`；JOINT_SYNTHESIS 需先有 human/AI parents。這裡沒有新增 ontology，也沒有把原作者或使用者的 internal state 推定為 self-report。

## 4. H1–H5 的可證偽研究問題

| 候選 | Operational question | 反證／競爭解釋 |
|---|---|---|
| H1 IECW | 可否在事先定義的 episode sample 中可靠 coding correction/provenance/reframing/transfer，而不是單向 answer uptake？ | independent coders agreement 很低、workflow stages 無法跨样本識別，或表現只由任務熟悉度解釋 |
| H2 Ambiguity-Amplified Branch Lock-in | 固定 model/task，增加 ambiguity、competing context salience 與 reasoning condition 時，intent fidelity 是否有交互變化？ | 更高 reasoning 始終改善 intent 與 correction，沒有不利 interaction；context truncation、採樣、工具差异也是競爭解釋 |
| H3 Branch Utility–Intent Competition | intent fit 之外的 salience/actionability/coherence 是否改善 out-of-sample branch prediction？ | 加入指標無預測增益、評分與 outcome 洩漏、事後合理化；此向量不是 LLM 內部機制聲明 |
| H4 Productive Divergence | off-intent episode 的獨立價值評分、後續實際 reuse/transfer 與 error cost 能否分開量測？ | side branches 未被重用、增加負擔，盲評價值低於 baseline；不是 Kapur technical productive failure 的同一操作 |
| H5 Mainline Authority | mainline-first＋optional branch 與先確認／直接猜測策略比較，是否保留意圖又不抹除有用分歧？ | 這首先是 normative governance proposal；empirical 部分須量化 fidelity、延遲、探索價值等 trade-offs，不把偏好當因果真理 |

## 5. 實驗設計（未執行、未 preregister）

A：2（ambiguity）×2（context salience）×3（matched reasoning condition）factorial，固定 model/version、task type、tools、context truncation policy；使用事前獨立建立的 intent labels。測量 intent-selection accuracy、clarification、premature commitment、correction recovery、額外生成長度。reasoning 條件實際不可控時標不可比，不猜設定。

B：同一題組比較 best guess、explicit confirmation、mainline-first optional branch、enumeration-first；盲評 fidelity 與 episode value，並記時間／token／認知負荷候選指標。不只挑成功案例。

C：productive reliance vs dependence；匹配題目比較協作、較低支援、另一 AI、無 AI 的 reconstruction/transfer。控制先備知識、練習、order/fatigue；個案研究不能推 population rarity 或 causal development。

D：先定 coding book 再兩名獨立 coders；記 agreement、disagreement adjudication、missing data。採樣規則、排除規則與主要 outcomes 先行；樣本量由 power/sensitivity 或可辯護精度決定，本輪不任意填數字。

資料若涉及真人對話，需先確定同意、隱私、去識別化與適用審閱；目前不抓取任何私人對話。失敗注入 fixture 只支持 D3 工程，不當人類學習效果證據。

## 6. 正式 Four-Domain 對應

- **D1 Human construct/source concepts**：epistemic agency、AIR、metacognition、vigilance、self-explanation、productive failure、co-agency、dependence 作假說來源。
- **D2 LLM-specific/human–AI falsifiable question**：intent selection、branch value、correction、source-role fidelity、transfer 與 governance activation。
- **D3 Engineering operation**：coding protocol、replay、bounded probes、既有 evidence/provenance models；研究 runtime 實作保持 deferred。
- **D4 Governance**：mainline authority、對歷史與 attribution 的約束、無自動 canonical/deployment、scope/owner review 與 falsification。

## 7. Bibliography／citation 核查

查核日 2026-09-10。以下核對的是一手出版／arXiv 頁面或其搜尋結果的 metadata/abstract；**不是每篇 full-text 方法與結果的再分析**。DOI resolver 的讀取錯誤記為取用問題，後續使用同一 publisher 的 canonical page，不據此斷言論文不存在。

| 原來源 | 本輪核查與可用範圍 |
|---|---|
| Liu et al. 2024, Lost in the Middle | [ACL/TACL](https://aclanthology.org/2024.tacl-1.9/) 核對 title、年份、157–173、DOI；摘要研究 context position，不直接測本個案 intent drift |
| Zhang et al. 2024, CLAMBER | [ACL](https://aclanthology.org/2024.acl-long.578/) 核對 title/record；ambiguity benchmark，非本次根因證據 |
| Li et al. 2025, When Thinking Fails | [arXiv](https://arxiv.org/abs/2505.11423) 核對題名與記錄；原 dossier 的 NeurIPS venue 未於本輪單獨完成 conference PDF 核查，保留 venue-check pending |
| Kwon et al. 2026, ReasonIF | [ACL Findings](https://aclanthology.org/2026.findings-acl.1456/) 核對作者/年份/題名/DOI 與摘要；reasoning instruction adherence，不是本 host introspection |
| Fu et al. 2026, Scaling Reasoning, Losing Control | [ACL](https://aclanthology.org/2026.acl-long.1878/) 核對 title/publication record；不外推所有模型或所有 reasoning 增量 |
| Caldarella et al. 2026, Thinking Past the Answer | [arXiv](https://arxiv.org/abs/2606.02835) 由 arXiv 搜尋結果核對 title/authors/摘要；preprint，完整全文與後續版本尚待審閱 |
| Sperber et al. 2010, Epistemic Vigilance | [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/j.1468-0017.2010.01394.x) 核對 title/publisher record；只作人類來源概念 |
| Mercier & Sperber 2011, Why do humans reason? | [Cambridge](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/abs/why-do-humans-reason-arguments-for-an-argumentative-theory/53E3F3180014E80E8BE9FB7A2DD44049) 核對 authors/date/DOI/摘要；argumentative theory 不是 LLM 同機制的證據 |
| Chi et al. 1989, Self-Explanations | [Wiley](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1302_1) 核對題名/record；原實驗效果未在此 workflow 重現 |
| Kapur 2008, Productive Failure | [Taylor & Francis](https://www.tandfonline.com/doi/abs/10.1080/07370000802212669) 出版結果核對 title/year/pages 379–424；本輪未全文復核 |
| Panadero 2017, A Review of Self-Regulated Learning | [Frontiers](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.00422/full) 核對 review record；不是個人 metacognitive trait 測量 |
| Learning with machines: Toward a theory of epistemic co-agency | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666920X26000354) 核對 title、volume 10、100573、DOI 與 abstract；作者署名 Samuel 尚待 metadata 完整核對，不將原署名猜寫成已證實 |
| Epistemic dependence in AI-mediated learning | [Springer](https://link.springer.com/article/10.1007/s00146-026-03294-1) 核對 Du & Yuan、2026-08-29、critical-integrative review；六 criteria 是概念診斷框架，不是 validated scale |

原 dossier 另外列出的 Knowledge Building HKU principles、AIR 2017/2025 兩 DOI、Nelson/Narens 1994 chapter、2026 metacognition measurement review，均保存為 **supplementary bibliography pending**；本輪沒有把它們算入「已完整驗證引用」。以下為待查定位，不作已查證來源：

- https://kbkcc.edu.hku.hk/knowledge-building/kb-principles/
- DOI 10.1080/00461520.2017.1350180
- DOI 10.1080/07370008.2025.2497240
- https://sites.socsci.uci.edu/~lnarens/1994/Nelson%26Narens_Book%20Chapter_1994.pdf
- DOI 10.1007/s10648-026-10157-0

## 8. 最強可守住的結論與 handoff

目前有一份可保存的研究 dossier，內容提出可 operationalize 的 workflow、branch selection 與 authority 區分，部分一手文獻記錄確實存在且概念相關。這不足以證明 observed history 的完整性、trait、learning gain、transfer、novelty、populational rarity、AI subjectivity 或當日 cascade 的模型內部原因。

後續 coding 應先完成 source/attribution 核對、界定 observation unit 與 factors、取得適用 human review，沿用 existing provenance／Four-Domain／inquiry／HOLD owners。禁止把這份 handoff 當任意 runtime 實作的批准。

```text
ORIGINAL_DIALOGUE_REVALIDATION = NOT_PERFORMED
PATTERN = PRIOR_DOSSIER_SOURCE_REPORT
STABLE_TRAIT = NOT_ESTABLISHED
LEARNING_BENEFIT = NOT_ESTABLISHED
TRANSFER = NOT_ESTABLISHED
NOVEL_CONSTRUCT = NOT_ESTABLISHED
LLM_INTERNAL_MECHANISM = NOT_ESTABLISHED
RESEARCH_RUNTIME_IMPLEMENTATION = DEFERRED
SCIENTIFIC_CONCLUSION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
