"""Podcast RSS feed generator.

Scans reading_plus/audio/*.mp3, generates docs/ static site:
  - docs/feed.xml       (Apple Podcast compatible RSS)
  - docs/index.html     (simple episode listing)
  - docs/audio/*.mp3    (copied from reading_plus/audio/)
  - docs/cover.jpg      (resized from reading_plus/94.jpg)
"""

import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────

BASE_URL = "https://huansbox.github.io/aiden-english"
PODCAST_TITLE = "Aiden English Reading"
PODCAST_DESC = "兒童英文閱讀聽力練習"
PODCAST_AUTHOR = "Aiden's Dad"
PODCAST_LANGUAGE = "en-us"
PODCAST_CATEGORY = "Education"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
READING_PLUS = PROJECT_ROOT / "reading_plus"
AUDIO_SRC = READING_PLUS / "audio"
COVER_SRC = READING_PLUS / "94.jpg"
DOCS_DIR = PROJECT_ROOT / "docs"
AUDIO_DST = DOCS_DIR / "audio"

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"

# edge-tts outputs ~48kbps; used for duration estimation
BITRATE_BPS = 48000


# ── Helpers ─────────────────────────────────────────────────────────

def read_title_from_md(episode_num: int, stem: str) -> str:
    """Read real title from the corresponding .md file's first heading, prefixed with page number."""
    md_path = READING_PLUS / f"{stem}.md"
    if md_path.exists():
        first_line = md_path.read_text(encoding="utf-8").split("\n", 1)[0]
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            return f"{episode_num}. {title}"
    # Fallback: derive from filename
    parts = stem.split("_", 1)
    raw_title = parts[1] if len(parts) > 1 else f"Episode {episode_num}"
    return f"{episode_num}. {raw_title.replace('_', ' ').title()}"


def parse_episode(mp3_path: Path) -> dict:
    """Parse episode metadata from filename like '94_the_skunks_present.mp3'."""
    stem = mp3_path.stem  # e.g. '94_the_skunks_present'
    episode_num = int(stem.split("_", 1)[0])
    title = read_title_from_md(episode_num, stem)

    file_size = mp3_path.stat().st_size
    duration_secs = int(file_size / (BITRATE_BPS / 8))
    minutes, seconds = divmod(duration_secs, 60)
    duration_str = f"{minutes}:{seconds:02d}"

    return {
        "number": episode_num,
        "title": title,
        "filename": mp3_path.name,
        "file_size": file_size,
        "duration": duration_str,
    }


def build_feed(episodes: list[dict]) -> str:
    """Build RSS XML string for the podcast feed."""
    ET.register_namespace("itunes", ITUNES_NS)

    rss = ET.Element("rss", version="2.0")

    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = PODCAST_TITLE
    ET.SubElement(channel, "link").text = f"{BASE_URL}/"
    ET.SubElement(channel, "description").text = PODCAST_DESC
    ET.SubElement(channel, "language").text = PODCAST_LANGUAGE
    ET.SubElement(channel, f"{{{ITUNES_NS}}}author").text = PODCAST_AUTHOR
    ET.SubElement(channel, f"{{{ITUNES_NS}}}image").set(
        "href", f"{BASE_URL}/cover.jpg"
    )
    cat = ET.SubElement(channel, f"{{{ITUNES_NS}}}category")
    cat.set("text", PODCAST_CATEGORY)
    ET.SubElement(channel, f"{{{ITUNES_NS}}}explicit").text = "false"

    # Sort episodes by number (newest first in feed)
    sorted_eps = sorted(episodes, key=lambda e: e["number"])
    # Assign pubDate: earliest episode gets base_date, each subsequent +1 day
    base_date = datetime(2026, 3, 9, 8, 0, 0, tzinfo=timezone.utc)
    for i, ep in enumerate(sorted_eps):
        ep["pub_date"] = base_date + timedelta(days=i)

    for ep in reversed(sorted_eps):
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = ep["title"]

        enclosure = ET.SubElement(item, "enclosure")
        enclosure.set("url", f"{BASE_URL}/audio/{ep['filename']}")
        enclosure.set("length", str(ep["file_size"]))
        enclosure.set("type", "audio/mpeg")

        ET.SubElement(item, "guid").text = f"episode-{ep['number']}"
        ET.SubElement(item, "pubDate").text = ep["pub_date"].strftime(
            "%a, %d %b %Y %H:%M:%S +0000"
        )
        ET.SubElement(item, f"{{{ITUNES_NS}}}duration").text = ep["duration"]
        ET.SubElement(item, f"{{{ITUNES_NS}}}episode").text = str(ep["number"])

    ET.indent(rss, space="  ")
    xml_bytes = ET.tostring(rss, encoding="unicode", xml_declaration=False)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_bytes + "\n"


