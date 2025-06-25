from fastapi import (
    FastAPI,
    Request,
    status
)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from .routers import api_router
from ..common.config import setting
from ..common.schema import MessageSchema


app = FastAPI()
app.include_router(api_router)

# mount the status directory
app.mount("/static", StaticFiles(directory=setting.STATIC_DIR), name="static")

# mounting the templates directory
templates = Jinja2Templates(directory=setting.TEMPLATES_DIR)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='upload.html'
    )


def main():
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()