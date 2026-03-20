import pdfplumber
import re
from app.models.schemas import AnswerChunk, ParsedSheet
import uuid

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def split_into_chunks(text: str) -> list[AnswerChunk]:
    chunks = []
    pattern = re.split(r'(Q\d+[\.\)]|Question\s*\d+[\.\)])', text, flags=re.IGNORECASE)
    
    i = 1
    while i < len(pattern) - 1:
        question_label = pattern[i].strip()
        answer_text = pattern[i + 1].strip()
        if answer_text:
            chunks.append(AnswerChunk(
                question_number=question_label,
                answer_text=answer_text
            ))
        i += 2

    return chunks

def parse_answer_sheet(file_path: str, filename: str) -> ParsedSheet:
    text = extract_text_from_pdf(file_path)
    chunks = split_into_chunks(text)
    
    return ParsedSheet(
        session_id=str(uuid.uuid4()),
        filename=filename,
        chunks=chunks
    )