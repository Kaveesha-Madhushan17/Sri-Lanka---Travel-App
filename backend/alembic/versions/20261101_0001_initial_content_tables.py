"""Initial content tables + pgvector extension.

Written by hand (instead of autogenerate) so every step is easy to read.

Revision ID: 0001
Revises:
Create Date: 2026-11-01
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # pgvector adds the `vector` column type. We enable it now; the
    # knowledge_chunks table that uses it comes in Phase 5.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "regions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("province", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("best_months", postgresql.ARRAY(sa.Integer), nullable=False),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
    )
    op.create_index("ix_regions_slug", "regions", ["slug"], unique=True)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("icon", sa.String(50), nullable=False),
    )
    op.create_index("ix_categories_slug", "categories", ["slug"], unique=True)

    op.create_table(
        "places",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(200), nullable=False),
        sa.Column("region_id", sa.Integer, sa.ForeignKey("regions.id"), nullable=False),
        sa.Column("short_description", sa.String(300), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
        sa.Column("entry_fee_foreign_usd", sa.Numeric(8, 2)),
        sa.Column("entry_fee_local_lkr", sa.Integer),
        sa.Column("best_time_to_visit", sa.String(200), nullable=False),
        sa.Column("recommended_duration_hours", sa.Numeric(4, 1)),
        sa.Column("tips", postgresql.ARRAY(sa.Text), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.Text), nullable=False),
        sa.Column("is_published", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_places_slug", "places", ["slug"], unique=True)
    op.create_index("ix_places_region_id", "places", ["region_id"])

    op.create_table(
        "place_categories",
        sa.Column("place_id", sa.Integer, sa.ForeignKey("places.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "images",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("owner_type", sa.String(20), nullable=False),
        sa.Column("owner_id", sa.Integer, nullable=False),
        sa.Column("cloudinary_public_id", sa.String(255)),
        sa.Column("url", sa.String(500), nullable=False),
        sa.Column("alt_text", sa.String(300), nullable=False),
        sa.Column("sort_order", sa.Integer, nullable=False),
    )
    # We always look images up by owner, so index those two columns together.
    op.create_index("ix_images_owner", "images", ["owner_type", "owner_id"])


def downgrade() -> None:
    # Drop in reverse order of dependencies.
    op.drop_table("images")
    op.drop_table("place_categories")
    op.drop_table("places")
    op.drop_table("categories")
    op.drop_table("regions")
    # The extension is left in place on purpose (other objects may use it).

