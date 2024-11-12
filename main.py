import base64
import os
import time

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up your API keys
TILE_API_KEY = os.getenv("TILE_API_KEY")
file_path = "/Users/henry/Desktop/pdf-ticket-both-ways.pdf"

# 1. Upload the file
url = "https://api.tile.run/v1/upload"
headers = {
    "Authorization": f"Bearer {TILE_API_KEY}",
    "Content-Type": "application/json",
}

with open(file_path, "rb") as file:
    base_64_file = base64.b64encode(file.read()).decode("utf-8")
    data = {
        "file_base64": base_64_file,
        "content_type": "application/pdf",
    }  # Remember to change this to the correct content type
    response = requests.post(url=url, headers=headers, json=data).json()
    file_id = response["file_id"]

# 2. Extract data using a schema
url = "https://api.tile.run/v1/extract"
data = {
    "file_id": file_id,
    "document_schema": {
        "name": "invoices",
        "description": "A schema for invoices",
        "fields": [
            {
                "name": "Invoice number",
                "description": "The unique identifier for the invoice",
                "type": "string",
            }
        ],
    },
}
post_response = requests.post(url, headers=headers, json=data).json()
extraction_id = post_response["extraction_id"]

# 3. Poll for results
url = f"https://api.tile.run/v1/extract/{extraction_id}"

for i in range(60 * 5):  # Poll every second for 5 minutes
    response_data = requests.get(url, headers=headers).json()
    if response_data and "status" in response_data:
        if (
            response_data["status"] == "PENDING"
            or response_data["status"] == "PROCESSING"
        ):
            print("Extraction processing...")
        elif response_data["status"] == "COMPLETED":
            print("Extraction completed")
            print(response_data["extracted_data"])
            break
        elif response_data["status"] == "FAILED":
            print("Extraction failed")
            print(response_data)
            break
    time.sleep(1)
