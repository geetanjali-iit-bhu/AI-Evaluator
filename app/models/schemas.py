from pydantic import BaseModel
from typing import List, Optional

class AnswerChunk(BaseModel):
    question_number: str
    answer_text: str

class ParsedSheet(BaseModel):
    session_id: str
    filename: str
    chunks: List[AnswerChunk]

class SessionResponse(BaseModel):
    session_id: str
    message: str
    total_chunks: int

class VivaQuestion(BaseModel):
    session_id: str
    question: str

class VivaAnswer(BaseModel):
    session_id: str
    question: str
    answer: str


