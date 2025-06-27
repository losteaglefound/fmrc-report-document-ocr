import logging
import os
from typing import Literal

from dotenv import load_dotenv


assert load_dotenv(override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Setting:
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SCOPE: str = os.getenv("GOOGLE_CLIENT_SCOPE").split(",")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_DEFAULT_MODEL: str = 'gpt-4o'
    OPEN_AI_MODELS: list = Literal["gpt-4o"]

setting = Setting()