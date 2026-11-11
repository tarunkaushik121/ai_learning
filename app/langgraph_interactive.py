
from uuid import uuid4

from langgraph.types import Command

from app.graph.interview_graph import build_interview_graph


def main():

    graph = build_interview_graph()

    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "topic": "Java 8",
        "experience_level": "5 years",
        "difficulty": "Intermediate",
        "evaluations": []
    }

    print("\n===== INTERACTIVE LANGGRAPH INTERVIEW =====")
    print("Thread ID:", thread_id)

    result = graph.invoke(
        initial_state,
        config=config
    )

    while "__interrupt__" in result:

        interrupts = result["__interrupt__"]

        if not interrupts:
            break

        payload = interrupts[0].value

        print(
            f"\nQuestion {payload['question_number']}:"
        )
        print(payload["question"])

        while True:
            answer = input("\nYour answer: ").strip()

            if answer:
                break

            print("Answer cannot be empty.")

        result = graph.invoke(
            Command(resume=answer),
            config=config
        )

    print("\n===== INTERVIEW COMPLETED =====")

    evaluations = result.get("evaluations", [])

    print("Questions evaluated:", len(evaluations))
    print("Average score:", result.get("average_score"))

    assert len(evaluations) == 5, (
        f"Expected 5 evaluations, got {len(evaluations)}"
    )


if __name__ == "__main__":
    main()
