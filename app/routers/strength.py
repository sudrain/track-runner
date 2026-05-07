from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_current_user, get_db
from app.models import Exercise, Set, StrengthWorkout, User
from app.schemas import (
    StrengthWorkoutCreate,
    StrengthWorkoutOut,
    StrengthWorkoutUpdate,
)

router = APIRouter(prefix="/api/strength", tags=["strength"])


@router.post(
    "/", response_model=StrengthWorkoutOut, status_code=status.HTTP_201_CREATED
)
async def create_strength_workout(
    data: StrengthWorkoutCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout = StrengthWorkout(
        user_id=current_user.id,
        datetime=data.datetime,
        notes=data.notes,
    )
    db.add(workout)
    for ex_data in data.exercises:
        exercise = Exercise(
            workout=workout,
            name=ex_data.name,
        )
        db.add(exercise)
        for set_data in ex_data.sets:
            s = Set(
                exercise=exercise,
                weight_kg=set_data.weight_kg,
                repetitions=set_data.repetitions,
            )
            db.add(s)
    await db.commit()
    await db.refresh(workout)
    # Загружаем со связями
    result = await db.execute(
        select(StrengthWorkout)
        .where(StrengthWorkout.id == workout.id)
        .options(
            selectinload(StrengthWorkout.exercises).selectinload(Exercise.sets)
        )
    )
    workout = result.scalar_one()
    return workout


@router.get("/", response_model=list[StrengthWorkoutOut])
async def list_strength_workouts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(StrengthWorkout)
        .where(StrengthWorkout.user_id == current_user.id)
        .options(
            selectinload(StrengthWorkout.exercises).selectinload(Exercise.sets)
        )
        .order_by(StrengthWorkout.datetime.desc())
    )
    return result.scalars().all()


@router.get("/{workout_id}", response_model=StrengthWorkoutOut)
async def get_strength_workout(
    workout_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(StrengthWorkout)
        .where(
            StrengthWorkout.id == workout_id,
            StrengthWorkout.user_id == current_user.id,
        )
        .options(
            selectinload(StrengthWorkout.exercises).selectinload(Exercise.sets)
        )
    )
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.put("/{workout_id}", response_model=StrengthWorkoutOut)
async def update_strength_workout(
    workout_id: int,
    data: StrengthWorkoutUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(StrengthWorkout)
        .where(
            StrengthWorkout.id == workout_id,
            StrengthWorkout.user_id == current_user.id,
        )
        .options(
            selectinload(StrengthWorkout.exercises).selectinload(Exercise.sets)
        )
    )
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    if data.datetime is not None:
        workout.datetime = data.datetime  # type: ignore
    if data.notes is not None:
        workout.notes = data.notes  # type: ignore

    if data.exercises is not None:
        # Удаляем старые упражнения (каскад удалит подходы)
        for ex in workout.exercises:
            await db.delete(ex)
        for ex_data in data.exercises:
            new_ex = Exercise(
                workout=workout,
                name=ex_data.name,
            )
            db.add(new_ex)
            for set_data in ex_data.sets:
                s = Set(
                    exercise=new_ex,
                    weight_kg=set_data.weight_kg,
                    repetitions=set_data.repetitions,
                )
                db.add(s)

    await db.commit()
    await db.refresh(workout)
    result = await db.execute(
        select(StrengthWorkout)
        .where(StrengthWorkout.id == workout.id)
        .options(
            selectinload(StrengthWorkout.exercises).selectinload(Exercise.sets)
        )
    )
    return result.scalar_one()


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_strength_workout(
    workout_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(StrengthWorkout).where(
            StrengthWorkout.id == workout_id,
            StrengthWorkout.user_id == current_user.id,
        )
    )
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    await db.delete(workout)
    await db.commit()
    return None
