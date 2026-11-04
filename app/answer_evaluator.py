from app.services.interview_service import evaluate_answer


def main():

    print("\n===== AI Interview Answer Evaluator =====\n")

    question = input("Enter interview question: ")

    print("\nEnter your answer:")
    candidate_answer = input("> ")

    experience_level = input("\nEnter your experience level: ")

    try:

        result = evaluate_answer(
            question=question,
            candidate_answer=candidate_answer,
            experience_level=experience_level
        )

        print("\n========== EVALUATION REPORT ==========")

        print(f"\nScore: {result.score}/10")
        print(f"Verdict: {result.verdict}")

        print("\nTechnical Correctness:")
        print(result.technical_correctness)

        print("\nStrengths:")
        for strength in result.strengths:
            print(f"- {strength}")

        print("\nMissing Concepts:")
        for concept in result.missing_concepts:
            print(f"- {concept}")

        print("\nImprovement Suggestions:")
        for suggestion in result.improvement_suggestions:
            print(f"- {suggestion}")

        print("\nIdeal Answer:")
        print(result.ideal_answer)

        print("\nFeedback Summary:")
        print(result.feedback_summary)

        print("\n=======================================")

    except Exception as exception:
        print(f"\nError evaluating answer: {exception}")


if __name__ == "__main__":
    main()