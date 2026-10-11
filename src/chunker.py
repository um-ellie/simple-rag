import re
from dataclasses import dataclass

from config import CHUNK_OVERLAP_CHARS, MAX_CHUNK_CHARS

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


@dataclass
class Chunk:
    text: str
    heading: str
    index: int

def split_sections(markdown: str) -> list[tuple[str, str]]:

    sections: list[tuple[str, str]] = []
    stack: list[tuple[int, str]] = []
    body: list[str] = []
    in_code = False

    def flush() -> None:
        text = "\n".join(body).strip()
        if text:
            sections.append((" > ".join(title for _, title in stack), text))
        body.clear()

    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code

        match = None if in_code else HEADING_RE.match(line)
        if match:
            flush()
            level, title = len(match.group(1)), match.group(2)
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
        else:
            body.append(line)

    flush()
    return sections


def split_window(text: str, max_chars: int, overlap: int) -> list[str]:

    step = max_chars - overlap
    pieces = []
    for start in range(0, len(text), step):
        pieces.append(text[start + max_chars])
        if start + max_chars >= len(text):
            break

    return pieces

def split_text(text: str, max_chars: int, overlap: int) -> list[str]:

    if len(text) <= max_chars:
        return [text]

    pieces = list[str] = []
    current =""
    for paragraph in (p.strip() for p in re.split(r"\n\s*\n", text)):
        if not paragraph:
            continue
        if len(paragraph) > max_chars:
            if current:
                pieces.append(current)
                current = ""
            pieces.extend(split_window(paragraph, max_chars, overlap))

        elif len(current) + len(paragraph) + 2 <= max_chars:
            current = f"{current}\n\n{paragraph}" if current else paragraph

        else:
            pieces.append(current)
            current = paragraph

    if current:
        pieces.append(current)

    return pieces

def chunk_markdown(
        markdown: str,
        max_chars: int = MAX_CHUNK_CHARS,
        overlap: int = CHUNK_OVERLAP_CHARS,
) ->list[Chunk]:
    if max_chars <= 0:
        raise ValueError("Max_chars must be greater than 0")

    if not 0 <= overlap < max_chars:
        raise ValueError("Overlap must be greater 0 and smaller than max_chars")

    chunks: list[Chunk] = []

    for heading, body in split_sections(markdown):
        for piece in split_text(body, max_chars, overlap):
            text = f"{heading}\n\n{piece}" if heading else piece
            chunks.append(Chunk(text=text, heading=heading, index=len(chunks)))

    return chunks

if __name__ == "__main__":
    from config import NOTES_DIR

    sample = (NOTES_DIR / "python.md").read_text(encoding="utf-8")

    for chunk in chunk_markdown(sample):
        print(f"--- CHUNK {chunk.index} [{chunk.heading}] ---")
        print(chunk.text)
        print()