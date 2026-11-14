
from pathlib import Path
from uuid import uuid4

from app.agents.pdf_react_agent import build_pdf_react_agent
from app.rag.pdf_indexer import build_pdf_index


DEFAULT_PDF = "data/pdfs/java_interview_notes.pdf"


def main():
    print("\n================================")
    print(" AI INTERVIEW ASSISTANT")
    print(" ReAct Agent + PDF RAG")
    print("================================\n")

    pdf_path = input(
        f"Enter PDF path [{DEFAULT_PDF}]: "
    ).strip() or DEFAULT_PDF

    if not Path(pdf_path).is_file():
        print(f"PDF not found: {pdf_path}")
        return

    print("\nIndexing PDF...")
    index_id = build_pdf_index(pdf_path)

    print("Creating ReAct agent...")
    agent = build_pdf_react_agent(index_id)

    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        },
        "recursion_limit": 20,
    }

    print(f"\nSession ID: {thread_id}")
    print("Agent ready! Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        try:
            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question,
                        }
                    ]
                },
                config=config,
            )

            answer = result["messages"][-1].content

            print(f"\nAssistant: {answer}\n")

        except Exception as exc:
            print(
                f"\nError: {type(exc).__name__}: {exc}\n"
            )


if __name__ == "__main__":
    main()
