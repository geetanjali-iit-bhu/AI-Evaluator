import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import parse_answer_sheet
from app.models.schemas import ParsedSheet

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ParsedSheet)
async def upload_answer_sheet(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = parse_answer_sheet(file_path, file.filename)
    
    if not result.chunks:
        raise HTTPException(
            status_code=422,
            detail="No Q&A sections found. Make sure answers are labelled Q1, Q2 etc."
        )
    
    return result