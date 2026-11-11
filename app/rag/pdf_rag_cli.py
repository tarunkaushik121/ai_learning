
from pathlib import Path

from app.rag.pdf_indexer import build_pdf_index
from app.rag.pdf_rag_service import answer_from_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_pdf_interview_assistant():

    print("\n========== PDF RAG ASSISTANT ==========")

    pdf_input = input(
        "Enter PDF path: "
    ).strip().strip('"')

    pdf_path = Path(pdf_input)

    if not pdf_path.is_absolute():
        pdf_path = PROJECT_ROOT / pdf_path

    print("\nIndexing PDF...")

    index_id = build_pdf_index(str(pdf_path))

    print("\nPDF indexed successfully!")
    print("Ask questions about the PDF.")
    print("Type 'exit' to stop.\n")

    while True:
        try:
            question = input("Your question: ").strip()

            if question.lower() in {"exit", "quit"}:
                print("\nSession ended.")
                break

            if not question:
                print("Please enter a question.")
                continue

            print("\nSearching PDF...")

            result = answer_from_pdf(
                index_id=index_id,
                question=question
            )

            print("\n========== AI ANSWER ==========")
            print(result["answer"])

            print("\n========== PDF REFERENCES ==========")

            seen = set()

            for source in result["sources"]:
                reference = (
                    source["file"],
                    source["page"]
                )

                if reference in seen:
                    continue

                seen.add(reference)

                print(
                    f"File: {Path(source['file']).name}, "
                    f"Page: {source['page']}"
                )

            print("\n" + "=" * 45)

        except KeyboardInterrupt:
            print("\nSession interrupted.")
            break


if __name__ == "__main__":
    run_pdf_interview_assistant()
