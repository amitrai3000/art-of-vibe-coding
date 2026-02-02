"""Health check endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint.

    Returns:
        Health status
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "ai-chat-platform-backend",
        }
    )


@router.get("/ready")
async def readiness_check() -> JSONResponse:
    """Readiness check endpoint.

    Returns:
        Readiness status
    """
    # TODO: Add checks for database, Redis, etc.
    return JSONResponse(
        content={
            "status": "ready",
            "service": "ai-chat-platform-backend",
        }
    )
