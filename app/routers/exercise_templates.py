from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models import ExerciseTemplate, User
from app.schemas import ExerciseTemplateOut

router = APIRouter(prefix="/api/exercise-templates", tags=["exercise-templates"])


@router.get("/", response_model=list[ExerciseTemplateOut])
async def list_exercise_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ExerciseTemplate).order_by(ExerciseTemplate.name)
    )
    return result.scalars().all()
