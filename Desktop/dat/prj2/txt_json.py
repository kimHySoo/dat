import json

def convert_to_qdrant_format(input_path, output_path, source_name="OSS_Lecture_09"):
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 문단 단위로 분할
    paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]

    json_data = []
    for idx, paragraph in enumerate(paragraphs):
        entry = {
            "id": str(idx + 1),
            "source": source_name,
            "page": (idx // 5) + 1,  # 예: 5문단마다 1 page로 가정
            "section": f"Section {((idx // 3) + 1)}",  # 예: 3문단마다 1 section
            "text": paragraph
        }
        json_data.append(entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)


# 사용 예시
if __name__ == "__main__":
    input_txt = "C:/Users/ime/Downloads/Files/추출_20250514_134430/pageAll_text.txt"
    output_json = "C:/Users/ime/Desktop/dat/pageAll.json"
    convert_to_qdrant_format(input_txt, output_json)
