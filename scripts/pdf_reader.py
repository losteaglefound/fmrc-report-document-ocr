import sys
import pdfplumber
import re



def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or "" + "\n"
    return text


def extract_fields(text):
    return {
        "child_name": re.search(r"Child(?:'s)? Name:\s*(.+)", text, re.I).group(1) if re.search(r"Child(?:'s)? Name:\s*", text, re.I) else "TBD",
        "dob": re.search(r"Date of Birth:\s*(\d{2}/\d{2}/\d{4})", text).group(1) if re.search(r"Date of Birth:\s*", text) else "TBD",
        "uci": re.search(r"UCI#:\s*(\w+)", text).group(1) if re.search(r"UCI#:\s*", text) else "TBD",
        "language": re.search(r"Language:\s*(\w+)", text).group(1) if re.search(r"Language:\s*", text) else "TBD",
        "encounter_date": re.search(r"Date of Encounter:\s*(\d{2}/\d{2}/\d{4})", text).group(1) if re.search(r"Date of Encounter:\s*", text) else "TBD",
        "guardian_name": re.search(r"Parent(?:/Guardian)? Name:\s*(.+)", text, re.I).group(1) if re.search(r"Parent(?:/Guardian)? Name:\s*", text, re.I) else "TBD",
        # Add more rules as needed
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python pdf-reader.py <path_to_pdf>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    try:
        content = extract_text_from_pdf(pdf_path)
        output = extract_fields(content)
        print(output)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
