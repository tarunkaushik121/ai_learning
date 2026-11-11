
from app.rag.rag_service import answer_with_rag


def run_rag_cli():
    print("\n========== JAVA RAG ASSISTANT ==========")
    print("Ask questions about the Java knowledge document.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            question = input("Your question: ").strip()

            if question.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not question:
                print("Please enter a question.")
                continue

            print("\nSearching knowledge base...")

            result = answer_with_rag(question)

            print("\n---------- AI ANSWER ----------")
            print(result["answer"])

            print("\n---------- SOURCES ----------")
            for source in result["sources"]:
                print(f"- {source}")

            print(
                f"\nRetrieved chunks: "
                f"{result['retrieved_chunks']}"
            )

            print("\n" + "=" * 45 + "\n")

        except KeyboardInterrupt:
            print("\nSession ended.")
            break

        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    run_rag_cli()
