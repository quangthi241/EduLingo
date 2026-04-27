from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class RegisterRequest(_Base):
    email: str
    password: str
    display_name: str | None = None


class LoginRequest(_Base):
    email: str
    password: str


class AuthResponse(_Base):
    user_id: str
    email: str
    role: str


class ProfileResponse(_Base):
    user_id: str
    email: str
    role: str
    display_name: str | None = None
    target_cefr: str | None = None
    goals: list[str] = Field(default_factory=list)


class UpdateProfileRequest(_Base):
    display_name: str | None = None
    target_cefr: str | None = None
    goals: list[str] = Field(default_factory=list)
