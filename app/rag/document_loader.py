
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENT_PATH = (
    PROJECT_ROOT / "data" / "knowledge" / "java8.txt"
)


def load_documents():
    loader = TextLoader(
        str(DOCUMENT_PATH),
        encoding="utf-8"
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} document(s)")

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    return chunks


def main():
    documents = load_documents()

    chunks = split_documents(documents)

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n========== CHUNK {index} ==========")
        print(chunk.page_content)
        print("Metadata:", chunk.metadata)


if __name__ == "__main__":
    main()
