from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        description="Raw clinical text to be analyzed",
        examples=["Patient presents with high fever and cough for 3 days. BP 120/80."],
    )

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Clinical text must not be empty or contain only whitespace.")
        return value.strip()


class PatientInformation(BaseModel):
    name: Optional[str] = Field(default=None, description="Patient full name if stated")
    age: Optional[str] = Field(default=None, description="Patient age if stated")
    gender: Optional[str] = Field(default=None, description="Patient gender if stated")
    mrn: Optional[str] = Field(default=None, description="Medical Record Number / ID if stated")


class Vitals(BaseModel):
    blood_pressure: Optional[str] = Field(default=None, description="Blood pressure reading")
    heart_rate: Optional[str] = Field(default=None, description="Heart rate / pulse")
    temperature: Optional[str] = Field(default=None, description="Body temperature")
    respiratory_rate: Optional[str] = Field(default=None, description="Respiratory rate")
    oxygen_saturation: Optional[str] = Field(default=None, description="SpO2 percentage")


class ClinicalReport(BaseModel):
    report_summary: str = Field(
        default="",
        description="Concise summary of the clinical document",
    )
    patient_information: PatientInformation = Field(
        default_factory=PatientInformation,
        description="Patient demographic information",
    )
    symptoms: List[str] = Field(
        default_factory=list,
        description="List of patient-reported symptoms",
    )
    diagnoses: List[str] = Field(
        default_factory=list,
        description="List of clinical diagnoses",
    )
    medications: List[str] = Field(
        default_factory=list,
        description="List of medications mentioned",
    )
    vitals: Vitals = Field(
        default_factory=Vitals,
        description="Vital signs recorded",
    )
    allergies: List[str] = Field(
        default_factory=list,
        description="Documented allergies",
    )
    clinical_observations: List[str] = Field(
        default_factory=list,
        description="Objective clinical observations and exam findings",
    )
    clinical_concerns: List[str] = Field(
        default_factory=list,
        description="Flagged concerns or urgent issues requiring attention",
    )
    missing_information: List[str] = Field(
        default_factory=list,
        description="Expected clinical details missing from the document",
    )
    potential_inconsistencies: List[str] = Field(
        default_factory=list,
        description="Conflicting or contradictory information detected in the text",
    )
    requires_review: List[str] = Field(
        default_factory=list,
        description="Uncertain, vague, or critical items needing clinician verification",
    )
