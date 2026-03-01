import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OUTPUT_BASE_DIR: str = os.getenv("OUTPUT_BASE_DIR", "e:/SmartGradeVisionVault/output")
    LOG_LEVEL: str = "INFO"
    
    # Cloud Storage Settings
    USE_CLOUD_STORAGE: bool = os.getenv("USE_CLOUD_STORAGE", "False").lower() == "true"
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "")
    GOOGLE_APPLICATION_CREDENTIALS_JSON: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "")
    
    
    class Config:
        env_file = ".env"

settings = Settings()
