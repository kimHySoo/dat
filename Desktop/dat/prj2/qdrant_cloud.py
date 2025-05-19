from fastapi import FastAPI, Query
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import uuid, os

load_dotenv(r"C:\Users\ime\Desktop\dat\.env")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

app = FastAPI()
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
model = SentenceTransformer("intfloat/e5-small-v2")

COLLECTION_NAME = "test-texts"
VECTOR_DIM = 384

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_DIM, distance="Cosine")
)

@app.post("/add/")
def add_text(text: str = Query(...)):
    vector = model.encode(text).tolist()
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"text": text})]
    )
    return {"status": "저장 완료", "text": text}

@app.get("/search/")
def search_text(query: str = Query(...)):
    qvec = model.encode(query).tolist()
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=qvec,
        limit=3
    )
    return {"matches": [r.payload['text'] for r in results]}
