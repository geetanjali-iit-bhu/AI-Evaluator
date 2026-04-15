from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Question:
    id: str
    type: str  # mcq | short | long
    text: str
    options: Optional[Dict[str, str]] = None
    correct_answer: Optional[str] = None
    marks: int = 0
    rubric: List[Dict] = None
    ideal_answer: Optional[str] = None