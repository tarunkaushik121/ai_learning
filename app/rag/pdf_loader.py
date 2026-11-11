
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


def load_pdf(pdf_path: str):
    path = Path(pdf_path).resolve()

    if not path.is_file():
        raise FileNotFoundError(
            f"PDF file not found: {path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")

    loader = PyPDFLoader(
        file_path=str(path),
        mode="page"
    )

    documents = loader.load()

    if not documents:
        raise ValueError("PDF contains no pages")

    print(f"Loaded {len(documents)} PDF pages")

    return documents


def split_pdf_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True
    )

    chunks = splitter.split_documents(documents)

    chunks = [
        chunk for chunk in chunks
        if chunk.page_content.strip()
    ]

    if not chunks:
        raise ValueError(
            "No extractable text found in PDF"
        )

    print(f"Created {len(chunks)} PDF chunks")

    return chunks
