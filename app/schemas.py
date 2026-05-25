from datetime import datetime
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)


def _check_password_bytes(v: SecretStr) -> SecretStr:
    if len(v.get_secret_value().encode("utf-8")) > 72:
        raise ValueError("Password too long: bcrypt limit is 72 bytes")
    return v


class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int


def _ensure_aware(v: datetime) -> datetime:
    if v.tzinfo is None:
        raise ValueError(
            "Datetime must be timezone-aware (e.g. '2026-05-20T06:00:00Z')"
        )
    return v


AwareDatetime = Annotated[datetime, AfterValidator(_ensure_aware)]


# ---------- Пользователь ----------
class UserRegister(BaseModel):
    email: EmailStr
    password: SecretStr = Field(
        min_length=6,
        max_length=128,
    )

    _check_password_bytes = field_validator("password")(_check_password_bytes)


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr = Field(max_length=128)

    _check_password_bytes = field_validator("password")(_check_password_bytes)


class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


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
    model_config = ConfigDict(from_attributes=True)


# ---------- Кардио-тренировка ----------
class CardioWorkoutCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    datetime: AwareDatetime
    notes: str = ""
    intervals: list[CardioIntervalCreate] = Field(
        ..., min_length=1
    )


class CardioWorkoutUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    datetime: AwareDatetime | None = None
    notes: str | None = None
    intervals: list[CardioIntervalCreate] | None = Field(None, min_length=1)


class CardioWorkoutOut(BaseModel):
    id: int
    name: str
    datetime: datetime
    notes: str
    intervals: list[CardioIntervalOut]
    model_config = ConfigDict(from_attributes=True)


# ---------- Подход (Set) ----------
class SetCreate(BaseModel):
    weight_kg: float = Field(gt=0, description="Вес в кг")
    repetitions: int = Field(gt=0, description="Количество повторений")


class SetOut(BaseModel):
    id: int
    weight_kg: float
    repetitions: int
    model_config = ConfigDict(from_attributes=True)


# ---------- Упражнение ----------
class ExerciseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    sets: list[SetCreate] = Field(..., min_length=1)  # хотя бы один подход


class ExerciseOut(BaseModel):
    id: int
    name: str
    sets: list[SetOut]
    model_config = ConfigDict(from_attributes=True)


# ---------- Силовая тренировка ----------
class StrengthWorkoutCreate(BaseModel):
    datetime: AwareDatetime
    notes: str = ""
    exercises: list[ExerciseCreate] = Field(..., min_length=1)


class StrengthWorkoutUpdate(BaseModel):
    datetime: AwareDatetime | None = None
    notes: str | None = None
    exercises: list[ExerciseCreate] | None = Field(None, min_length=1)


class StrengthWorkoutOut(BaseModel):
    id: int
    datetime: datetime
    notes: str
    exercises: list[ExerciseOut]
    model_config = ConfigDict(from_attributes=True)


class RunningStatsOut(BaseModel):
    week_km: float = Field(description="Километраж за текущую неделю (ПН-ВС)")
    month_km: float = Field(description="Километраж за текущий месяц")
    year_km: float = Field(description="Километраж за текущий год")
    week_avg_tempo: float | None = Field(
        default=None, description="Средний темп за неделю (мин/км)"
    )
    month_avg_tempo: float | None = Field(
        default=None, description="Средний темп за месяц (мин/км)"
    )
    year_avg_tempo: float | None = Field(
        default=None, description="Средний темп за год (мин/км)"
    )
