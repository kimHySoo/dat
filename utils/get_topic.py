# utils/get_word.py

import re
from collections import Counter
from qdrant_client import QdrantClient

def load_stopwords(filepath: str) -> set:
    with open(filepath, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def clean_text(text: str) -> str:
    return re.sub(r'[^가-힣a-zA-Z\s]', '', text)

def tokenize_and_clean(text: str, stopwords_ko: set, stopwords_en: set) -> list[str]:
    text = clean_text(text)
    tokens = text.split()
    return [
        token for token in tokens
        if len(token) > 1 and token.lower() not in stopwords_en and token not in stopwords_ko
    ]

def get_top_words(qdrant_url: str, collection_name: str, stopwords_ko_path: str, stopwords_en_path: str, top_n: int = 10):
    # Qdrant 연결
    client = QdrantClient(url=qdrant_url)
    points, _ = client.scroll(collection_name=collection_name, limit=10_000, with_payload=True)

    # 모든 텍스트 수집
    texts = [p.payload.get("text", "") for p in points if "text" in p.payload]
    all_text = " ".join(texts)

    # 불용어 로드
    stopwords_ko = load_stopwords(stopwords_ko_path)
    stopwords_en = load_stopwords(stopwords_en_path)

    # 토큰화 및 카운팅
    tokens = tokenize_and_clean(all_text, stopwords_ko, stopwords_en)
    freq = Counter(tokens)
    return freq.most_common(top_n)
