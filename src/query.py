import os
from dotenv import load_dotenv
from groq import Groq

from src.retrieve import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask(question: str):
    retrieved_chunks = retrieve(question, k=3)

    context_blocks = []
    sources = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        source_label = f'{chunk["source"]}, chunk {chunk["chunk_index"]}'
        sources.append(source_label)

        context_blocks.append(
            f"[Source {i}: {source_label}]\n{chunk['text']}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are a grounded question-answering assistant for student reviews of SJSU Computer Science professors.

Use only the source context below to answer the user's question.

Rules:
1. Do not use outside knowledge.
2. Do not guess or infer beyond the provided reviews.
3. If the source context does not contain enough information, say:
   "I don't have enough information from the provided documents to answer that."
4. Mention the relevant source filename in your answer.

Source context:
{context}

User question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


if __name__ == "__main__":
    question = input("Ask a question: ")
    result = ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print("-", source)