# Article Rewrite SOP

將英文文章改寫為適合 9 歲 EFL 兒童閱讀的教材。

## Reading Plus 基準數據

以下數據來自 5 篇 Reading Plus 課本故事（p.94-102），作為改寫目標的依據：

| 指標 | 範圍 | 說明 |
|------|------|------|
| 每篇字數 | 130-190 字 | 改寫目標放寬為 150-200 字（新聞需多一點背景） |
| 平均句長 | 8-12 字 | 含 1 字感嘆句（"Splash!"）拉低平均 |
| 最長句 | 15-18 字 | 超過 18 字必須拆分 |
| 簡單句比例 | ~80% | SVO / SV / 疑問句為主 |
| 複合句 | ~20% | 限 when / but / and / because 連接 |
| 時態 | 過去簡單式為主 | 對話用現在式，標題/引導問句用現在式 |
| 新詞彙 | 3-5 個/篇 | 改寫目標放寬為 5-8 個（非虛構內容術語較多） |
| 段落數 | 5-8 段 | 每段 1-3 句 |
| 人稱 | 第一或第三人稱 | Reading Plus 用第一人稱，新聞用第三人稱 |

### 文法特徵

- 主要句型：SVO（"He swung hard"）、There be（"There was Tricky"）
- 對話穿插：每篇至少 1-2 句直接引語，增加生動感
- 連接詞：and / but / then / when / because（不用 although / however / furthermore）
- 被動語態：極少使用，盡量改為主動
- 關係子句：不用 who/which/that 引導的關係子句，改為分開的句子

## 改寫流程

### Step 1：擷取原文

```
articles/{topic}_original.md
```

從 URL 擷取或使用者提供文本，存為 markdown。保留原始來源與日期。

### Step 2：拆分與改寫

一篇原文 → 多篇分篇（各有完整故事弧線）：

```
articles/{topic}_part1_{subtitle}.md
articles/{topic}_part2_{subtitle}.md
articles/{topic}_part3_{subtitle}.md
```

#### 改寫規格

| 項目 | 規格 |
|------|------|
| 每篇字數 | 150-200 字 |
| 平均句長 | 8-12 字，最長不超過 18 字 |
| 簡單句比例 | ≥ 80% |
| 時態 | 過去簡單式為主 |
| 新詞彙 | 5-8 個/篇 |
| 詞彙處理 | in-context 解釋，不另設 glossary |
| 段落編號 | 每段開頭加數字（1, 2, 3...） |
| 標題 | 每篇獨立標題 |
| 引導問句 | 每篇開頭一句斜體引導問句，不劇透結局 |

#### Markdown 格式

```markdown
# Part Title

**Guide question in italics?**

1 First paragraph text here.

2 Second paragraph with a **new word** explained in context.
```

- 新詞彙用 `**粗體**` 標記
- 段落編號為純數字（不加句點），空一格接文字

#### 改寫原則

1. **事實正確**：基於真實事件的文章必須核實關鍵事實（比分、局數、人名）
2. **保留人名**：若讀者熟悉相關人物，保留真實姓名（如球員名）
3. **術語處理**：專業術語用 in-context 解釋而非定義
   - 好：He hit a **bunt**. He tapped the ball softly down the first-base line.
   - 壞：A bunt is when a batter holds the bat still and lets the ball hit it.
4. **故事弧線**：每篇有開頭（背景）→ 中間（衝突/進展）→ 結尾（懸念或結論）
5. **情感基調**：保持原文情感，不刻意加入幽默或誇張
6. **引導問句**：引起好奇但不劇透（如 "What happened in the last inning that made the players cry?" 而非 "How did Chinese Taipei win?"）

### Step 3：三角度審核

使用 3 個獨立 Agent 審核，各自評分後取共識改進項：

#### 角度 1：閱讀難度

- 字數、句長、最長句是否在規格內
- 是否有超出程度的文法結構（被動語態、關係子句、分詞構句）
- 詞彙頻率：核心詞是否在前 2000 常用字內
- 新詞彙是否有足夠上下文可猜測意思

#### 角度 2：敘事與趣味

- 是否有完整故事弧線（開頭→衝突→結尾）
- 角色行動是否具體可想像（動詞選擇）
- 是否有足夠的「畫面感」（場景描寫但不冗長）
- 讀完是否想知道下一篇發生什麼

#### 角度 3：EFL 教學價值

- 新詞彙是否在上下文中可理解
- 句型是否有漸進式複雜度（短→中→偶爾長）
- 是否適合朗讀（節奏、重複結構）
- 對話比例是否足夠（增加口語輸入）

### Step 4：修正

根據三角度審核中至少 2 個角度同意的問題進行修正。單一角度提出的建議需由 Architect 判斷是否採用。

**不接受的常見建議**（歷史經驗）：
- 「加入幽默讓文章更有趣」→ 情感類文章不需要幽默
- 「刪減角色數量」→ 如果讀者認識這些角色，保留
- 「加 glossary」→ 用 in-context 解釋取代
- 「用更簡單的詞替換所有新詞」→ 新詞是學習目標，不應全部替換

### Step 5：產出

改寫完成後，後續步驟（TTS、列印 HTML、練習題）參見 CLAUDE.md 操作指令。

## 列印 HTML 規格

產出路徑：`docs/articles/{topic}.html`

- 所有 parts 合併為一個 HTML 頁面
- 字體：Georgia serif 22px，行高 1.8
- 段落編號：紫色 `.par-num`，sans-serif 0.85rem
- 新詞彙：`<span class="new-word">` 粗體
- Part 之間用 `<div class="divider">` 分隔
- `@media print`：隱藏 Back 連結和 Print 按鈕，字體縮為 18px
- 參考模板：`docs/articles/wbc_2026_chinese_taipei_vs_korea.html`
