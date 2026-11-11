
from pathlib import Path
from uuid import uuid4

from langchain_community.vectorstores import FAISS

from app.rag.embedding_service import get_embedding_model
from app.rag.pdf_loader import (
    load_pdf,
    split_pdf_documents,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PDF_INDEX_ROOT = (
    PROJECT_ROOT / "data" / "vector_store" / "pdfs"
)


def build_pdf_index(pdf_path: str) -> str:
    """
    Build a new FAISS index for one PDF.

    Returns a generated index identifier.
    """

    documents = load_pdf(pdf_path)

    chunks = split_pdf_documents(documents)

    embeddings = get_embedding_model()

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    index_id = str(uuid4())

    index_path = PDF_INDEX_ROOT / index_id
    index_path.mkdir(parents=True, exist_ok=False)

    vector_store.save_local(str(index_path))

    print(f"Index created: {index_id}")

    return index_id


def load_pdf_index(index_id: str) -> FAISS:
    """
    Load a trusted, locally generated PDF index.
    """

    from uuid import UUID

    validated_id = str(UUID(index_id))

    index_path = PDF_INDEX_ROOT / validated_id

    if not (index_path / "index.faiss").is_file():
        raise FileNotFoundError(
            f"PDF index not found: {validated_id}"
        )

    embeddings = get_embedding_model()

    return FAISS.load_local(
        str(index_path),
        embeddings,
        allow_dangerous_deserialization=True
    )
