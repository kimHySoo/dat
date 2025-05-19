from fastapi import FastAPI, Query
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import uuid
import os
load_dotenv(dotenv_path=r"C:\Users\ime\Desktop\dat\.env")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
app = FastAPI()

#터미널에서 다음 코드를 실행해서 서버 열기기
#uvicorn main:app --reload
#서버 주소 http://127.0.0.1:8000

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
model = SentenceTransformer("intfloat/e5-small-v2")

COLLECTION_NAME = "test-texts"
VECTOR_DIM = 384

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_DIM, distance="Cosine")
)

@app.post("/add/")
def add_text(text: str = Query(..., description="저장할 텍스트 입력")):
    vector = model.encode("passage: " + text).tolist()
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"text": text})]
    )
    return {"status": "저장 완료", "text": text}

@app.get("/search/")
def search_text(query: str = Query(..., description="검색할 문장 입력")):
    qvec = model.encode("query: " + query).tolist()
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=qvec,
        limit=3
    )
    return {"matches": [r.payload['text'] for r in results]}

@app.get("/all/")
def get_all_vectors():
    result, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=100 
    )
    return [{"id": r.id, "text": r.payload.get("text", "")} for r in result]


