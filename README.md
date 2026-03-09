# Aiden English Reading

私人 Podcast — 兒童英文閱讀聽力練習。透過 GitHub Pages 託管靜態 RSS feed，供 Podcast App 訂閱收聽。

## 環境設置

```bash
pip install -r requirements.txt
```

## 使用方式

### 產生音檔（從故事文字）

```bash
cd reading_plus
python generate_audio.py
```

### 產生 Podcast 靜態站點

```bash
python podcast/generate_feed.py
```

產出目錄 `docs/` 包含：
- `feed.xml` — Podcast RSS feed
- `index.html` — 簡易首頁
- `cover.jpg` — 封面圖
- `audio/` — MP3 音檔

### 訂閱

在 Podcast App 中以 RSS URL 訂閱：

```
https://huansbox.github.io/aiden-english/feed.xml
```

## 新增集數

1. 將新故事的 `.md` 檔放入 `reading_plus/`
2. 執行 `cd reading_plus && python generate_audio.py` 產生 MP3
3. 執行 `python podcast/generate_feed.py` 重新生成 docs/
4. `git add docs/ && git commit -m "feat: add new episodes" && git push`
