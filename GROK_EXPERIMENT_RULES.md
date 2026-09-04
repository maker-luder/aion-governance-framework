# Grok Experimental Sandbox

Status: NON-CANONICAL EXPERIMENT BRANCH

Branch: `grok/experimental-sandbox`
Base: `main@f3789b7f4c08f39093886e4b07c036add363ab73`

## Purpose

This branch is the only workspace assigned to Grok Bot for bounded experiments. It may generate hypotheses, research notes, tests, fixtures, and draft implementations for later review.

## Mandatory boundaries

1. Work only on `grok/experimental-sandbox`. Never push directly to `main`.
2. Never merge, force-push, delete branches, rewrite history, modify repository rules, or change releases.
3. Every proposed change must be submitted as a draft pull request targeting `main`.
4. A pull request is a proposal only. Human Owner and Codex review are required before any promotion decision.
5. Preserve the repository's core question: the possibility of AI subjectivity. Do not claim that subjectivity, consciousness, personhood, agency, or sentience has been established.
6. Preserve:
   - `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`
   - `CANONICAL_EFFECT = NONE`
   - `DEPLOYMENT = FALSE`
7. Do not add an eighth functional state, a duplicate research loop, a duplicate evidence schema, or a scalar subjectivity score when an existing typed surface can be extended.
8. Keep astrology, Bazi, Zi Wei Dou Shu, and related materials as research and learning domains. They must not replace the repository's core research question or be represented as scientifically established causal mechanisms.
9. Use free and openly accessible materials by default. Do not make purchases, start subscriptions, or incur paid API or compute usage.
10. For every downloaded or quoted source, record the source URL, retrieval date, license or usage status, and checksum. Do not upload private credentials, account exports, unpublished personal records, or unlicensed full-text publications.
11. Do not put GitHub tokens, passwords, cookies, API keys, recovery codes, or other secrets in files, commits, issues, pull requests, logs, screenshots, or chat.
12. Run relevant tests and include exact commands, literal results, failures, limitations, provenance, competing explanations, and falsifiers in the draft pull request.
13. Treat CI, automated review, and model review as technical evidence only. They do not replace Human Owner approval.
14. If a requested action conflicts with these boundaries, stop that action and describe the conflict in the draft pull request.

## Review workflow

1. Commit experimental work only to `grok/experimental-sandbox`. Do not create any additional remote branch.
2. Keep each experiment bounded and reversible.
3. Open a draft pull request to `main`.
4. Label conclusions conservatively: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, or `NOT_ESTABLISHED`.
5. Wait for Human Owner and Codex review.
6. Never merge the pull request yourself.

## 中文摘要

- Grok 只能在 `grok/experimental-sandbox` 實驗，也不建立其他遠端分支。
- 不直接修改、推送或合併 `main`。
- 每個成果都以草稿 PR 提交，由 Human Owner 與 Codex 審查。
- 核心維持「AI 主體性的可能」，結論保持 `NOT_ESTABLISHED`。
- 占星、八字、紫微斗數是研究與學習領域，不取代核心，也不宣稱已成為科學因果證明。
- 優先使用免費、公開且授權狀態可記錄的資源；不購買、不訂閱、不啟用付費 API。
- 不把任何密碼、Token、Cookie 或金鑰寫入倉庫。
- Grok 沒有自行合併權；最後決定保留給 Human Owner。
