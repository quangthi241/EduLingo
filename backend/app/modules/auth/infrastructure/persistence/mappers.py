from app.modules.auth.domain.entities import Role, User
from app.modules.auth.domain.value_objects import Email, HashedPassword
from app.modules.auth.infrastructure.persistence.models import UserModel


def to_domain(m: UserModel) -> User:
    return User(
        id=m.id,
        email=Email(m.email),
        password=HashedPassword(m.password_hash),
        role=Role(m.role),
        display_name=m.display_name,
        target_cefr=m.target_cefr,
        goals=list(m.goals or []),
        created_at=m.created_at,
    )


def to_model(u: User) -> UserModel:
    return UserModel(
        id=u.id,
        email=u.email.value,
        password_hash=u.password.value,
        role=u.role.value,
        display_name=u.display_name,
        target_cefr=u.target_cefr,
        goals=list(u.goals),
        created_at=u.created_at,
    )
