import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,  # noqa: F401
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.sqlite import BLOB  # noqa: F401 # только для SQLite
from sqlalchemy.orm import relationship

# from sqlalchemy.sql import func
from app.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    # columns
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # relations
    cardio_workouts = relationship(
        "CardioWorkout", back_populates="user", lazy="dynamic"
    )
    strength_workouts = relationship(
        "StrengthWorkout", back_populates="user", lazy="dynamic"
    )


class CardioWorkout(Base):
    __tablename__ = "cardio_workouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(100), nullable=False)  #  "Бег", "Интервалы"
    datetime = Column(DateTime, nullable=False)  # дата+время тренировки
    notes = Column(Text, default="")

    user = relationship("User", back_populates="cardio_workouts")
    intervals = relationship(
        "CardioInterval", back_populates="workout", cascade="all, delete-orphan"
    )


class CardioInterval(Base):
    __tablename__ = "cardio_intervals"

    id = Column(Integer, primary_key=True)
    workout_id = Column(
        Integer,
        ForeignKey("cardio_workouts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    duration_minutes = Column(Float, nullable=False)  # длительность в минутах
    distance_km = Column(Float, nullable=False)  # дистанция в км
    tempo_min_per_km = Column(Float, nullable=True)  # темп мин/км, опционально
    avg_heart_rate = Column(Integer, nullable=True)  # средний пульс

    workout = relationship("CardioWorkout", back_populates="intervals")


class StrengthWorkout(Base):
    __tablename__ = "strength_workouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    datetime = Column(DateTime, nullable=False)
    notes = Column(Text, default="")

    user = relationship("User", back_populates="strength_workouts")
    exercises = relationship(
        "Exercise", back_populates="workout", cascade="all, delete-orphan"
    )


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    workout_id = Column(
        Integer,
        ForeignKey("strength_workouts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(100), nullable=False)  # например "Жим лежа"

    workout = relationship("StrengthWorkout", back_populates="exercises")
    sets = relationship(
        "Set", back_populates="exercise", cascade="all, delete-orphan"
    )


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True)
    exercise_id = Column(
        Integer,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    weight_kg = Column(Float, nullable=False)  # вес в кг
    repetitions = Column(Integer, nullable=False)  # количество повторений

    exercise = relationship("Exercise", back_populates="sets")
