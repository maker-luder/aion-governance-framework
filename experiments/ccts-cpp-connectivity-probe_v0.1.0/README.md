# CCTS C++17 graph-connectivity probe／CCTS C++17 關係圖連通性試驗

Status: EXPERIMENTAL / SYNTHETIC_ONLY / NO_ADMISSION_EFFECT / NO_CANONICAL_EFFECT

## Scope / 範圍

This is not a new CCTS construct, not a language-selection decision, and not a replacement for the original Python validator. Human proposed C++; Teacher selected the existing graph-connectivity subroutine for a bounded engineering probe. Only synthetic graphs are used. AI subjectivity, consciousness, real Human learning and CCTS scientific validity are not tested.

本實驗不是新增 CCTS 學術構念，不代表正式指定程式語言，更不是替代 Python CCTS 判定器。由小博提出 C++ 候選方案，老師選定既有的「修訂關係圖連通性檢查」作為有限比較對象。只使用合成人工圖，不驗證 AI 主體性、意識、真實人類學習或 CCTS 科學效度。

Python reference / Python 基準：
research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/co_constructed_thinking_space.py 中的 _revision_graph_is_connected。

## Complete Chinese behavior guide / 程式完整中文功能說明

1. connectivity.cpp：提供 C 語言介面 ccts_graph_connected(n, m, pairs)，分別接收節點數、邊數，以及每條邊的來源與目標整數索引（32 位元無號整數）。利用「並查集（Disjoint Set Union）」逐一合併邊的兩端，最後檢查所有節點是否屬於相同連通分量。1 表示連通，0 表示不連通，-1 表示輸入錯誤或 C++ 運算失敗。空圖、自連線、越界索引及空指標拒絕；節點上限 10,000、邊上限 100,000，重複邊可接受。程式捕捉全部 C++ 例外，避免例外越過 C 語言 ABI。此函式**不負責**人類或 AI 角色、證據、grounding、修訂性質、身分資訊或任何 CCTS 准入條件；這些必須維持由既有 Python 驗證。

2. probe.py：從目前 checkout 載入真正的 Python CCTS 基準函式，在 Linux 使用 g++ 按 C++17、O2 最佳化及警告視為錯誤編譯成暫存共享函式庫。由 Python 標準庫 ctypes 將整數陣列傳入。建立 7 個固定合成圖與可設定數量的固定亂數種子圖，逐筆比較 Python／C++ 的連通結果；不同就直接拋出錯誤。另檢查空圖、自連線、越界、空指標四個拒絕案例。也能量測四組時間：包含 Python 資料物件建構、已建構物件的 Python 核心、含陣列轉換的 C++ 呼叫、預先轉換陣列的 C++ 核心。編譯產物只放在暫存資料夾，回傳 JSON，不寫入 repo 或呼叫模型。

3. tests/test_ccts_cpp_connectivity_probe.py：透過既有根目錄的 pytest tests 步驟執行 runner；要求固定 7 + 隨機 320 = 327 個有效案例及 4 個非法輸入案例通過，並確認回報沒有提升 CCTS 科學結論。若 Linux 或 g++ 不可用，測試會明確失敗；跨平台尚未驗證。

## Reproduce / 重現

從倉庫根目錄依序執行：

    python experiments/ccts-cpp-connectivity-probe_v0.1.0/probe.py --random-cases 300 --benchmark-iterations 1200
    python -m pytest -q tests/test_ccts_cpp_connectivity_probe.py

第一行：編譯、驗證並輸出合成資料效能測量。第二行：執行適合 CI 的不測速版一致性檢查。僅支援 Linux、g++、Python 3.11 以上，C++ 標準為 C++17；未增加 pip 依賴或修改 CI 定義。

## Claim boundary / 主張與停止邊界

A parity pass supports only the sampled undirected graph-connectivity cases, not full Python/C++ CCTS equivalence, safety, formal scientific validity, learning or identity claims. Benchmarks vary in construction and marshalling costs and are **not** controlled equal-workload end-to-end comparisons. Native-only speed is not a reason to rewrite CCTS. The C function must not receive raw unvalidated user data. Linux-only, cross-compiler builds, Windows/macOS ABI, packaging and binary supply-chain integrity remain unverified. No automatic merge, promotion, deployment, or publication.

中文：測試通過只代表受測無向圖案例結果相符，不代表完整 CCTS 驗證器等價，也不代表安全性、科學效度或學習效果成立。測速分別包含不同程度的資料建構與轉換成本，不能據此宣稱 C++ 一定更適合整個 CCTS。C++ 函式不能單獨接受未經既有驗證的使用者資料。Windows／macOS、跨編譯器、ABI、打包及原生二進位供應鏈皆未驗證。結果不得自動導致合併、部署、發布或變更研究構念。

STOP if parity mismatch, rejected input is accepted, base semantics drift, compiling fails, or project costs exceed bounded spike. Report to Human instead of rewriting existing code.

停止條件：任何一致性失敗、非法輸入被接受、基準語意漂移、編譯失敗或成本超出這次試驗，都要停止並回報小博，不能直接改寫核心。下一階段技術決策由 Human 審查。
