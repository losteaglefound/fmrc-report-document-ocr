from fastapi import APIRouter

from .v1.upload import upload_router


api_router = APIRouter()

api_router.include_router(upload_router)