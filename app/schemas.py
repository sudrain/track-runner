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
    intervals: list[CardioIntervalCreate] = Field(
        ..., min_length=1
    )  # хотя бы один интервал


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


# ---------- Подход (Set) ----------
class SetCreate(BaseModel):
    weight_kg: float = Field(gt=0, description="Вес в кг")
    repetitions: int = Field(gt=0, description="Количество повторений")


class SetOut(BaseModel):
    id: int
    weight_kg: float
    repetitions: int
    model_config = {"from_attributes": True}


# ---------- Упражнение ----------
class ExerciseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    sets: list[SetCreate] = Field(..., min_length=1)  # хотя бы один подход


class ExerciseOut(BaseModel):
    id: int
    name: str
    sets: list[SetOut]
    model_config = {"from_attributes": True}


# ---------- Силовая тренировка ----------
class StrengthWorkoutCreate(BaseModel):
    datetime: datetime
    notes: str = ""
    exercises: list[ExerciseCreate] = Field(..., min_length=1)


class StrengthWorkoutUpdate(BaseModel):
    datetime: datetime | None
    notes: str | None = None
    exercises: list[ExerciseCreate] | None = None


class StrengthWorkoutOut(BaseModel):
    id: int
    datetime: datetime
    notes: str
    exercises: list[ExerciseOut]
    model_config = {"from_attributes": True}
