from fastapi import FastAPI
from src.api.v1.endpoints import router as api_router
from src.core.logging import logger

app = FastAPI(title="SmartGradeVisionVault", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("SmartGradeVisionVault starting up...")

@app.get("/")
async def root():
    return {"message": "SmartGradeVisionVault is operational"}
