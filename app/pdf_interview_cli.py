
from pathlib import Path
from uuid import uuid4

from langgraph.types import Command

from app.graph.pdf_interview_graph import (
    build_pdf_interview_graph,
)
from app.rag.pdf_indexer import build_pdf_index


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def resolve_pdf_path(user_path: str) -> Path:
    """
    Resolve a PDF path relative to the project root.
    """

    path = Path(user_path.strip().strip('"'))

    if not path.is_absolute():
        path = PROJECT_ROOT / path

    path = path.resolve()

    if not path.is_file():
        raise FileNotFoundError(
            f"PDF not found: {path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")

    return path


def print_evaluation(evaluation: dict):
    print("\n" + "-" * 50)
    print("ANSWER EVALUATION")
    print("-" * 50)

    print(
        f"Score: {evaluation['score']}/10"
    )

    print(
        f"\nFeedback:\n{evaluation['feedback']}"
    )

    print(
        "\nExpected Answer:\n"
        f"{evaluation['expected_answer']}"
    )


def print_final_report(state: dict):
    evaluations = state.get("evaluations", [])

    print("\n" + "=" * 55)
    print("FINAL PDF INTERVIEW REPORT")
    print("=" * 55)

    for index, item in enumerate(
        evaluations,
        start=1
    ):
        evaluation = item["evaluation"]

        print(f"\nQuestion {index}:")
        print(item["question"])

        print("\nYour Answer:")
        print(item["candidate_answer"])

        print(
            f"\nScore: {evaluation['score']}/10"
        )

        print("Feedback:", evaluation["feedback"])

    print("\n" + "-" * 55)

    print(
        "Total Questions:",
        len(evaluations)
    )

    print(
        "Average Score:",
        state.get("average_score", 0),
        "/10"
    )

    print(
        "PDF Reference Pages:",
        state.get("source_pages", [])
    )


def run_pdf_interview():
    print("\n========== AI PDF INTERVIEW ==========")

    pdf_input = input(
        "Enter PDF path: "
    )

    pdf_path = resolve_pdf_path(pdf_input)

    topic = input(
        "Interview topic: "
    ).strip()

    experience_level = input(
        "Experience level: "
    ).strip()

    difficulty = input(
        "Difficulty (Easy/Intermediate/Advanced): "
    ).strip()

    if not topic or not experience_level or not difficulty:
        raise ValueError(
            "Topic, experience, and difficulty are required"
        )

    print("\nIndexing PDF knowledge...")

    index_id = build_pdf_index(str(pdf_path))

    print("PDF indexing completed.")

    graph = build_pdf_interview_graph()

    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "index_id": index_id,
        "topic": topic,
        "experience_level": experience_level,
        "difficulty": difficulty,
        "evaluations": []
    }

    print("\nGenerating interview questions...")

    graph.invoke(
        initial_state,
        config=config
    )

    previous_evaluation_count = 0

    while True:
        snapshot = graph.get_state(config)

        # When the graph has no pending nodes,
        # execution has completed.
        if not snapshot.next:
            break

        if not snapshot.interrupts:
            raise RuntimeError(
                "Graph is pending but no human interrupt "
                "was found."
            )

        question_data = snapshot.interrupts[0].value

        print("\n" + "=" * 55)

        print(
            f"QUESTION {question_data['question_number']}"
        )

        print(question_data["question"])

        answer = input(
            "\nYour answer (or 'exit'): "
        ).strip()

        if answer.lower() in {"exit", "quit"}:
            print("\nInterview stopped.")
            return

        if not answer:
            print("Answer cannot be empty.")
            continue

        # Resume the exact same graph thread.
        graph.invoke(
            Command(resume=answer),
            config=config
        )

        updated_state = graph.get_state(config).values

        evaluations = updated_state.get(
            "evaluations",
            []
        )

        # Print feedback only if a new evaluation
        # was created during this resume.
        if len(evaluations) > previous_evaluation_count:
            latest = evaluations[-1]["evaluation"]

            print_evaluation(latest)

            previous_evaluation_count = len(evaluations)

    final_state = graph.get_state(config).values

    print_final_report(final_state)


if __name__ == "__main__":
    run_pdf_interview()
