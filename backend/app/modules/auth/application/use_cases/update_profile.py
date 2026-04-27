from app.modules.auth.application.dto import ProfileView, UpdateProfileInput
from app.modules.auth.application.ports import UserRepository
from app.shared.errors import DomainError, NotFoundError

_VALID_CEFR = {"A1", "A2", "B1", "B2", "C1", "C2"}


class UpdateProfile:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def execute(self, cmd: UpdateProfileInput) -> ProfileView:
        if cmd.target_cefr is not None and cmd.target_cefr not in _VALID_CEFR:
            raise DomainError(f"invalid target_cefr: {cmd.target_cefr}")
        if len(cmd.goals) > 10:
            raise DomainError("at most 10 goals allowed")

        user = await self.repo.get_by_id(cmd.user_id)
        if user is None:
            raise NotFoundError("user not found")

        user.display_name = cmd.display_name
        user.target_cefr = cmd.target_cefr
        user.goals = list(cmd.goals)

        saved = await self.repo.update(user)
        assert saved.id is not None
        return ProfileView(
            user_id=saved.id,
            email=saved.email.value,
            role=saved.role.value,
            display_name=saved.display_name,
            target_cefr=saved.target_cefr,
            goals=list(saved.goals),
        )
