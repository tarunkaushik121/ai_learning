
from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.interviews import router as interview_router


def create_app() -> FastAPI:

    application = FastAPI(
        title="AI Interview Assistant API",
        description=(
            "AI-powered interview assistant using "
            "LangChain, LangGraph and FastAPI."
        ),
        version="1.0.0"
    )

    application.include_router(health_router)
    application.include_router(interview_router)

    return application


app = create_app()
