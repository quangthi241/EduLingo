from collections.abc import AsyncIterator
from dataclasses import dataclass
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.application.ports import PasswordHasher, TokenIssuer, UserRepository
from app.modules.auth.application.use_cases.get_profile import GetProfile
from app.modules.auth.application.use_cases.login_user import LoginUser
from app.modules.auth.application.use_cases.register_user import RegisterUser
from app.modules.auth.application.use_cases.update_profile import UpdateProfile
from app.modules.auth.infrastructure.bcrypt_hasher import BcryptHasher
from app.modules.auth.infrastructure.jwt_issuer import JwtIssuer
from app.modules.auth.infrastructure.persistence.repository import SqlUserRepository
from app.modules.content.application.ports import (
    ContentGenerator,
    GenerationLogRepository,
    MediaStorage,
    PieceRepository,
    RateLimiter,
)
from app.modules.content.infrastructure.generation.gemini_client import GeminiApiClient
from app.modules.content.infrastructure.generation.gemini_generator import GeminiContentGenerator
from app.modules.content.infrastructure.media.local_disk import LocalDiskMediaStorage
from app.modules.content.infrastructure.media.minio import MinioMediaStorage
from app.modules.content.infrastructure.persistence.generation_log_repository import (
    SqlGenerationLogRepository,
)
from app.modules.content.infrastructure.persistence.piece_repository import (
    SqlPieceRepository,
)
from app.modules.content.infrastructure.rate_limiter.in_process import (
    InProcessRateLimiter,
)
from app.shared.config import Settings, get_settings
from app.shared.db import get_session


async def db() -> AsyncIterator[AsyncSession]:
    async for s in get_session():
        yield s


def provide_user_repo(s: AsyncSession = Depends(db)) -> UserRepository:
    return SqlUserRepository(s)


def provide_hasher() -> PasswordHasher:
    return BcryptHasher()


def provide_token_issuer() -> TokenIssuer:
    s = get_settings()
    return JwtIssuer(s.jwt_secret, s.jwt_alg, s.jwt_ttl_min)


def provide_register_user(
    repo: UserRepository = Depends(provide_user_repo),
    hasher: PasswordHasher = Depends(provide_hasher),
    tokens: TokenIssuer = Depends(provide_token_issuer),
) -> RegisterUser:
    return RegisterUser(repo, hasher, tokens)


def provide_login_user(
    repo: UserRepository = Depends(provide_user_repo),
    hasher: PasswordHasher = Depends(provide_hasher),
    tokens: TokenIssuer = Depends(provide_token_issuer),
) -> LoginUser:
    return LoginUser(repo, hasher, tokens)


def provide_get_profile(
    repo: UserRepository = Depends(provide_user_repo),
) -> GetProfile:
    return GetProfile(repo)


def provide_update_profile(
    repo: UserRepository = Depends(provide_user_repo),
) -> UpdateProfile:
    return UpdateProfile(repo)


@dataclass(slots=True)
class ContentDeps:
    pieces: PieceRepository
    media: MediaStorage
    generator: ContentGenerator
    log: GenerationLogRepository
    rate_limiter: RateLimiter


@lru_cache
def _rate_limiter_singleton() -> RateLimiter:
    return InProcessRateLimiter()


def get_gemini_client() -> GeminiApiClient:
    settings: Settings = get_settings()
    return GeminiApiClient(
        api_key=settings.gemini_api_key or "",
        base_url=settings.gemini_api_base_url,
    )


def get_content_deps(
    session: AsyncSession = Depends(db),
    client: GeminiApiClient = Depends(get_gemini_client),
) -> ContentDeps:
    settings = get_settings()
    if settings.media_storage_backend == "minio":
        assert settings.minio_bucket is not None, "MINIO_BUCKET required"
        assert settings.minio_region is not None, "MINIO_REGION required"
        assert settings.minio_access_key is not None, "MINIO_ACCESS_KEY required"
        assert settings.minio_secret_key is not None, "MINIO_SECRET_KEY required"
        media: MediaStorage = MinioMediaStorage(
            bucket=settings.minio_bucket,
            region=settings.minio_region,
            endpoint_url=settings.minio_endpoint_url,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            signed_url_ttl_seconds=settings.minio_signed_url_ttl_seconds,
        )
    else:
        media = LocalDiskMediaStorage(root=settings.media_root)
    return ContentDeps(
        pieces=SqlPieceRepository(session),
        media=media,
        generator=GeminiContentGenerator(client=client, model=settings.content_gen_model),
        log=SqlGenerationLogRepository(session),
        rate_limiter=_rate_limiter_singleton(),
    )
