# Aiden English Reading

9 歲小孩英文閱讀聽力練習平台。GitHub Pages 託管，包含 Podcast + 可列印文章 + 互動練習題。

## 兩條內容 Pipeline

### Pipeline 1：Reading Plus（課本故事）

**輸入**：使用者提供課本掃描圖（偶數頁=故事，奇數頁=練習題）

**處理流程**：
1. Claude 視覺 OCR 圖片 → `reading_plus/{頁碼}_{title}.md`
2. edge-tts 生成音檔 → `reading_plus/audio/*.mp3`
3. 根據練習題圖片設計 JSON 題目（參考 SOP 轉換原則）→ `docs/exercises/{頁碼}_*.html`

**產出**：
- 聽：Podcast Season 1（課本音檔）
- 讀：課本紙本（使用者已有）
- 練：互動練習題（Pad 瀏覽器）

### Pipeline 2：Articles（改寫文章）

**輸入**：使用者提供英文文章 URL 或文本

**處理流程**：
1. 擷取原文 → `reading_plus/news/{topic}_原文.md`
2. AI 簡化改寫為多篇（遵循簡化標準）→ `reading_plus/news/{topic}_part*.md`
3. 三角度審核（閱讀難度 / 敘事趣味 / 教學價值）→ 修正
4. edge-tts 生成音檔 → `reading_plus/news/audio/*.mp3`
5. 建立可列印 HTML → `docs/articles/*.html`
6. 設計練習題 → `docs/exercises/{topic}_part*.html`

**產出**：
- 聽：Podcast Season 2（文章音檔）
- 讀：可列印 HTML 頁面（大字體、段落編號、新詞粗體）
- 練：互動練習題（Pad 瀏覽器）

## 簡化標準（Pipeline 2）

- 每篇 150-200 字，平均句長 8-12 字，最長不超過 18 字
- 80% 簡單句，過去簡單式為主
- 新詞彙 5-8 個/篇，in-context 解釋（不另設 glossary）
- 一篇原文可拆為多篇（各有完整故事弧線）
- 三角度審核：閱讀難度分析 / 敘事與趣味性 / EFL 教學價值

## 學習流程（使用者端）

| 步驟 | Reading Plus | Articles |
|------|-------------|----------|
| 讀 | 課本紙本 | 列印 HTML（[Articles](https://huansbox.github.io/aiden-english/articles/)） |
| 聽 | Podcast Season 1 | Podcast Season 2 |
| 練 | [Exercises](https://huansbox.github.io/aiden-english/exercises/) | 同左（統一入口） |

## 目錄結構

```
reading_plus/                   素材與音檔（不部署）
├── *.jpg                       課本掃描圖
├── {頁碼}_{title}.md           課本故事 OCR 文字
├── audio/*.mp3                 課本故事 TTS 音檔
├── generate_audio.py           課本音檔生成腳本
└── news/                       文章素材（非 Reading Plus，歷史命名）
    ├── {topic}_*.md            原文 + 簡化分篇
    ├── audio/*.mp3             文章 TTS 音檔
    └── generate_audio.py       文章音檔生成腳本

podcast/
└── generate_feed.py            RSS feed 生成器（自動掃描兩個來源）

docs/                           GitHub Pages 部署目錄
├── index.html                  首頁（Exercises / Articles / Podcast 入口）
├── feed.xml                    Podcast RSS（Season 1 + 2，itunes:season 標籤）
├── cover.jpg                   Podcast 封面
├── audio/*.mp3                 所有 MP3（Podcast 統一路徑）
├── articles/                   可列印文章（純列印，無音檔無練習連結）
│   ├── index.html              文章列表
│   └── {topic}.html            列印頁（大字體、段落編號、新詞粗體、Print 按鈕）
├── exercises/                  互動練習題（統一入口）
│   ├── index.html              首頁（分 Reading Plus / News 兩區）
│   ├── quiz-engine.js          共用引擎（6 題型 + 兩次重試邏輯）
│   ├── style-v2.css            共用樣式（橫式卡片佈局）
│   ├── {頁碼}_*.html           Reading Plus 練習
│   └── {topic}_part*.html      文章練習
└── plans/                      設計文檔
    ├── exercise-v2-sop.md      練習題建立 SOP（題型規格 + 轉換原則）
    └── *.md                    各次開發的設計與實作 plan
```

## 技術決策

- **TTS**：edge-tts `en-US-JennyNeural`（美式女聲），免費
- **Podcast**：RSS feed + `itunes:season`，Apple Podcast 相容
- **練習引擎**：vanilla JS，JSON-driven，6 題型，兩次重試
- **託管**：GitHub Pages（public repo），`docs/` 目錄
- **零依賴前端**：無 build step，無 framework

## 操作指令

### 新增 Reading Plus

```bash
# 1. OCR 圖片為 md（Claude 視覺）
# 2. 生成音檔
cd reading_plus && python generate_audio.py
# 3. 更新 feed
python podcast/generate_feed.py
# 4. 建立練習頁（參考 docs/plans/exercise-v2-sop.md）
# 5. 更新 docs/exercises/index.html
```

### 新增文章

```bash
# 1. 擷取原文、簡化改寫、審核（Claude 對話中完成）
# 2. 生成音檔
cd reading_plus/news && python generate_audio.py
# 3. 更新 feed
python podcast/generate_feed.py
# 4. 建立列印 HTML（docs/articles/）
# 5. 建立練習頁（docs/exercises/）
# 6. 更新 docs/articles/index.html 和 docs/exercises/index.html
```

## 依賴

- Python 3.10+
- edge-tts >= 7.0（`pip install -r requirements.txt`）
