from pathlib import Path
import html
import re

RAW_DIR = Path("documents/raw")
CLEAN_DIR = Path("documents/clean")

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\xa0", " ")

    # Remove extra spaces but preserve line breaks
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)

    cleaned = "\n".join(lines)

    # Collapse excessive blank lines/spaces
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    return cleaned


def main():
    files = list(RAW_DIR.glob("*.txt"))

    if not files:
        raise FileNotFoundError("No .txt files found in documents/raw")

    for path in files:
        raw_text = path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        output_path = CLEAN_DIR / path.name
        output_path.write_text(cleaned_text, encoding="utf-8")

        print(f"Cleaned {path.name} -> {output_path}")

    print(f"Processed {len(files)} files.")


if __name__ == "__main__":
    main()