from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import case, func, select
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


def _sum_distance(period_start: datetime, period_end: datetime):
    return func.coalesce(
        func.sum(CardioInterval.distance_km).filter(
            CardioWorkout.datetime >= period_start,
            CardioWorkout.datetime < period_end,
        ),
        0,
    )


def _sum_duration(period_start: datetime, period_end: datetime):
    return func.coalesce(
        func.sum(CardioInterval.duration_minutes).filter(
            CardioWorkout.datetime >= period_start,
            CardioWorkout.datetime < period_end,
        ),
        0,
    )


def _avg_tempo(dist, dur):
    return case((dist > 0, dur / dist), else_=None)


def _year_range(today: datetime):
    """Возвращает первое января года и первое января следующего года (exclusive)."""
    today = _ensure_tz(today)
    first_jan = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    next_jan = first_jan.replace(year=first_jan.year + 1)
    return first_jan, next_jan


@router.get("/running", response_model=RunningStatsOut)
async def running_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.now(UTC)
    week_start, week_end = _week_range(now)
    month_start, month_end = _month_range(now)
    year_start, year_end = _year_range(now)

    week_dist = _sum_distance(week_start, week_end)
    month_dist = _sum_distance(month_start, month_end)
    year_dist = _sum_distance(year_start, year_end)

    week_dur = _sum_duration(week_start, week_end)
    month_dur = _sum_duration(month_start, month_end)
    year_dur = _sum_duration(year_start, year_end)

    aggregate_query = (
        select(
            week_dist,
            month_dist,
            year_dist,
            _avg_tempo(week_dist, week_dur),
            _avg_tempo(month_dist, month_dur),
            _avg_tempo(year_dist, year_dur),
        )
        .select_from(CardioInterval)
        .join(CardioWorkout, CardioInterval.workout_id == CardioWorkout.id)
        .where(CardioWorkout.user_id == current_user.id)
    )

    result = await db.execute(aggregate_query)
    row = result.one()
    return RunningStatsOut(
        week_km=row[0], month_km=row[1], year_km=row[2],
        week_avg_tempo=row[3], month_avg_tempo=row[4], year_avg_tempo=row[5],
    )
