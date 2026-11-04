from app.services.interview_service import generate_questions


def main():

    print("\n===== AI Interview Question Generator =====\n")

    topic = input("Enter interview topic: ")
    experience_level = input("Enter experience level: ")

    print("\nDifficulty:")
    print("1. Easy")
    print("2. Intermediate")
    print("3. Advanced")

    difficulty_choice = input("Choose difficulty (1/2/3): ")

    difficulty_map = {
        "1": "Easy",
        "2": "Intermediate",
        "3": "Advanced"
    }

    difficulty = difficulty_map.get(difficulty_choice)

    if not difficulty:
        print("Invalid difficulty selection.")
        return

    try:
        result = generate_questions(
            topic=topic,
            experience_level=experience_level,
            difficulty=difficulty
        )

        print(f"\nTopic: {result.topic}")
        print(f"Difficulty: {result.difficulty}")

        print("\n===== Generated Questions =====")

        for index, question in enumerate(result.questions, start=1):

            print(f"\n{index}. {question.question}")
            print(f"Difficulty: {question.difficulty}")

            print("Expected answer points:")

            for point in question.expected_points:
                print(f"  - {point}")

    except Exception as exception:
        print(f"\nError generating questions: {exception}")


if __name__ == "__main__":
    main()