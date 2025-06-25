import os

import aiofiles
from fastapi import (
    APIRouter,
    status,
    UploadFile
)
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from ...common.config import setting
from ...common.logging import logging
from ...common.utils import (
    pdf_is_native,
    UniqueID
)
from ...utils.v1 import (
    create_google_docs,
    build_report
)


logger = logging.getLogger()

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


@upload_router.post("")
async def upload_file(files: list[UploadFile]):

    if len(files) == 1 and files[0].filename == "":
        logger.info("No file uploaded")
        return JSONResponse(
            {"error": "No files uploaded"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        for file in files:
            logger.info(f"Uploading file: {file.filename}")
            # storing path
            filename = "_".join([await UniqueID.get_uuid4(), file.filename])
            file_path = os.path.join(setting.STATIC_DIR, filename)
            
            async with aiofiles.open(file_path, 'wb') as f:
                while content := await file.read(1024 * 1024):
                    await f.write(content)
            
            native_pdf = await pdf_is_native(file.file)
            logger.info("Native pdf: {}".format(native_pdf))

            # report = await build_report(file_path)
            # logger.info(f"Report: {report}")
            report = "Hello, this is a test report."

            google_docs_url = await create_google_docs(report)
            logger.info(f"Google docs url: {google_docs_url}")

        return JSONResponse(
            {
                "message": f"File uploaded successfully, report has beend generated and uploaded to google docs {google_docs_url}."
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return JSONResponse(
            content={
                "error": f"{str(e)}",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )