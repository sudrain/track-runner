from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ---------- Пользователь ----------
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=6,
        max_length=72,
        description="Пароль до 72 символов (ограничение bcrypt)",
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72)


class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


# Для ответа с токенами (установить куки)
class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
