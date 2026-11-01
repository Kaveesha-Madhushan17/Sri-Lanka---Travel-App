"""Test setup shared by all tests.

Tests use a SEPARATE database (<name>_test) so they never touch your dev data.
Before the test session we create it, build the tables from the models and
insert a small, known dataset. Then we override the app's `get_db`
dependency so every request in a test uses this database.
"""

import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

import app.models  # noqa: F401
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import Category, Image, Place, Region

DEV_URL = make_url(settings.database_url)
TEST_URL = DEV_URL.set(database=f"{DEV_URL.database}_test")

# NullPool: open a fresh connection each time. TestClient runs the app in its
# own event loop, and pooled asyncpg connections cannot move between loops.
test_engine = create_async_engine(TEST_URL, poolclass=NullPool)
TestSession = async_sessionmaker(test_engine, expire_on_commit=False)


async def _create_database() -> None:
    # CREATE DATABASE cannot run inside a transaction -> AUTOCOMMIT.
    admin = create_async_engine(DEV_URL.set(database="postgres"), isolation_level="AUTOCOMMIT")
    async with admin.connect() as conn:
        exists = await conn.scalar(text("SELECT 1 FROM pg_database WHERE datname = :n"), {"n": TEST_URL.database})
        if not exists:
            await conn.execute(text(f'CREATE DATABASE "{TEST_URL.database}"'))
    await admin.dispose()


async def _reset_schema_and_insert_data() -> None:
    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestSession() as db:
        south = Region(slug="south-coast", name="South Coast", province="Southern", description="Beaches",
                       best_months=[12, 1, 2, 3], latitude=6.0, longitude=80.2)
        triangle = Region(slug="cultural-triangle", name="Cultural Triangle", province="North Central",
                          description="Ancient cities", best_months=[1, 2, 3, 4, 5], latitude=7.9, longitude=80.7)
        heritage = Category(slug="culture-heritage", name="Culture & Heritage", icon="landmark")
        beach = Category(slug="beach", name="Beach", icon="waves")
        db.add_all([south, triangle, heritage, beach])
        await db.flush()  # assigns ids

        sigiriya = Place(
            slug="sigiriya", name="Sigiriya Rock Fortress", region_id=triangle.id,
            short_description="Rock fortress", description="Ancient palace on a rock.",
            latitude=7.957, longitude=80.760, entry_fee_foreign_usd=36, entry_fee_local_lkr=100,
            best_time_to_visit="Early morning", recommended_duration_hours=3,
            tips=["Start early"], tags=["unesco"], categories=[heritage],
        )
        mirissa = Place(
            slug="mirissa", name="Mirissa", region_id=south.id, short_description="Beach town",
            description="Whales and beaches.", latitude=5.95, longitude=80.47,
            best_time_to_visit="Nov-Apr", tips=[], tags=["whales"], categories=[beach],
        )
        hidden = Place(
            slug="draft-place", name="Draft", region_id=south.id, short_description="Not published",
            description="-", latitude=6.0, longitude=80.0, best_time_to_visit="-",
            tips=[], tags=[], is_published=False,
        )
        db.add_all([sigiriya, mirissa, hidden])
        await db.flush()
        db.add(Image(owner_type="place", owner_id=sigiriya.id, url="https://example.com/s.jpg",
                     alt_text="Sigiriya", sort_order=0))
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
def test_database():
    asyncio.run(_create_database())
    asyncio.run(_reset_schema_and_insert_data())
    yield
    asyncio.run(test_engine.dispose())


async def _override_get_db():
    async with TestSession() as session:
        yield session


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

