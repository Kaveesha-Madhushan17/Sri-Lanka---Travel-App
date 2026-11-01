"""Content tables: regions, categories, places (+ their many-to-many link) and images.

See PLAN.md section 7 for the full database design.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# Association table for the many-to-many relation Place <-> Category.
# It has no extra columns, so a plain Table (not a model class) is enough.
place_categories = Table(
    "place_categories",
    Base.metadata,
    Column("place_id", ForeignKey("places.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    province: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    # Months (1-12) with the best weather; used by the season guide in Phase 2.
    best_months: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    places: Mapped[list["Place"]] = relationship(back_populates="region")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    icon: Mapped[str] = mapped_column(String(50))  # lucide icon name, e.g. "waves"


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), index=True)
    short_description: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    # Numeric (not Float) for money: exact decimal values, no rounding errors.
    # Nullable because some places are free or the fee is unknown.
    entry_fee_foreign_usd: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    entry_fee_local_lkr: Mapped[int | None] = mapped_column(Integer)
    best_time_to_visit: Mapped[str] = mapped_column(String(200))
    recommended_duration_hours: Mapped[Decimal | None] = mapped_column(Numeric(4, 1))
    tips: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list)
    tags: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    region: Mapped[Region] = relationship(back_populates="places")
    categories: Mapped[list[Category]] = relationship(secondary=place_categories)

    # Images are "polymorphic": one table serves places, foods and articles,
    # identified by (owner_type, owner_id). There is no real foreign key, so we
    # tell SQLAlchemy how to join and mark the relation read-only (viewonly).
    images: Mapped[list["Image"]] = relationship(
        primaryjoin="and_(Image.owner_type == 'place', foreign(Image.owner_id) == Place.id)",
        order_by="Image.sort_order",
        viewonly=True,
    )

    @property
    def cover_image_url(self) -> str | None:
        """First image, used on cards. Requires `images` to be loaded."""
        return self.images[0].url if self.images else None


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_type: Mapped[str] = mapped_column(String(20))  # "place" | "food" | "article"
    owner_id: Mapped[int] = mapped_column(Integer)
    cloudinary_public_id: Mapped[str | None] = mapped_column(String(255))  # set in Phase 4
    url: Mapped[str] = mapped_column(String(500))
    alt_text: Mapped[str] = mapped_column(String(300), default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

