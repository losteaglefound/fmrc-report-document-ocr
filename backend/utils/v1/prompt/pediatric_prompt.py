
async def get_pediatric_prompt(data: dict) -> str:
    prompt = f"""
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
    return prompt