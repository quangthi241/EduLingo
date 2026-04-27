import pytest

from app.modules.auth.domain.entities import Role, User
from app.modules.auth.domain.exceptions import InvalidEmail, WeakPassword
from app.modules.auth.domain.value_objects import Email, HashedPassword


@pytest.mark.unit
def test_email_valid_and_normalized() -> None:
    assert Email("USER@Example.com").value == "user@example.com"


@pytest.mark.unit
def test_email_rejects_malformed() -> None:
    with pytest.raises(InvalidEmail):
        Email("not-an-email")


@pytest.mark.unit
def test_hashed_password_requires_bcrypt_prefix() -> None:
    with pytest.raises(WeakPassword):
        HashedPassword("plainvalue")


@pytest.mark.unit
def test_user_construction_defaults_role_to_learner() -> None:
    u = User(
        id=None,
        email=Email("a@b.co"),
        password=HashedPassword("$2b$12$abcdefghijklmnopqrstuv"),
    )
    assert u.role == Role.LEARNER
