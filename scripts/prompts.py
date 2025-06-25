
PROMPT = f"""
    You are a pediatric occupational therapist writing a detailed clinical report based on extracted information from a child’s assessment files. Maintain a professional, clinically accurate tone matching the FMRC Health Master Report 6:4.

    Please generate the report content using the following data:

    ### Demographics:
    - Child’s Full Name: {{child_name}}
    - Date of Birth: {{dob}}
    - Chronological Age: {{chronological_age}} (auto-calculated)
    - UCI#: {{uci}}
    - Sex: {{sex}}
    - Preferred Language: {{language}}
    - Parent/Guardian Name: {{guardian_name}}
    - Date of Encounter: {{encounter_date}}

    ---

    ### Clinical Notes (Convert these bullet points into a professional paragraph):
    {{bullet_notes}}

    ---

    ### Assessment Score Interpretations:

    #### 🧠 Bayley-4:
    - Cognitive: Scaled Score: {{cog_score}}, Age Equivalent: {{cog_age_eq}}, Delay: {{cog_delay_pct}}
    - Language: {{lang_score}}, {{lang_age_eq}}, {{lang_delay_pct}}
    - Motor: {{motor_score}}, {{motor_age_eq}}, {{motor_delay_pct}}

    Interpret these scores in relation to the child’s chronological age. Use classification labels (e.g., "Extremely Low", "Below Average") and describe functional implications observed in the child’s performance.

    ---

    #### 🎧 SP2 (Sensory Profile 2):
    - Seeking: {{sp2_seeking}}, Avoiding: {{sp2_avoiding}}, Sensitivity: {{sp2_sensitivity}}, Registration: {{sp2_registration}}

    Explain these sensory tendencies with real-world examples (e.g., behavior during play, feeding, grooming). Describe how these patterns may affect occupational performance.

    ---

    #### 🍴 CHOMPS:
    - Scores: {{chomps_scores_summary}}

    Interpret domain-specific oral-motor concerns. Comment on feeding safety, bolus control, food hoarding, gag reflex, etc.

    ---

    #### 🥄 PEDI-EAT:
    - Symptoms (Physiology, Processing, Mealtime Behavior, Selectivity): {{pedieat_scores}}

    Describe implications for feeding safety, endurance, selectivity, and caregiver support needs.

    ---

    ### Summary & Recommendations:
    Based on the child’s observed behaviors, assessment scores, and clinical impressions, generate a concise summary paragraph followed by:
    - 3 measurable goals
    - 2–3 specific recommendations for caregivers or next steps for care

    ---

    ### Additional Instructions:
    - Fill only the sections marked in **green/yellow** in the Google Docs template.
    - If any field is missing or unclear, mark it as “TBD” in the output.
    - Follow the tone, formatting, and language model of the Master Report 6:4.


"""