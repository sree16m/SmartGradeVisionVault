import fitz  # PyMuPDF
import os
from ..core.logging import logger

class DocumentHandler:
    @staticmethod
    def extract_page_as_image(pdf_path: str, page_number: int, output_path: str):
        """Extracts a specific page from a PDF and saves it as an image."""
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(page_number)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Better resolution
            pix.save(output_path)
            doc.close()
            return output_path
        except Exception as e:
            logger.error(f"Error extracting page {page_number} from {pdf_path}: {e}")
            raise e

    @staticmethod
    def get_page_count(pdf_path: str) -> int:
        """Returns the number of pages in a PDF."""
        try:
            doc = fitz.open(pdf_path)
            count = len(doc)
            doc.close()
            return count
        except Exception as e:
            logger.error(f"Error getting page count for {pdf_path}: {e}")
            raise e
