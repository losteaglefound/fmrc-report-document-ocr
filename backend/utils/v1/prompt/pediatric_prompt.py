
async def get_pediatric_prompt(data: dict) -> str:
    prompt = f"""
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

    return prompt