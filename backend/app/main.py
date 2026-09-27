from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes import analysis_router
from app.schemas import HealthStatus

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="AI Clinical Document Reviewer API",
    description="API backend for AI Clinical Document Reviewer",
    version="0.1.0",
)

# Register routers
app.include_router(analysis_router)


@app.get("/api/health", response_model=HealthStatus, tags=["Health"])
def health_check():
    return HealthStatus(status="ok")
