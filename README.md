# Aiden English Reading

私人 Podcast — 兒童英文閱讀聽力練習。

將補習班教材（掃描圖片）轉為語音，透過 GitHub Pages 託管 Podcast RSS feed，在平板的 Podcast App 訂閱收聽。

## 環境設置

```bash
pip install -r requirements.txt
```

需要 Python 3.10 以上。Windows 環境執行時建議加 `PYTHONIOENCODING=utf-8`。

## 使用方式

### 1. 產生音檔

```bash
cd reading_plus
python generate_audio.py
```

從 `reading_plus/*.md` 讀取故事文字，用 edge-tts 生成 MP3 至 `reading_plus/audio/`。

### 2. 產生 Podcast 站點

```bash
python podcast/generate_feed.py
```

掃描 `reading_plus/audio/*.mp3`，自動產生 `docs/` 目錄下的所有檔案：
- `feed.xml` — Podcast RSS feed（Apple Podcast 相容）
- `index.html` — 網頁播放器
- `audio/` — MP3 副本
- `cover.jpg` — 封面圖

### 3. 推送上線

```bash
git add docs/
git commit -m "feat: add new episodes"
git push
```

GitHub Pages 會自動部署，約 1-2 分鐘後生效。

## 訂閱 Podcast

RSS URL：

```
https://huansbox.github.io/aiden-english/feed.xml
```

- **Apple Podcasts**：資料庫 → ⋯ → 透過 URL 追蹤節目 → 貼上 RSS URL
- **Pocket Casts**：搜尋 → Submit RSS URL → 貼上
- **網頁播放**：直接開啟 https://huansbox.github.io/aiden-english/

## 互動練習

每篇故事對應一頁互動練習題，在平板瀏覽器直接作答：

- 練習首頁：https://huansbox.github.io/aiden-english/exercises/
- 橫式全螢幕、一次一題、全按鈕操作
- 答錯可重試一次，第二次才顯示正確答案

新增練習頁請參考 `docs/plans/exercise-v2-sop.md`。

## 目前集數

| # | 故事 | 練習 |
|---|------|------|
| 94/95 | The Skunks' Present | v2 |
| 96/97 | Make Way for Betsy | coming soon |
| 98/99 | A Narrow Escape | coming soon |
| 100/101 | The String House | coming soon |
| 102/103 | Breakfast with Barnie | coming soon |
