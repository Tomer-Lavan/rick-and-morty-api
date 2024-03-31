from fastapi import FastAPI
from app.api.router import api_router
from app.api.endpoints import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(api_router)
