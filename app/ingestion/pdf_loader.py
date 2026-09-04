from pathlib import Path
import fitz


def load_pdf(file_path: str):

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            "The provided file is not a PDF."
        )

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        pages.append({
            "text": text,
            "metadata": {
                "source": pdf_path.name,
                "page": page_number + 1
            }
        })

    document.close()

    return pages