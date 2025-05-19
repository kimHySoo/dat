import json
import uuid

def convert_txt_by_line(input_path, output_path, source_name="OSS_Lecture_09"):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 줄 단위 분리 + 빈 줄 제거
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    json_data = []
    for idx, line in enumerate(lines):
        entry = {
            "id": str(uuid.uuid4()),
            "source": source_name,
            "index": idx + 1,
            "text": line
        }
        json_data.append(entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

# 실행 예시
if __name__ == "__main__":
    input_txt = "C:/Users/ime/Downloads/Files/추출_20250514_134430/pageAll_text.txt"
    output_json = "C:/Users/ime/Desktop/dat/pageAll_2.json"
    convert_txt_by_line(input_txt, output_json)
