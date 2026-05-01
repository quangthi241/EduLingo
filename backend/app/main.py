from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.modules.auth.api.router import router as auth_router
from app.modules.content.api.admin_router import router as admin_content_router
from app.modules.content.api.learner_router import router as library_router
from app.shared.config import get_settings
from app.shared.errors import install_exception_handlers
from app.shared.logging import configure_logging


def create_app() -> FastAPI:
    """Application factory. Keeps module-level state minimal for testability."""
    configure_logging()
    settings = get_settings()

    app = FastAPI(
        title="EduLingo AI",
        version="0.1.0",
        openapi_url="/api/openapi.json",
        docs_url="/docs",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
        # allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    install_exception_handlers(app)
    app.include_router(auth_router)
    app.include_router(library_router)
    app.include_router(admin_content_router)

    if settings.media_storage_backend == "local":
        import os

        os.makedirs(settings.media_root, exist_ok=True)
        app.mount("/media", StaticFiles(directory=settings.media_root), name="media")

    @app.get("/api/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
