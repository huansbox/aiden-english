# Aiden English Reading

9 歲小孩英文閱讀聽力練習。兩種內容來源：Reading Plus 課本故事 + AI 改寫新聞文章。

## 學習流程

1. **讀文章**：列印紙本閱讀（Reading Plus 用課本，新聞用 `docs/articles/` 列印頁）
2. **聽音檔**：Podcast App 收聽（Season 1 = Reading Plus, Season 2 = News & Articles）
3. **做練習**：Pad 橫式瀏覽器做互動練習題（`docs/exercises/` 統一入口）

## 目錄結構

```
reading_plus/               Reading Plus 課本素材
├── *.jpg                   教材掃描圖（偶數頁=故事，奇數頁=練習題）
├── *_<title>.md            故事文字（OCR 轉錄）
├── audio/*.mp3             TTS 音檔
├── generate_audio.py       音檔生成腳本
└── news/                   新聞文章素材
    ├── *_original.md       原始新聞
    ├── *_part*.md          簡化後的分篇文章
    ├── audio/*.mp3         TTS 音檔
    └── generate_audio.py   音檔生成腳本

podcast/
└── generate_feed.py        RSS feed 生成器（Season 支援）

docs/                       GitHub Pages 根目錄
├── feed.xml                Podcast RSS feed（Season 1 + 2）
├── index.html              首頁（Podcast + Exercises + Articles 入口）
├── cover.jpg               封面圖
├── audio/*.mp3             所有 MP3（Podcast 統一路徑）
├── articles/               可列印文章（純閱讀用，無音檔無練習）
│   ├── index.html          文章列表
│   └── *.html              各篇文章（大字體、段落編號、新詞粗體、Print 按鈕）
├── exercises/              互動練習題（統一入口）
│   ├── index.html          練習首頁（分 Reading Plus / News 兩區）
│   ├── quiz-engine.js      共用引擎（6 題型 + 兩次重試）
│   ├── style-v2.css        共用樣式（橫式卡片佈局）
│   ├── 95_*.html           Reading Plus 練習（題目 JSON 內嵌）
│   └── wbc_*.html          新聞文章練習
└── plans/                  設計文檔與 SOP
```

## 技術決策

### Podcast
- **TTS**：edge-tts，語音 `en-US-JennyNeural`（美式女聲）
- **RSS feed**：Python `xml.etree.ElementTree`，支援 `itunes:season`
- **Season 1**：Reading Plus 課本故事（episode number = 頁碼）
- **Season 2**：News & Articles（episode number = 順序編號）
- **託管**：GitHub Pages（main branch `/docs`），public repo
- **Base URL**：`https://huansbox.github.io/aiden-english/`

### 練習題（v2）
- **架構**：JSON-driven quiz engine，題目內嵌在 `<script type="application/json">`
- **引擎**：`quiz-engine.js`（vanilla JS，零依賴）
- **佈局**：橫式優先（iPad 1024×768），一次一題卡片式，全按鈕化
- **題型**：vocab / synonym / wordbank / radio / order / select（共 6 種）
- **重試**：第一次錯標記錯誤選項；第二次錯顯示正確答案
- **SOP**：`docs/plans/exercise-v2-sop.md`

### 新聞文章簡化標準
- 每篇 150-200 字，平均句長 8-12 字，最長不超過 18 字
- 80% 簡單句，過去簡單式為主，新詞彙 5-8 個/篇
- 干擾詞 / 選項全部來自文章本身
- 詳見 `docs/plans/exercise-v2-sop.md` 題型轉換表

## 新增 Reading Plus 集數

1. 掃描圖放入 `reading_plus/`
2. OCR 為 `{頁碼}_{title}.md`
3. 更新 `reading_plus/generate_audio.py` 的 `MD_FILES`
4. `cd reading_plus && python generate_audio.py`
5. `python podcast/generate_feed.py`
6. 建立練習頁（參考 SOP）
7. 更新 `docs/exercises/index.html`

## 新增新聞文章

1. 存原始新聞為 `reading_plus/news/{topic}_original.md`
2. 簡化改寫為多篇 `{topic}_part*.md`（遵循簡化標準）
3. `cd reading_plus/news && python generate_audio.py`（更新 MD_FILES）
4. `python podcast/generate_feed.py`（自動加入 Season 2）
5. 建立可列印 HTML（`docs/articles/`）
6. 建立練習頁（`docs/exercises/`）
7. 更新兩個 index.html

## 依賴

- Python 3.10+
- edge-tts >= 7.0（`pip install -r requirements.txt`）
