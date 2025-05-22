from fastapi import APIRouter, HTTPException
from schemas.quiz_schemas import QuizBatchRequest, QuizBatchResponse
from services.generate_quiz import generate_quizzes  # 새로운 함수 (get_topic 사용)

router = APIRouter()

@router.post("/generate-batch", response_model=QuizBatchResponse)
async def create_quiz_batch(request: QuizBatchRequest):
    try:
        results = await generate_quizzes(
            quiz_type=request.quiz_type,
            config=request.config
        )
        return {"quizzes": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
