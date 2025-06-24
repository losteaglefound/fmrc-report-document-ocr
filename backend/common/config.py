import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class Setting:
    @property
    def STATIC_DIR(self):
        static_path: str = os.path.join(BASE_DIR, "static")
        if not os.path.exists(os.path.join(static_path)):
            os.makedirs(static_path)
        return static_path
    

setting = Setting()
