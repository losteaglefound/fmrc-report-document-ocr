import pdfplumber


async def pdf_is_native(file: str | bytes) -> bool:
    """
    The function check is the pdf is native or scanned.
    Args:
        file: Takes the path of the pdf file.
    Returns:
        True if the pdf is native, False if pdf is scanned
    """
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                return True
    return False