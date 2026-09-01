"""
Health Check Router — Day 1
Provides /health and / endpoints to verify the API is alive.
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime, timezone

from app.core.config import settings
from app.core.custom_docs import get_developer_dashboard_html

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    timestamp: str
    message: str


@router.get(
    "/",
    summary="Root endpoint",
    description="Welcome endpoint — serves Developer Dashboard HTML or JSON status.",
)
async def root(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return get_developer_dashboard_html()
    return HealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        message="Welcome to the Stock Portfolio & Investment Management API 🚀",
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns API health status. Used by load balancers and uptime monitors.",
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        message="All systems operational",
    )
