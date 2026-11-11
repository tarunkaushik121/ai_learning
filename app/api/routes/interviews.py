
from uuid import UUID

from fastapi import APIRouter, status

from app.schemas.interview_api_schema import (
    StartInterviewRequest,
    StartInterviewResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)

from app.services.interview_api_service import (
    start_interview as start_interview_service,
    submit_answer as submit_answer_service,
)


router = APIRouter(
    prefix="/api/v1/interviews",
    tags=["Interviews"],
)


@router.post(
    "/start",
    response_model=StartInterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_interview(
    request: StartInterviewRequest,
) -> StartInterviewResponse:
    return start_interview_service(request)


@router.post(
    "/{thread_id}/answer",
    response_model=SubmitAnswerResponse,
    status_code=status.HTTP_200_OK,
)
def submit_interview_answer(
    thread_id: UUID,
    request: SubmitAnswerRequest,
) -> SubmitAnswerResponse:
    return submit_answer_service(
        thread_id=thread_id,
        request=request,
    )
