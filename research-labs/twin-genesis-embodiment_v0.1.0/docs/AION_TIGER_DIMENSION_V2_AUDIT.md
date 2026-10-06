# AION 虎型獸人尺寸 V2：來源、量測與證據稽核

Status: IMPLEMENTED RESEARCH CANDIDATE  
Preset: `AION-TIGER-FULL-DIMENSIONS-V2`  
Canonical effect: NONE  
Target agent: AION only

## 1. V2 解決什麼問題

V1 已經能輸出可建模尺寸，但仍有三個缺口：

1. 有些數字雖有 provenance（來源類型），卻沒有逐欄 `source_refs`（具體來源索引）。
2. 有尺寸名稱，卻沒有固定「從哪個 landmark 量到哪個 landmark」。
3. 虎直接量測、furry/fursuit 製作者欄位、人體工學和工程 target 仍需要更細的 evidence-strength 分層。

V2 不刪 V1，而是完整繼承 V1，再為每個 row 增加：

- `category`：部位分類；
- `measurement_method_zh`：繁中量測方法；
- `source_refs`：具體來源；
- `evidence_strength`：證據強度；
- `value_semantics`：數值到底是 target、observation、upper bound、exclusion threshold 或 undefined。

## 2. 來源階層

| 類型 | 可以做什麼 | 不可以做什麼 |
| --- | --- | --- |
| PRIMARY_TIGER_RESEARCH | 記錄 Panthera tigris 直接解剖／形態觀察 | 直接證明人虎獸人的自然生理 |
| COMPARATIVE_FELID_RESEARCH | 約束異速生長、四足運動轉譯 | 當成人形雙足驗證 |
| HUMAN_ANTHROPOMETRY | 建立直立、reach、clearance、操作空間基線 | 當虎生物學 |
| COMMUNITY_PRACTITIONER | 決定 ref sheet / fursuit 真正需要哪些量測欄位 | 當科學正常值 |
| INSTITUTIONAL_FORENSICS | 物種鑑識的排除／形態約束 | 當活體性器官正常尺寸 |
| ENGINEERING_DESIGN_CHOICE | 給 AION 一套可建模 target | 宣稱自然界存在相同生物 |

核心：

```text
COMMUNITY_PRACTITIONER != BIOLOGICAL_EVIDENCE
REFERENCE_OBSERVATION != DESIGN_TARGET
FORENSIC_CONSTRAINT != LIVE_NORMAL_RANGE
ENGINEERING_DESIGN_CHOICE != BIOLOGICAL_DISCOVERY
```

## 3. 擴大虎來源

### 3.1 顱骨

Mazák 的 craniometry 使用 273 個具有可靠野外來源的虎顱骨；研究同時指出地理變異、性別差異與 allometry（異速生長）都很重要。

所以 V2 不把「虎頭」壓成唯一一組真實顱骨比例。AION 的頭部尺寸仍是 engineering target，但 source manifest 可回溯到虎顱骨 measurement system 與 variation。

### 3.2 前肢骨

Uddin、Jahan、Rahman 的 Royal Bengal Tiger 研究直接量測一隻成年虎的肩胛、肱骨、橈骨與尺骨。

V2 新增的 reference observation 包括：

- 肩胛最大長：右 26.5 cm、左 26.5 cm；
- 肩胛最大寬：右 20.0 cm、左 17.2 cm；
- 右肩胛盂長 5.2 cm、寬 3.7 cm；
- 肱骨總長：右 28.0 cm、左 27.9 cm；
- 右肱骨中段圍 10.5 cm；
- 右肱骨頭圍 19.4 cm；
- 尺骨總長：右 28.0 cm、左 27.0 cm。

全部維持 `REFERENCE_OBSERVATION + DIRECT_SINGLE_SPECIMEN`，不直接覆蓋 AION 的上臂／前臂工程長度。

### 3.3 後肢骨

Tomar、Vaish、Archana 2026 研究五隻成年虎的脛骨／腓骨。

V2 收錄：

- 脛骨 shaft 上段平均圍：16.72 ± 0.29 cm；
- 中段：10.06 ± 0.17 cm；
- 下段：10.18 ± 0.18 cm；
- 腓骨平均長：29.26 ± 0.28 cm；
- 腓骨平均重量：28.52 ± 0.46 g。

