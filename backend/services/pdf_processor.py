import os
import shutil
from fastapi import UploadFile
from langchain_community.document_loaders import PyMuPDFLoader

async def save_and_process_pdf(file: UploadFile):
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return filepath
