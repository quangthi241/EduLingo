from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.domain.entities import User
from app.modules.auth.domain.value_objects import Email
from app.modules.auth.infrastructure.persistence.mappers import to_domain, to_model
from app.modules.auth.infrastructure.persistence.models import UserModel


class SqlUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_email(self, email: Email) -> User | None:
        r = await self._s.execute(select(UserModel).where(UserModel.email == email.value))
        m = r.scalar_one_or_none()
        return to_domain(m) if m else None

    async def get_by_id(self, user_id: UUID) -> User | None:
        m = await self._s.get(UserModel, user_id)
        return to_domain(m) if m else None

    async def add(self, user: User) -> User:
        m = to_model(user)
        self._s.add(m)
        await self._s.flush()
        return to_domain(m)

    async def update(self, user: User) -> User:
        assert user.id is not None, "cannot update user without id"
        m = await self._s.get(UserModel, user.id)
        if m is None:
            raise LookupError(f"user {user.id} not found")
        m.display_name = user.display_name
        m.target_cefr = user.target_cefr
        m.goals = list(user.goals)
        m.role = user.role.value
        await self._s.flush()
        return to_domain(m)
