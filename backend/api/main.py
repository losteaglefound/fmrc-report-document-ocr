from fastapi import (
    FastAPI,
    status
)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .routers import api_router
from ..common.config import setting
from ..common.schema import MessageSchema


app = FastAPI()
app.include_router(api_router)

# mount the status directory
app.mount("/static", StaticFiles(directory=setting.STATIC_DIR), name="static")


@app.get("/", response_model=MessageSchema)
async def read_root():
    return JSONResponse(
        {
            "message": "Hello World",
        },
        status_code=status.HTTP_200_OK
    )