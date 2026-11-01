"""Declarative base class that all SQLAlchemy models inherit from.

Base.metadata collects every table definition; Alembic and the tests use it.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

