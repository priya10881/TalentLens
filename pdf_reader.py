
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """Extract text from a text-based PDF resume."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume file not found: {path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError("Please provide a PDF file.")

    reader = PdfReader(str(path))
    extracted_pages = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        extracted_pages.append(page_text)

    return "\n".join(extracted_pages).strip()


if __name__ == "__main__":
    pdf_file = Path(__file__).parent / "sample_resume.pdf"

    try:
        resume_text = extract_text_from_pdf(pdf_file)

        print("\n========== EXTRACTED RESUME TEXT ==========")
        print(resume_text if resume_text else "No text found in PDF.")
        print("===========================================")

    except (FileNotFoundError, ValueError) as error:
        print("Error:", error)
