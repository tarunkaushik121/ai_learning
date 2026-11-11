
from typing import Any

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from app.llm.model import get_chat_model
from app.rag.rag_prompt import RAG_PROMPT
from app.rag.retriever_service import get_retriever


NO_CONTEXT_RESPONSE = (
    "I don't have enough information in the "
    "provided documents to answer that question."
)


def format_documents(documents: list[Document]) -> str:
    """
    Convert retrieved documents into text
    suitable for the LLM prompt.
    """

    formatted_chunks = []

    for index, document in enumerate(
        documents,
        start=1
    ):
        source = document.metadata.get(
            "source",
            "unknown"
        )

        formatted_chunks.append(
            f"[Document {index}]\n"
            f"Source: {source}\n"
            f"Content:\n{document.page_content}"
        )

    return "\n\n".join(formatted_chunks)


def answer_with_rag(
    question: str,
    top_k: int = 3
) -> dict[str, Any]:
    """
    Retrieve relevant documents and generate
    a grounded answer using the LLM.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty")

    retriever = get_retriever(top_k=top_k)

    documents = retriever.invoke(question)

    if not documents:
        return {
            "question": question,
            "answer": NO_CONTEXT_RESPONSE,
            "sources": [],
            "retrieved_chunks": 0
        }

    context = format_documents(documents)

    llm = get_chat_model()

    chain = (
        RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke({
        "context": context,
        "question": question
    })

    sources = list(dict.fromkeys(
        document.metadata.get("source", "unknown")
        for document in documents
    ))

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": len(documents)
    }
