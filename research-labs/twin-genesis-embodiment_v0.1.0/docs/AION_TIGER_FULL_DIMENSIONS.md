# AION 虎型獸人完整尺寸表 / Full Measurable Dimension Preset

Preset: `AION-TIGER-FULL-DIMENSIONS-V1`  
Agent: AION  
Species profile: `AION-TIGER-ANTHROPOMORPH-V1`  
Posture: neutral upright A-pose  
Locomotion: bipedal digitigrade  
Canonical effect: NONE

## 1. 為什麼需要福瑞社群資料

福瑞 fandom 的 reference sheet（角色設定圖）不是生物學論文，但對「模型到底要量什麼」非常實用。WikiFur 把 character/reference sheet 視為 fandom 中用來穩定傳遞角色設定的重要工件；FurMakers 特別指出 fursuit／3D 轉譯時，需要看清肩寬、腿長、paw 大小、尾巴附著與整體輪廓。其他 furry ref-sheet 指南同樣把 plantigrade/digitigrade、paw type、tail、ear、front/back/side view 與比例比較列為核心欄位。

因此本規格採：

- `COMMUNITY_DESIGN_REFERENCE`：決定「哪些部位一定要量」；
- `ENGINEERING_DESIGN_CHOICE`：給出 AION 的實際設計數值；
- 不把 fandom 慣例冒充 `TIGER_CONFIRMED`。

## 2. AION 完整工程尺寸 V1

這是一套可直接拿去做模型、rig、ref sheet 的 **design target**，不是自然界人虎混合體的量測。

| 區域 | 尺寸 | V1 |
| --- | --- | ---: |
| 全身 | 直立總身高 | 190 cm |
| 全身 | 設計體重 | 112 kg |
| 全身 | 臂展 | 198 cm |
| 全身 | 肩峰離地 | 154 cm |
| 全身 | 眼位離地 | 171 cm |
| 全身 | 髖關節中心離地 | 101 cm |
| 全身 | 胯下離地 | 92 cm |
| 全身 | 膝中心離地 | 53 cm |
| 頭 | 頭高 | 38 cm |
| 頭 | 最大寬 | 24 cm |
| 頭 | 前後深度 | 31 cm |
| 頭 | 吻部突出 | 10.5 cm |
| 頭 | 吻部寬 | 14.5 cm |
| 耳 | 單耳高 | 10.5 cm |
| 耳 | 單耳基部寬 | 9 cm |
| 頸 | 頸長 | 13 cm |
| 頸 | 頸圍 | 48 cm |
| 軀幹 | 肩寬 | 54 cm |
| 軀幹 | 胸寬 | 42 cm |
| 軀幹 | 胸深 | 30 cm |
| 軀幹 | 胸圍 | 118 cm |
| 軀幹 | 腰圍 | 94 cm |
| 軀幹 | 臀／髖圍 | 108 cm |
| 軀幹 | 髖寬 | 41 cm |
| 軀幹 | 頸根到腰 | 50 cm |
| 軀幹 | 腰到胯下 | 28 cm |
| 上肢 | 上臂長 | 37 cm |
| 上肢 | 前臂長 | 31.5 cm |
| 上肢 | 前掌／手長 | 23 cm |
| 上肢 | 前掌／手寬 | 12 cm |
| 上肢 | 前爪可露出長 | 2.5 cm |
| 上肢 | 上臂圍 | 42 cm |
| 上肢 | 前臂圍 | 35 cm |
| 下肢 | 大腿段長 | 50 cm |
| 下肢 | 小腿主段長 | 44 cm |
| 下肢 | 趾行飛節離地 | 19 cm |
| 下肢 | 後掌接地長 | 31 cm |
| 下肢 | 後掌寬 | 13.5 cm |
| 下肢 | 大腿圍 | 69 cm |
| 下肢 | 小腿／飛節圍 | 43 cm |
| 尾 | 尾長 | 105 cm |
| 尾 | 尾根直徑 | 13 cm |
| 尾 | 中段直徑 | 9 cm |
| 尾 | 尾尖直徑 | 5.5 cm |
| 尾 | 尾根中心離地 | 101 cm |
| 表面 | 軀幹短毛視覺厚度 | 2 cm |
| 表面 | 頰側蓬毛視覺厚度 | 5 cm |

### 設計邏輯

- 190 cm 是工程 target，仍落在 NASA Human Integration Design Handbook 所示成人 stature 上界（約 194.6 cm）以內。
- 38 cm 頭高 = 身高的 20%，故 `head:stature = 1:5`。這是 anthropomorphic 設計比例，不是人類或野生虎比例。
- 胸、肩、手掌、足掌比一般人類人體工學資料更大，屬虎型 robust morphology（強壯形態）的工程增量。
- 尾長 105 cm 落在臺北市立動物園所列老虎尾長約 60–110 cm 的範圍內，但把這個數值用在雙足獸人仍是工程轉譯。
- digitigrade（趾行）腿不能直接使用人類腳踝 rig，因此增加 `digitigrade_hock_height_cm` 與較長後掌。

## 3. 虎直接量測：只當 reference observation

Meireles et al. 2012 的 N=1 成年雄虎（12 歲、200 kg）：

| 參考量測 | 數值 |
| --- | ---: |
| 右睪丸長 | 4.42 cm |
| 右睪丸寬 | 3.84 cm |
| 左睪丸長 | 3.93 cm |
| 左睪丸寬 | 3.67 cm |
| 陰莖尿道直徑 | 1.73 mm |
| 生殖系統總重量 | 429 g |

這些在程式裡全部標為 `REFERENCE_OBSERVATION + TIGER_CONFIRMED`，不是 AION 固定尺寸。

目前 admitted evidence 沒有足夠虎直接資料支持「陰莖總長」；因此程式明確保留：

```
aion_total_penile_length_cm = UNKNOWN_SOURCE_NOT_ESTABLISHED
```

這不是漏做，而是防止用 fandom、其他貓科或猜測數值填補證據空白。

## 4. 參考來源層

### Tiger / zoological
- Meireles et al. 2012. DOI 10.5216/cab.v13i4.14346.
- Taipei Zoo tiger profile: tiger body length ~160–390 cm, tail ~60–110 cm, body mass ~180–380 kg, shoulder height ~95–110 cm.
- Tokyo/Ueno Zoo Sumatran tiger profile: male body length and skull-length reference.
- Tiger skull morphometrics literature is used only for head-shape constraints, not direct anthropomorphic scaling.

### Human anthropometry
- NASA Human Integration Design Handbook, anthropometric tables.
- NASA body-size range tables derived from NASA-STD-3000.

### Furry community design references
- WikiFur: Character sheet / refsheet as standard character-description artifact.
- FurMakers: builder-facing ref sheets should expose shoulder width, leg length, paw size, tail placement and silhouette.
- Taebear / Fur Affinity: furry anatomy design categories including plantigrade, digitigrade, anthro and feral.
- Ref-sheet guides emphasizing front/back/side neutral views, species anatomy base, paw type, tail and scale/proportion guide.

## 5. Claim boundary

```
COMMUNITY_DESIGN_REFERENCE != BIOLOGICAL_EVIDENCE
ENGINEERING_DESIGN_CHOICE != TIGER_MEASUREMENT
REFERENCE_OBSERVATION != AION_TARGET
COMPLETE_FIELD_COVERAGE != SCIENTIFIC_ESTABLISHMENT
3D_READY_DIMENSIONS != LIVE_BODY
```
