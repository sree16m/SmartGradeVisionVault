import google.generativeai as genai
from ..core.config import settings
from ..core.logging import logger
import json
import re

class VisualAgent:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def detect_visuals(self, image_path: str):
        """Detects visual elements in an image and returns bounding boxes."""
        try:
            sample_file = genai.upload_file(path=image_path, display_name="Page Scan")
            
            prompt = """
            Identify all visual elements like diagrams, photos, illustrations, or handwritten drawings in this image.
            For each element, provide:
            1. A brief description of the element.
            2. The bounding box coordinates in the format [ymin, xmin, ymax, xmax] where values are 0-1000.
            
            Return the result as a JSON array of objects with 'description' and 'coordinates' keys.
            """
            
            response = self.model.generate_content([sample_file, prompt])
            
            # Clean up the response to extract JSON
            json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                logger.warning(f"No JSON found in Gemini response for {image_path}")
                return []
                
        except Exception as e:
            logger.error(f"Error detecting visuals in {image_path}: {e}")
            raise e
