"""Import every model here so Base.metadata knows about all tables
(Alembic and the test setup import this package)."""

from app.models.content import Category, Image, Place, Region, place_categories

__all__ = ["Category", "Image", "Place", "Region", "place_categories"]

