import requests

API_URL = "http://127.0.0.1:8000/add/"

# 딥러닝 요약 문장 (300자 이내)
dl_summary = (
    "딥러닝은 인공신경망을 기반으로 한 기계학습 기술로, 사람의 뇌처럼 계층적으로 데이터를 처리합니다. "
    "이미지, 음성, 자연어 등의 복잡한 패턴을 스스로 학습해 인식하며, "
    "대표적인 모델로는 CNN, RNN, Transformer 등이 있습니다."
)

# API 요청
response = requests.post(API_URL, params={"text": dl_summary})

# 결과 출력
print("📨 입력된 내용:")
print(dl_summary)
print("\n✅ 서버 응답:")
print(response.json())
