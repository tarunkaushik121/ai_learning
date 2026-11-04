
from app.services.interview_service import explain_topic


def main():

    print("===================================")
    print(" AI INTERVIEW PREPARATION ASSISTANT")
    print("===================================")

    topic = input("\nEnter technical topic: ")

    experience_level = input(
        "Enter experience level: "
    )

    difficulty = input(
        "Enter difficulty (Beginner/Intermediate/Advanced): "
    )

    print("\nGenerating AI explanation...\n")

    response = explain_topic(
        topic=topic,
        experience_level=experience_level,
        difficulty=difficulty
    )

    print("\n========== AI RESPONSE ==========\n")

    print(response)


if __name__ == "__main__":
    main()
