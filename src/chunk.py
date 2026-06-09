from pathlib import Path
import json
import re

CLEAN_DIR = Path("documents/clean")
CHUNKS_PATH = Path("documents/chunks.jsonl")


def split_reviews(text: str):
    """
    Split a professor document into chunks by Review sections.
    This keeps each review together instead of cutting in the middle of words.
    """
    professor_match = re.search(r"Professor:\s*(.+)", text)
    professor = professor_match.group(1).strip() if professor_match else "Unknown"

    source_url_match = re.search(r"Source URL:\s*(.+)", text)
    source_url = source_url_match.group(1).strip() if source_url_match else "Unknown"

    parts = re.split(r"(?=Review\s+\d+:)", text)

    header = parts[0].strip()
    review_parts = [p.strip() for p in parts[1:] if p.strip()]

    chunks = []

    for review in review_parts:
        chunk = f"Professor: {professor}\nSource URL: {source_url}\n\n{review}"
        chunks.append(chunk)

    # Fallback: if no Review sections found, keep the full document.
    if not chunks and text.strip():
        chunks.append(text.strip())

    return chunks


def main():
    files = list(CLEAN_DIR.glob("*.txt"))

    if not files:
        raise FileNotFoundError("No .txt files found in documents/clean. Run src/ingest.py first.")

    total_chunks = 0

    with CHUNKS_PATH.open("w", encoding="utf-8") as f:
        for path in files:
            text = path.read_text(encoding="utf-8")
            chunks = split_reviews(text)

            for i, chunk in enumerate(chunks):
                record = {
                    "id": f"{path.stem}_{i}",
                    "source": path.name,
                    "chunk_index": i,
                    "text": chunk,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                total_chunks += 1

    print(f"Wrote {total_chunks} chunks to {CHUNKS_PATH}")


if __name__ == "__main__":
    main()