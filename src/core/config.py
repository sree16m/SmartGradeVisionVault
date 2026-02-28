import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OUTPUT_BASE_DIR: str = os.getenv("OUTPUT_BASE_DIR", "e:/SmartGradeVisionVault/output")
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
