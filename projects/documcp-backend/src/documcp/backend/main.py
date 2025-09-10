from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from documcp.backend.api.generation import initialize_services
from documcp.backend.api.generation import router as generation_router
from documcp.backend.container import ApplicationContainer
from documcp.backend.settings import Settings
from documcp.shared_kernel.domain.exception import BaseMsgException
from documcp.shared_kernel.infra.fastapi.exception_handlers.base import custom_exception_handler
from documcp.shared_kernel.infra.fastapi.middlewares.correlation_id import CorrelationIdMiddleware
from documcp.shared_kernel.infra.fastapi.middlewares.session import SessionMiddleware
from documcp.shared_kernel.infra.fastapi.utils.responses import MsgSpecJSONResponse

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

container = ApplicationContainer()
settings: Settings = container.settings.provided()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting up DocuMCP application")

    # Initialize services on startup
    try:
        await initialize_services()
        logger.info("Application startup completed successfully")
        yield
    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise
    finally:
        logger.info("Shutting down DocuMCP application")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    middleware = [
        Middleware(CorrelationIdMiddleware),
        Middleware(
            CORSMiddleware,
            allow_origins=settings.cors.allow_origins,
            allow_credentials=settings.cors.allow_credentials,
            allow_methods=settings.cors.allow_methods,
            allow_headers=settings.cors.allow_headers,
        ),
        Middleware(SessionMiddleware, secret_key=settings.session.secret_key),
        Middleware(GZipMiddleware),
    ]

    app = FastAPI(
        title=settings.fastapi.title,
        description=settings.fastapi.description,
        contact=settings.fastapi.contact,
        summary=settings.fastapi.summary,
        middleware=middleware,
        docs_url=settings.fastapi.docs_url,
        redoc_url=settings.fastapi.redoc_url,
        openapi_url=settings.fastapi.openapi_url,
        default_response_class=MsgSpecJSONResponse,
        exception_handlers={
            BaseMsgException: custom_exception_handler,
        },
        lifespan=lifespan,
    )

    app.container = container  # type: ignore
    app.settings = settings  # type: ignore

    # Include API routers
    app.include_router(generation_router, prefix="/api/v1", tags=["generation"])

    return app


app = create_app()
