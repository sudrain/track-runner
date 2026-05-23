from datetime import timedelta

import pytest
from jose import JWTError, jwt

from app.config import ALGORITHM, SECRET_KEY
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)


class TestPassword:
    def test_hash_and_verify(self):
        password = "my-secure-password"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        hashed = get_password_hash("correct")
        assert verify_password("wrong", hashed) is False


class TestAccessToken:
    def test_create_and_decode(self):
        token = create_access_token({"sub": "user-123"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "user-123"
        assert "exp" in payload

    def test_decode_expired_token(self):
        token = create_access_token(
            {"sub": "user-123"}, expires_delta=timedelta(minutes=-1)
        )
        assert decode_token(token) is None

    def test_decode_invalid_token(self):
        assert decode_token("invalid-token") is None

    def test_token_contains_expected_claims(self):
        token = create_access_token({"sub": "user-123"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "user-123"
        assert "exp" in payload


class TestRefreshToken:
    def test_create_and_decode(self):
        token = create_refresh_token({"sub": "user-123"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "user-123"
        assert payload["type"] == "refresh"

    def test_access_token_not_marked_as_refresh(self):
        token = create_access_token({"sub": "user-123"})
        payload = decode_token(token)
        assert payload.get("type") != "refresh"

    def test_refresh_token_has_jti(self):
        token = create_refresh_token({"sub": "user-123"})
        payload = decode_token(token)
        assert "jti" in payload
        assert len(payload["jti"]) > 0

    def test_consecutive_refresh_tokens_have_unique_jti(self):
        t1 = create_refresh_token({"sub": "user-123"})
        t2 = create_refresh_token({"sub": "user-123"})
        p1 = decode_token(t1)
        p2 = decode_token(t2)
        assert p1["jti"] != p2["jti"]

    def test_decode_token_different_key(self):
        token = create_access_token({"sub": "user-123"})
        with pytest.raises(JWTError):
            jwt.decode(token, "different-secret", algorithms=["HS256"])
