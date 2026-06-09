import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path("documents/chunks.jsonl")
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "unofficial_guide"


def main():
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError("documents/chunks.jsonl not found. Run src/chunk.py first.")

    chunks = []
    with CHUNKS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    if not chunks:
        raise ValueError("No chunks found in documents/chunks.jsonl")

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print(f"Loaded {len(documents)} chunks.")
    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating embeddings...")
    embeddings = model.encode(documents).tolist()

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete old collection so reruns do not duplicate stale chunks.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {len(documents)} chunks in ChromaDB collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    main()