def build_index_html(episodes: list[dict]) -> str:
    """Build a simple HTML page listing all episodes."""
    rows = ""
    for ep in sorted(episodes, key=lambda e: e["number"]):
        rows += (
            f'      <tr><td>{ep["number"]}</td>'
            f'<td>{ep["title"]}</td>'
            f'<td>{ep["duration"]}</td>'
            f'<td><audio controls preload="none">'
            f'<source src="audio/{ep["filename"]}" type="audio/mpeg">'
            f"</audio></td></tr>\n"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{PODCAST_TITLE}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 2rem auto; padding: 0 1rem; }}
    h1 {{ font-size: 1.4rem; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: 0.5rem; border-bottom: 1px solid #eee; }}
    audio {{ width: 200px; height: 32px; }}
    .subscribe {{ margin: 1rem 0; padding: 0.7rem 1.2rem; background: #7c3aed; color: white;
                  border: none; border-radius: 6px; font-size: 0.9rem; cursor: pointer; }}
    .subscribe:hover {{ background: #6d28d9; }}
    .feed-url {{ font-size: 0.85rem; color: #666; word-break: break-all; }}
  </style>
</head>
<body>
  <h1>{PODCAST_TITLE}</h1>
  <p>{PODCAST_DESC}</p>
  <p>
    <button class="subscribe" onclick="navigator.clipboard.writeText('{BASE_URL}/feed.xml').then(()=>alert('RSS URL copied!'))">
      Copy RSS URL
    </button>
  </p>
  <p class="feed-url">{BASE_URL}/feed.xml</p>
  <table>
    <thead><tr><th>#</th><th>Title</th><th>Duration</th><th>Play</th></tr></thead>
    <tbody>
{rows}    </tbody>
  </table>
</body>
</html>
"""


# ── Main ────────────────────────────────────────────────────────────

def main():
    # Ensure output dirs exist
    DOCS_DIR.mkdir(exist_ok=True)
    AUDIO_DST.mkdir(exist_ok=True)

    # Copy MP3 files (only if newer or missing)
    mp3_files = sorted(AUDIO_SRC.glob("*.mp3"))
    if not mp3_files:
        print("No MP3 files found in", AUDIO_SRC)
        return

    for mp3 in mp3_files:
        dst = AUDIO_DST / mp3.name
        if not dst.exists() or mp3.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(mp3, dst)
            print(f"  Copied: {mp3.name}")

    # Copy cover image
    cover_dst = DOCS_DIR / "cover.jpg"
    if COVER_SRC.exists():
        shutil.copy2(COVER_SRC, cover_dst)
        print(f"  Cover:  {COVER_SRC.name} -> cover.jpg")
    else:
        print(f"  Warning: cover source not found at {COVER_SRC}")

    # Parse episodes
    episodes = [parse_episode(mp3) for mp3 in mp3_files]
    print(f"\n  Found {len(episodes)} episodes:")
    for ep in sorted(episodes, key=lambda e: e["number"]):
        print(f"    #{ep['number']:>3d}  {ep['title']}  ({ep['duration']})")

    # Generate feed.xml
    feed_xml = build_feed(episodes)
    (DOCS_DIR / "feed.xml").write_text(feed_xml, encoding="utf-8")
    print(f"\n  Generated: docs/feed.xml")

    # Generate index.html
    index_html = build_index_html(episodes)
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  Generated: docs/index.html")

    print("\nDone! Static site ready in docs/")


if __name__ == "__main__":
    main()
