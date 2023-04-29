import json 


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def get_data_from_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data