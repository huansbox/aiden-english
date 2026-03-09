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

docs/                   GitHub Pages 根目錄（自動生成，勿手動編輯）
├── feed.xml            Apple Podcast 相容 RSS feed
├── index.html          簡易首頁（含播放器 + RSS URL 複製按鈕）
├── cover.jpg           封面圖（來源：reading_plus/94.jpg）
└── audio/*.mp3         MP3 音檔副本
```

## 技術決策

- **TTS**：edge-tts，語音 `en-US-JennyNeural`（美式女聲），免費、音質好
- **RSS feed**：Python 標準庫 `xml.etree.ElementTree`，無額外依賴
- **MP3 duration**：以檔案大小 ÷ 48kbps 估算（edge-tts 預設位元率）
- **Episode title**：從對應 `.md` 檔的 H1 heading 讀取，fallback 用檔名推導
- **pubDate**：以 episode number 排序，從 2026-03-09 起每集 +1 天
- **託管**：GitHub Pages（main branch `/docs` 目錄），public repo
- **Base URL**：`https://huansbox.github.io/aiden-english/`

## 新增集數工作流

1. 將新教材掃描圖放入 `reading_plus/`
2. 用 Claude 視覺能力將圖片 OCR 為 `{頁碼}_{title}.md`
3. 更新 `reading_plus/generate_audio.py` 的 `MD_FILES` 清單
4. 執行 `cd reading_plus && python generate_audio.py`
5. 執行 `python podcast/generate_feed.py`
6. `git add . && git commit -m "feat: add new episodes" && git push`

## 依賴

- Python 3.10+
- edge-tts >= 7.0（`pip install -r requirements.txt`）
