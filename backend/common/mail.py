from fastapi_mail import FastMail

from .config import setting

mail = FastMail(setting.MAIl_CONFIG)