from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models import ExerciseTemplate, User
from app.schemas import ExerciseTemplateOut

router = APIRouter(prefix="/api/exercise-templates", tags=["exercise-templates"])


@router.get("/", response_model=list[ExerciseTemplateOut])
async def list_exercise_templates(
    exercise_type: str | None = Query(
        default=None, alias="type",
        description="Filter by type: cardio or strength",
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(ExerciseTemplate)
    if exercise_type:
        stmt = stmt.where(ExerciseTemplate.type == exercise_type)
    stmt = stmt.order_by(ExerciseTemplate.name)
    result = await db.execute(stmt)
    return result.scalars().all()
