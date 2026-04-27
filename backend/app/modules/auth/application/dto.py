from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class RegisterInput:
    email: str
    password: str
    display_name: str | None = None


@dataclass(slots=True)
class LoginInput:
    email: str
    password: str


@dataclass(slots=True)
class AuthResult:
    user_id: UUID
    email: str
    role: str
    token: str


@dataclass(slots=True)
class UpdateProfileInput:
    user_id: UUID
    display_name: str | None
    target_cefr: str | None
    goals: list[str]


@dataclass(slots=True)
class ProfileView:
    user_id: UUID
    email: str
    role: str
    display_name: str | None
    target_cefr: str | None
    goals: list[str]
