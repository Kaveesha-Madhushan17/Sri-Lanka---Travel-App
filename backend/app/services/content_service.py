"""Business logic / data access for places, regions and categories.

Routers stay thin (HTTP concerns only) and call these functions.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Category, Place, Region

# Load related rows up-front. Async SQLAlchemy cannot lazy-load on attribute
# access, and selectinload avoids the "N+1 queries" problem (one extra query
# per relation instead of one per row).
_PLACE_RELATIONS = (
    selectinload(Place.region),
    selectinload(Place.categories),
    selectinload(Place.images),
)


async def list_places(db: AsyncSession, limit: int, offset: int) -> tuple[list[Place], int]:
    base = select(Place).where(Place.is_published.is_(True))

    total = await db.scalar(select(func.count()).select_from(base.subquery()))
    result = await db.scalars(
        base.options(*_PLACE_RELATIONS).order_by(Place.name).limit(limit).offset(offset)
    )
    return list(result), total or 0


async def get_place_by_slug(db: AsyncSession, slug: str) -> Place | None:
    return await db.scalar(
        select(Place)
        .where(Place.slug == slug, Place.is_published.is_(True))
        .options(*_PLACE_RELATIONS)
    )


async def list_regions(db: AsyncSession) -> list[Region]:
    return list(await db.scalars(select(Region).order_by(Region.name)))


async def list_categories(db: AsyncSession) -> list[Category]:
    return list(await db.scalars(select(Category).order_by(Category.name)))

