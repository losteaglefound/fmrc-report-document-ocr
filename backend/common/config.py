import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv


assert load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

open_ai_models = Literal["gpt-4o", "gpt-4o-mini"]
"""OpenAI models"""

class Setting:
    

    @property
    def STATIC_DIR(self):
        static_path: str = os.path.join(BASE_DIR, "static")
        if not os.path.exists(os.path.join(static_path)):
            os.makedirs(static_path)
        return static_path
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: open_ai_models = os.getenv("OPENAI_MODEL")
    GOOGLE_CLIENT_SCOPE: list[str] = os.getenv("GOOGLE_CLIENT_SCOPE").split(",")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")

setting = Setting()
