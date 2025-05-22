import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.embedding import EmbeddingModel
from utils.get_topic import get_topic
from qdrant_client import QdrantClient

# 환경 변수 로드
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Qdrant 및 임베딩 모델 설정
COLLECTION_NAME = "korean-texts"
QDRANT_URL = "http://localhost:6333"
STOPWORDS_KO_PATH = "utils/stopwords-ko.txt"
STOPWORDS_EN_PATH = "utils/stopwords-en.txt"

client = QdrantClient(url=QDRANT_URL)
model = EmbeddingModel()

async def generate_quizzes(quiz_type: str, config: dict) -> list[dict]:
    # ✅ get_topic 사용해 상위 단어 추출
    top_words = get_topic(
        qdrant_url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
        stopwords_ko_path=STOPWORDS_KO_PATH,
        stopwords_en_path=STOPWORDS_EN_PATH,
        top_n=10
    )

    quizzes = []

    for word, _ in top_words:
        query_vec = model.encode(word)
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vec,
            limit=3,
            with_payload=True
        )
        context = "\n".join([r.payload["text"] for r in results])

        prompt = f"""
"{word}"에 대해 아래 문단들을 참고하여 객관식 퀴즈를 만들어줘.
- 보기 4개 포함
- 정답을 명확하게 표기
- 유형: {quiz_type}
- 추가 설정: {config}

문단:
{context}
"""

        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 교육용 퀴즈 생성기야."},
                {"role": "user", "content": prompt}
            ]
        )

        quizzes.append({
            "question": word,
            "answer": response.choices[0].message.content.strip()
        })

    return quizzes
