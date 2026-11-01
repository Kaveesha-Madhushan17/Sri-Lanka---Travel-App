"""Places endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas import PlaceDetail, PlaceList
from app.services import content_service

router = APIRouter(prefix="/places", tags=["places"])


@router.get("", response_model=PlaceList)
async def list_places(
    # Query() adds validation: bad values get an automatic 422 response.
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> PlaceList:
    items, total = await content_service.list_places(db, limit=limit, offset=offset)
    return PlaceList(items=items, total=total, limit=limit, offset=offset)


@router.get("/{slug}", response_model=PlaceDetail)
async def get_place(slug: str, db: AsyncSession = Depends(get_db)):
    place = await content_service.get_place_by_slug(db, slug)
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place

