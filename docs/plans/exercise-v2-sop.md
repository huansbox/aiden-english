# Exercise v2 — 套用 SOP

將 quiz-engine v2 套用到新練習頁的標準作業流程。

## 前置條件

共用檔案已存在，不需修改：
- `docs/exercises/quiz-engine.js` — 6 種題型引擎 + 兩次重試邏輯
- `docs/exercises/style-v2.css` — 橫式卡片佈局

## 步驟

### 1. 準備題目資料

從原始 plan 檔 `docs/plans/2026-03-10-exercise-v2-plan.md` 取得該頁的題目資料（Task 3-7 對應 p.97/99/101/103）。

如果 plan 中缺少某頁，需要：
1. 讀取對應的 `reading_plus/{頁碼}_*.md` 故事文本
2. 參考課本練習圖片 `reading_plus/{頁碼}.jpg`
3. 依照下方題型規格建立 JSON 資料

### 2. 建立 HTML 檔案

複製 `95_the_skunks_present.html` 為模板，修改：

1. `<title>` 標題
2. `<h1>` 標題
3. `<script id="quiz-data">` 中的 JSON 資料
4. `<span class="progress">` 中的初始題數 `1 / N`

檔案命名：`{頁碼}_the_story_title.html`

### 3. JSON 資料結構

```json
{
  "title": "Story Title",
  "questions": [ ... ]
}
```

### 4. 題型規格

#### vocab — 詞義選單字
```json
{
  "type": "vocab",
  "section": "Knowing the Words",
  "prompt": "詞義描述 (Par. N)",
  "options": ["正確答案", "干擾詞1", "干擾詞2", ...],
  "answer": "正確答案"
}
```
- options 包含 4-5 個選項，全部來自同篇故事的單字
- 單選

#### synonym — 同義詞多選
```json
{
  "type": "synonym",
  "section": "Knowing the Words",
  "prompt": "Pick the two synonyms:",
  "options": ["word1", "word2", "word3", "word4"],
  "answer": ["synonym1", "synonym2"],
  "pick": 2
}
```
- 固定選 2 個
- answer 是陣列

#### wordbank — 填空題組
```json
{
  "type": "wordbank",
  "section": "Learning to Study",
  "prompt": "Fill in the blanks using the words above:",
  "words": ["word1", "word2", "word3", "word4", "干擾1", "干擾2"],
  "sentences": [
    { "text": "句子前半 ___ 句子後半", "answer": "正確單字" },
    { "text": "需要加後綴的 ___.", "answer": "base", "suffix": "ed" }
  ]
}
```
- words 包含 6 個單字（4 正確 + 2 干擾），全來自故事
- 句子用 `___` 標記空格位置
- 需要詞形變化時加 `suffix` 欄位（如 `"s"`, `"ed"`, `"ing"`）
- suffix 會自動顯示在填入的單字後面

#### radio — 單選題
```json
{
  "type": "radio",
  "section": "Reading and Thinking",
  "prompt": "題目敘述",
  "options": ["選項A", "選項B", "選項C"],
  "answer": "正確選項"
}
```

#### order — 排序題
```json
{
  "type": "order",
  "section": "Reading and Thinking",
  "prompt": "Tap the sentences in the order they happened:",
  "items": ["句子A", "句子B", "句子C", "句子D"],
  "correctOrder": ["正確順序1", "正確順序2", "正確順序3", "正確順序4"]
}
```
- items 是亂序顯示
- correctOrder 是正確順序

#### select — 選詞填空
```json
{
  "type": "select",
  "section": "Reading and Thinking",
  "prompt": "句子 ___.",
  "options": ["選項1", "選項2", "選項3"],
  "answer": "正確選項"
}
```

### 5. 題目設計原則

- **干擾詞全部來自同篇故事**，不用無關單字
- **Word Bank 取代 ABC order**：用故事原文造句，加 2 個干擾詞
- **簡答題轉選擇題**：如果原本是 open-ended，改為 select 或 radio
- **True/False 改為 radio**：選項為 True / False
- 題目順序依課本 section 排列

### 6. 更新 index.html

將 `coming soon` 改為連結：
```html
<li><a href="{頁碼}_story_title.html"><strong>{頁碼}.</strong> Story Title</a></li>
```

### 7. 測試清單

- [ ] 所有題目可正確作答
- [ ] 第一次答錯：錯誤選項變灰，可重試
- [ ] 第二次答錯：顯示正確答案，自動進下題
- [ ] Word Bank suffix 正確顯示（如 skunks, turned）
- [ ] 排序題可點擊排列、退回
- [ ] 完成後顯示總分
- [ ] 橫式排版正常（iPad 1024×768）
- [ ] Try Again 可重新開始

## 注意事項

- `quiz-engine.js` 和 `style-v2.css` 是共用的，除非有 bug 否則不修改
- 比對答案時忽略大小寫和前後空白（`norm()` 函數）
- 每個 HTML 檔案完全獨立，題目資料內嵌在 JSON 中
