# Aiden English Reading

9 歲小孩英文補習班教材的私人 Podcast。將掃描圖片 OCR 為文字，用 edge-tts 生成語音，透過 GitHub Pages 託管 RSS feed，供 Podcast App 訂閱。

## 目錄結構

```
reading_plus/           原始素材與音檔生成
├── *.jpg               教材掃描圖（偶數頁=故事，奇數頁=練習題）
├── *_<title>.md        故事文字（從圖片人工 OCR 轉錄）
├── audio/*.mp3         TTS 生成的音檔
└── generate_audio.py   edge-tts 音檔生成腳本

podcast/                Podcast 工具
└── generate_feed.py    RSS feed + 靜態站點生成器（輸出至 docs/）

docs/                   GitHub Pages 根目錄
├── feed.xml            Apple Podcast 相容 RSS feed
├── index.html          簡易首頁（含播放器 + RSS URL + 練習連結）
├── cover.jpg           封面圖（來源：reading_plus/94.jpg）
├── audio/*.mp3         MP3 音檔副本
├── exercises/          互動練習題（v2）
│   ├── index.html      練習首頁
│   ├── quiz-engine.js  共用引擎（6 題型 + 兩次重試）
│   ├── style-v2.css    共用樣式（橫式卡片佈局）
│   └── 95_*.html       各頁練習（題目 JSON 內嵌）
└── plans/              設計文檔與 SOP
```

## 技術決策

### Podcast
- **TTS**：edge-tts，語音 `en-US-JennyNeural`（美式女聲），免費、音質好
- **RSS feed**：Python 標準庫 `xml.etree.ElementTree`，無額外依賴
- **MP3 duration**：以檔案大小 ÷ 48kbps 估算（edge-tts 預設位元率）
- **Episode title**：從對應 `.md` 檔的 H1 heading 讀取，fallback 用檔名推導
- **pubDate**：以 episode number 排序，從 2026-03-09 起每集 +1 天
- **託管**：GitHub Pages（main branch `/docs` 目錄），public repo
- **Base URL**：`https://huansbox.github.io/aiden-english/`

### 練習題（v2）
- **架構**：JSON-driven quiz engine，題目內嵌在 HTML `<script type="application/json">` 中
- **引擎**：`quiz-engine.js`（vanilla JS，零依賴）— 讀取 JSON、建構 DOM、處理互動與計分
- **佈局**：橫式優先（iPad 1024×768），一次一題卡片式，全按鈕化（無文字輸入）
- **題型**：vocab / synonym / wordbank / radio / order / select（共 6 種）
- **重試**：第一次錯只標記錯誤選項、保留互動；第二次錯顯示正確答案並前進
- **Word Bank**：取代原本 ABC order 題型，用故事原文造句 + 干擾詞
- **Suffix**：Word Bank 的 JSON 支援 `suffix` 欄位，自動在填入的單字後加上詞形變化（-s, -ed 等）
- **新增練習頁 SOP**：`docs/plans/exercise-v2-sop.md`

## 新增集數工作流

1. 將新教材掃描圖放入 `reading_plus/`
2. 用 Claude 視覺能力將圖片 OCR 為 `{頁碼}_{title}.md`
3. 更新 `reading_plus/generate_audio.py` 的 `MD_FILES` 清單
4. 執行 `cd reading_plus && python generate_audio.py`
5. 執行 `python podcast/generate_feed.py`
6. `git add . && git commit -m "feat: add new episodes" && git push`

## 新增練習頁工作流

1. 參考 `docs/plans/exercise-v2-sop.md`
2. 複製 `95_the_skunks_present.html` 為模板
3. 替換 JSON 題目資料
4. 更新 `docs/exercises/index.html`
5. 測試所有題型互動

## 依賴

- Python 3.10+
- edge-tts >= 7.0（`pip install -r requirements.txt`）
