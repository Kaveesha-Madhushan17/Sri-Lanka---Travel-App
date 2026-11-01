"""FastAPI application entry point. Run with: uvicorn app.main:app --reload"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")

# CORS: the browser blocks requests from http://localhost:3000 (frontend)
# to http://localhost:8000 (backend) unless the backend explicitly allows it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,  # needed later for httpOnly auth cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"message": "Sri Lanka Travel API. See /docs"}

