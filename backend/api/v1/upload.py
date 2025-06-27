import os
from traceback import format_exc

import aiofiles
from fastapi import (
    APIRouter,
    status,
    UploadFile
)
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from ...common import (
    logging,
    setting
)
from ...common.utils import (
    pdf_is_native,
    UniqueID
)
from ...utils.v1 import (
    build_report
)
from ...utils.v1.report.document import get_child_name
from ...utils.v1.report.google.services import (
    assign_permission,
    create_new_document,
    get_document_by_id,
    get_services,
    insert_text,
    extract_plain_text,
    parse_markdown_and_create_requests
)
from ...utils.v1.markdown import clear_body


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


async def convert_markdown_to_google_format(doc_service, doc_id: str):
    """
    This function will convert the markdown to 
    google format.
    """
    doc = await get_document_by_id(doc_id)
    content = await extract_plain_text(doc)
    clear = await clear_body(doc)
    requests = await parse_markdown_and_create_requests(content)

    full_requests = clear + requests
    doc_service.documents().batchUpdate(documentId=doc_id, body={'requests': full_requests}).execute()

    print(f"Document {doc_id} has been updated with markdown formatting.")


async def create_google_docs(report: str, doc_name: str = "New document") -> str:
    logging.info("Initialing google service")
    drive_service, docs_service = await get_services(
        drive=True,
        docs=True
    )

    logging.info("Creating new document")
    doc_id = await create_new_document(docs_service, doc_name=doc_name)
    await insert_text(docs_service, doc_id, report)

    logger.info("Assigning permission")
    await assign_permission(drive_service, doc_id, perm_type="anyone", perm_role="reader")

    logger.info("Formatted markdown to google format")
    await convert_markdown_to_google_format(docs_service, doc_id)



    # Get document content
    # doc_content = docs_service.documents().get(documentId=doc_id).execute()
    # async with aiofiles.open(f"doc_content_{doc_id}.json", 'w') as f:
    #     await f.write(json.dumps(doc_content, indent=4))
    
    return f'Document created: https://docs.google.com/document/d/{doc_id}/edit'


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

            response = await build_report(file_path)
            logger.info(f"Report: {response}")
            # report = "Hello, this is a test report."

            child_name = await get_child_name(response)
            logging.info("Child name is: {}".format(child_name))


            logging.info("Printing reponse")
            print(response)

            logging.info("Creating google documents")
            if child_name:
                document_link = await create_google_docs(response, doc_name=child_name)
            else:
                document_link = await create_google_docs(response)

            logging.info("Link to google document: {}".format(document_link))

            # google_docs_url = await create_google_docs(response)
            # logger.info(f"Google docs url: {google_docs_url}")

        return JSONResponse(
            {
                "message": f"File uploaded successfully, report has beend generated and uploaded to google docs {document_link}."
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        print(format_exc())
        logger.error(f"Error: {str(e)}")
        return JSONResponse(
            content={
                "error": f"{str(e)}",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )