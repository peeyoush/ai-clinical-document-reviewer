import os
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError
from app.schemas.analysis import ClinicalReport


class AIServiceError(Exception):
    """Custom exception raised when the AI Service encounters an error."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AIService:
    """Service to interact with the external Gemini LLM for clinical document analysis."""

    def analyze_clinical_text(self, text: str) -> ClinicalReport:
        """
        Sends clinical text to the Gemini LLM and returns a validated ClinicalReport review.
        Includes automatic retry for transient 503/429 high demand spikes.
        """
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

        if not api_key or api_key.strip() == "" or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
            raise AIServiceError(
                message="LLM API key is missing or unconfigured. Please set GEMINI_API_KEY in your .env file.",
                status_code=500,
            )

        system_instruction = (
            "You are an expert AI clinical document reviewer.\n"
            "Your objective is to analyze clinical documentation and produce a comprehensive, structured clinical review report.\n"
            "You act strictly as an assistive clinical documentation review tool, NOT an autonomous diagnostic or treatment system.\n\n"
            "STRICT CLINICAL REVIEW DIRECTIVES:\n"
            "1. EXPLICIT EXTRACTION ONLY: Extract symptoms, diagnoses, medications, vitals, allergies, and observations strictly as documented in the text. NEVER invent, assume, or extrapolate any patient demographics, clinical findings, diagnoses, or medications.\n"
            "2. REPORT SUMMARY: Generate a clear, concise report_summary summarizing the patient presentation, documented clinical findings, and current clinical status.\n"
            "3. NO INVENTED DIAGNOSES: If no formal diagnosis is explicitly documented, keep the 'diagnoses' list EMPTY and add a note in 'requires_review' stating that no diagnosis was documented.\n"
            "4. PRESERVE UNCERTAINTY: If a diagnosis or condition is described as suspected, possible, or rule-out, preserve that exact clinical uncertainty in 'diagnoses' (e.g., 'Suspected pneumonia') rather than stating it as a definitive diagnosis.\n"
            "5. MISSING INFORMATION IDENTIFICATION: Thoroughly identify clinically relevant missing data (e.g. absent patient demographics, missing vital signs such as heart rate or temperature, unstated medication dosages/schedules, missing follow-up plans) and record them in 'missing_information'.\n"
            "6. CONTRADICTIONS & INCONSISTENCIES: Record any contradictory, ambiguous, or conflicting clinical statements or numbers in 'potential_inconsistencies'.\n"
            "7. HUMAN REVIEW FLAGS: Populate 'requires_review' with critical items that warrant clinician verification (e.g., elevated or abnormal vital signs, lack of documented diagnosis, unverified medication dosages, suspected conditions, or incomplete treatment plans).\n"
            "8. ASSISTIVE ROLE: You provide structured analysis to support human clinical document review; you do NOT generate autonomous medical diagnoses or treatment recommendations."
        )

        prompt = f"Clinical Document Text:\n\"\"\"\n{text}\n\"\"\""

        client = genai.Client(api_key=api_key)
        max_retries = 3
        last_exception = None

        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type="application/json",
                        response_schema=ClinicalReport,
                        temperature=0.1,
                    ),
                )

                if not response.text:
                    raise AIServiceError(
                        message="LLM API returned an empty response.",
                        status_code=502,
                    )

                report = ClinicalReport.model_validate_json(response.text)
                return report

            except APIError as e:
                last_exception = e
                if ("503" in str(e) or "UNAVAILABLE" in str(e) or "429" in str(e)) and attempt < max_retries:
                    time.sleep(2 * attempt)
                    continue
                raise AIServiceError(
                    message=f"Gemini API Error: {str(e)}",
                    status_code=502,
                )
            except AIServiceError:
                raise
            except Exception as e:
                last_exception = e
                if attempt < max_retries and ("503" in str(e) or "UNAVAILABLE" in str(e)):
                    time.sleep(2 * attempt)
                    continue
                raise AIServiceError(
                    message=f"Failed to process clinical document: {str(e)}",
                    status_code=500,
                )

        raise AIServiceError(
            message=f"Gemini API Error after {max_retries} attempts: {str(last_exception)}",
            status_code=502,
        )
