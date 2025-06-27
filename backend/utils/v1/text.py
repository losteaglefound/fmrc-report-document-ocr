import re

async def extract_field(pattern, text, default="", flags=0):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else default
