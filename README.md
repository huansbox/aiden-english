# Aiden English Reading

兒童英文閱讀聽力練習。兩種內容：Reading Plus 課本故事 + AI 改寫新聞文章。

## 環境設置

```bash
pip install -r requirements.txt
```

需要 Python 3.10 以上。Windows 環境執行時建議加 `PYTHONIOENCODING=utf-8`。

## 學習流程

1. **讀文章**：課本或列印文章（[Articles](https://huansbox.github.io/aiden-english/articles/)）
2. **聽音檔**：Podcast App 訂閱收聽
3. **做練習**：平板瀏覽器做互動練習題（[Exercises](https://huansbox.github.io/aiden-english/exercises/)）

## Podcast

RSS URL：`https://huansbox.github.io/aiden-english/feed.xml`

| Season | 內容 |
|--------|------|
| Season 1 | Reading Plus 課本故事 |
| Season 2 | News & Articles（改寫新聞） |

- **Apple Podcasts**：資料庫 → ... → 透過 URL 追蹤節目 → 貼上 RSS URL
- **Pocket Casts**：搜尋 → Submit RSS URL → 貼上

## 產生音檔與 Feed

```bash
# Reading Plus 音檔
python generate_audio.py reading_plus

# 文章音檔
python generate_audio.py articles

# 產生 Podcast feed（掃描所有來源）
python podcast/generate_feed.py

# 推送
git add docs/ && git commit -m "feat: add new episodes" && git push
```

## 目前內容

### Season 1: Reading Plus

| # | 故事 | 練習 |
|---|------|------|
| 94/95 | The Skunks' Present | v2 |
| 96/97 | Make Way for Betsy | v2 |
| 98/99 | A Narrow Escape | v2 |
| 100/101 | The String House | v2 |
| 102/103 | Breakfast with Barnie | v2 |

### Season 2: News & Articles

| 文章 | 篇數 | 練習 |
|------|------|------|
| WBC 2026: Chinese Taipei vs Korea | 3 parts | v2 |
