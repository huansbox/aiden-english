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
1. 擷取原文 → `articles/{topic}_原文.md`
2. AI 簡化改寫為多篇（遵循簡化標準）→ `articles/{topic}_part*.md`
3. 三角度審核（閱讀難度 / 敘事趣味 / 教學價值）→ 修正
4. edge-tts 生成音檔 → `articles/audio/*.mp3`
5. 建立可列印 HTML → `docs/articles/*.html`
6. 設計練習題 → `docs/exercises/{topic}_part*.html`

**產出**：
- 聽：Podcast Season 2（文章音檔）
- 讀：可列印 HTML 頁面（大字體、段落編號、新詞粗體）
- 練：互動練習題（Pad 瀏覽器）

## SOP 文件

| SOP | 用途 | 何時載入 |
|-----|------|---------|
| `plans/exercise-sop.md` | 建立互動練習題 | Pipeline 1 & 2 最後一步 |
| `plans/article-rewrite-sop.md` | 改寫文章（含基準數據、審核流程） | Pipeline 2 Step 1-3 |

## 學習流程（使用者端）

| 步驟 | Reading Plus | Articles |
|------|-------------|----------|
| 讀 | 課本紙本 | 列印 HTML（[Articles](https://huansbox.github.io/aiden-english/articles/)） |
| 聽 | Podcast Season 1 | Podcast Season 2 |
| 練 | [Exercises](https://huansbox.github.io/aiden-english/exercises/) | 同左（統一入口） |

## 目錄結構

```
reading_plus/                   Pipeline 1 素材（課本）
├── scans/                      課本掃描圖（.jpg）
├── {頁碼}_{title}.md           故事 OCR 文字
└── audio/                      TTS 音檔

articles/                       Pipeline 2 素材（改寫文章）
├── {topic}_*.md                原文 + 簡化分篇
└── audio/                      TTS 音檔

generate_audio.py               通用 TTS 腳本（CLI 參數選來源）
podcast/
└── generate_feed.py            RSS feed 生成器

plans/                          設計文檔與 SOP（不部署）
├── exercise-sop.md             練習題建立 SOP
├── article-rewrite-sop.md      文章改寫 SOP
└── archive/                    歷史 plan（已完成）

docs/                           GitHub Pages 部署目錄
├── index.html
├── feed.xml
├── apple-touch-icon.png        PWA 主畫面圖示（180×180）
├── pwa.js                      Standalone 模式內部連結攔截
├── audio/                      所有 MP3（由 generate_feed.py 複製）
├── articles/                   可列印文章 HTML
└── exercises/                  互動練習題（含分數記錄）
```

## 技術決策

- **TTS**：edge-tts `en-US-JennyNeural`（美式女聲），免費
- **Podcast**：RSS feed + `itunes:season`，Apple Podcast 相容
- **練習引擎**：vanilla JS，JSON-driven，6 題型，兩次重試，localStorage 存最佳分數
- **PWA**：apple-mobile-web-app-capable，iPad 主畫面全螢幕，pwa.js 攔截內部連結
- **託管**：GitHub Pages（public repo），`docs/` 目錄
- **零依賴前端**：無 build step，無 framework

## 操作指令

### 新增 Reading Plus

```bash
# 1. OCR 圖片為 md（Claude 視覺）
# 2. 生成音檔
python generate_audio.py reading_plus
# 3. 更新 feed
python podcast/generate_feed.py
# 4. 建立練習頁（參考 plans/exercise-sop.md）
# 5. 更新 docs/exercises/index.html
```

### 新增文章

```bash
# 1. 擷取原文、簡化改寫、審核（Claude 對話中完成）
# 2. 生成音檔
python generate_audio.py articles
# 3. 更新 feed
python podcast/generate_feed.py
# 4. 建立列印 HTML（docs/articles/）
# 5. 建立練習頁（docs/exercises/）
# 6. 更新 docs/articles/index.html 和 docs/exercises/index.html
```

## 依賴

- Python 3.10+
- edge-tts >= 7.0（`pip install -r requirements.txt`）
