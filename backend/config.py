"""Application configuration sourced from environment variables."""
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_name: str = "NCBI BioIntelligence"
    ncbi_email: str = os.getenv("NCBI_EMAIL", "")
    ncbi_api_key: str = os.getenv("NCBI_API_KEY", "")
    ncbi_tool: str = os.getenv("NCBI_TOOL", "NCBI_BioIntelligence")
    ncbi_base_url: str = os.getenv("NCBI_BASE_URL", "https://eutils.ncbi.nlm.nih.gov/entrez/eutils")
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "25"))
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

settings = Settings()
