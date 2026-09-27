import os

from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


class DatabaseService:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_secret_key = os.getenv("SUPABASE_SECRET_KEY")

        if not supabase_url:
            raise RuntimeError("SUPABASE_URL is missing from .env")

        if not supabase_secret_key:
            raise RuntimeError("SUPABASE_SECRET_KEY is missing from .env")

        self.client = create_client(
            supabase_url,
            supabase_secret_key,
        )

    def save_report(
        self,
        source_type: str,
        original_filename: str | None,
        extracted_text: str | None,
        report: dict,
    ):
        response = (
            self.client
            .table("clinical_reports")
            .insert({
                "source_type": source_type,
                "original_filename": original_filename,
                "extracted_text": extracted_text,
                "report": report,
            })
            .execute()
        )

        return response.data