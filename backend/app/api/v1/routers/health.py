"""Health check endpoint: tells us if the API and the database are up."""

from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response schema. FastAPI uses it for validation and for the /docs page."""

    status: Literal["ok", "degraded"]
    database: Literal["ok", "unreachable"]


@router.get("/health", response_model=HealthResponse)
async def health(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    try:
        # The simplest possible query: proves we can reach PostgreSQL.
        await db.execute(text("SELECT 1"))
        return HealthResponse(status="ok", database="ok")
    except Exception:
        # The API itself still responds, but reports the DB problem.
        return HealthResponse(status="degraded", database="unreachable")

