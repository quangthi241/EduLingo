from typing import Any
from uuid import UUID, uuid4

from app.modules.auth.domain.entities import User
from app.modules.auth.domain.value_objects import Email


class InMemoryUserRepo:
    def __init__(self) -> None:
        self.by_id: dict[UUID, User] = {}

    async def get_by_email(self, email: Email) -> User | None:
        return next((u for u in self.by_id.values() if u.email.value == email.value), None)

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self.by_id.get(user_id)

    async def add(self, user: User) -> User:
        if user.id is None:
            user.id = uuid4()
        self.by_id[user.id] = user
        return user

    async def update(self, user: User) -> User:
        assert user.id is not None
        if user.id not in self.by_id:
            raise LookupError(f"user {user.id} not found")
        self.by_id[user.id] = user
        return user


class FakeHasher:
    def hash(self, plain: str) -> str:
        return "$2b$12$" + "x" * 22 + plain

    def verify(self, plain: str, hashed: str) -> bool:
        return hashed.endswith(plain)


class FakeTokenIssuer:
    def issue(self, user_id: UUID, role: str) -> str:
        return f"fake.{user_id}.{role}"

    def decode(self, token: str) -> dict[str, Any]:
        _, uid, role = token.split(".", 2)
        return {"sub": uid, "role": role}
