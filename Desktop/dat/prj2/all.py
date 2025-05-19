import requests

API_URL = "http://127.0.0.1:8000/all/"

response = requests.get(API_URL)

print("🗂 저장된 벡터 목록:")
for item in response.json():
    print(f"- ID: {item['id']}")
    print(f"  Text: {item['text']}\n")
