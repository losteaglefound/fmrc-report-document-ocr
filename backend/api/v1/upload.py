from fastapi import (
    APIRouter,
    status,
    UploadFile
)
from fastapi.responses import JSONResponse

upload_router = APIRouter(
    prefix="/upload",
    tags=['upload']
)


@upload_router.get("")
async def uploaded_files():
    return JSONResponse(
        {
            "files": ["these are uploaded files"]
        },
        status_code=status.HTTP_200_OK
    )


# @upload_router.post("")
# async def upload_file(file: UploadFile)