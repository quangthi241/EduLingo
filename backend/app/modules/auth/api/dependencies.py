from typing import cast as _cast
from uuid import UUID

from fastapi import Depends, Request

from app.container import provide_token_issuer
from app.modules.auth.application.ports import TokenIssuer
from app.shared.errors import PermissionDeniedError

COOKIE_NAME = "edu_jwt"


async def current_user_claims(
    request: Request,
    tokens: TokenIssuer = Depends(provide_token_issuer),
) -> dict[str, object]:
    raw = request.cookies.get(COOKIE_NAME)
    if not raw:
        raise PermissionDeniedError("not authenticated")
    try:
        return tokens.decode(raw)
    except Exception as e:
        raise PermissionDeniedError("invalid token") from e


async def current_user_id(
    claims: dict[str, object] = Depends(current_user_claims),
) -> UUID:
    return UUID(_cast(str, claims["sub"]))


async def require_admin(
    claims: dict[str, object] = Depends(current_user_claims),
) -> UUID:
    if claims.get("role") != "admin":
        raise PermissionDeniedError("admin required")
    return UUID(_cast(str, claims["sub"]))
