"""Database engine and session factory.

The engine manages a pool of connections to PostgreSQL. A session is a
short-lived "unit of work" used inside one request.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# pool_pre_ping checks a connection is alive before using it.
engine = create_async_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: opens a session per request and always closes it."""
    async with SessionLocal() as session:
        yield session

