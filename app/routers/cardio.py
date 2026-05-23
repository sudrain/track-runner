from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_current_user, get_db
from app.models import CardioInterval, CardioWorkout, User
from app.schemas import (
    CardioWorkoutCreate,
    CardioWorkoutOut,
    CardioWorkoutUpdate,
)

router = APIRouter(prefix="/api/cardio", tags=["cardio"])


# Создание тренировки с интервалами
@router.post(
    "/", response_model=CardioWorkoutOut, status_code=status.HTTP_201_CREATED
)
async def create_cardio_workout(
    data: CardioWorkoutCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout = CardioWorkout(
        user_id=current_user.id,
        name=data.name,
        datetime=data.datetime,
        notes=data.notes,
    )
    db.add(workout)
    # Добавляем интервалы
    for interval_data in data.intervals:
        interval = CardioInterval(
            workout=workout,
            duration_minutes=interval_data.duration_minutes,
            distance_km=interval_data.distance_km,
            tempo_min_per_km=interval_data.tempo_min_per_km,
            avg_heart_rate=interval_data.avg_heart_rate,
        )
        db.add(interval)
    await db.commit()
    await db.refresh(workout)
    # Загружаем интервалы для ответа
    result = await db.execute(
        select(CardioWorkout)
        .where(CardioWorkout.id == workout.id)
        .options(selectinload(CardioWorkout.intervals))
    )
    workout = result.scalar_one()
    return workout


# Получение всех своих тренировок (с интервалами)
@router.get("/", response_model=list[CardioWorkoutOut])
async def list_cardio_workouts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(CardioWorkout)
        .where(CardioWorkout.user_id == current_user.id)
        .options(selectinload(CardioWorkout.intervals))
        .order_by(CardioWorkout.datetime.desc())
    )
    return result.scalars().all()


# Получение одной тренировки
@router.get("/{workout_id}", response_model=CardioWorkoutOut)
async def get_cardio_workout(
    workout_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(CardioWorkout)
        .where(
            CardioWorkout.id == workout_id,
            CardioWorkout.user_id == current_user.id,
        )
        .options(selectinload(CardioWorkout.intervals))
    )
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


# Обновление (замена интервалов)
@router.put("/{workout_id}", response_model=CardioWorkoutOut)
async def update_cardio_workout(
    workout_id: int,
    data: CardioWorkoutUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(CardioWorkout)
        .where(
            CardioWorkout.id == workout_id,
            CardioWorkout.user_id == current_user.id,
        )
        .options(selectinload(CardioWorkout.intervals))
    )
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    # Частичное обновление полей
    if data.name is not None:
        workout.name = data.name  # type: ignore
    if data.datetime is not None:
        workout.datetime = data.datetime  # type: ignore
    if data.notes is not None:
        workout.notes = data.notes

    # Если переданы новые интервалы, удаляем старые и создаём новые
    if data.intervals is not None:
        for interval in workout.intervals:
            await db.delete(interval)
        for interval_data in data.intervals:
            new_interval = CardioInterval(
                workout=workout,
                duration_minutes=interval_data.duration_minutes,
                distance_km=interval_data.distance_km,
                tempo_min_per_km=interval_data.tempo_min_per_km,
                avg_heart_rate=interval_data.avg_heart_rate,
            )
            db.add(new_interval)

    await db.commit()
    await db.refresh(workout)
    # Перезапрашиваем с интервалами
    result = await db.execute(
        select(CardioWorkout)
        .where(CardioWorkout.id == workout.id)
        .options(selectinload(CardioWorkout.intervals))
    )
    return result.scalar_one()


# Удаление
@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cardio_workout(
    workout_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(CardioWorkout).where(
            CardioWorkout.id == workout_id,
            CardioWorkout.user_id == current_user.id,
        )
    )
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    await db.delete(workout)
    await db.commit()
    return None