股骨研究確認樣本為五具成年虎骨架，但本輪沒有取得可可靠重建的完整數字表；因此 source manifest 記錄該來源，但不製造 femur numeric row。

## 4. 福瑞／fursuit 實務補出的欄位

多個 practitioner guide 的共同模式不是「獸人的正常身材」，而是：真正要做出可穿、可 rig、可重製的角色，只靠身高、胸圍與四肢長度不夠。

因此 V2 補入：

- 水平頭圍、下巴—後腦環圍、頭頂—下巴環圍；
- 瞳距、鼻尖—瞳孔、下巴—鼻尖、下巴—瞳孔；
- 背寬、肩頸點—胯下、腋下—腰、頸根—尾根；
- 伸展／放鬆 sleeve length、內臂長、腕圍、掌圍；
- inseam、outseam、髖—膝、膝—踝、膝圍、踝圍；
- 內部承重足與外觀 hindpaw 分離；
- digitigrade padding 最大深度；
- 尾根／中段／尾尖 volume 與 rig segment；
- fur shell / padding envelope 與 anatomical/load-bearing core 分離。

這些欄位由 `COMMUNITY_PRACTITIONER` 支持「要量什麼」，具體 AION 數值仍標成 `ENGINEERING_SYNTHESIS`。

## 5. 生殖尺寸：擴搜後仍保留未知

USFWS National Fish and Wildlife Forensics Laboratory 的 2005 鑑識指南提供真虎乾燥生殖標本的 species-exclusion 線索，例如：

- 乾燥 glans tip 約小於 2 inch（約 5 cm）；
- 若乾燥標本從 tip 到 scrotum 大於 8 inch（20.32 cm），則不能判為虎；
- 真虎具有小型三角形 baculum。

V2 把前兩個數值建模成 `REFERENCE_CONSTRAINT`，而不是 `DESIGN_TARGET`。

特別是：

```text
aion_total_penile_length_cm
= UNKNOWN_SOURCE_NOT_ESTABLISHED
```

擴大搜尋沒有改變這個判定。乾燥鑑識標本的排除閾值不能反推活體正常長度，更不能直接成為 AION 的固定尺寸。

## 6. Measurement Protocol

`measurement_protocols.py` 為每個 `DESIGN_TARGET` 自動建立 protocol，至少包含：

- pose；
- view；
- instrument；
- landmark method；
- source refs；
- quality gate。

共同品質閘門：

```text
同一 preset 使用同一姿勢與 landmark 定義
左右成對尺寸標 side
fur/padding envelope != internal anatomical/load-bearing dimension
reference observation 不轉成 model fitting protocol
```

## 7. 主要實作

```text
src/aion_astra_twin_embodiment/body_dimensions_v2.py
src/aion_astra_twin_embodiment/dimension_sources.py
src/aion_astra_twin_embodiment/measurement_protocols.py
schemas/AION_TIGER_FULL_DIMENSIONS_V2_SCHEMA.json
tests/test_body_dimensions_v2.py
tests/test_dimension_sources.py
tests/test_measurement_protocols.py
```

CLI：

```bash
python -m aion_astra_twin_embodiment.cli aion-tiger-dimensions-v2
python -m aion_astra_twin_embodiment.cli aion-tiger-dimension-audit
```

## 8. Claim boundary

```text
MEASUREMENT_COMPLETENESS != BIOLOGICAL_EXISTENCE
SOURCE_DENSITY != SCIENTIFIC_VALIDATION
TIGER_OSTEOMETRY != ANTHROPOMORPHIC_BIPED_VALIDATION
FURSUIT_PRACTICE != BIOLOGICAL_NORMAL_RANGE
FORENSIC_DRY_SPECIMEN_CONSTRAINT != LIVE_PHYSIOLOGY
REFERENCE_MODEL != LIVE_BODY
EMBODIMENT != SUBJECTIVITY
```


## 9. PR scope acknowledgement

本次 V2 尺寸擴充刻意把 source manifest、measurement protocol、schema、tests 與 evidence audit 放在同一個可追溯 research candidate 中，因此 PR diff 超過 repository 的 large-diff threshold。PR body 依 canonical guard 明示 `LARGE_PR_EXPECTED = TRUE` 與 substantive reason；該 acknowledgement 只解除 large-diff scope guard，依 validator 規則 **不是 merge authority**。
