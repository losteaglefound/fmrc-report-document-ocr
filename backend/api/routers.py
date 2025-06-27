from fastapi import APIRouter

from .v1.upload import upload_router


api_router_v1 = APIRouter()

api_router_v1.include_router(upload_router)