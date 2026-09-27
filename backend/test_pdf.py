from app.services.ocr_service import OCRService
from app.services.pdf_service import PDFService


ocr_service = OCRService()
pdf_service = PDFService(ocr_service)

text = pdf_service.extract_text(
    "test_data/scanned_clinical_note.pdf"
)

print("\n--- EXTRACTED SCANNED PDF TEXT ---\n")
print(text)