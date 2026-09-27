from pathlib import Path
from tempfile import TemporaryDirectory

import pymupdf
from pypdf import PdfReader

from app.services.ocr_service import OCRService


class PDFService:
    def __init__(self, ocr_service: OCRService):
        self.ocr_service = ocr_service

    def extract_text(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)

        extracted_pages = []

        with pymupdf.open(pdf_path) as pdf_document:
            for page_number, page in enumerate(reader.pages):
                text = page.extract_text()

                if text and text.strip():
                    extracted_pages.append(text.strip())
                    continue

                # No text layer found, so render this PDF page
                # as an image and send it through PaddleOCR.
                with TemporaryDirectory() as temp_dir:
                    image_path = Path(temp_dir) / f"page_{page_number + 1}.png"

                    pixmap = pdf_document[page_number].get_pixmap(dpi=200)
                    pixmap.save(str(image_path))

                    ocr_text = self.ocr_service.extract_text(
                        str(image_path)
                    )

                    if ocr_text.strip():
                        extracted_pages.append(ocr_text.strip())

        return "\n\n".join(extracted_pages)