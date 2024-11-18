# services/file_handler.py
import shutil
import base64
from fastapi import UploadFile

def save_temp_file(document: UploadFile) -> str:
    file_path = f"temp_{document.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)
    return file_path

def encode_image(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def load_api_key(file_path='config.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()
