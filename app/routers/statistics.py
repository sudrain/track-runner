from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models import CardioInterval, CardioWorkout, User
from app.schemas import RunningStatsOut

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


def _week_range(today: datetime):
    """Возвращает начало и конец текущей недели (пн 00:00 - вс 23:59)."""
    monday = today.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return monday, sunday


def _month_range(today: datetime):
    """Возвращает первый день месяца и последний день месяца (начало/конец дня)."""
    first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Вычисляем последний день месяца (можно через calendar, но для простоты next_month - 1 сек)
    next_month = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)
    last_day = next_month - timedelta(seconds=1)
    return first_day, last_day


@router.get("/running", response_model=RunningStatsOut)
async def running_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.now(timezone.utc)
    week_start, week_end = _week_range(now)
    month_start, month_end = _month_range(now)

    # Сумма дистанций за неделю
    week_result = await db.execute(
        select(func.coalesce(func.sum(CardioInterval.distance_km), 0))
        .join(CardioWorkout, CardioInterval.workout_id == CardioWorkout.id)
        .where(
            CardioWorkout.user_id == current_user.id,
            CardioWorkout.datetime >= week_start,
            CardioWorkout.datetime <= week_end,
        )
    )
    week_km = week_result.scalar_one()

    # Сумма дистанций за месяц
    month_result = await db.execute(
        select(func.coalesce(func.sum(CardioInterval.distance_km), 0))
        .join(CardioWorkout, CardioInterval.workout_id == CardioWorkout.id)
        .where(
            CardioWorkout.user_id == current_user.id,
            CardioWorkout.datetime >= month_start,
            CardioWorkout.datetime <= month_end,
        )
    )
    month_km = month_result.scalar_one()

    return RunningStatsOut(week_km=week_km, month_km=month_km)
