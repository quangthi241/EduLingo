from app.modules.auth.application.dto import AuthResult, RegisterInput
from app.modules.auth.application.ports import PasswordHasher, TokenIssuer, UserRepository
from app.modules.auth.domain.entities import Role, User
from app.modules.auth.domain.value_objects import Email, HashedPassword
from app.shared.errors import ConflictError


class RegisterUser:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher, tokens: TokenIssuer) -> None:
        self.repo = repo
        self.hasher = hasher
        self.tokens = tokens

    async def execute(self, cmd: RegisterInput) -> AuthResult:
        email = Email(cmd.email)
        if await self.repo.get_by_email(email):
            raise ConflictError("email already registered")
        hashed = HashedPassword(self.hasher.hash(cmd.password))
        user = User(
            id=None,
            email=email,
            password=hashed,
            role=Role.LEARNER,
            display_name=cmd.display_name,
        )
        saved = await self.repo.add(user)
        assert saved.id is not None
        token = self.tokens.issue(saved.id, saved.role.value)
        return AuthResult(saved.id, saved.email.value, saved.role.value, token)
