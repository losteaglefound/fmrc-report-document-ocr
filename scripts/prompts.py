
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

async def get_prompt_json_with_structure(data: str):
    PROMPT_JSON = f"""
    You are a highly skilled pediatric occupational therapist and medical report writer. Based on the provided evaluation text extracted from a PDF, your task is to extract structured data and rewrite observations and test results into detailed, clinically accurate narratives.

    The text will contain demographic details, clinical observations, and standardized test results (Bayley-4, SP2, ChOMPS, PediEAT). Do not guess. If a section is missing, write `"Not available"`.

    This is the file context: {context}

    Use the tone and level of detail in the FMRC Health Group Master Report as your standard. Your final output should include the following sections:

    ---

    ### 📄 Output Format (Structured JSON-like)

    ```json
    {{
    "Demographics": {{
        "Name": "",
        "Dob": "",
        "Chronological Age": "",
        "Sex": "",
        "Language": "",
        "Parent Guardian": "",
        "Uci Number": "",
        "Service Coordinator": "",
        "Examiner": "",
        "Date Of Report": "",
        "Date Of Encounter": ""
    }},
    "Referral Reason And Background": {{
        "Background Info": "",
        "Birth And Medical History": "",
        "Speech Language Hearing": "",
        "Fine Motor Development": "",
        "Feeding History": "",
        "Dental And Oral Behaviors": ""
    }},
    "Test Observations": "",
    "Assessment Tools Used": [],
    "Bayley 4": {{
        "Cognitive": {{
        "Scaled Score": "",
        "Age Equivalent": "",
        "Narrative": ""
        }},
        "Receptive Communication": {{
        "Scaled Score": "",
        "Age Equivalent": "",
        "Narrative": ""
        }},
        "Expressive Communication": {{
        "Scaled Score": "",
        "Age Equivalent": "",
        "Narrative": ""
        }},
        "Fine Motor": {{
        "Scaled Score": "",
        "Age Equivalent": "",
        "Narrative": ""
        }},
        "Gross Motor": {{
        "Scaled Score": "",
        "Age Equivalent": "",
        "Narrative": ""
        }},
        "Social Emotional": {{
        "Scaled Score": "",
        "Narrative": ""
        }},
        "Adaptive Behavior": {{
        "Scaled Score": "",
        "Narrative": ""
        }}
    }},
    "Sp2 Summary": {{
        "Summary": "",
        "Implications": ""
    }},
    "Chomps Summary": {{
        "Score Breakdown": {{
        "Complex Movement Patterns": "",
        "Basic Movement Patterns": "",
        "Oral Motor Coordination": "",
        "Fundamental Oral Motor Skills": "",
        "Total Score": ""
        }},
        "Narrative": ""
    }},
    "Pedieat Summary": {{
        "Score Breakdown": {{
        "Physiologic Symptoms": "",
        "Mealtime Behaviors": "",
        "Selective Eating": "",
        "Oral Processing": "",
        "Total Score": ""
        }},
        "Narrative": ""
    }},
    "Physical Exam Summary": "",
    "Cranial Nerve Screening Summary": "",
    "Summary": "",
    "Recommendations": [
        "e.g. Feeding therapy one time per week...",
        "..."
    ],
    "Goals": [
        "Child will reduce finger use during mealtime...",
        "..."
    ]
    }}

    """

    return PROMPT_JSON


async def get_prompt_markdown_without_structure(data: str):
    PROMPT_MARKDOWN_WITHOUT_STRUCTURE =  f"""

    You are a highly skilled pediatric occupational therapist and medical report writer. Based on the provided evaluation text extracted from a PDF, your task is to extract structured data and rewrite observations and test results into detailed, clinically accurate narratives.

    The text will contain demographic details, clinical observations, and standardized test results (Bayley-4, SP2, ChOMPS, PediEAT). **Do not guess**. If a section is missing, write `"Not available"`.

    This is the file context: {data}

    ---

    ## 🔁 Output Format: Markdown

    ❗Return your final output as a **Markdown document**, following the structure shown below. This format will be used for generating a human-readable report in Google Docs. Use `**bold**` for section titles and keep the output readable with paragraph spacing.

    ---

    ### 📄 Markdown Output Structure
    """

    return PROMPT_MARKDOWN_WITHOUT_STRUCTURE


async def get_prompt_markdown_with_structure(data: str):
    PROMPT_MARKDOWN_WITH_STRUCTURE = f"""
    You are a highly skilled pediatric occupational therapist and medical report writer. Based on the provided evaluation text extracted from a PDF, your task is to extract structured data and rewrite observations and test results into detailed, clinically accurate narratives.

    The text will contain demographic details, clinical observations, and standardized test results (Bayley-4, SP2, ChOMPS, PediEAT). **Do not guess**. If a section is missing, write `"Not available"`.

    This is the file context: {data}

    ---

    ## 🔁 Output Format: Markdown

    ❗Return your final output as a **Markdown document**, following the exact structure and formatting below. This report will be copied into Google Docs for final submission, so follow this format precisely:

    ---

    ### 📄 Markdown Output Structure

    **Clinical Evaluation Report**

    **Client Information**

    - Name: ...
    - Date of Birth: ...
    - Chronological Age: ...
    - Sex: ...
    - Primary Language: ...
    - Parent/Guardian: ...
    - Service Coordinator: ...
    - Examiner: ...
    - Date of Report: ...
    - Date of Encounter: ...

    **Reason for Referral and Background Information**

    Summarize the reason for referral and include bulleted or paragraph-style entries for:

    - Birth & Medical History
    - Speech, Language, & Hearing History
    - Fine Motor Development
    - Feeding History
    - Dental History & Oral Behaviors

    **Test Observations**

    Summarize direct clinical observations during the session in paragraph form.

    **Assessment Tools Used**

    List the standardized assessments used:
    - [Tool 1]
    - [Tool 2]
    ...

    **Bayley Scales of Infant and Toddler Development - Fourth Edition (BSID-4)**

    Summarize each domain in bullet or paragraph form:
    - Cognitive Scale
    - Receptive Communication
    - Expressive Communication
    - Fine Motor
    - Gross Motor
    - Social-Emotional
    - Adaptive Behavior

    **Toddler Sensory Profile 2 (SP2)**

    Narrative interpretation of sensory processing patterns and implications for function.

    **Child Oral and Motor Proficiency Scale (ChOMPS)**

    Narrative summary and feeding implications.

    **Pediatric Eating Assessment Tool (PediEAT)**

    Narrative interpretation and clinical impact of results.

    **Physical Examination**

    List or describe physical findings including:
    - Body
    - Head & Neck
    - Face
    - Jaw
    - Lips
    - Tongue
    - Cheeks
    - Palate

    **Cranial Nerve Screening**

    Summarize screening results:
    - CN I (Olfactory): ...
    - CN V (Trigeminal): ...
    - CN VII (Facial): ...
    - CN IX (Glossopharyngeal): ...
    - CN X (Vagus): ...
    - CN XI (Accessory): ...
    - CN XII (Hypoglossal): ...

    **Summary**

    Summarize findings across all assessments and observations.

    **Recommendations**

    - Recommendation 1
    - Recommendation 2
    ...

    **Goals**

    - Goal 1
    - Goal 2
    ...

    **Contact Information**

    - Fushia Crooms, MOT, OTR/L  
    - Email: fushia@fmrchealth.com  
    - Phone #: 323-229-6025 Ext. 1
    """

    return PROMPT_MARKDOWN_WITH_STRUCTURE