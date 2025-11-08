from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

class GenerateIn(BaseModel):
    url: HttpUrl

class QuizItem(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class QuizRecordOut(BaseModel):
    id: int
    url: str
    title: Optional[str]
    summary: Optional[str]
    key_entities: Optional[Dict[str, List[str]]]
    sections: Optional[List[str]]
    quiz: List[QuizItem]
    related_topics: Optional[List[str]]
    created_at: Optional[str]

    class Config:
        orm_mode = True
