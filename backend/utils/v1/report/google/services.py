import json
import os

import aiofiles
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .....common import (
    google_document_permissions,
    google_permission_roles,
    logging, 
    setting
)
from ...markdown import (
    extract_plain_text,
    clear_body,
    parse_markdown_and_create_requests
)


logger = logging.getLogger(__name__)

current_drive_service = None
current_document_service = None


async def get_document_by_id(doc_id: str, /):
    doc = current_document_service.documents().get(documentId=doc_id).execute()
    return doc


async def get_services(
    drive: bool = False,
    docs: bool = False,
):
    """
    Intializes google services `drive` and `docs`
    Args:
        None
    Returns:
        drive_service: Google Drive service
        docs_service: Google Docs service
    """

    global current_document_service, current_drive_service

    if not any([drive, docs]):
        raise ValueError("Either drive or docs must be True")
    
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', setting.GOOGLE_CLIENT_SCOPE)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            setting.GOOGLE_CLIENT_ID, 
            setting.GOOGLE_CLIENT_SCOPE
        )
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    if drive:
        current_drive_service = drive_service = build('drive', 'v3', credentials=creds)
    if docs:
        current_document_service = docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service


async def insert_text(docs_service, document_id, text="Hello, this is an automated message!"):
    try:
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,  # 1 is right after the start of the doc
                    },
                    'text': text
                }
            }
        ]
        result = docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
    except Exception as e:
        raise Exception(f"Error inserting text: {e}") from e
    

async def create_new_document(docs_service, /, doc_name: str = "New Document") -> str:
    """
    Create new document and returns it's id
    Args:
        docs_service: Google Docs service
    Returns:
        doc_id: Document id
    """
    docs = docs_service.documents().create(body={
        'title': doc_name
    }).execute()
    doc_id = docs.get("documentId")
    return doc_id


async def assign_permission(
    drive_service, 
    doc_id: str, 
    /,
    perm_type: google_document_permissions = setting.GOOGLE_DOCUMENT_DEFAULT_PERM_TYPE,
    perm_role: google_permission_roles = setting.GOOGLE_DOCUMENT_DEFAULT_PERM_ROLE
) -> None:
    """
    Assign permissions to google document.
    """
    permission = {
        'type': perm_type,
        'role': perm_role,  # or reader / commenter / owner
    }

    response = drive_service.permissions().create(
        fileId=doc_id,
        body=permission,
        fields='id'
    ).execute()

    return response.get("id")


