from uuid import uuid4

import pytest

from app.modules.auth.application.dto import UpdateProfileInput
from app.modules.auth.application.use_cases.update_profile import UpdateProfile
from app.modules.auth.domain.entities import Role, User
from app.modules.auth.domain.value_objects import Email, HashedPassword
from app.shared.errors import DomainError, NotFoundError
from tests.fakes.auth import InMemoryUserRepo


def _seed_user() -> tuple[InMemoryUserRepo, User]:
    repo = InMemoryUserRepo()
    user = User(
        id=uuid4(),
        email=Email("x@y.co"),
        password=HashedPassword("$2b$12$" + "x" * 22 + "secret"),
        role=Role.LEARNER,
        display_name="old",
    )
    repo.by_id[user.id] = user  # type: ignore[index]
    return repo, user


@pytest.mark.unit
async def test_update_profile_persists_fields() -> None:
    repo, user = _seed_user()
    uc = UpdateProfile(repo)

    view = await uc.execute(
        UpdateProfileInput(
            user_id=user.id,  # type: ignore[arg-type]
            display_name="New Name",
            target_cefr="B1",
            goals=["travel", "work"],
        )
    )

    assert view.display_name == "New Name"
    assert view.target_cefr == "B1"
    assert view.goals == ["travel", "work"]


@pytest.mark.unit
async def test_update_profile_rejects_invalid_cefr() -> None:
    repo, user = _seed_user()
    uc = UpdateProfile(repo)

    with pytest.raises(DomainError):
        await uc.execute(
            UpdateProfileInput(
                user_id=user.id,  # type: ignore[arg-type]
                display_name=None,
                target_cefr="Z9",
                goals=[],
            )
        )


@pytest.mark.unit
async def test_update_profile_rejects_too_many_goals() -> None:
    repo, user = _seed_user()
    uc = UpdateProfile(repo)

    with pytest.raises(DomainError):
        await uc.execute(
            UpdateProfileInput(
                user_id=user.id,  # type: ignore[arg-type]
                display_name=None,
                target_cefr="B1",
                goals=[f"g{i}" for i in range(11)],
            )
        )


@pytest.mark.unit
async def test_update_profile_missing_user_raises_not_found() -> None:
    repo = InMemoryUserRepo()
    uc = UpdateProfile(repo)

    with pytest.raises(NotFoundError):
        await uc.execute(
            UpdateProfileInput(
                user_id=uuid4(),
                display_name="x",
                target_cefr=None,
                goals=[],
            )
        )
