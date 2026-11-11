
import numpy as np

from app.rag.document_loader import (
    load_documents,
    split_documents,
)
from app.rag.embedding_service import (
    get_embedding_model,
)


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float]
) -> float:

    a = np.array(vector_a, dtype=float)
    b = np.array(vector_b, dtype=float)

    denominator = (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def main():
    documents = load_documents()
    chunks = split_documents(documents)

    embeddings = get_embedding_model()

    # Embed all document chunks in one batch.
    document_vectors = embeddings.embed_documents(
        [chunk.page_content for chunk in chunks]
    )

    question = (
        "How do lambda expressions work in Java?"
    )

    query_vector = embeddings.embed_query(question)

    results = []

    for chunk, vector in zip(
        chunks,
        document_vectors
    ):
        score = cosine_similarity(
            query_vector,
            vector
        )

        results.append((score, chunk))

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    print("\nUSER QUESTION:")
    print(question)

    print("\nTOP 3 RELEVANT CHUNKS:")

    for rank, (score, chunk) in enumerate(
        results[:3],
        start=1
    ):
        print(f"\nResult {rank}")
        print(f"Similarity: {score:.4f}")
        print("Content:", chunk.page_content)


if __name__ == "__main__":
    main()
