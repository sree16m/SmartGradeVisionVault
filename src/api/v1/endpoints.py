from fastapi import APIRouter, HTTPException, BackgroundTasks
from .schemas import ExtractionRequest, ExtractionResponse, VisualAsset
from ...services.document_handler import DocumentHandler
from ...services.visual_agent import VisualAgent
from ...services.image_processor import ImageProcessor
from ...core.config import settings
from ...core.logging import logger
import os
import uuid

router = APIRouter()
visual_agent = VisualAgent()

@router.post("/extract", response_model=ExtractionResponse)
async def extract_visuals(request: ExtractionRequest):
    """
    Extracts visual elements from a document.
    """
    if not os.path.exists(request.input_path):
        raise HTTPException(status_code=400, detail=f"Input path does not exist: {request.input_path}")
    
    # Resolve output directory
    output_dir = request.output_dir or os.path.join(settings.OUTPUT_BASE_DIR, str(uuid.uuid4()))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"Starting extraction for {request.input_path} into {output_dir}")
    
    assets = []
    
    try:
        # Determine pages to process
        if request.input_path.lower().endswith('.pdf'):
            total_pages = DocumentHandler.get_page_count(request.input_path)
            pages_to_process = request.page_filter if request.page_filter is not None else list(range(total_pages))
            
            async def process_page(page_num):
                if page_num >= total_pages:
                    logger.warning(f"Page {page_num} out of range for {request.input_path}")
                    return []
                
                # Extract page as image
                page_image_path = os.path.join(output_dir, f"page_{page_num}.png")
                DocumentHandler.extract_page_as_image(request.input_path, page_num, page_image_path)
                
                # Detect visuals
                detections = await visual_agent.detect_visuals(page_image_path)
                
                page_assets = []
                # Process each detection
                for i, detection in enumerate(detections):
                    crop_filename = f"page_{page_num}_crop_{i}.png"
                    crop_path = os.path.join(output_dir, crop_filename)
                    
                    ImageProcessor.crop_and_save(page_image_path, detection['coordinates'], crop_path)
                    
                    page_assets.append(VisualAsset(
                        file=crop_path,
                        description=detection['description'],
                        coordinates=detection['coordinates'],
                        page_number=page_num
                    ))
                return page_assets

            import asyncio
            results = await asyncio.gather(*(process_page(p) for p in pages_to_process))
            for page_assets in results:
                assets.extend(page_assets)
                
                # Optionally remove intermediate page images
                # os.remove(page_image_path)
                
        else:  # Assume direct image file
            detections = await visual_agent.detect_visuals(request.input_path)
            for i, detection in enumerate(detections):
                crop_filename = f"crop_{i}.png"
                crop_path = os.path.join(output_dir, crop_filename)
                
                ImageProcessor.crop_and_save(request.input_path, detection['coordinates'], crop_path)
                
                assets.append(VisualAsset(
                    file=crop_path,
                    description=detection['description'],
                    coordinates=detection['coordinates'],
                    page_number=0
                ))
        
        return ExtractionResponse(document=request.input_path, assets=assets)
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
