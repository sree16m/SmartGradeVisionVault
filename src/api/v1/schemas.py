from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractionRequest(BaseModel):
    input_path: str = Field(..., description="Absolute path to the input PDF or image file.")
    output_dir: Optional[str] = Field(None, description="Directory where snippets should be saved. Defaults to a unique subfolder in OUTPUT_BASE_DIR.")
    page_filter: Optional[List[int]] = Field(None, description="List of page numbers (0-indexed) to process.")
    enable_fast_scan: bool = Field(False, description="Whether to perform a quick scan to detect pages with visuals first.")

class VisualAsset(BaseModel):
    file: str
    description: str
    coordinates: List[float]
    page_number: int

class ExtractionResponse(BaseModel):
    document: str
    assets: List[VisualAsset]
    status: str = "success"
