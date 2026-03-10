"""Podcast RSS feed generator with Season support.

Scans multiple audio sources, generates docs/ static site:
  - docs/feed.xml       (Apple Podcast compatible RSS with itunes:season)
  - docs/audio/*.mp3    (copied from all sources)
  - docs/cover.jpg      (resized from reading_plus/94.jpg)

Season 1: Reading Plus (textbook stories)
Season 2: News & Articles (AI-rewritten news)
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
NEWS_DIR = READING_PLUS / "news"
COVER_SRC = READING_PLUS / "94.jpg"
DOCS_DIR = PROJECT_ROOT / "docs"
AUDIO_DST = DOCS_DIR / "audio"

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"

# edge-tts outputs ~48kbps; used for duration estimation
BITRATE_BPS = 48000


# ── Episode Parsing ────────────────────────────────────────────────

def read_md_title(md_path: Path) -> str | None:
    """Read H1 title from a markdown file."""
    if md_path.exists():
        first_line = md_path.read_text(encoding="utf-8").split("\n", 1)[0]
        if first_line.startswith("# "):
            return first_line[2:].strip()
    return None


def estimate_duration(mp3_path: Path) -> str:
    """Estimate MP3 duration from file size."""
    file_size = mp3_path.stat().st_size
    duration_secs = int(file_size / (BITRATE_BPS / 8))
    minutes, seconds = divmod(duration_secs, 60)
    return f"{minutes}:{seconds:02d}"


def parse_reading_plus_episodes() -> list[dict]:
    """Parse Season 1 episodes from reading_plus/audio/*.mp3."""
    audio_dir = READING_PLUS / "audio"
    if not audio_dir.exists():
        return []

    episodes = []
    for mp3 in sorted(audio_dir.glob("*.mp3")):
        stem = mp3.stem  # e.g. '94_the_skunks_present'
        episode_num = int(stem.split("_", 1)[0])

        md_path = READING_PLUS / f"{stem}.md"
        md_title = read_md_title(md_path)
        if md_title:
            title = f"{episode_num}. {md_title}"
        else:
            parts = stem.split("_", 1)
            raw_title = parts[1] if len(parts) > 1 else f"Episode {episode_num}"
            title = f"{episode_num}. {raw_title.replace('_', ' ').title()}"

        episodes.append({
            "season": 1,
            "number": episode_num,
            "title": title,
            "filename": mp3.name,
            "file_size": mp3.stat().st_size,
            "duration": estimate_duration(mp3),
            "src_path": mp3,
        })

    return episodes


def parse_news_episodes() -> list[dict]:
    """Parse Season 2 episodes from reading_plus/news/audio/*.mp3."""
    audio_dir = NEWS_DIR / "audio"
    if not audio_dir.exists():
        return []

    episodes = []
    for i, mp3 in enumerate(sorted(audio_dir.glob("*.mp3")), start=1):
        stem = mp3.stem  # e.g. 'wbc_part1_the_big_game'

        md_path = NEWS_DIR / f"{stem}.md"
        md_title = read_md_title(md_path)
        title = md_title if md_title else stem.replace("_", " ").title()

        episodes.append({
            "season": 2,
            "number": i,
            "title": title,
            "filename": mp3.name,
            "file_size": mp3.stat().st_size,
            "duration": estimate_duration(mp3),
            "src_path": mp3,
        })

    return episodes


# ── Feed Builder ───────────────────────────────────────────────────

def build_feed(episodes: list[dict]) -> str:
    """Build RSS XML string with itunes:season support."""
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
    ET.SubElement(channel, f"{{{ITUNES_NS}}}type").text = "serial"

    # Sort: Season 1 first (by number), then Season 2 (by number)
    sorted_eps = sorted(episodes, key=lambda e: (e["season"], e["number"]))

    # Assign pubDate: all episodes sequentially, +1 day each
    base_date = datetime(2026, 3, 9, 8, 0, 0, tzinfo=timezone.utc)
    for i, ep in enumerate(sorted_eps):
        ep["pub_date"] = base_date + timedelta(days=i)

    # Output newest first
    for ep in reversed(sorted_eps):
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = ep["title"]

        enclosure = ET.SubElement(item, "enclosure")
        enclosure.set("url", f"{BASE_URL}/audio/{ep['filename']}")
        enclosure.set("length", str(ep["file_size"]))
        enclosure.set("type", "audio/mpeg")

        ET.SubElement(item, "guid").text = f"s{ep['season']}-e{ep['number']}"
        ET.SubElement(item, "pubDate").text = ep["pub_date"].strftime(
            "%a, %d %b %Y %H:%M:%S +0000"
        )
        ET.SubElement(item, f"{{{ITUNES_NS}}}duration").text = ep["duration"]
        ET.SubElement(item, f"{{{ITUNES_NS}}}season").text = str(ep["season"])
        ET.SubElement(item, f"{{{ITUNES_NS}}}episode").text = str(ep["number"])

    ET.indent(rss, space="  ")
    xml_bytes = ET.tostring(rss, encoding="unicode", xml_declaration=False)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_bytes + "\n"


# ── Main ────────────────────────────────────────────────────────────

def main():
    DOCS_DIR.mkdir(exist_ok=True)
    AUDIO_DST.mkdir(exist_ok=True)

    # Collect episodes from all sources
    all_episodes = parse_reading_plus_episodes() + parse_news_episodes()

    if not all_episodes:
        print("No MP3 files found.")
        return

    # Copy MP3 files (only if newer or missing)
    for ep in all_episodes:
        dst = AUDIO_DST / ep["filename"]
        src = ep["src_path"]
        if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
            shutil.copy2(src, dst)
            print(f"  Copied: {ep['filename']}")

    # Copy cover image
    cover_dst = DOCS_DIR / "cover.jpg"
    if COVER_SRC.exists():
        shutil.copy2(COVER_SRC, cover_dst)

    # Print summary
    for season_num in sorted(set(ep["season"] for ep in all_episodes)):
        season_eps = [ep for ep in all_episodes if ep["season"] == season_num]
        season_name = "Reading Plus" if season_num == 1 else "News & Articles"
        print(f"\n  Season {season_num}: {season_name} ({len(season_eps)} episodes)")
        for ep in sorted(season_eps, key=lambda e: e["number"]):
            print(f"    #{ep['number']:>3d}  {ep['title']}  ({ep['duration']})")

    # Generate feed.xml (does NOT touch index.html — manually maintained)
    feed_xml = build_feed(all_episodes)
    (DOCS_DIR / "feed.xml").write_text(feed_xml, encoding="utf-8")
    print(f"\n  Generated: docs/feed.xml")

    print("\nDone!")


if __name__ == "__main__":
    main()
