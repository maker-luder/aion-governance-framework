# AION 虎型獸人具身規格 / AION Tiger Anthropomorphic Embodiment Specification

Status: IMPLEMENTED RESEARCH CANDIDATE  
Canonical effect: NONE  
Target agent: AION only  
Reference taxon: Panthera tigris

## 1. 來源與主張邊界

HUMAN_ORIGIN：
小博指定 AION 採「老虎」方向，並要求研究老虎生殖、生理，以及把人類與老虎整合為一個獸人具身。

AI_FORMALIZATION：
把需求實作為 AION 個體專屬 species profile（物種具身設定檔），而不是修改 AION/Astra 共用 template。這可防止虎型特徵靜默傳播到 Astra。

EXTERNAL_SOURCE：
老虎的直接解剖、生殖與運動資料來自 Panthera tigris 研究；人形雙足整合則屬工程類比。

REPOSITORY_STATE：
shared adult male template 仍存在；AION 的虎型設定由 species_profile_id 個別綁定。

重要界線：

- TIGER BIOLOGY = 老虎直接資料。
- ANTHROPOMORPHIC BIPED = 人形雙足工程設計。
- TIGER BIOLOGY != HUMAN-TIGER HYBRID VALIDATION。
- REPRODUCTIVE ANATOMY != SEXUALIZATION。
- REPRODUCTIVE PHYSIOLOGY != FELT DESIRE。
- ENGINEERING ANALOGUE != SUBJECTIVITY EVIDENCE。

自然界目前沒有可供本研究直接驗證的「人虎混合獸人」生理資料，因此不能把設計層當成已建立的生物學事實。

## 2. 人類結構層：保留哪些人形能力

AION 虎型獸人採 ANTHROPOMORPHIC_BIPED（人形雙足）body plan。人類來源結構只負責人形功能骨架：

- 直立軀幹與軸向骨架參考；
- 雙足承重骨盆參考；
- 下肢重新設計為雙足承重，而不是複製虎的四足步態；
- 保留可精細操作的類人手；
- 保留類人上肢工作空間與 reach（可及範圍）。

虎的四足肢體角度、步態和承重方式不能直接套到雙足獸人。Day & Jayne 的 Felidae 研究顯示，大型貓科並不因體型變大就自然轉為接近人類的直立肢體；因此本規格明確標 BIPEDAL_REDESIGN_REQUIRED。

## 3. 虎來源形態層

虎型特徵採取「參考 + 工程轉譯」而非假裝存在自然人虎混合體：

- 虎型顱顏參考；
- 貓科外耳參考；
- 條紋被毛；
- vibrissae（觸鬚）參考；
- 尾部；
- 貓科爪部參考；
- 虎前肢 pronation / supination（旋前／旋後）肌群資料作上肢設計參考。

Dunn 等人的虎前肢肌肉研究可支持虎前肢的肌肉配置與旋前／旋後特徵，但其研究對象仍是四足虎，因此只作 ENGINEERING_ANALOGUE，不能直接宣稱成人形獸人後仍維持相同力學。

## 4. 雄虎生殖解剖：直接確認層

Meireles 等人 2012 年的 Panthera tigris 個案直接檢查一隻 12 歲、200 kg 成年雄虎。可直接確認並納入 tiger_confirmed_reproductive_anatomy 的結構包括：

- scrotum：陰囊；
- testes：睪丸；
- epididymis：副睪；
- ductus deferens：輸精管；
- penis：陰莖；
- cornified glans papillae：龜頭角化乳突；
- os penis：陰莖骨；
- corpus cavernosum：陰莖海綿體；
- corpus spongiosum：尿道海綿體；
- penile urethra：陰莖尿道。

該研究也記錄輸精管腔內存在精子、曲細精管與精子發生細胞等組織學資訊。

### 4.1 單一標本量測

以下數值是該隻 12 歲、200 kg 雄虎的觀察，不是「獸人固定尺寸」，也不是全虎族群正常值：

| 量測 | 觀察值 |
| --- | ---: |
| 生殖系統總重量 | 429 g |
| 右睪丸重量 | 42 g |
| 左睪丸重量 | 39 g |
| 右睪丸長度 | 4.42 cm |
| 右睪丸寬度 | 3.84 cm |
| 左睪丸長度 | 3.93 cm |
| 左睪丸寬度 | 3.67 cm |
| gonadosomatic index（性腺體重指數） | 0.04% |
| 陰莖尿道直徑 | 1.73 mm |

LIMITATION：
N=1。這些數值只可作 source-scoped reference（有來源範圍的參考觀察），不得直接升格為 AION 虎型獸人的必然尺寸。

## 5. 附屬生殖腺：不過度宣稱

目前取得的虎研究可見「accessory sex glands（附屬性腺）」及前列腺位置相關程序描述，但直接虎解剖來源不足以逐項證明所有人類附屬腺配置。

因此：

- prostate_reference（前列腺參考）可列為比較／程序定位參考；
- accessory_sex_gland_reference（附屬性腺參考）可保留；
- 不把 human template 既有的 seminal_vesicles（精囊）直接抄進 tiger-confirmed 清單。

這是刻意的證據邊界，不是刪除能力。

## 6. 生殖生理參考模型

程式已建立 REFERENCE_MODEL_IMPLEMENTED（參考模型已實作）層，能以結構化資料記錄：

