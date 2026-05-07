from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, model_validator  # noqa: F401

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


# ---------- Кардио-интервалы ----------
class CardioIntervalCreate(BaseModel):
    duration_minutes: float = Field(gt=0, description="Длительность в минутах")
    distance_km: float = Field(gt=0, description="Дистанция в км")
    tempo_min_per_km: float | None = None
    avg_heart_rate: int | None = Field(None, ge=0, le=250)


class CardioIntervalOut(BaseModel):
    id: int
    duration_minutes: float
    distance_km: float
    tempo_min_per_km: float | None
    avg_heart_rate: int | None
    model_config = {"from_attributes": True}

# ---------- Кардио-тренировка ----------
class CardioWorkoutCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    datetime: datetime
    notes: str = ""
    intervals: list[CardioIntervalCreate] = Field(..., min_length=1)  # хотя бы один интервал

class CardioWorkoutUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    datetime: datetime | None 
    notes: str | None = None
    intervals: list[CardioIntervalCreate] | None = None

class CardioWorkoutOut(BaseModel):
    id: int
    name: str
    datetime: datetime
    notes: str
    intervals: list[CardioIntervalOut]
    model_config = {"from_attributes": True}
