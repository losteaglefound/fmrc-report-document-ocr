import os
import pdfplumber
import re
import openai
from datetime import datetime

from dotenv import load_dotenv

assert load_dotenv()

# ----------------------------
# PDF Parsing
# ----------------------------
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

# ----------------------------
# GPT Prompt
# ----------------------------
def build_prompt(data):
    return f"""
You are a pediatric occupational therapist writing a detailed clinical report based on extracted information from a child’s assessment files. Maintain a professional, clinically accurate tone matching the FMRC Health Master Report 6:4.

Please generate the report content using the following data:

### Demographics:
- Child’s Full Name: {data['child_name']}
- Date of Birth: {data['dob']}
- Chronological Age: {data['chronological_age']}
- UCI#: {data['uci']}
- Sex: {data['sex']}
- Preferred Language: {data['language']}
- Parent/Guardian Name: {data['guardian_name']}
- Date of Encounter: {data['encounter_date']}

---

### Clinical Notes (Convert these bullet points into a professional paragraph):
{data['bullet_notes']}

---

### Assessment Score Interpretations:

#### 🧠 Bayley-4:
- Cognitive: Scaled Score: {data['cog_score']}, Age Equivalent: {data['cog_age_eq']}, Delay: {data['cog_delay_pct']}
- Language: {data['lang_score']}, {data['lang_age_eq']}, {data['lang_delay_pct']}
- Motor: {data['motor_score']}, {data['motor_age_eq']}, {data['motor_delay_pct']}

Interpret these scores in relation to the child’s chronological age. Use classification labels (e.g., "Extremely Low", "Below Average") and describe functional implications observed in the child’s performance.

---

#### 🎧 SP2 (Sensory Profile 2):
- Seeking: {data['sp2_seeking']}, Avoiding: {data['sp2_avoiding']}, Sensitivity: {data['sp2_sensitivity']}, Registration: {data['sp2_registration']}

Explain these sensory tendencies with real-world examples (e.g., behavior during play, feeding, grooming). Describe how these patterns may affect occupational performance.

---

#### 🍴 CHOMPS:
- Scores: {data['chomps_scores_summary']}

Interpret domain-specific oral-motor concerns. Comment on feeding safety, bolus control, food hoarding, gag reflex, etc.

---

#### 🥄 PEDI-EAT:
- Symptoms: {data['pedieat_scores']}

Describe implications for feeding safety, endurance, selectivity, and caregiver support needs.

---

### Summary & Recommendations:
Generate a concise summary paragraph followed by:
- 3 measurable goals
- 2–3 specific recommendations for caregivers or next steps for care

---

### Additional Instructions:
- Only populate sections marked in green/yellow in the report template.
- Mark anything missing as “TBD”.
- Follow the tone, formatting, and language model of the Master Report 6:4.
"""

# ----------------------------
# GPT Execution
# ----------------------------
def call_openai_gpt(prompt, model="gpt-4o", temperature=0.4):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a clinical report writing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    file_path = "/home/lap-49/Documents/fmcr-health-group/backend/static/d92e8e35-9dca-4f11-95f6-c0e48d3a5058_Master Report 6_4.pdf"
    text = extract_text_from_pdf(file_path)
    structured_data = extract_structured_data(text)
    prompt = build_prompt(structured_data)
    
    print("🔍 Sending prompt to OpenAI...\n")
    report = call_openai_gpt(prompt)
    
    print("✅ Clinical Report Generated:\n")
    print(report)
