import asyncio
import json
import os
import re
from typing import Literal


from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import openai
import pdfplumber

from config import (
    logging,
    setting
)
from report import REPORT
from convert_markdown import (
    extract_plain_text,
    clear_body,
    parse_markdown_and_create_requests
)


logger = logging.getLogger(__name__)


key_heading_mapping = {
    "demographics": "Demographics",
    "name": "Name",
    "dob": "Dob",
    "chronological_age": "Chronological Age",
    "sex": "Sex",
    "language": "Language",
    "parent_guardian": "Parent Guardian",
    "uci_number": "Uci Number",
    "service_coordinator": "Service Coordinator",
    "examiner": "Examiner",
    "date_of_report": "Date Of Report",
    "date_of_encounter": "Date Of Encounter",
    
    "referral_reason_and_background": "Referral Reason And Background",
    "background_info": "Background Info",
    "birth_and_medical_history": "Birth And Medical History",
    "speech_language_hearing": "Speech Language Hearing",
    "fine_motor_development": "Fine Motor Development",
    "feeding_history": "Feeding History",
    "dental_and_oral_behaviors": "Dental And Oral Behaviors",
    
    "test_observations": "Test Observations",
    "assessment_tools_used": "Assessment Tools Used",
    
    "bayley_4": "Bayley 4",
    "cognitive": "Cognitive",
    "receptive_communication": "Receptive Communication",
    "expressive_communication": "Expressive Communication",
    "fine_motor": "Fine Motor",
    "gross_motor": "Gross Motor",
    "social_emotional": "Social Emotional",
    "adaptive_behavior": "Adaptive Behavior",
    "scaled_score": "Scaled Score",
    "age_equivalent": "Age Equivalent",
    "narrative": "Narrative",
    
    "sp2_summary": "SP2 Summary",
    "summary": "Summary",
    "implications": "Implications",
    
    "chomps_summary": "ChOMPS Summary",
    "score_breakdown": "Score Breakdown",
    "complex_movement_patterns": "Complex Movement Patterns",
    "basic_movement_patterns": "Basic Movement Patterns",
    "oral_motor_coordination": "Oral Motor Coordination",
    "fundamental_oral_motor_skills": "Fundamental Oral Motor Skills",
    "total_score": "Total Score",
    
    "pedieat_summary": "PediEAT Summary",
    "physiologic_symptoms": "Physiologic Symptoms",
    "mealtime_behaviors": "Mealtime Behaviors",
    "selective_eating": "Selective Eating",
    "oral_processing": "Oral Processing",
    
    "physical_exam_summary": "Physical Exam Summary",
    "cranial_nerve_screening_summary": "Cranial Nerve Screening Summary",
    
    "recommendations": "Recommendations",
    "goals": "Goals"
}



async def get_prompt(context: str):
    # PROMPT = f"""
    # You are a highly skilled pediatric occupational therapist and medical report writer. Based on the provided evaluation text extracted from a PDF, your task is to extract structured data and rewrite observations and test results into detailed, clinically accurate narratives.

    # The text will contain demographic details, clinical observations, and standardized test results (Bayley-4, SP2, ChOMPS, PediEAT). Do not guess. If a section is missing, write `"Not available"`.

    # This is the file context: {context}

    # Use the tone and level of detail in the FMRC Health Group Master Report as your standard. Your final output should include the following sections:

    # ---

    # ### 📄 Output Format (Structured JSON-like)

    # ```json
    # {{
    # "Demographics": {{
    #     "Name": "",
    #     "Dob": "",
    #     "Chronological Age": "",
    #     "Sex": "",
    #     "Language": "",
    #     "Parent Guardian": "",
    #     "Uci Number": "",
    #     "Service Coordinator": "",
    #     "Examiner": "",
    #     "Date Of Report": "",
    #     "Date Of Encounter": ""
    # }},
    # "Referral Reason And Background": {{
    #     "Background Info": "",
    #     "Birth And Medical History": "",
    #     "Speech Language Hearing": "",
    #     "Fine Motor Development": "",
    #     "Feeding History": "",
    #     "Dental And Oral Behaviors": ""
    # }},
    # "Test Observations": "",
    # "Assessment Tools Used": [],
    # "Bayley 4": {{
    #     "Cognitive": {{
    #     "Scaled Score": "",
    #     "Age Equivalent": "",
    #     "Narrative": ""
    #     }},
    #     "Receptive Communication": {{
    #     "Scaled Score": "",
    #     "Age Equivalent": "",
    #     "Narrative": ""
    #     }},
    #     "Expressive Communication": {{
    #     "Scaled Score": "",
    #     "Age Equivalent": "",
    #     "Narrative": ""
    #     }},
    #     "Fine Motor": {{
    #     "Scaled Score": "",
    #     "Age Equivalent": "",
    #     "Narrative": ""
    #     }},
    #     "Gross Motor": {{
    #     "Scaled Score": "",
    #     "Age Equivalent": "",
    #     "Narrative": ""
    #     }},
    #     "Social Emotional": {{
    #     "Scaled Score": "",
    #     "Narrative": ""
    #     }},
    #     "Adaptive Behavior": {{
    #     "Scaled Score": "",
    #     "Narrative": ""
    #     }}
    # }},
    # "Sp2 Summary": {{
    #     "Summary": "",
    #     "Implications": ""
    # }},
    # "Chomps Summary": {{
    #     "Score Breakdown": {{
    #     "Complex Movement Patterns": "",
    #     "Basic Movement Patterns": "",
    #     "Oral Motor Coordination": "",
    #     "Fundamental Oral Motor Skills": "",
    #     "Total Score": ""
    #     }},
    #     "Narrative": ""
    # }},
    # "Pedieat Summary": {{
    #     "Score Breakdown": {{
    #     "Physiologic Symptoms": "",
    #     "Mealtime Behaviors": "",
    #     "Selective Eating": "",
    #     "Oral Processing": "",
    #     "Total Score": ""
    #     }},
    #     "Narrative": ""
    # }},
    # "Physical Exam Summary": "",
    # "Cranial Nerve Screening Summary": "",
    # "Summary": "",
    # "Recommendations": [
    #     "e.g. Feeding therapy one time per week...",
    #     "..."
    # ],
    # "Goals": [
    #     "Child will reduce finger use during mealtime...",
    #     "..."
    # ]
    # }}

    # """

    PROMPT = f"""

    You are a highly skilled pediatric occupational therapist and medical report writer. Based on the provided evaluation text extracted from a PDF, your task is to extract structured data and rewrite observations and test results into detailed, clinically accurate narratives.

    The text will contain demographic details, clinical observations, and standardized test results (Bayley-4, SP2, ChOMPS, PediEAT). **Do not guess**. If a section is missing, write `"Not available"`.

    This is the file context: {context}

    ---

    ## 🔁 Output Format: Markdown

    ❗Return your final output as a **Markdown document**, following the structure shown below. This format will be used for generating a human-readable report in Google Docs. Use `**bold**` for section titles and keep the output readable with paragraph spacing.

    ---

    ### 📄 Markdown Output Structure
    """

    return PROMPT


