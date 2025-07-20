"""
API v1 router configuration.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import categories

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    categories.router,
    prefix="/categories",
    tags=["categories"]
)
