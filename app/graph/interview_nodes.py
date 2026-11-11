
from app.graph.interview_state import InterviewState
from app.services.interview_service import generate_questions
from typing import Literal
from app.services.interview_service import evaluate_answer
from langgraph.types import interrupt
from app.graph.interview_state import InterviewState
from langgraph.types import interrupt
def generate_questions_node(
    state: InterviewState
) -> dict:

    print("\n[LangGraph] Generating interview questions...")

    result = generate_questions(
        topic=state["topic"],
        experience_level=state["experience_level"],
        difficulty=state["difficulty"]
    )

    return {
    "questions": [
        question.model_dump()
        for question in result.questions
    ],
    "current_question_index": 0
}


def prepare_question_node(
    state: InterviewState
) -> dict:

    index = state["current_question_index"]
    questions = state["questions"]

    question = questions[index]["question"]

    print(f"\n[LangGraph] Question {index + 1}:")
    print(question)

    return {
        "current_question": question
    }






def advance_question_node(
    state: InterviewState
) -> dict:

    current_index = state["current_question_index"]

    next_index = current_index + 1

    print(
        f"[LangGraph] Moving to question index {next_index}"
    )

    return {
        "current_question_index": next_index
    }


def route_next_question(
    state: InterviewState
) -> Literal["continue", "finish"]:

    current_index = state["current_question_index"]
    total_questions = len(state["questions"])

    if current_index < total_questions:
        print("[LangGraph] More questions available")
        return "continue"

    print("[LangGraph] All questions processed")
    return "finish"


def evaluate_answer_node(
    state: InterviewState
) -> dict:

    question = state["current_question"]
    candidate_answer = state["candidate_answer"]

    print("\n[LangGraph] Evaluating answer...")

    result = evaluate_answer(
        question=question,
        candidate_answer=candidate_answer,
        experience_level=state["experience_level"]
    )

    evaluation = {
        "question": question,
        "candidate_answer": candidate_answer,
        "evaluation": result.model_dump()
    }

    print(f"Score: {result.score}/10")
    print(f"Verdict: {result.verdict}")

    return {
        "evaluations": [evaluation]
    }



def final_report_node(
    state: InterviewState
) -> dict:

    evaluations = state["evaluations"]

    if not evaluations:
        average_score = 0.0
    else:
        total_score = sum(
            item["evaluation"]["score"]
            for item in evaluations
        )

        average_score = total_score / len(evaluations)

    print("\n===== FINAL INTERVIEW REPORT =====")
    print(f"Topic: {state['topic']}")
    print(f"Questions evaluated: {len(evaluations)}")
    print(f"Average score: {average_score:.2f}/10")

    return {
        "average_score": average_score
    }



def sample_answer_node(
    state: InterviewState
) -> dict:

    question = state["current_question"]

    print(f"\n[LangGraph] Answering: {question}")

    sample_answer = (
        "I understand the general concept. "
        "In Java 8, this feature helps developers "
        "write cleaner and more maintainable code."
    )

    return {
        "candidate_answer": sample_answer
    }



def human_answer_node(
    state: InterviewState
) -> dict:

    question = state["current_question"]
    question_number = state["current_question_index"] + 1

    candidate_answer = interrupt({
        "question_number": question_number,
        "question": question,
        "message": "Please provide your interview answer."
    })

    if not isinstance(candidate_answer, str):
        raise ValueError("Candidate answer must be a string.")

    if not candidate_answer.strip():
        raise ValueError("Candidate answer cannot be empty.")

    return {
        "candidate_answer": candidate_answer.strip()
    }


def human_answer_node(
    state: InterviewState
) -> dict:

    question = state["current_question"]
    question_number = state["current_question_index"] + 1

    print(
        f"\n[LangGraph] Waiting for answer "
        f"to question {question_number}..."
    )

    candidate_answer = interrupt({
        "question_number": question_number,
        "question": question,
        "message": "Please provide your interview answer."
    })

    if not isinstance(candidate_answer, str):
        raise ValueError(
            "Candidate answer must be a string."
        )

    if not candidate_answer.strip():
        raise ValueError(
            "Candidate answer cannot be empty."
        )

    return {
        "candidate_answer": candidate_answer.strip()
    }
