from app.shared.errors import DomainError


class InvalidEmail(DomainError):
    code = "invalid_email"
    http_status = 422


class WeakPassword(DomainError):
    code = "weak_password"
    http_status = 422
