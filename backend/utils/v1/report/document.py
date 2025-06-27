from datetime import datetime
import os
import re

import pdfplumber
import openai

from ....common import (
    logging,
    open_ai_models,
    setting
)
from ..prompt.pediatric_prompt import get_pediatric_prompt
from ..text import extract_field
from .sample import REPORT


logger = logging.getLogger(__name__)


async def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


async def extract_field(pattern, text, default="TBD", flags=0):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else default

async def calculate_chronological_age(dob_str, encounter_str):
    try:
        dob = datetime.strptime(dob_str, "%m/%d/%Y")
        encounter = datetime.strptime(encounter_str, "%m/%d/%Y")
        delta = encounter - dob
        years, days = divmod(delta.days, 365)
        months = days // 30
        return f"{years} years, {months} months"
    except:
        return "TBD"


async def extract_structured_data(text) -> dict:
    dob = await extract_field(r"Date of Birth:\s*(\d{1,2}/\d{1,2}/\d{4})", text)
    encounter_date = await extract_field(r"Date of Encounter:\s*(\d{1,2}/\d{1,2}/\d{4})", text)
    
    return {
        "child_name": await extract_field(r"Name:\s*(.*?)\s*Date of Birth", text),
        "dob": dob,
        "encounter_date": encounter_date,
        "chronological_age": await calculate_chronological_age(dob, encounter_date),
        "uci": await extract_field(r"UCI#\s*(\d+)", text),
        "sex": await extract_field(r"Sex:\s*(\w+)", text),
        "language": await extract_field(r"Primary Language:\s*(\w+)", text),
        "guardian_name": await extract_field(r"Parent/Guardian:\s*(.*?)\s", text),

        "cog_score": "2",
        "cog_age_eq": "18 months",
        "cog_delay_pct": "Extremely low",
        "lang_score": "1",
        "lang_age_eq": "10 months",
        "lang_delay_pct": "Extremely low",
        "motor_score": "4",
        "motor_age_eq": "17 months",
        "motor_delay_pct": "41%",
        "sp2_seeking": "Less Than Others",
        "sp2_avoiding": "Much More Than Others",
        "sp2_sensitivity": "Much More Than Others",
        "sp2_registration": "Typical",
        "chomps_scores_summary": "High concern in all domains (complex, basic movement, coordination, fundamental skills)",
        "pedieat_scores": "Concern in Physiologic Symptoms, Oral Processing, and Selective Eating. No concern in Mealtime Behaviors.",
        "bullet_notes": "- Frequently placed fingers in mouth\n- Overstuffed mouth multiple times\n- Gagged during session\n- Used both hands to self-feed\n- Accepted assistance"
    }


async def call_openai_gpt(prompt, /, model: open_ai_models, temperature=0.4):
    openai.api_key = setting.OPENAI_API_KEY
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a clinical report writing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content


async def build_report(file: str):
    logger.info(f"Building report for file: {file}")

    text = await extract_text_from_pdf(file)
    # logger.info(f"Extracted text: {text}")
    
    
    # structured_data = await extract_structured_data(text)
    # logger.info(f"Extracted structured data: {structured_data}")
    
    prompt = await get_pediatric_prompt(text)
    # logger.info(f"Prompt: {prompt}")

    # TODO: remove the sample removed in production
    response = await call_openai_gpt(prompt, model="gpt-4o")
    # response = REPORT
    logger.info(f"Report: {response}")

    response_splited = response.split("\n")
    response_removed_md = response_splited[1:len(response_splited)-2]
    response = "\n".join(response_removed_md)

    return response



async def get_child_name(content: str) -> str:
    child_name = await extract_field(r'\*\*Name:\*\*\s*(.+)', content)
    return child_name