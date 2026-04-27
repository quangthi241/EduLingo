import pytest

from app.modules.auth.application.dto import LoginInput, RegisterInput
from app.modules.auth.application.use_cases.login_user import LoginUser
from app.modules.auth.application.use_cases.register_user import RegisterUser
from app.shared.errors import ConflictError, NotFoundError
from tests.fakes.auth import FakeHasher, FakeTokenIssuer, InMemoryUserRepo


@pytest.mark.unit
async def test_register_new_user_issues_token() -> None:
    repo, hasher, tokens = InMemoryUserRepo(), FakeHasher(), FakeTokenIssuer()
    uc = RegisterUser(repo, hasher, tokens)
    out = await uc.execute(RegisterInput(email="a@b.co", password="secret123", display_name="A"))
    assert out.email == "a@b.co"
    assert out.token.startswith("fake.")


@pytest.mark.unit
async def test_register_rejects_duplicate_email() -> None:
    repo, hasher, tokens = InMemoryUserRepo(), FakeHasher(), FakeTokenIssuer()
    uc = RegisterUser(repo, hasher, tokens)
    await uc.execute(RegisterInput(email="a@b.co", password="secret123"))
    with pytest.raises(ConflictError):
        await uc.execute(RegisterInput(email="a@b.co", password="secret123"))


@pytest.mark.unit
async def test_login_returns_token_for_valid_credentials() -> None:
    repo, hasher, tokens = InMemoryUserRepo(), FakeHasher(), FakeTokenIssuer()
    await RegisterUser(repo, hasher, tokens).execute(RegisterInput(email="a@b.co", password="secret123"))
    out = await LoginUser(repo, hasher, tokens).execute(LoginInput(email="a@b.co", password="secret123"))
    assert out.token.startswith("fake.")


@pytest.mark.unit
async def test_login_rejects_wrong_password() -> None:
    repo, hasher, tokens = InMemoryUserRepo(), FakeHasher(), FakeTokenIssuer()
    await RegisterUser(repo, hasher, tokens).execute(RegisterInput(email="a@b.co", password="secret123"))
    with pytest.raises(NotFoundError):
        await LoginUser(repo, hasher, tokens).execute(LoginInput(email="a@b.co", password="wrong"))
