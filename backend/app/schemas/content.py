"""Pydantic schemas: the shape of data the API sends.

Kept separate from the SQLAlchemy models so the API contract can differ
from the database (e.g. hide columns, add computed fields).
`from_attributes=True` lets Pydantic read values straight from ORM objects.
"""

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CategoryOut(ORMModel):
    id: int
    name: str
    slug: str
    icon: str


class RegionBrief(ORMModel):
    id: int
    name: str
    slug: str


class RegionOut(RegionBrief):
    province: str
    description: str
    best_months: list[int]
    latitude: float
    longitude: float


class ImageOut(ORMModel):
    url: str
    alt_text: str


class PlaceSummary(ORMModel):
    """Small version of a place for lists and cards."""

    id: int
    name: str
    slug: str
    short_description: str
    latitude: float
    longitude: float
    cover_image_url: str | None
    region: RegionBrief
    categories: list[CategoryOut]


class PlaceDetail(PlaceSummary):
    """Full version for the detail page."""

    description: str
    # Decimal columns are converted to float so JSON has numbers, not strings.
    entry_fee_foreign_usd: float | None
    entry_fee_local_lkr: int | None
    best_time_to_visit: str
    recommended_duration_hours: float | None
    tips: list[str]
    tags: list[str]
    images: list[ImageOut]


class PlaceList(BaseModel):
    """Paginated list: the items of this page plus the total count."""

    items: list[PlaceSummary]
    total: int
    limit: int
    offset: int

