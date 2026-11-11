
from app.services.interview_service import (
    generate_questions,
    evaluate_answer
)


def conduct_mock_interview(
    topic: str,
    difficulty: str,
    experience_level: str,
    number_of_questions: int = 5
):
    print("\n================================")
    print("       MOCK INTERVIEW")
    print("================================")

    # Step 1: Generate interview questions
    question_set = generate_questions(
        topic=topic,
        difficulty=difficulty,
        experience_level=experience_level
    )

    questions = question_set.questions[:number_of_questions]

    evaluations = []

    # Step 2: Ask questions one by one
    for index, question in enumerate(questions, start=1):

        print(f"\nQuestion {index}/{len(questions)}")
        print(question.question)

        print("\nYour answer (type 'exit' to stop):")
        candidate_answer = input("> ").strip()

        if candidate_answer.lower() == "exit":
            print("\nInterview stopped by candidate.")
            break

        if not candidate_answer:
            print("Empty answer submitted. Skipping evaluation.")
            continue

        # Step 3: Evaluate candidate answer
        evaluation = evaluate_answer(
            question=question.question,
            candidate_answer=candidate_answer,
            experience_level=experience_level
        )

        evaluations.append(evaluation)

        # Step 4: Display feedback
        print("\n---------- FEEDBACK ----------")
        print(f"Score: {evaluation.score}/10")
        print(f"Verdict: {evaluation.verdict}")
        print(f"Summary: {evaluation.feedback_summary}")

        print("\nStrengths:")
        for strength in evaluation.strengths:
            print(f"- {strength}")

        print("\nMissing Concepts:")
        for concept in evaluation.missing_concepts:
            print(f"- {concept}")

        print("\nImprovement Suggestions:")
        for suggestion in evaluation.improvement_suggestions:
            print(f"- {suggestion}")

    # Step 5: Generate final report
    if evaluations:
        average_score = sum(
            evaluation.score for evaluation in evaluations
        ) / len(evaluations)

        print("\n================================")
        print("       FINAL INTERVIEW REPORT")
        print("================================")

        print(f"Questions evaluated: {len(evaluations)}")
        print(f"Average score: {average_score:.2f}/10")

        if average_score >= 8:
            print("Performance: Excellent")
        elif average_score >= 6:
            print("Performance: Good")
        elif average_score >= 4:
            print("Performance: Average")
        else:
            print("Performance: Needs Improvement")

    else:
        print("\nNo answers were evaluated.")
