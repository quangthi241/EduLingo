from uuid import uuid4

import pytest

from app.modules.auth.infrastructure.bcrypt_hasher import BcryptHasher
from app.modules.auth.infrastructure.jwt_issuer import JwtIssuer


@pytest.mark.unit
def test_bcrypt_hasher_round_trip() -> None:
    hasher = BcryptHasher(rounds=4)
    h = hasher.hash("secret123")
    assert h.startswith("$2b$")
    assert hasher.verify("secret123", h)
    assert not hasher.verify("wrong", h)


@pytest.mark.unit
def test_bcrypt_hasher_rejects_invalid_hash_format() -> None:
    assert not BcryptHasher().verify("x", "not-a-bcrypt-hash")


@pytest.mark.unit
def test_jwt_issuer_encodes_sub_and_role() -> None:
    issuer = JwtIssuer(secret="unit-secret", alg="HS256", ttl_minutes=60)
    uid = uuid4()
    tok = issuer.issue(uid, "learner")
    claims = issuer.decode(tok)
    assert claims["sub"] == str(uid)
    assert claims["role"] == "learner"
    assert "exp" in claims and "iat" in claims
