
from uuid import uuid4
from uuid import UUID

from fastapi import HTTPException
from langgraph.types import Command

from app.schemas.interview_api_schema import (
    SubmitAnswerRequest,
    SubmitAnswerResponse
)
from langgraph.checkpoint.memory import InMemorySaver

from app.graph.interview_graph import build_interview_graph
from app.schemas.interview_api_schema import (
    StartInterviewRequest,
    StartInterviewResponse
)


# Shared checkpointer for all interview sessions.
checkpointer = InMemorySaver()

# Compile once so subsequent requests can access
# the same in-memory interview state.
interview_graph = build_interview_graph(
    checkpointer=checkpointer
)


def start_interview(
    request: StartInterviewRequest
) -> StartInterviewResponse:

    thread_id = uuid4()

    config = {
        "configurable": {
            "thread_id": str(thread_id)
        }
    }

    initial_state = {
        "topic": request.topic,
        "experience_level": request.experience_level,
        "difficulty": request.difficulty.value,
        "evaluations": []
    }

    result = interview_graph.invoke(
        initial_state,
        config=config
    )

    interrupts = result.get("__interrupt__", [])

    if not interrupts:
        raise RuntimeError(
            "Interview graph did not pause for candidate input."
        )

    payload = interrupts[0].value

    return StartInterviewResponse(
        thread_id=thread_id,
        status="waiting_for_answer",
        topic=request.topic,
        question_number=payload["question_number"],
        question=payload["question"]
    )


def submit_answer(
    thread_id: UUID,
    request: SubmitAnswerRequest
) -> SubmitAnswerResponse:

    config = {
        "configurable": {
            "thread_id": str(thread_id)
        }
    }

    # 1. Load the existing interview checkpoint.
    snapshot = interview_graph.get_state(config)

    if not snapshot.values:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    # 2. The graph must be paused at human_answer.
    if not snapshot.interrupts:
        raise HTTPException(
            status_code=409,
            detail="Interview is not waiting for an answer."
        )

    previous_evaluations = snapshot.values.get(
        "evaluations", []
    )

    question = snapshot.values.get("current_question")

    if not question:
        raise HTTPException(
            status_code=409,
            detail="No active interview question found."
        )

    print("\n========== CANDIDATE ANSWER ==========", flush=True)
    print(f"Thread ID: {thread_id}", flush=True)
    print(f"Question: {question}", flush=True)
    print(f"Answer: {request.answer}", flush=True)

    # 3. Resume the existing LangGraph thread.
    result = interview_graph.invoke(
        Command(resume=request.answer),
        config=config
    )

    # 4. Find the newly generated evaluation.
    evaluations = result.get("evaluations", [])

    if len(evaluations) != len(previous_evaluations) + 1:
        raise RuntimeError(
            "Expected exactly one new answer evaluation."
        )

    latest = evaluations[-1]

    evaluation = latest["evaluation"]

    print("\n========== AI EVALUATION ==========", flush=True)
    print(f"Score: {evaluation['score']}/10", flush=True)
    print(
        f"Feedback: {evaluation['feedback_summary']}",
        flush=True
    )

    # 5. If LangGraph interrupted again,
    # return the next question.
    interrupts = result.get("__interrupt__", [])

    if interrupts:
        payload = interrupts[0].value

        print("\n========== NEXT QUESTION ==========", flush=True)
        print(
            f"Question {payload['question_number']}: "
            f"{payload['question']}",
            flush=True
        )

        return SubmitAnswerResponse(
            thread_id=thread_id,
            status="waiting_for_answer",
            evaluated_question=latest["question"],
            submitted_answer=latest["candidate_answer"],
            evaluation=evaluation,
            next_question_number=payload["question_number"],
            next_question=payload["question"]
        )

    # 6. Otherwise the interview is completed.
    if "average_score" not in result:
        raise RuntimeError(
            "Interview finished without a final report."
        )

    print("\n========== INTERVIEW COMPLETED ==========", flush=True)
    print(
        f"Average Score: {result['average_score']}/10",
        flush=True
    )

    return SubmitAnswerResponse(
        thread_id=thread_id,
        status="completed",
        evaluated_question=latest["question"],
        submitted_answer=latest["candidate_answer"],
        evaluation=evaluation,
        average_score=result["average_score"],
        total_questions=len(evaluations)
    )

