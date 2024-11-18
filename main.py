from datetime import datetime
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Union
from collections import Counter
from services.date_check import get_passport_date_format
from services.file_handler import save_temp_file, encode_image
from services.fireworks_client import extract_document_details
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import httpx
from httpx import RemoteProtocolError
import backoff

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Result(BaseModel):
    document_type: str
    document_number: str
    name: str
    sex: str
    dob: str
    expiry_date: str
    address: str
    error: Union[str, None] = None

@app.get("/ready")
async def ready() -> Dict[str, str]:
    """Returns a simple health check endpoint to indicate the application is ready."""
    return {"message": "Ready"}

def get_most_frequent_value(values: List[str]) -> str:
    if not values:
        return None
    return Counter(values).most_common(1)[0][0]

@backoff.on_exception(backoff.expo, RemoteProtocolError, max_tries=5)
async def extract_details_retry(image_base64: str) -> Dict:
    response = extract_document_details(image_base64)
    return json.loads(response)

@app.post("/verify_identity/")
async def verify_identity(
    full_name: str = Form(...),
    dob: str = Form(...),
    address: str = Form(...),
    document: UploadFile = File(...),
) -> Dict:
    file_path = save_temp_file(document)
    image_base64 = encode_image(file_path)

    # Perform multiple extraction attempts in parallel without using ThreadPoolExecutor
    extraction_attempts = 5
    tasks = [extract_details_retry(image_base64) for _ in range(extraction_attempts)]
    try:
        extracted_results = await asyncio.gather(*tasks)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

    aggregated_result = {}
    keys = extracted_results[0].keys()
    for key in keys:
        values = [result[key] for result in extracted_results if key in result]
        aggregated_result[key] = get_most_frequent_value(values)

    status, date_format = get_passport_date_format(dob, aggregated_result["dob"])
    if not status:
        os.remove(file_path)
        return {"error": "Invalid dates: Verification failed"}

    try:
        aggregated_result["dob"] = datetime.strptime(aggregated_result["dob"], date_format).strftime("%Y-%m-%d")
        aggregated_result["expiry_date"] = datetime.strptime(aggregated_result["expiry_date"], date_format).strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        aggregated_result["error"] = "Date parsing failed: Verification failed"
        return aggregated_result

    if datetime.strptime(aggregated_result["expiry_date"], "%Y-%m-%d") < datetime.now():
        aggregated_result["error"] = "Expired document: Verification failed"
        return aggregated_result

    os.remove(file_path)
    return aggregated_result
