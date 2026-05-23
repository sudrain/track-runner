from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models import CardioInterval, CardioWorkout, User
from app.schemas import RunningStatsOut

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


def _ensure_tz(today: datetime) -> datetime:
    if today.tzinfo is None:
        raise ValueError("_week_range / _month_range requires timezone-aware datetime")
    return today


def _week_range(today: datetime):
    """Возвращает начало недели (пн 00:00) и начало следующей недели (exclusive)."""
    today = _ensure_tz(today)
    monday = today.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - timedelta(days=today.weekday())
    next_monday = monday + timedelta(days=7)
    return monday, next_monday


def _month_range(today: datetime):
    """Возвращает первый день месяца и первый день следующего месяца (exclusive)."""
    today = _ensure_tz(today)
    first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)
    return first_day, next_month


@router.get("/running", response_model=RunningStatsOut)
async def running_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.now(UTC)
    week_start, week_end = _week_range(now)
    month_start, month_end = _month_range(now)

    # Единый запрос: дистанции за неделю + месяц
    aggregate_query = (
        select(
            func.coalesce(
                func.sum(CardioInterval.distance_km).filter(
                    CardioWorkout.datetime >= week_start,
                    CardioWorkout.datetime < week_end,
                ),
                0,
            ),
            func.coalesce(
                func.sum(CardioInterval.distance_km).filter(
                    CardioWorkout.datetime >= month_start,
                    CardioWorkout.datetime < month_end,
                ),
                0,
            ),
        )
        .select_from(CardioInterval)
        .join(CardioWorkout, CardioInterval.workout_id == CardioWorkout.id)
        .where(CardioWorkout.user_id == current_user.id)
    )

    result = await db.execute(aggregate_query)
    row = result.one()
    return RunningStatsOut(week_km=row[0], month_km=row[1])
