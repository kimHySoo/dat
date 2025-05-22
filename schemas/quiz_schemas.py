from pydantic import BaseModel
from typing import List, Dict

class QuizRequest(BaseModel):
    quiz_type: str
    topic: str
    config: Dict[str, str]

class QuizResponse(BaseModel):
    question: str
    answer: str

# 새로 추가
class QuizBatchRequest(BaseModel):
    quiz_type: str
    config: Dict[str, str]

class QuizBatchResponse(BaseModel):
    quizzes: List[QuizResponse]
