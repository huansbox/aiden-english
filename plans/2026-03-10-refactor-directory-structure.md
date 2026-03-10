# Directory Structure Refactor

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restructure project directories to clearly separate two content pipelines and eliminate code duplication.

**Architecture:** Three changes — (1) move `reading_plus/news/` to root-level `articles/`, (2) move `.jpg` scans into `reading_plus/scans/`, (3) merge two identical `generate_audio.py` into one. Plus update all references in docs and scripts.

**Tech Stack:** Python, git mv, shell

---

## Summary of Changes

| What | Before | After |
|------|--------|-------|
| 文章素材 | `reading_plus/news/` | `articles/` (root) |
| 課本掃描圖 | `reading_plus/*.jpg` | `reading_plus/scans/*.jpg` |
| TTS 腳本 | 2 copies (`reading_plus/generate_audio.py` + `reading_plus/news/generate_audio.py`) | 1 copy at root (`generate_audio.py`) |
| 設計文檔 | `docs/plans/` (會被部署) | `plans/` (root, 不部署) |

---

### Task 1: Move `reading_plus/news/` → `articles/`

**Risk: Medium** — path references in 2 Python files + 2 doc files

**Step 1: Move the directory**

```bash
git mv reading_plus/news articles
```

This moves everything including `articles/audio/`, `articles/generate_audio.py`, and all `.md` files.

**Step 2: Update `podcast/generate_feed.py`**

Change line 28:
```python
# Before
NEWS_DIR = READING_PLUS / "news"

# After
ARTICLES_DIR = PROJECT_ROOT / "articles"
```

Change line 92-93 comment + variable:
```python
# Before
def parse_news_episodes() -> list[dict]:
    """Parse Season 2 episodes from reading_plus/news/audio/*.mp3."""
    audio_dir = NEWS_DIR / "audio"
    ...
    md_path = NEWS_DIR / f"{stem}.md"

# After
def parse_news_episodes() -> list[dict]:
    """Parse Season 2 episodes from articles/audio/*.mp3."""
    audio_dir = ARTICLES_DIR / "audio"
    ...
    md_path = ARTICLES_DIR / f"{stem}.md"
```

All 4 occurrences of `NEWS_DIR` → `ARTICLES_DIR`.

**Step 3: Commit**

```bash
git add -A
git commit -m "refactor: move reading_plus/news/ to articles/"
```

---

### Task 2: Move `.jpg` scans into `reading_plus/scans/`

**Risk: Low** — only `generate_feed.py` references `94.jpg` for cover

**Step 1: Create directory and move files**

```bash
mkdir -p reading_plus/scans
git mv reading_plus/94.jpg reading_plus/scans/
git mv reading_plus/95.jpg reading_plus/scans/
git mv reading_plus/96.jpg reading_plus/scans/
git mv reading_plus/97.jpg reading_plus/scans/
git mv reading_plus/98.jpg reading_plus/scans/
git mv reading_plus/99.jpg reading_plus/scans/
git mv reading_plus/100.jpg reading_plus/scans/
git mv reading_plus/101.jpg reading_plus/scans/
git mv reading_plus/102.jpg reading_plus/scans/
git mv reading_plus/103.jpg reading_plus/scans/
```

**Step 2: Update `podcast/generate_feed.py` cover path**

Change line 29:
```python
# Before
COVER_SRC = READING_PLUS / "94.jpg"

# After
COVER_SRC = READING_PLUS / "scans" / "94.jpg"
```

Also update the docstring (line 6):
```python
# Before
#   - docs/cover.jpg      (resized from reading_plus/94.jpg)
# After
#   - docs/cover.jpg      (copied from reading_plus/scans/94.jpg)
```

**Step 3: Commit**

```bash
git add -A
git commit -m "refactor: move scanned images to reading_plus/scans/"
```

---

### Task 3: Merge two `generate_audio.py` into one

**Risk: High** — must work correctly for both pipelines, auto-discover md files

**Step 1: Delete both old scripts**

```bash
git rm reading_plus/generate_audio.py
git rm articles/generate_audio.py
```

**Step 2: Create `generate_audio.py` at project root**

