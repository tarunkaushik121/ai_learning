
from langchain_core.retrievers import BaseRetriever

from app.rag.vector_store import load_vector_store


def get_retriever(
    top_k: int = 3
) -> BaseRetriever:

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    vector_store = load_vector_store()

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )


def retrieve_documents(
    question: str,
    top_k: int = 3
):
    retriever = get_retriever(top_k)

    return retriever.invoke(question)


def main():
    question = "What are default methods in Java?"

    documents = retrieve_documents(question)

    for index, document in enumerate(
        documents,
        start=1
    ):
        print(f"\nResult {index}")
        print(document.page_content)


if __name__ == "__main__":
    main()
