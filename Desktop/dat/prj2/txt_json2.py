import re
import json
import uuid

def simple_sentence_split(text):
    # 문장 구분 정규표현식 (., !, ? 뒤에 공백 있으면 분리)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def convert_txt_to_json(input_path, output_path, source_name="OSS_Lecture_09"):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    sentences = simple_sentence_split(text)

    json_data = []
    for idx, sentence in enumerate(sentences):
        entry = {
            "id": str(uuid.uuid4()),
            "source": source_name,
            "index": idx + 1,
            "text": sentence
        }
        json_data.append(entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

# 실행 예시
if __name__ == "__main__":
    input_txt = "C:/Users/ime/Downloads/Files/추출_20250514_134430/pageAll_text.txt"
    output_json = "C:/Users/ime/Desktop/dat/pageAll_1.json"
    convert_txt_to_json(input_txt, output_json)
