import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig


assert load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent
"""Project base directory"""

open_ai_models = Literal["gpt-4o", "gpt-4o-mini"]
"""OpenAI models"""

google_document_permissions = Literal['reader', 'writer', 'commenter']
"""Google document permissions"""

google_permission_roles = Literal['user', 'group', 'anyone']
"""Google permission roles"""



class Setting:
    @property
    def UPLOAD_DIR(self):
        static_path: str = os.path.join(BASE_DIR, "upload")
        if not os.path.exists(os.path.join(static_path)):
            os.makedirs(static_path)
        return static_path
    
    MAIl_CONFIG = ConnectionConfig(
        MAIL_USERNAME = os.getenv("GOOGLE_USERNAME"),
        MAIL_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD"),
        MAIL_FROM = os.getenv("GOOGLE_EMAIL"),
        MAIL_PORT = 465,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_STARTTLS = False,
        MAIL_SSL_TLS = True,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: open_ai_models = os.getenv("OPENAI_MODEL")
    GOOGLE_CLIENT_SCOPE: list[str] = os.getenv("GOOGLE_CLIENT_SCOPE").split(",")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_DOCUMENT_DEFAULT_PERM_TYPE: google_document_permissions = "reader"
    GOOGLE_DOCUMENT_DEFAULT_PERM_ROLE: google_permission_roles = "user"
    TEMPLATES_DIR: str = os.path.join(BASE_DIR, "templates")
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")

setting = Setting()
