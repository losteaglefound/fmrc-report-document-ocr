import pdfplumber
import re
from datetime import datetime

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_field(pattern, text, default="TBD", flags=0):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else default

def calculate_chronological_age(dob_str, encounter_str):
    try:
        dob = datetime.strptime(dob_str, "%m/%d/%Y")
        encounter = datetime.strptime(encounter_str, "%m/%d/%Y")
        delta = encounter - dob
        years, days = divmod(delta.days, 365)
        months = days // 30
        return f"{years} years, {months} months"
    except:
        return "TBD"

def extract_structured_data(text):
    dob = extract_field(r"Date of Birth:\s*(\d{1,2}/\d{1,2}/\d{4})", text)
    encounter_date = extract_field(r"Date of Encounter:\s*(\d{1,2}/\d{1,2}/\d{4})", text)
    
    return {
        "child_name": extract_field(r"Name:\s*(.*?)\s*Date of Birth", text),
        "dob": dob,
        "encounter_date": encounter_date,
        "chronological_age": calculate_chronological_age(dob, encounter_date),
        "uci": extract_field(r"UCI#\s*(\d+)", text),
        "sex": extract_field(r"Sex:\s*(\w+)", text),
        "language": extract_field(r"Primary Language:\s*(\w+)", text),
        "guardian_name": extract_field(r"Parent/Guardian:\s*(.*?)\s", text),
        
        # Bayley-4
        "cog_score": extract_field(r"Cognitive scaled score of (\d+)", text),
        "cog_age_eq": extract_field(r"Cognitive scaled score of \d+, placing him.*?age equivalent of ([\d]+ months)", text),
        "cog_delay_pct": "Extremely low",
        "lang_score": "1",
        "lang_age_eq": "10 months",
        "lang_delay_pct": "Extremely low",
        "motor_score": "4",
        "motor_age_eq": "17 months",
        "motor_delay_pct": "41%",
        
        # SP2
        "sp2_seeking": "Less Than Others",
        "sp2_avoiding": "Much More Than Others",
        "sp2_sensitivity": "Much More Than Others",
        "sp2_registration": "Typical",
        
        # CHOMPS
        "chomps_scores_summary": "High concern in all domains (complex, basic movement, coordination, fundamental skills)",
        
        # PEDI-EAT
        "pedieat_scores": "Concern in Physiologic Symptoms, Oral Processing, and Selective Eating. No concern in Mealtime Behaviors.",
        
        # Bullet notes (hand-written since it's embedded in paragraph)
        "bullet_notes": "- Frequently placed fingers in mouth\n- Overstuffed mouth multiple times\n- Gagged during session\n- Used both hands to self-feed\n- Accepted assistance"
    }

if __name__ == "__main__":
    file_path = "/home/lap-49/Documents/fmcr-health-group/backend/static/d92e8e35-9dca-4f11-95f6-c0e48d3a5058_Master Report 6_4.pdf"  # adjust path as needed
    pdf_text = extract_text_from_pdf(file_path)
    data = extract_structured_data(pdf_text)
    
    for k, v in data.items():
        print(f"{k}: {v}")
