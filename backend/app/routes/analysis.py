import os
import tempfile
import shutil

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    UploadFile,
    File,
    Query,
)

from app.schemas import (
    AnalyzeRequest,
    ClinicalReport,
    ClinicalReportRecord,
)
from uuid import UUID

from app.services import AIService, AIServiceError
from app.services.ocr_service import OCRService
from app.services.pdf_service import PDFService
from app.services.database_service import DatabaseService

router = APIRouter(prefix="/api", tags=["Analysis"])
ai_service = AIService()
ocr_service = OCRService()
pdf_service = PDFService(ocr_service)
database_service = DatabaseService()


@router.post(
    "/analyze",
    response_model=ClinicalReport,
    status_code=status.HTTP_200_OK,
    summary="Analyze Clinical Document Text",
    description="Extracts structured clinical information from raw clinical text using AI.",
)
def analyze_clinical_text(payload: AnalyzeRequest) -> ClinicalReport:
    try:
        report = ai_service.analyze_clinical_text(payload.text)

        database_service.save_report(
            source_type="text",
            original_filename=None,
            extracted_text=payload.text,
            report=report.model_dump(),
        )

        return report
    except AIServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during text analysis: {str(e)}",
        )
@router.post(
    "/analyze/image",
    response_model=ClinicalReport,
    status_code=status.HTTP_200_OK,
    summary="Analyze Clinical Document Image",
    description="Extracts text from a clinical document image using OCR and analyzes it using AI.",
)
def analyze_clinical_image(
    file: UploadFile = File(...)
) -> ClinicalReport:

    allowed_types = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/webp": ".webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Please upload a PNG, JPEG, or WEBP image.",
        )

    temporary_path = None

    try:
        suffix = allowed_types[file.content_type]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temporary_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        extracted_text = ocr_service.extract_text(temporary_path)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No text could be extracted from the uploaded image.",
            )

        report = ai_service.analyze_clinical_text(extracted_text)

        database_service.save_report(
            source_type="image",
            original_filename=file.filename,
            extracted_text=extracted_text,
            report=report.model_dump(),
        )

        return report

    except AIServiceError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during image analysis: {str(e)}",
        )

    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)


@router.post(
    "/analyze/pdf",
    response_model=ClinicalReport,
    status_code=status.HTTP_200_OK,
    summary="Analyze Clinical Document PDF",
    description="Extracts text from a clinical PDF and analyzes it using AI.",
)
def analyze_clinical_pdf(
    file: UploadFile = File(...)
) -> ClinicalReport:

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Please upload a PDF file.",
        )

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:
            temporary_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        extracted_text = pdf_service.extract_text(temporary_path)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No text could be extracted from the uploaded PDF.",
            )

        report = ai_service.analyze_clinical_text(extracted_text)

        database_service.save_report(
            source_type="pdf",
            original_filename=file.filename,
            extracted_text=extracted_text,
            report=report.model_dump(),
        )

        return report

    except AIServiceError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during PDF analysis: {str(e)}",
        )

    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)
@router.get(
    "/reports",
    response_model=list[ClinicalReportRecord],
    status_code=status.HTTP_200_OK,
    summary="Get Clinical Report History",
    description="Returns saved clinical reports, optionally filtered by patient name.",
)
def get_clinical_reports(
    patient_name: str | None = Query(
        default=None,
        description="Search reports by patient name",
    ),
) -> list[ClinicalReportRecord]:
    try:
        rows = database_service.get_reports(patient_name)

        return [
            ClinicalReportRecord.model_validate(row)
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve clinical reports: {str(e)}",
        )