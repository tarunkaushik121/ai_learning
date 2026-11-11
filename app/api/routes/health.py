
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Health"]
)


@router.get("/health")
def health_check():
    return {
        "status": "UP",
        "application": "AI Interview Assistant",
        "version": "1.0.0"
    }


@router.get("/welcome")
def welcome():
    return {
        "message": "Welcome to AI Interview Assistant",
        "features": [
            "AI Topic Explanation",
            "Question Generation",
            "Answer Evaluation",
            "LangGraph Interview Workflow"
        ]
    }
