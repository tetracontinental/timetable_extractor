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

# ファイル名から week_type を抽出する
def get_week_type(file_name):
    week_type = ""
    if "Ａ" in file_name or "A" in file_name:
        week_type = "A"
    elif "Ｃ" in file_name or "C" in file_name:
        week_type = "C"
    elif "Ｂ" in file_name or "B" in file_name:
        week_type = "B"
    elif "Ｄ" in file_name or "D" in file_name:
        week_type = "D"
    return week_type

# リストからデータを抽出する
def list_extractor(base_list, file_name, Class=True):
    # 最初のリスト（ヘッダー）は削除
    base_list = base_list[1:]
    week_type = get_week_type(file_name)

    for row in base_list:
        class_info = extract_class_info(row, Class)
        class_info["Schedule"] = extract_schedule(row, Class)
        class_info["week_type"] = week_type
        yield class_info

# データをクレンジングする
def cleanse_data(extracted_data):
    return [jaconv.z2h(item, digit=True, ascii=True) for item in extracted_data]
