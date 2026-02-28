# SmartGradeVisionVault 🛡️🖼️

**SmartGradeVisionVault** is a stateless microservice designed for the automated detection and extraction of visual elements (diagrams, photos, illustrations, and handwritten drawings) from educational documents.

It leverages the spatial reasoning power of **Google Gemini 1.5 Flash** to identify elements and **OpenCV** for high-precision cropping and processing.

## 🚀 Features

- **Multi-Format Support**: Process both PDF documents and standard image files (`.png`, `.jpg`, `.pdf`).
- **AI-Powered Detection**: Uses Gemini 1.5 Flash for superior bounding box extraction without document-specific templates.
- **High-Precision Cropping**: Automated cropping with adaptive padding using OpenCV.
- **Parallel Processing**: Asynchronous page handling for fast extraction from large textbooks.
- **Stateless Architecture**: Zero-dependency logic (no database required), making it easy to deploy as a sidecar or independent service.
- **Flexible API**: Support for page filtering, custom output directories, and "Fast Scan" modes.

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python)
- **AI Engine**: Google Gemini 1.5 Flash
- **Document Parsing**: PyMuPDF (fitz)
- **Image Processing**: OpenCV & NumPy
- **Containerization**: Docker

## 📥 Installation

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sree16m/SmartGradeVisionVault.git
   cd SmartGradeVisionVault
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   OUTPUT_BASE_DIR=./output
   LOG_LEVEL=INFO
   ```

4. **Run the application**:
   ```bash
   python -m uvicorn main:app --reload
   ```

### Docker Setup

```bash
docker build -t smartgrade-vision-vault .
docker run -p 8000:8000 --env-file .env smartgrade-vision-vault
```

## 📖 Usage

### API Endpoint: `POST /api/v1/visuals/extract`

**Request Body:**
```json
{
  "input_path": "/path/to/textbook.pdf",
  "page_filter": [10, 11, 12],
  "enable_fast_scan": true
}
```

### CLI Testing
Use the provided test script to quickly verify extraction:
```bash
python test_extraction.py "path/to/document.pdf"
```

## 📂 Project Structure

- `src/api/`: FastAPI route definitions and Pydantic schemas.
- `src/core/`: Configuration and logging utilities.
- `src/services/`: Core logic for document handling, Gemini interaction, and image processing.
- `main.py`: Entry point for the service.
- `test_extraction.py`: Functional test script for the extraction pipeline.

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.
