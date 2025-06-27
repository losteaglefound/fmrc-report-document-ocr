import os
import sys
from glob import glob


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "backend", "upload")


def remove_pdf(file_path):
    files = glob(f"{file_path}/*.pdf")
    for file in files:
        print(f"Removing file -> %s" % file)
        os.remove(file)


if __name__ == "__main__":
    remove_pdf(STATIC_DIR)
    sys.exit(0)