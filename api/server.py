"""
FastAPI application factory for RuleBot AI.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from api.routes import router
from core.logging import configure_logging, logger
from core.settings import get_settings
from services.chat_service import ChatService

settings = get_settings()
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler to attach long-lived application services.

    This replaces the deprecated `on_event("startup")` usage and keeps
    initialization deterministic for modern FastAPI versions.
    """
    try:
        app.state.chat_service = ChatService(settings)
        logger.info("ChatService initialized and attached to app state.")
    except Exception as exc:  # pragma: no cover - startup should not crash, but log fully
        logger.exception("Failed to initialize ChatService: %s", exc)

    try:
        yield
    finally:
        logger.info("Application shutdown complete.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["*"],
    )

app.include_router(router)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://cdnjs.cloudflare.com; "
        "style-src 'self' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "worker-src 'self' blob:; " # For potential web workers, e.g., for STT/TTS
        "media-src 'self'; " # For potential audio playback/recording
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self';"
    )

    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

    return response

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(
    directory="templates",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Return clean validation errors without exposing internals.
    """
    logger.info("Validation error on %s: %s", request.url.path, exc.errors())

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Please check your request and try again.",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """
    Return consistent HTTP error payloads.
    """
    logger.info("HTTP error on %s: %s", request.url.path, exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Hide unexpected implementation details from API clients.
    """
    logger.exception("Unhandled error on %s: %s", request.url.path, exc)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "RuleBot AI encountered an unexpected error.",
        },
    )


@app.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def home(request: Request):
    """
    Render the chat interface.
    """
    # If a built SPA exists at static/frontend/index.html, serve it directly.
    import os

    spa_index = "static/frontend/index.html"
    if os.path.exists(spa_index):
        return FileResponse(spa_index, media_type="text/html")

    # Fall back to the server-rendered Jinja template if the SPA isn't built.
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