```python
"""Generate MP3 audio files from markdown files using edge-tts.

Usage:
    python generate_audio.py reading_plus    # Reading Plus textbook stories
    python generate_audio.py articles        # Rewritten articles
"""

import asyncio
import re
import sys
from pathlib import Path

import edge_tts

VOICE = "en-US-JennyNeural"
PROJECT_ROOT = Path(__file__).resolve().parent

SOURCES = {
    "reading_plus": PROJECT_ROOT / "reading_plus",
    "articles": PROJECT_ROOT / "articles",
}


def extract_text(md_path: Path) -> str:
    """Read markdown file and strip formatting to plain text."""
    raw = md_path.read_text(encoding="utf-8")
    text = re.sub(r"^#\s+.*$", "", raw, flags=re.MULTILINE)
    text = text.replace("**", "")
    text = re.sub(r"(?m)^\d+\s+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


async def generate_one(md_path: Path, out_path: Path) -> None:
    text = extract_text(md_path)
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(out_path))
    print(f"  OK: {out_path.name}")


async def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SOURCES:
        print(f"Usage: python {Path(__file__).name} <{'|'.join(SOURCES.keys())}>")
        sys.exit(1)

    source_name = sys.argv[1]
    source_dir = SOURCES[source_name]
    audio_dir = source_dir / "audio"
    audio_dir.mkdir(exist_ok=True)

    # Find all .md files in source_dir (not subdirectories)
    md_files = sorted(source_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {source_dir}")
        return

    print(f"Generating audio for {source_name} ({len(md_files)} files):")
    for md_path in md_files:
        out_path = audio_dir / md_path.with_suffix(".mp3").name
        await generate_one(md_path, out_path)

    print(f"\nDone. {len(md_files)} files in {audio_dir}")


if __name__ == "__main__":
    asyncio.run(main())
```

Key design decisions:
- Auto-discovers all `.md` files in the source directory (no manual `MD_FILES` list to maintain)
- Uses `source_dir.glob("*.md")` — non-recursive, won't pick up subdirectory files
- CLI argument selects source: `python generate_audio.py reading_plus` or `python generate_audio.py articles`
- Output goes to `{source_dir}/audio/`

**Step 3: Commit**

```bash
git add -A
git commit -m "refactor: merge two generate_audio.py into one at root"
```

---

### Task 4: Move `docs/plans/` → `plans/`

**Risk: Low** — these files are reference docs, not imported by any code

**Step 1: Move**

```bash
git mv docs/plans plans
```

**Step 2: Commit**

```bash
git add -A
git commit -m "refactor: move plans/ out of docs/ to avoid deploying"
```

---

### Task 5: Update documentation (CLAUDE.md + README.md)

**Risk: Medium** — must accurately reflect new structure

**Step 1: Update CLAUDE.md**

All path references need updating. Key changes:

| Old path | New path |
|----------|----------|
| `reading_plus/news/{topic}_*.md` | `articles/{topic}_*.md` |
| `reading_plus/news/audio/*.mp3` | `articles/audio/*.mp3` |
| `reading_plus/news/generate_audio.py` | `generate_audio.py articles` |
| `reading_plus/generate_audio.py` | `generate_audio.py reading_plus` |
| `docs/plans/exercise-v2-sop.md` | `plans/exercise-v2-sop.md` |
| `.jpg` files in reading_plus root | `reading_plus/scans/*.jpg` |

Update the directory tree in CLAUDE.md to:

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

plans/                          設計文檔（不部署）
├── exercise-v2-sop.md
└── *.md

docs/                           GitHub Pages 部署目錄
├── index.html
├── feed.xml
├── audio/                      所有 MP3（由 generate_feed.py 複製）
├── articles/                   可列印文章 HTML
└── exercises/                  互動練習題
```

Update the operation commands section:

```bash
# Reading Plus 音檔
python generate_audio.py reading_plus

# 文章音檔
python generate_audio.py articles

# Podcast feed
python podcast/generate_feed.py
```

**Step 2: Update README.md**

Same path changes. Update the "產生音檔與 Feed" section:

```bash
# Reading Plus 音檔
python generate_audio.py reading_plus

# 文章音檔
python generate_audio.py articles

# 產生 Podcast feed（掃描所有來源）
python podcast/generate_feed.py
```

**Step 3: Update cross-references in plan files**

In `plans/exercise-v2-sop.md` (already moved), update any `docs/plans/` self-references to `plans/`.

**Step 4: Commit**

```bash
git add -A
git commit -m "docs: update all path references after directory refactor"
```

---

### Task 6: Verify

**Step 1: Verify no broken references**

```bash
# Should return NO results for old paths
grep -r "reading_plus/news" --include="*.py" --include="*.md" --include="*.html" .
grep -r "reading_plus/.*\.jpg" --include="*.py" --include="*.md" . | grep -v scans
grep -r "docs/plans" --include="*.py" --include="*.md" --include="*.html" . | grep -v "\.git"
```

All three commands should return empty.

**Step 2: Verify generate_audio.py runs**

```bash
python generate_audio.py reading_plus 2>&1 | head -3
python generate_audio.py articles 2>&1 | head -3
```

Should list md files found (don't need to actually generate — just verify it finds files).

**Step 3: Verify generate_feed.py runs**

```bash
python podcast/generate_feed.py
```

Should complete without errors and show both Season 1 and Season 2 episodes.

**Step 4: Push**

```bash
git push
```
