import os

from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


from config import setting


# Scopes for Google Drive and Docs
SCOPES = setting.GOOGLE_CLIENT_SCOPE

def get_services():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(setting.GOOGLE_CLIENT_ID, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service


def copy_template(drive_service, template_id, new_title):
    body = {'name': new_title}
    new_doc = drive_service.files().copy(fileId=template_id, body=body).execute()
    return new_doc['id']


def replace_placeholders(docs_service, document_id, replacements):
    requests = []
    for placeholder, value in replacements.items():
        requests.append({
            'replaceAllText': {
                'containsText': {'text': f'{{{{{placeholder}}}}}', 'matchCase': True},
                'replaceText': value
            }
        })
    docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()


def insert_text(docs_service, document_id, text="Hello, this is an automated message!"):
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
        documentId=document_id, body={'requests': requests}).execute()
    print("Text inserted successfully.")

def create_new_document(docs_service):
    """
    Create new document and get it's id
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



def main():
    drive_service, docs_service = get_services()

    # doc_id = create_new_document(docs_service)
    doc_id = "1iEg_wTbRorPXU6oJf7ATV6kv20yNFFI3wwrldf3C6fE"

    # TEMPLATE_ID = doc_id  # Found in the URL of the template
    # NEW_TITLE = 'Generated Document from Template'
    # PLACEHOLDERS = {
    #     'NAME': 'Alice',
    #     'DATE': '2025-06-24',
    #     'PROJECT': 'Automation Demo'
    # }

    # Step 1: Copy the template
    # new_doc_id = copy_template(drive_service, TEMPLATE_ID, NEW_TITLE)
    
    # Step 2: Replace placeholders
    # replace_placeholders(docs_service, new_doc_id, PLACEHOLDERS)
    insert_text(docs_service, doc_id)
    
    print(f'Document created: https://docs.google.com/document/d/{doc_id}/edit')

if __name__ == "__main__":
    main()