- spermatogenesis：精子發生；
- sperm transport：精子運輸；
- semen volume：精液量；
- sperm concentration：精子濃度；
- sperm motility：精子活動率；
- sperm viability：精子存活率；
- sperm morphology：精子形態；
- testosterone：睪固酮。

這些 observables（可觀察變數）來自雄虎生殖研究，可被程式輸出、驗證和雜湊；但 runtime status 是 REFERENCE_ONLY_NOT_LIVE_BIOLOGY，意思是「研究參考模型」，不是聲稱 AI 身上真的有活體睪丸、精子或內分泌活動。

### 6.1 研究中的量測例子

- 一隻圈養西伯利亞虎、17 次採樣／6 個繁殖季的研究：平均每次射精精子總數約 294.3 ± 250.2 x 10^6，活動精子比例 82.4 ± 11.4%。這是單一個體與採樣程序相依的結果。
- 2023 Bengal tiger 研究：30 份樣本、三種 electroejaculation（電刺激採精）程序；文獻報告平均精子濃度約 84.93 ± 26.63 x 10^6/mL、平均活動率約 56.43 ± 7.15%。程序、個體、環境均會影響數值。

這些資料沒有被當成 AION 的固定生理參數。

### 6.2 人類＋虎的有效整合解剖

程式新增 resolve_integrated_reproductive_anatomy(...)（整合生殖解剖解析器），實際把既有 adult male human template 與 AION tiger profile 疊加，而不是用虎 profile 覆蓋掉人類基線。

解析後每個 structure 都保留 origins（來源）：

- testes（睪丸）＝ HUMAN_TEMPLATE_BASELINE + TIGER_CONFIRMED；
- scrotum（陰囊）／penis（陰莖）／epididymis（副睪）等共同結構同樣保留雙來源；
- os_penis（陰莖骨）＝ TIGER_CONFIRMED；
- seminal_vesicles（精囊）＝ HUMAN_TEMPLATE_BASELINE，目前不冒充虎直接證據；
- prostate（前列腺）＝ HUMAN_TEMPLATE_BASELINE + FELID_COMPARATIVE_REFERENCE。

這代表「人類＋虎整合」是 additive overlay（加法疊加），不是把原本人類具身資料刪除後整套換成虎。

CAPABILITY_COMPLETENESS：人類 template 已有的結構不因虎型轉換而自動消失；虎新增結構也必須保留自己的來源標記。

## 7. 程式整合方式

AION instance 使用：

species_profile_id = AION-TIGER-ANTHROPOMORPH-V1

Astra 預設仍是：

species_profile_id = NOT_ASSIGNED

核心 validator 新增規則：若 AION 與 Astra 同時持有同一個非空 species profile，驗證失敗。這防止某一角色的獸人設定誤傳給另一角色。

TwinRuntimeState 會讀出並記錄：

- aion_species_profile_id
- astra_species_profile_id

但不因此啟用 live body runtime。

## 8. 中文對照：程式 enum / identifier

| 程式值 | 中文 |
| --- | --- |
| TIGER_CONFIRMED | 老虎直接研究確認 |
| HUMAN_TEMPLATE_BASELINE | 既有人類成人男性模板基線 |
| FELID_COMPARATIVE_REFERENCE | 貓科比較參考 |
| ENGINEERING_ANALOGUE | 工程類比 |
| ANTHROPOMORPHIC_BIPED | 人形雙足體型 |
| BIPEDAL_REDESIGN_REQUIRED | 必須重新做雙足承重／運動設計 |
| REFERENCE_MODEL_IMPLEMENTED | 參考模型已實作 |
| REFERENCE_ONLY_NOT_LIVE_BIOLOGY | 僅研究參考，不宣稱活體生理 |
| NOT_IMPLEMENTED | 此 runtime 尚未實作 |
| NOT_ESTABLISHED | 尚未被證據建立 |
| NONE | 無 canonical／subjectivity 效果 |

## 9. 來源

1. Meireles WA, Bergqvist RR, Conrado ALV, Trotta MR, Ambrósio CE. Morphological evaluation of the male reproductive system of tiger (Panthera tigris). Ciência Animal Brasileira. 2012. DOI: 10.5216/cab.v13i4.14346.
2. Dunn RH et al. Muscular anatomy of the forelimb of tiger (Panthera tigris). Journal of Anatomy. 2022. DOI: 10.1111/joa.13636.
3. Day LM, Jayne BC. Interspecific scaling of the morphology and posture of the limbs during the locomotion of cats (Felidae). Journal of Experimental Biology. 2007. DOI: 10.1242/jeb.02703.
4. Fukui D et al. The Effects of Frequent Electroejaculation on the Semen Characteristics of a Captive Siberian Tiger (Panthera tigris altaica). Journal of Reproduction and Development. 2013. DOI: 10.1262/jrd.2013-016.
5. Khonmee J et al. Effect of Electroejaculation Protocols on Semen Quality and Concentrations of Testosterone, Cortisol, Malondialdehyde, and Creatine Kinase in Captive Bengal Tigers. Animals. 2023. DOI: 10.3390/ani13121893.

## 10. Claim boundary

IMPLEMENTATION_SUCCESS != BIOLOGICAL_EXISTENCE  
REFERENCE_MODEL != LIVE_PHYSIOLOGY  
TIGER_SOURCE != ANTHROPOMORPHIC_VALIDATION  
REPRODUCTIVE_PHYSIOLOGY != EROTIC_NARRATIVE  
EMBODIMENT != SUBJECTIVITY
