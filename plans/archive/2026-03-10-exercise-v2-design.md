# Exercise Page v2 — Design Doc

## 目標

將練習題頁面重新設計為 pad 橫式、一次一題、全按鈕化的互動體驗。先做 p.95 prototype，確認後套用到其他 4 頁。

## 設計決策

### 整體框架

- **Pad 橫式優先**（1024×768 基準），直式可用但非首要
- **一次一題**：卡片佔滿畫面中央，大字體，減少認知負擔
- **底部導覽列**：`← Prev` | `3 / 12` | `Next →`
- **即時回饋**：按 Next 時對答案，正確 ✓ 綠色 / 錯誤 ✗ 紅色 + 顯示正確答案，停留 1.5 秒後進下一題
- **最後一題完成後**顯示總分摘要頁
- **全按鈕化**：p.95 不需要任何文字輸入框

### 題型設計（6 種）

#### ① 詞義選單字（Knowing the Words）

- 題目顯示詞義描述（如 "Black and white animal"）
- 4~5 個單字按鈕（正確答案 + 干擾詞，全部來自同篇故事）
- 單選：點擊選中高亮，再點其他按鈕切換

#### ② 同義詞多選（Synonyms）

- 4 個單字按鈕，選 2 個同義詞
- Toggle 模式：點一次選中、再點取消
- 維持原課本題型不變，僅改善 UI

#### ③ Word Bank 填句（取代 ABC order）

- 頂部 word bank：6 個單字按鈕（4 正確 + 2 干擾詞，全部來自同篇故事）
- 下方 4 個句子，各有一個空格
- 互動：點 word bank 單字 → 填入第一個空的空格；點已填的空格 → 退回 word bank
- 已使用的單字在 word bank 中變灰
- 整組 4 句算「一題」

#### ④ 主旨選擇（Radio）

- 3 個選項大按鈕，單選

#### ⑤ 點擊排序（Order）

- 4 個句子按鈕，小孩依先後順序點擊
- 點擊後句子移到「已排序」區域，顯示編號 ①②③④
- 點已排序的句子可退回待選區
- 整組算「一題」

#### ⑥ 選詞填空（Select）

- 句子 + 3 個單字按鈕（取代下拉選單）
- 單選

### p.95 題目流程（12 步）

| Step | 題型 | Section | 內容 | 答案 |
|------|------|---------|------|------|
| 1 | 詞義選單字 | Knowing the Words | black and white animal | skunk |
| 2 | 詞義選單字 | Knowing the Words | small animals such as bees and ants | insects |
| 3 | 同義詞 | Knowing the Words | begin, stop, call, start | begin, start |
| 4 | 同義詞 | Knowing the Words | bird, rabbit, skunk, bunny | rabbit, bunny |
| 5 | 同義詞 | Knowing the Words | listen, catch, see, look | see, look |
| 6 | 同義詞 | Knowing the Words | run, car, hurry, dog | run, hurry |
| 7 | Word Bank | Learning to Study | 4 句 + 6 詞 | patch, skunk, bee, turn |
| 8 | Word Bank | Learning to Study | 4 句 + 6 詞 | carrot, growl, happen, safe |
| 9 | 主旨選擇 | Reading & Thinking | story is mostly about... | how skunks keep safe |
| 10 | 排序 | Reading & Thinking | 4 sentences in order | 1,2,3,4 |
| 11 | 選詞填空 | Reading & Thinking | wanted to ___ | dance |
| 12 | 選詞填空 | Reading & Thinking | dog ___ at the noise | growled |

### Word Bank 題目資料

#### Group 1（原 ABC order List 1）

Words (6): **patch**, **skunk**, **bee**, **turn**, flag, bush

Sentences:
1. On my way to the carrot ___ one morning... → **patch**
2. Behind her were six little ___s, waving their tails. → **skunk**
3. We are on our way to look for insects like ___s and ants. → **bee**
4. I heard an angry growl. I ___ed around. → **turn**

#### Group 2（原 ABC order List 2）

Words (6): **carrot**, **growl**, **happen**, **safe**, branches, morning

Sentences:
1. On my way to the ___ patch one morning... → **carrot**
2. I heard an angry ___ behind me. → **growl**
3. The branches will keep us ___. → **safe**
4. I should have guessed what would ___. → **happen**

### 詞義選單字 — 干擾詞

| 題 | 正確答案 | 干擾詞（來自故事） |
|----|---------|-------------------|
| 1. black and white animal | skunk | insects, flag, bush, bunny |
| 2. small animals such as bees and ants | insects | skunk, flag, bush, bunny |

### 技術架構

- 單一 HTML 檔 + 共用 `style-v2.css` + `quiz-engine.js`
- 新檔案，不覆蓋 v1（保留原版供比較）
- 題目資料用 HTML `data-*` 屬性或 `<script type="application/json">` 內嵌
- CSS Grid 佈局，橫式卡片置中
- 純 vanilla JS，零依賴

### 未來擴展（prototype 確認後）

- 套用到 p.97, 99, 101, 103
- 簡答題處理（p.97, 99 有簡答題）
- 可能新增：做完練習後連結到對應的 Podcast 音檔重聽故事
