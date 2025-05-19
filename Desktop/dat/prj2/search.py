import requests

API_URL = "http://127.0.0.1:8000/search/"

# 검색할 문장 (유사 문장을 찾고 싶은 자연어 문장)
query = "딥러닝 대표 모델에는 무엇이 있나요?"

# 요청 보내기
response = requests.get(API_URL, params={"query": query})

# 결과 출력
print("🔍 검색 문장:")
print(query)
print("\n✅ 검색 결과:")
print(response.json())
