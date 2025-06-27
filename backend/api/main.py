from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Request,
    status
)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .routers import api_router_v1
from ..common.config import setting
from ..common.schema import MessageSchema


@asynccontextmanager
async  def lifespan(app: FastAPI):
    setting.UPLOAD_DIR
    yield


app = FastAPI(
    lifespan=lifespan
)
app.include_router(api_router_v1, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)



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