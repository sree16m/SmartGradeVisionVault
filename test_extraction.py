import requests
import sys
import json
import os

def test_extraction(input_path, output_dir=None):
    url = "http://localhost:8000/api/v1/visuals/extract"
    payload = {
        "input_path": input_path,
        "output_dir": output_dir,
        "enable_fast_scan": True
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"Status: {result.get('status')}")
        print(f"Document: {result.get('document')}")
        print(f"Extracted {len(result.get('assets', []))} assets.")
        
        for i, asset in enumerate(result.get('assets', [])):
            print(f"Asset {i+1}: {asset['description']}")
            print(f"  File: {asset['file']}")
            print(f"  Page: {asset['page_number']}")
            print(f"  Coordinates: {asset['coordinates']}")
            
    except Exception as e:
        print(f"Error: {e}")
        if 'response' in locals() and response is not None:
            print(f"Detail: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_extraction.py <input_path> [<output_dir>]")
        sys.exit(1)
    
    input_path = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None
    
    test_extraction(input_path, output_dir)
