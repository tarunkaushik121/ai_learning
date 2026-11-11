
from langchain_core.documents import Document

from app.rag import rag_service


class FakeRetriever:
    def invoke(self, question):
        return [
            Document(
                page_content=(
                    "A functional interface contains "
                    "exactly one abstract method."
                ),
                metadata={"source": "java8.txt"}
            )
        ]


class FakeChain:
    def invoke(self, inputs):
        assert "functional interface" in inputs["context"]
        return "A functional interface has one abstract method."


class FakePrompt:
    def __or__(self, other):
        return self


def test_answer_with_rag(monkeypatch):
    monkeypatch.setattr(
        rag_service,
        "get_retriever",
        lambda top_k: FakeRetriever()
    )

    monkeypatch.setattr(
        rag_service,
        "get_chat_model",
        lambda: object()
    )

    monkeypatch.setattr(
        rag_service,
        "RAG_PROMPT",
        FakePrompt()
    )

    monkeypatch.setattr(
        rag_service,
        "StrOutputParser",
        lambda: FakeChain()
    )

    result = rag_service.answer_with_rag(
        "What is a functional interface?"
    )

    assert result["retrieved_chunks"] == 1
    assert result["sources"] == ["java8.txt"]
    assert "one abstract method" in result["answer"]
