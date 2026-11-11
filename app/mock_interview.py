
from app.services.mock_interview_service import (
    conduct_mock_interview
)


def main():
    print("\nWelcome to AI Mock Interview Assistant!")

    topic = input("Enter interview topic: ").strip()
    difficulty = input(
        "Enter difficulty (Easy/Intermediate/Advanced): "
    ).strip()

    experience_level = input(
        "Enter your experience level: "
    ).strip()

    number_of_questions = int(
        input("How many questions? (1-5): ")
    )

    if not topic or not experience_level:
        print("Topic and experience level are required.")
        return

    if difficulty.lower() not in [
        "easy", "intermediate", "advanced"
    ]:
        print("Invalid difficulty level.")
        return

    if not 1 <= number_of_questions <= 5:
        print("Please enter a number between 1 and 5.")
        return

    conduct_mock_interview(
        topic=topic,
        difficulty=difficulty.title(),
        experience_level=experience_level,
        number_of_questions=number_of_questions
    )


if __name__ == "__main__":
    main()
