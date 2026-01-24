import pdfplumber

def extract_text_by_page(pdf_path: str):
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({
                "page": i + 1,
                "text": text.strip()
            })

    return pages
