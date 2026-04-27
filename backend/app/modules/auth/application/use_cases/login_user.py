from app.modules.auth.application.dto import AuthResult, LoginInput
from app.modules.auth.application.ports import PasswordHasher, TokenIssuer, UserRepository
from app.modules.auth.domain.value_objects import Email
from app.shared.errors import NotFoundError


class LoginUser:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher, tokens: TokenIssuer) -> None:
        self.repo = repo
        self.hasher = hasher
        self.tokens = tokens

    async def execute(self, cmd: LoginInput) -> AuthResult:
        user = await self.repo.get_by_email(Email(cmd.email))
        if not user or not self.hasher.verify(cmd.password, user.password.value):
            raise NotFoundError("invalid credentials")
        assert user.id is not None
        token = self.tokens.issue(user.id, user.role.value)
        return AuthResult(user.id, user.email.value, user.role.value, token)
