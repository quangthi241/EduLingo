from uuid import UUID

from app.modules.auth.application.dto import ProfileView
from app.modules.auth.application.ports import UserRepository
from app.shared.errors import NotFoundError


class GetProfile:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def execute(self, user_id: UUID) -> ProfileView:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("user not found")
        assert user.id is not None
        return ProfileView(
            user_id=user.id,
            email=user.email.value,
            role=user.role.value,
            display_name=user.display_name,
            target_cefr=user.target_cefr,
            goals=list(user.goals),
        )
