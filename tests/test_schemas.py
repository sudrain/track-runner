import pytest
from pydantic import ValidationError

from app.schemas import (
    CardioIntervalCreate,
    CardioWorkoutCreate,
    ExerciseCreate,
    SetCreate,
    StrengthWorkoutCreate,
    UserRegister,
)


class TestUserRegister:
    def test_valid(self):
        data = UserRegister(email="user@example.com", password="secure123")
        assert data.email == "user@example.com"

    def test_short_password(self):
        with pytest.raises(ValidationError):
            UserRegister(email="user@example.com", password="12345")

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserRegister(email="not-an-email", password="secure123")

    def test_password_too_long(self):
        with pytest.raises(ValidationError):
            UserRegister(email="user@example.com", password="x" * 73)


class TestCardioIntervalCreate:
    def test_valid(self):
        data = CardioIntervalCreate(duration_minutes=30.0, distance_km=5.0)
        assert data.duration_minutes == 30.0

    def test_zero_duration(self):
        with pytest.raises(ValidationError):
            CardioIntervalCreate(duration_minutes=0, distance_km=5.0)

    def test_zero_distance(self):
        with pytest.raises(ValidationError):
            CardioIntervalCreate(duration_minutes=30.0, distance_km=0)

    def test_heart_rate_range(self):
        with pytest.raises(ValidationError):
            CardioIntervalCreate(
                duration_minutes=30.0, distance_km=5.0, avg_heart_rate=300
            )


class TestCardioWorkoutCreate:
    def test_valid(self):
        data = CardioWorkoutCreate(
            name="Run",
            datetime="2026-05-20T06:00:00Z",
            intervals=[
            CardioIntervalCreate(duration_minutes=30.0, distance_km=5.0)
        ],
        )
        assert data.name == "Run"

    def test_empty_intervals(self):
        with pytest.raises(ValidationError):
            CardioWorkoutCreate(
                name="Run",
                datetime="2026-05-20T06:00:00Z",
                intervals=[],
            )

    def test_naive_datetime_rejected(self):
        with pytest.raises(ValidationError):
            CardioWorkoutCreate(
                name="Run",
                datetime="2026-05-20T06:00:00",
                intervals=[
            CardioIntervalCreate(duration_minutes=30.0, distance_km=5.0)
        ],
            )

    def test_name_empty(self):
        with pytest.raises(ValidationError):
            CardioWorkoutCreate(
                name="",
                datetime="2026-05-20T06:00:00Z",
                intervals=[
            CardioIntervalCreate(duration_minutes=30.0, distance_km=5.0)
        ],
            )

    def test_name_too_long(self):
        with pytest.raises(ValidationError):
            CardioWorkoutCreate(
                name="x" * 101,
                datetime="2026-05-20T06:00:00Z",
                intervals=[
            CardioIntervalCreate(duration_minutes=30.0, distance_km=5.0)
        ],
            )


class TestSetCreate:
    def test_valid(self):
        data = SetCreate(weight_kg=50.0, repetitions=10)
        assert data.weight_kg == 50.0

    def test_zero_weight(self):
        with pytest.raises(ValidationError):
            SetCreate(weight_kg=0, repetitions=10)

    def test_zero_repetitions(self):
        with pytest.raises(ValidationError):
            SetCreate(weight_kg=50.0, repetitions=0)


class TestExerciseCreate:
    def test_valid(self):
        data = ExerciseCreate(
            name="Bench Press",
            sets=[SetCreate(weight_kg=50.0, repetitions=10)],
        )
        assert data.name == "Bench Press"

    def test_empty_sets(self):
        with pytest.raises(ValidationError):
            ExerciseCreate(name="Bench Press", sets=[])

    def test_empty_name(self):
        with pytest.raises(ValidationError):
            ExerciseCreate(
                name="", sets=[SetCreate(weight_kg=50.0, repetitions=10)]
            )


class TestStrengthWorkoutCreate:
    def test_valid(self):
        data = StrengthWorkoutCreate(
            datetime="2026-05-20T10:00:00Z",
            exercises=[
                ExerciseCreate(
                    name="Squat",
                    sets=[SetCreate(weight_kg=80.0, repetitions=10)],
                )
            ],
        )
        assert len(data.exercises) == 1

    def test_empty_exercises(self):
        with pytest.raises(ValidationError):
            StrengthWorkoutCreate(
                datetime="2026-05-20T10:00:00Z", exercises=[]
            )

    def test_naive_datetime_rejected(self):
        with pytest.raises(ValidationError):
            StrengthWorkoutCreate(
                datetime="2026-05-20T10:00:00",
                exercises=[
                    ExerciseCreate(
                        name="Squat",
                        sets=[SetCreate(weight_kg=80.0, repetitions=10)],
                    )
                ],
            )
