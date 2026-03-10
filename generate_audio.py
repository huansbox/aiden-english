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
