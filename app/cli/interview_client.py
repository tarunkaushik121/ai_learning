
import httpx
print("Interview client module loaded")
BASE_URL = "http://127.0.0.1:8000/api/v1/interviews"


def start_interview():
    print("\n========== AI MOCK INTERVIEW ==========\n")

    topic = input("Enter interview topic: ").strip()
    experience = input("Enter experience level: ").strip()
    difficulty = input(
        "Difficulty (1=Easy, 2=Medium, 3=Advanced): "
    ).strip()

    response = httpx.post(
        f"{BASE_URL}/start",
        json={
            "topic": topic,
            "experience_level": experience,
            "difficulty": difficulty
        },
        timeout=120.0
    )

    response.raise_for_status()

    return response.json()


def submit_answer(thread_id, answer):
    response = httpx.post(
        f"{BASE_URL}/{thread_id}/answer",
        json={"answer": answer},
        timeout=120.0
    )

    response.raise_for_status()

    return response.json()


def show_evaluation(evaluation):
    print("\n---------- AI FEEDBACK ----------")
    print(f"Score: {evaluation.get('score', 'N/A')}/10")
    print(
        f"Feedback: "
        f"{evaluation.get('feedback_summary', 'N/A')}"
    )

    strengths = evaluation.get("strengths", [])
    if strengths:
        print("\nStrengths:")
        for strength in strengths:
            print(f"  + {strength}")

    missing = evaluation.get("missing_concepts", [])
    if missing:
        print("\nMissing Concepts:")
        for concept in missing:
            print(f"  - {concept}")


def run_interview():
    try:
        data = start_interview()

        thread_id = data["thread_id"]
        question_number = data["question_number"]
        question = data["question"]

        while True:
            print(
                f"\n========== QUESTION {question_number} =========="
            )
            print(question)

            answer = input("\nYour answer: ").strip()

            if not answer:
                print("Answer cannot be empty. Try again.")
                continue

            result = submit_answer(thread_id, answer)

            show_evaluation(result["evaluation"])

            if result["status"] == "completed":
                print("\n========== FINAL REPORT ==========")
                print(
                    f"Questions Answered: "
                    f"{result['total_questions']}"
                )
                print(
                    f"Average Score: "
                    f"{result['average_score']}/10"
                )
                print("\nInterview completed successfully!")
                break

            question_number = result["next_question_number"]
            question = result["next_question"]

    except httpx.HTTPStatusError as exc:
        print(
            f"\nAPI Error {exc.response.status_code}: "
            f"{exc.response.text}"
        )

    except httpx.RequestError:
        print(
            "\nCannot connect to FastAPI. "
            "Make sure the server is running."
        )

    except KeyboardInterrupt:
        print("\nInterview stopped by user.")


if __name__ == "__main__":
    run_interview()
