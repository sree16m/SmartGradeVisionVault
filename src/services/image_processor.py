import cv2
import os
import numpy as np
from ..core.logging import logger

class ImageProcessor:
    @staticmethod
    def crop_and_save(image_path: str, coordinates: list, output_path: str):
        """Crops an image based on normalized coordinates [ymin, xmin, ymax, xmax]."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
                
            h, w = img.shape[:2]
            ymin, xmin, ymax, xmax = coordinates
            
            # Convert normalized to pixel coordinates
            left = int(xmin * w / 1000)
            top = int(ymin * h / 1000)
            right = int(xmax * w / 1000)
            bottom = int(ymax * h / 1000)
            
            # Add padding
            padding = 10
            left = max(0, left - padding)
            top = max(0, top - padding)
            right = min(w, right + padding)
            bottom = min(h, bottom + padding)
            
            crop_img = img[top:bottom, left:right]
            cv2.imwrite(output_path, crop_img)
            return output_path
        except Exception as e:
            logger.error(f"Error cropping image {image_path}: {e}")
            raise e
