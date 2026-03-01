import cv2
import os
import json
import numpy as np
from ..core.logging import logger
from ..core.config import settings
from google.cloud import storage
from google.oauth2 import service_account

def get_gcs_client():
    if not settings.GCS_BUCKET_NAME:
        raise ValueError("GCS_BUCKET_NAME is not set")
    if settings.GOOGLE_APPLICATION_CREDENTIALS_JSON:
        credentials_dict = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS_JSON)
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        return storage.Client(credentials=credentials, project=credentials.project_id)
    return storage.Client()

def upload_to_gcs(local_path: str, destination_blob_name: str) -> str:
    client = get_gcs_client()
    bucket = client.bucket(settings.GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_path)
    return f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/{destination_blob_name}"

class ImageProcessor:
    @staticmethod
    def crop_and_save(image_path: str, coordinates: list, output_path: str):
        """Crops an image based on normalized coordinates [ymin, xmin, ymax, xmax] and optionally uploads to GCS."""
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
            
            if settings.USE_CLOUD_STORAGE:
                # Include parent folder name to avoid collisions
                parent_folder = os.path.basename(os.path.dirname(output_path))
                blob_name = f"visuals/{parent_folder}/{os.path.basename(output_path)}"
                logger.info(f"Uploading {output_path} to GCS object {blob_name}")
                public_url = upload_to_gcs(output_path, blob_name)
                return public_url
                
            return output_path
        except Exception as e:
            logger.error(f"Error cropping image {image_path}: {e}")
            raise e
