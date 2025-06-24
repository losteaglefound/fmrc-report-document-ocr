import sys
import pdfplumber


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def main():
    if len(sys.argv) != 2:
        print("Usage: python pdf-reader.py <path_to_pdf>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    try:
        content = extract_text_from_pdf(pdf_path)
        print(content)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
