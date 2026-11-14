
from langchain_core.documents import Document

from app.tools import pdf_tools
from app.tools.interview_tools import create_interview_tools


class FakeStore:
    def similarity_search(self, query, k):
        return [
            Document(
                page_content="Optional represents an optional value.",
                metadata={"page": 2},
            )
        ]


def test_pdf_search_tool(monkeypatch):
    monkeypatch.setattr(
        pdf_tools,
        "load_pdf_index",
        lambda index_id: FakeStore(),
    )

    tools = pdf_tools.create_pdf_tools("test-index")

    result = tools[0].invoke({
        "query": "What is Optional?"
    })

    assert "Page 3" in result
    assert "Optional" in result


def test_interview_summary_tool():
    report = {
        "average_score": 8.0,
        "evaluations": [
            {
                "question": "What is Optional?",
                "evaluation": {
                    "score": 8,
                    "feedback": "Good explanation.",
                },
            }
        ],
    }

    tool = create_interview_tools(report)[0]

    result = tool.invoke({})

    assert "8.0/10" in result
    assert "Good explanation" in result
