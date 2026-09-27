from app.services.database_service import DatabaseService


database_service = DatabaseService()


test_report = {
    "report_summary": "Database connectivity test",
    "patient_information": {},
    "symptoms": [],
    "diagnoses": [],
    "medications": [],
    "vitals": {},
    "allergies": [],
    "clinical_observations": [],
    "clinical_concerns": [],
    "missing_information": [],
    "potential_inconsistencies": [],
    "requires_review": [],
}


result = database_service.save_report(
    source_type="text",
    original_filename=None,
    extracted_text="Database connectivity test",
    report=test_report,
)


print("Saved report:")
print(result)