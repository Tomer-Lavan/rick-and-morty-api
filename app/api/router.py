from fastapi import APIRouter, Depends
from app.api.endpoints import characters_router, episodes_router, locations_router, insights_router
from app.dependencies import get_current_user


api_router = APIRouter(dependencies=[Depends(get_current_user)])

api_router.include_router(
    characters_router, prefix="/characters", tags=["Characters"])
api_router.include_router(
    episodes_router, prefix="/episodes", tags=["Episodes"])
api_router.include_router(
    locations_router, prefix="/locations", tags=["Locations"])
api_router.include_router(
    insights_router, prefix="/insights", tags=["Insights"])
