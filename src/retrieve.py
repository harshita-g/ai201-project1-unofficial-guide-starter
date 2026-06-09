import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "unofficial_guide"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(COLLECTION_NAME)


def retrieve(query: str, k: int = 3):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )

    retrieved = []

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append(
            {
                "text": doc,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "distance": distance,
            }
        )

    return retrieved


def main():
    query = input("Ask a question: ")
    results = retrieve(query)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("SOURCE:", result["source"])
        print("CHUNK INDEX:", result["chunk_index"])
        print("DISTANCE:", result["distance"])
        print(result["text"])
        print("-" * 80)


if __name__ == "__main__":
    main()