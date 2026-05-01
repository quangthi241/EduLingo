from dataclasses import dataclass

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.modules.content.domain.exceptions import (
    GenerationFailed,
    MCQInvalid,
    PieceNotFound,
    PieceStateError,
    RateLimitExceeded,
    RubricInvalid,
    SlugAlreadyExists,
    SlugInvalid,
)


class DomainError(Exception):
    """Raised by the domain layer. Framework-free."""

    code: str = "domain_error"
    http_status: int = 422


class ApplicationError(Exception):
    """Raised by the application (use-case) layer."""

    code: str = "application_error"
    http_status: int = 400


class NotFoundError(ApplicationError):
    code = "not_found"
    http_status = 404


class PermissionDeniedError(ApplicationError):
    code = "permission_denied"
    http_status = 403


class ConflictError(ApplicationError):
    code = "conflict"
    http_status = 409


@dataclass
class ProblemDetails:
    type: str
    title: str
    status: int
    detail: str


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def on_domain(_: Request, exc: DomainError) -> JSONResponse:
        return _problem(exc.code, str(exc), exc.http_status)

    @app.exception_handler(ApplicationError)
    async def on_app(_: Request, exc: ApplicationError) -> JSONResponse:
        return _problem(exc.code, str(exc), exc.http_status)

    @app.exception_handler(PieceNotFound)
    async def on_piece_not_found(_: Request, exc: PieceNotFound) -> JSONResponse:
        return _problem("not_found", str(exc), 404)

    @app.exception_handler(SlugAlreadyExists)
    async def on_slug_conflict(_: Request, exc: SlugAlreadyExists) -> JSONResponse:
        return _problem("conflict", str(exc), 409)

    @app.exception_handler(PieceStateError)
    async def on_piece_state(_: Request, exc: PieceStateError) -> JSONResponse:
        return _problem("invalid_state", str(exc), 422)

    @app.exception_handler(SlugInvalid)
    async def on_slug_invalid(_: Request, exc: SlugInvalid) -> JSONResponse:
        return _problem("validation_error", str(exc), 422)

    @app.exception_handler(MCQInvalid)
    async def on_mcq_invalid(_: Request, exc: MCQInvalid) -> JSONResponse:
        return _problem("validation_error", str(exc), 422)

    @app.exception_handler(RubricInvalid)
    async def on_rubric_invalid(_: Request, exc: RubricInvalid) -> JSONResponse:
        return _problem("validation_error", str(exc), 422)

    @app.exception_handler(IntegrityError)
    async def on_integrity_error(_: Request, exc: IntegrityError) -> JSONResponse:
        return _problem("conflict", "A resource with the same unique key already exists.", 409)

    @app.exception_handler(RateLimitExceeded)
    async def on_rate_limited(_: Request, exc: RateLimitExceeded) -> JSONResponse:
        return _problem(
            "rate_limited",
            str(exc),
            429,
            headers={"Retry-After": str(exc.retry_after_seconds)},
        )

    @app.exception_handler(GenerationFailed)
    async def on_generation_failed(_: Request, exc: GenerationFailed) -> JSONResponse:
        return _problem(
            "generation_failed",
            exc.reason,
            502,
            extra={"details": exc.details},
        )

    @app.exception_handler(ValueError)
    async def on_value_error(_: Request, exc: ValueError) -> JSONResponse:
        return _problem("validation_error", str(exc), 422)


def _problem(
    title: str,
    detail: str,
    status: int,
    *,
    extra: dict[str, object] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    content = {"type": "about:blank", "title": title, "status": status, "detail": detail}
    if extra:
        content.update(extra)
    return JSONResponse(
        status_code=status,
        content=content,
        media_type="application/problem+json",
        headers=headers,
    )
