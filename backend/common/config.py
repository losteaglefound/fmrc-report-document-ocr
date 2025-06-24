import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class Setting:
    STATIC_DIR = os.path.join(BASE_DIR, "static")

setting = Setting()
