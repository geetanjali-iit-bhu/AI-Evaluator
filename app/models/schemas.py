from pydantic import BaseModel
from typing import List

class AnswerChunk(BaseModel):
    question_number: str
    answer_text: str

class ParsedSheet(BaseModel):
    session_id: str
    filename: str
    chunks: List[AnswerChunk]


