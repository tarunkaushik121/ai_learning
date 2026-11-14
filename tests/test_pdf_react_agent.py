
from unittest.mock import MagicMock

from langchain_core.documents import Document

from app.agents import pdf_react_agent


def test_agent_builds_with_pdf_tool(monkeypatch):
    fake_store = MagicMock()

    fake_store.similarity_search.return_value = [
        Document(
            page_content="CompletableFuture supports async tasks.",
            metadata={"page": 1},
        )
    ]

    fake_model = MagicMock()
    captured = {}

    def fake_create_agent(**kwargs):
        captured.update(kwargs)
        return "fake-agent"

    monkeypatch.setattr(
        pdf_react_agent,
        "load_pdf_index",
        lambda index_id: fake_store,
    )

    monkeypatch.setattr(
        pdf_react_agent,
        "get_chat_model",
        lambda: fake_model,
    )

    monkeypatch.setattr(
        pdf_react_agent,
        "create_agent",
        fake_create_agent,
    )

    result = pdf_react_agent.build_pdf_react_agent(
        "test-index"
    )

    assert result == "fake-agent"
    assert len(captured["tools"]) == 1

    tool = captured["tools"][0]

    response = tool.invoke({
        "query": "CompletableFuture"
    })

    assert "PDF Page 2" in response
    assert "async tasks" in response

    fake_store.similarity_search.assert_called_once_with(
        query="CompletableFuture",
        k=4,
    )


def test_empty_pdf_search_query(monkeypatch):
    fake_store = MagicMock()
    captured = {}

    monkeypatch.setattr(
        pdf_react_agent,
        "load_pdf_index",
        lambda index_id: fake_store,
    )

    monkeypatch.setattr(
        pdf_react_agent,
        "get_chat_model",
        lambda: MagicMock(),
    )

    monkeypatch.setattr(
        pdf_react_agent,
        "create_agent",
        lambda **kwargs: captured.update(kwargs),
    )

    pdf_react_agent.build_pdf_react_agent("test-index")

    tool = captured["tools"][0]

    result = tool.invoke({"query": " "})

    assert "nonempty search query" in result
    fake_store.similarity_search.assert_not_called()
