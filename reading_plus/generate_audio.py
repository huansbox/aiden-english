"""Generate MP3 audio files from markdown story files using edge-tts."""

import asyncio
import re
from pathlib import Path

import edge_tts

VOICE = "en-US-JennyNeural"
SCRIPT_DIR = Path(__file__).parent
AUDIO_DIR = SCRIPT_DIR / "audio"

MD_FILES = [
    "94_the_skunks_present.md",
    "96_make_way_for_betsy.md",
    "98_a_narrow_escape.md",
    "100_the_string_house.md",
    "102_breakfast_with_barnie.md",
]


def extract_text(md_path: Path) -> str:
    """Read markdown file and strip formatting to plain text."""
    raw = md_path.read_text(encoding="utf-8")
    # Remove H1 title line
    text = re.sub(r"^#\s+.*$", "", raw, flags=re.MULTILINE)
    # Remove bold markers
    text = text.replace("**", "")
    # Remove paragraph number prefixes like "1 ", "2 " at line start
    text = re.sub(r"(?m)^\d+\s+", "", text)
    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


async def generate_one(md_name: str) -> None:
    md_path = SCRIPT_DIR / md_name
    text = extract_text(md_path)
    out_path = AUDIO_DIR / md_name.replace(".md", ".mp3")

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(out_path))
    print(f"OK: {out_path.name}")


async def main():
    AUDIO_DIR.mkdir(exist_ok=True)
    for md_name in MD_FILES:
        await generate_one(md_name)
    print(f"\nDone. {len(MD_FILES)} files generated in {AUDIO_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
