import json
import os

import aiofiles
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .....common import setting

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
        drive_service = build('drive', 'v3', credentials=creds)
    if docs:
        docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service


async def copy_template(drive_service, template_id, new_title):
    body = {'name': new_title}
    new_doc = drive_service.files().copy(fileId=template_id, body=body).execute()
    return new_doc['id']


async def replace_placeholders(docs_service, document_id, replacements):
    requests = []
    for placeholder, value in replacements.items():
        requests.append({
            'replaceAllText': {
                'containsText': {'text': f'{{{{{placeholder}}}}}', 'matchCase': True},
                'replaceText': value
            }
        })
    docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()


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

async def create_new_document(docs_service) -> str:
    """
    Create new document and returns it's id
    Args:
        docs_service: Google Docs service
    Returns:
        doc_id: Document id
    """
    docs = docs_service.documents().create(body={
        'title': 'New Document'
    }).execute()
    doc_id = docs.get("documentId")
    return doc_id



async def create_google_docs(report: str) -> str:
    drive_service, docs_service = await get_services(
        drive=True,
        docs=True
    )
    doc_id = await create_new_document(docs_service)
    await insert_text(docs_service, doc_id, report)


    # Get document content
    # doc_content = docs_service.documents().get(documentId=doc_id).execute()
    # async with aiofiles.open(f"doc_content_{doc_id}.json", 'w') as f:
    #     await f.write(json.dumps(doc_content, indent=4))
    
    return f'Document created: https://docs.google.com/document/d/{doc_id}/edit'