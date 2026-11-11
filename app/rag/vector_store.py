
from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.rag.document_loader import (
    load_documents,
    split_documents,
)
from app.rag.embedding_service import get_embedding_model


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_STORE_PATH = (
    PROJECT_ROOT / "data" / "vector_store" / "faiss_index"
)


def build_vector_store() -> FAISS:
    """
    Load documents, create chunks, generate embeddings,
    and build a FAISS vector index.
    """

    documents = load_documents()
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("No document chunks found")

    embeddings = get_embedding_model()

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vector_store


def save_vector_store(vector_store: FAISS) -> None:
    """
    Persist the FAISS index to local disk.
    """

    VECTOR_STORE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    vector_store.save_local(
        str(VECTOR_STORE_PATH)
    )

    print(
        f"FAISS index saved to: {VECTOR_STORE_PATH}"
    )


def load_vector_store() -> FAISS:
    """
    Load a previously created FAISS index.

    Only load indexes created by this application
    from a trusted local directory.
    """

    embeddings = get_embedding_model()

    return FAISS.load_local(
        str(VECTOR_STORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def main():
    vector_store = build_vector_store()

    save_vector_store(vector_store)

    print("Vector store created successfully!")


if __name__ == "__main__":
    main()
