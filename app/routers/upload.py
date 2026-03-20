import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import parse_answer_sheet
from app.services.rag import build_knowledge_base
from app.models.schemas import SessionResponse

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=SessionResponse)
async def upload_answer_sheet(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    parsed = parse_answer_sheet(file_path, file.filename)
    
    if not parsed.chunks:
        raise HTTPException(
            status_code=422,
            detail="No Q&A sections found. Make sure answers are labelled Q1, Q2 etc."
        )
    
    session_id = build_knowledge_base(parsed)
    
    return SessionResponse(
        session_id=session_id,
        message="Answer sheet uploaded and knowledge base built successfully",
        total_chunks=len(parsed.chunks)
    )