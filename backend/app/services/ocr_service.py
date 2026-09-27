from paddleocr import PaddleOCR
class OCRService:
    def __init__(self):
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

    def extract_text(self, image_path: str) -> str:
        results = self.ocr.predict(image_path)

        extracted_text = []

        for result in results:
            texts = result["rec_texts"]
            extracted_text.extend(texts)

        return "\n".join(extracted_text)