from fastapi import (
    FastAPI,
    status
)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

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


def main():
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()