async def call_openai(
    prompt: str,
    model: Literal["gpt-4o"] = setting.OPENAI_DEFAULT_MODEL,
    temperature=0.4
):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a clinical report writing assistant."},
            {'role': "user", "content": prompt}
        ],
        temperature=temperature
    )

    return response.choices[0].message.content

async def get_context():
    context: str = ""
    with pdfplumber.open('/home/lap-20/Downloads/Master Report 6_4.pdf') as f:
        for page in f.pages:
            context += page.extract_text() + "\n"

    return context


async def format_key(key: str) -> str:
    """Convert snake_case or camelCase to Title Case with spaces."""
    return key.replace('_', ' ').title()


async def json_to_doc_string(data, indent_level=0):
    """Recursively converts JSON to formatted string for Google Docs."""
    indent = '  ' * indent_level
    output = ""

    if isinstance(data, dict):
        for key, value in data.items():
            formatted_key = await format_key(key)
            heading = f"{indent}**{formatted_key}**\n"
            if isinstance(value, (dict, list)):
                content = await json_to_doc_string(value, indent_level + 1)
            else:
                content = f"{indent}{formatted_key}: {value}\n" if value else ""
                heading = ""
            output += heading + content + "\n"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                output += await json_to_doc_string(item, indent_level + 1)
            else:
                output += f"{indent}- {item}\n"
    else:
        output += f"{indent}{data}\n"
    
    return output


async def get_services():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', setting.GOOGLE_CLIENT_SCOPE)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(setting.GOOGLE_CLIENT_ID, setting.GOOGLE_CLIENT_SCOPE)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service


async def insert_text(docs_service, document_id, text="Hello, this is an automated message!"):
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



async def create_new_google_document(docs_service, doc_name: str):
    """
    Create new document and get it's id
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


async def assign_permission(drive_service, doc_id: str) -> None:
    permission = {
        'type': 'anyone',
        'role': 'reader',  # or reader / commenter / owner
    }

    response = drive_service.permissions().create(
        fileId=doc_id,
        body=permission,
        fields='id'
    ).execute()

    return response.get("id")


async def create_google_document(content: str, doc_name: str = "New Document") -> str:
    drive_service, docs_service = await get_services()
    # print(dir(docs_service.documents()))

    doc_id = await create_new_google_document(docs_service, doc_name=doc_name)
    # doc_id = "1iEg_wTbRorPXU6oJf7ATV6kv20yNFFI3wwrldf3C6fE"
    await insert_text(docs_service, doc_id, content)

    logger.info("Assigning permission")
    await assign_permission(drive_service, doc_id)


    logger.info("Formatted markdown to google format")
    await convert_markdown_to_google_format(docs_service, doc_id)

    return f'Document created: https://docs.google.com/document/d/{doc_id}/edit'


async def extract_field(pattern, text, default="", flags=0):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else default


async def get_child_name(content: str) -> str:
    child_name = await extract_field(r'\*\*Name:\*\*\s*(.+)', content)
    return child_name


async def convert_markdown_to_google_format(doc_service, doc_id: str):
    doc = doc_service.documents().get(documentId=doc_id).execute()
    content = await extract_plain_text(doc)

    clear = await clear_body(doc_service, doc_id)
    requests = await parse_markdown_and_create_requests(content)

    full_requests = clear + requests
    doc_service.documents().batchUpdate(documentId=doc_id, body={'requests': full_requests}).execute()

    print(f"Document {doc_id} has been updated with markdown formatting.")


async def main():
    logging.info("Getting context")
    context = await get_context()

    logging.info("Getting prompt")
    prompt = await get_prompt(context)

    logging.info("Calling openai")
    response = await call_openai(prompt)
    # response = REPORT

    response_splited = response.split("\n")
    response_removed_md = response_splited[1:len(response_splited)-2]
    response = "\n".join(response_removed_md)

    # logging.info("Converting to doc string")
    # response_json = json.loads(response)
    # response_doc_string = await json_to_doc_string(response_json)

    child_name = await get_child_name(response)
    logging.info("Child name is: {}".format(child_name))


    logging.info("Printing reponse")
    print(response)

    logging.info("Creating google documents")
    if child_name:
        document_link = await create_google_document(response, doc_name=child_name)
    else:
        document_link = await create_google_document(response)

    logging.info("Link to google document: {}".format(document_link))


if __name__ == "__main__":
    asyncio.run(main())