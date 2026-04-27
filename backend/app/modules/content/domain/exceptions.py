class ContentError(Exception):
    """Base class for content domain errors."""


class SlugInvalid(ContentError):
    pass


class SlugAlreadyExists(ContentError):
    pass


class PieceNotFound(ContentError):
    pass


class PieceStateError(ContentError):
    pass


class MCQInvalid(ContentError):
    pass


class RubricInvalid(ContentError):
    pass


class GenerationFailed(ContentError):
    def __init__(self, reason: str, details: list[str] | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.details = details or []


class RateLimitExceeded(ContentError):
    def __init__(self, retry_after_seconds: int) -> None:
        if not isinstance(retry_after_seconds, int) or retry_after_seconds < 0:
            raise ValueError(f"retry_after_seconds must be a non-negative int, got {retry_after_seconds!r}")
        super().__init__(f"rate limited; retry after {retry_after_seconds}s")
        self.retry_after_seconds = retry_after_seconds
