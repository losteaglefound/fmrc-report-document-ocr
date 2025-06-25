import os

from dotenv import load_dotenv


assert load_dotenv(override=True)


class Setting:
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SCOPE: str = os.getenv("GOOGLE_CLIENT_SCOPE").split(",")

setting = Setting()