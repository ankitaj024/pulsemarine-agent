from fastapi import APIRouter

from app.api.endpoints import health, agent

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(agent.router, prefix="/ai", tags=["ai"])
