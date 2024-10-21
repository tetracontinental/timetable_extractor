import pdfplumber
import json
import os
import jaconv

# クラス情報を抽出する
def extract_class_info(row, Class):
    class_info = {}
    if Class:
        class_name = row[0].split("\n")[0]  # クラス名を取得
        class_info["Class"] = class_name
        class_info["Teacher"] = row[0].split("\n")[1]  # 担任の先生の名前
    else:
        class_info["Class"] = row[0]  # クラス名を取得
    return class_info

# スケジュールを抽出する
def extract_schedule(row, Class):
    day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    schedule = {}
    for day in range(5):
        day_schedule = {}
        for class_of_day in range(6):
            lesson = row[1 + class_of_day + day * 6]  # 授業名を取得
            if Class:
                lesson_parts = lesson.split("\n")
                if len(lesson_parts) == 3:
                    subject, teacher, room = lesson_parts
                else:
                    subject, teacher, room = lesson_parts[0], "", ""
                day_schedule[class_of_day + 1] = {
                    "Subject": subject,
                    "Teacher": teacher,
                    "Room": room
                }
            else:
                lesson_parts = lesson.split("\n")
                if len(lesson_parts) == 3:
                    subject, teacher, room = lesson_parts
                else:
                    subject, teacher, room = lesson_parts[0], "", ""
                day_schedule[class_of_day + 1] = {
                    "Subject": subject,
                    "Teacher": teacher,
                    "Room": room
                }
        schedule[day_of_week[day]] = day_schedule  # 曜日ごとにスケジュールを格納
    return schedule

# リストからデータを抽出する
def list_extractor(base_list, Class=True):
    json_data = []
    # 最初のリスト（ヘッダー）は削除
    base_list = base_list[1:]

    for row in base_list:
        class_info = extract_class_info(row, Class)
        class_info["Schedule"] = extract_schedule(row, Class)
        json_data.append(class_info)

    return json_data


# データをクレンジングする
def cleanse_data(extracted_data):
    return [jaconv.z2h(item, digit=True, ascii=True) for item in extracted_data]


# PDFファイルを読み込む
def extract_pdf_data(file_path, Class=True):
    with pdfplumber.open(file_path) as pdf:
        extracted_data = []
        for num_page in range(len(pdf.pages)):  # 全ページを処理する
            # 表を抽出する
            tables = pdf.pages[num_page].extract_tables()
            if tables and isinstance(tables[0], list):
                extracted_data = tables[0]
            else:
                extracted_data = []

            cleansed_data = [cleanse_data(row) for row in extracted_data]
            json_output = list_extractor(cleansed_data, Class=Class)

            # PDFファイル名でJSONファイル名を作成
            json_filename = os.path.splitext(os.path.basename(file_path))[0] + ".json"
            json_filepath = os.path.join('output_json', json_filename)

            with open(json_filepath, 'w', encoding='utf-8') as json_file:
                json.dump(json_output, json_file, ensure_ascii=False, indent=4)

