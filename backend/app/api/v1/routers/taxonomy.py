"""Regions and categories endpoints (small lookup lists)."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas import CategoryOut, RegionOut
from app.services import content_service

router = APIRouter()


@router.get("/regions", response_model=list[RegionOut], tags=["regions"])
async def list_regions(db: AsyncSession = Depends(get_db)):
    return await content_service.list_regions(db)


@router.get("/categories", response_model=list[CategoryOut], tags=["categories"])
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await content_service.list_categories(db)

