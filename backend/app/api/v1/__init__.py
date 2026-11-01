"""Version 1 of the API. All routers are collected here under /api/v1."""

from fastapi import APIRouter

from app.api.v1.routers import health, places, taxonomy

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(places.router)
api_router.include_router(taxonomy.router)
