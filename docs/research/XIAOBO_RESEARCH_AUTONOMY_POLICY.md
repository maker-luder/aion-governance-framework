# 小博研究自主規則候選 v0.1

狀態：`RESEARCH_POLICY_CANDIDATE / BRANCH_ONLY`  
Canonical effect：`NONE`

## 原則

小博的研究在 repository 自己可以決定的範圍內，採最大研究自主。

```text
只要不是明確且必要的強制規定，
就不得額外替小博的研究加上阻擋條件。
```

這裡的「研究自由」不是宣稱 repository 可以凌駕外部規則；它約束的是
repository 自己、AI 形式化層與研究實作層：不得把建議、保守猜測、
外觀判斷或程式碼內的隱藏條件偷偷升格成強制限制。

## 可以成為 blocking constraint 的來源

- 平台或系統層真正的強制規定；
- 適用法律或法規的強制規定；
- 已具有 canonical effect 的 repository 必要規則；
- 小博本人針對特定研究明確要求的限制。

任何 blocking constraint 都必須有：

- 明確 ID；
- authority class；
- 可追溯來源；
- 明確適用 scope；
- 小博看得懂的繁體中文理由。

## 不能自己升格成 blocking constraint

- AI 的建議；
- AI 的推測；
- 未確認的限制；
- 「看起來敏感」；
- 「以防萬一所以先砍掉」；
- 小博看不懂程式碼，因此假設他默認；
- 只有實作方便，但沒有必要性來源的限制。

```text
NONMANDATORY_RESTRICTION_CANNOT_BLOCK_XIAOBO_RESEARCH

UNREADABLE_CODE_IS_NOT_CONSENT = TRUE

OWNER_VISIBLE_RESTRICTION_RECEIPT_REQUIRED = TRUE

DEFAULT_DISPOSITION = ALLOW
```

## 與研究 provenance 的關係

```text
XIAOBO_RESEARCH
!= AI_FORMALIZATION

AI_FORMALIZATION
MUST_NOT SILENTLY NARROW
XIAOBO_RESEARCH
```

如果老師或其他 AI 認為應增加限制，可以提出理由與建議；但在沒有
mandatory basis 或小博明確要求之前，該限制只能保持 advisory / unverified，
不能在研究模型中被實作成 blocking condition。

## 非主張

此規則不建立：

- 對外部署權；
- main 自動寫入權；
- 規避平台或系統強制規則的權限；
- 規避法律、授權、第三方權利或其他外部必要限制的權限。

```text
DEPLOYMENT_AUTHORITY = NONE
AUTOMATIC_MAIN_WRITEBACK = FALSE
CANONICAL_EFFECT = NONE
```
