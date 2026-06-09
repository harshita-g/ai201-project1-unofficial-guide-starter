from pathlib import Path
import json
import random

CHUNKS_PATH = Path("documents/chunks.jsonl")


def main():
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError("documents/chunks.jsonl not found. Run src/chunk.py first.")

    with CHUNKS_PATH.open("r", encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]

    print(f"Total chunks: {len(chunks)}")
    print()

    sample_size = min(5, len(chunks))

    for chunk in random.sample(chunks, sample_size):
        print("SOURCE:", chunk["source"])
        print("CHUNK INDEX:", chunk["chunk_index"])
        print(chunk["text"])
        print("-" * 80)


if __name__ == "__main__":
    main()