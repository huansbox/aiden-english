# Aiden English Reading — 私人 Podcast

## 架構

- `reading_plus/` — 故事原始素材（掃描圖 JPG、故事文字 MD、generate_audio.py 產生 MP3）
- `podcast/generate_feed.py` — RSS feed 生成器，掃描 MP3 → 輸出 docs/ 靜態站點
- `docs/` — GitHub Pages 來源目錄（feed.xml、index.html、cover.jpg、audio/*.mp3）

## 技術決策

- 託管：GitHub Pages（main branch /docs 目錄）
- RSS feed：Python 標準庫 xml.etree.ElementTree 生成，符合 Apple Podcast 規格
- MP3 duration：以檔案大小 ÷ 48kbps 估算（edge-tts 預設位元率）
- Base URL：https://huansbox.github.io/aiden-english/

## 工作流（新增音檔）

```bash
cd reading_plus && python generate_audio.py
cd .. && python podcast/generate_feed.py
git add docs/ && git commit -m "feat: add new episodes" && git push
```
