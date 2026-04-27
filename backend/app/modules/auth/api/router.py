from uuid import UUID

from fastapi import APIRouter, Depends, Response

from app.container import (
    provide_get_profile,
    provide_login_user,
    provide_register_user,
    provide_update_profile,
)
from app.modules.auth.api.dependencies import COOKIE_NAME, current_user_id
from app.modules.auth.api.schemas import (
    AuthResponse,
    LoginRequest,
    ProfileResponse,
    RegisterRequest,
    UpdateProfileRequest,
)
from app.modules.auth.application.dto import LoginInput, RegisterInput, UpdateProfileInput
from app.modules.auth.application.use_cases.get_profile import GetProfile
from app.modules.auth.application.use_cases.login_user import LoginUser
from app.modules.auth.application.use_cases.register_user import RegisterUser
from app.modules.auth.application.use_cases.update_profile import UpdateProfile

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _profile(view: object) -> ProfileResponse:
    v = view  # ProfileView
    return ProfileResponse(
        user_id=str(v.user_id),  # type: ignore[attr-defined]
        email=v.email,  # type: ignore[attr-defined]
        role=v.role,  # type: ignore[attr-defined]
        display_name=v.display_name,  # type: ignore[attr-defined]
        target_cefr=v.target_cefr,  # type: ignore[attr-defined]
        goals=list(v.goals),  # type: ignore[attr-defined]
    )


@router.post("/register", response_model=AuthResponse)
async def register(
    body: RegisterRequest,
    response: Response,
    uc: RegisterUser = Depends(provide_register_user),
) -> AuthResponse:
    out = await uc.execute(RegisterInput(body.email, body.password, body.display_name))
    response.set_cookie(COOKIE_NAME, out.token, httponly=True, samesite="lax", secure=False, path="/")
    return AuthResponse(user_id=str(out.user_id), email=out.email, role=out.role)


@router.post("/login", response_model=AuthResponse)
async def login(
    body: LoginRequest,
    response: Response,
    uc: LoginUser = Depends(provide_login_user),
) -> AuthResponse:
    out = await uc.execute(LoginInput(body.email, body.password))
    response.set_cookie(COOKIE_NAME, out.token, httponly=True, samesite="lax", secure=False, path="/")
    return AuthResponse(user_id=str(out.user_id), email=out.email, role=out.role)


@router.post("/logout")
async def logout(response: Response) -> dict[str, bool]:
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/me", response_model=ProfileResponse)
async def me(
    user_id: UUID = Depends(current_user_id),
    uc: GetProfile = Depends(provide_get_profile),
) -> ProfileResponse:
    return _profile(await uc.execute(user_id))


@router.patch("/me", response_model=ProfileResponse)
async def update_me(
    body: UpdateProfileRequest,
    user_id: UUID = Depends(current_user_id),
    uc: UpdateProfile = Depends(provide_update_profile),
) -> ProfileResponse:
    view = await uc.execute(
        UpdateProfileInput(
            user_id=user_id,
            display_name=body.display_name,
            target_cefr=body.target_cefr,
            goals=list(body.goals),
        )
    )
    return _profile(view)
