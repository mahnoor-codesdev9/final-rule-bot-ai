"""API routes for RuleBot AI.

This module exposes the public HTTP endpoints used by the frontend and
external callers. The `ChatService` instance is provided from the
application state at request time to keep the router stateless and easy to
test.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status

from api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    HistoryResponse,
    SettingsResponse,
    StatsResponse,
    StatusResponse,
)
from core.settings import get_settings
from services.chat_service import ChatService

router = APIRouter()


def get_chat_service(request: Request) -> ChatService:
    """Dependency to retrieve the app-scoped ChatService instance."""
    service = getattr(request.app.state, "chat_service", None)

    if service is None:
        # Fallback for tests or direct imports where the server hasn't
        # attached a ChatService instance to the app state.
        settings = get_settings()
        service = ChatService(settings)
        # Persist the instance for subsequent requests in this app.
        setattr(request.app.state, "chat_service", service)

    return service


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["system"],
)
async def health(request: Request) -> dict[str, str]:
    """Return a lightweight health check for hosting platforms."""
    settings = get_settings()

    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }


@router.get(
    "/settings",
    response_model=SettingsResponse,
    tags=["system"],
)
async def public_settings(
    chat_service: ChatService = Depends(get_chat_service),
) -> dict:
    """Return frontend-safe runtime settings."""
    return chat_service.public_settings()


@router.get(
    "/history",
    response_model=HistoryResponse,
    tags=["chat"],
)
async def history(
    chat_service: ChatService = Depends(get_chat_service),
) -> dict:
    """Return the persisted conversation history."""
    return {"history": chat_service.history()}


@router.delete(
    "/history",
    response_model=StatusResponse,
    tags=["chat"],
)
async def clear_history(
    chat_service: ChatService = Depends(get_chat_service),
) -> dict[str, str]:
    """Clear history and reset in-process statistics."""
    chat_service.clear()

    return {"status": "success"}


@router.get(
    "/stats",
    response_model=StatsResponse,
    tags=["analytics"],
)
async def statistics(
    chat_service: ChatService = Depends(get_chat_service),
) -> dict[str, int]:
    """Return session statistics for the active server process."""
    return chat_service.stats()


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    tags=["chat"],
)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> dict:
    """Return a rule-based or optional AI response for the user message."""
    result = await chat_service.get_response(
        request.message,
        request.mode,
        request.provider,
    )

    return {
        "response": result.response,
        "mode": result.mode,
        "provider": result.provider,
        "fallback": result.fallback,
    }
