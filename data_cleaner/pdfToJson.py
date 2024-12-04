import pdfplumber
import jaconv

def extract_schedule(row, Class):
    day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    class_schedule = {}

    # クラス名と教師名の抽出
    if Class:
        class_schedule["Class"] = row[0].split("\n")[0]
        class_schedule["Teacher"] = row[0].split("\n")[1]
    else:
        class_schedule["Class"] = row[0]

    # 曜日ごとのスケジュールを構築
    schedule = {}
    for day in range(5):
        day_schedule = {}
        for class_of_day in range(6):
            lesson = row[1 + class_of_day + day * 6]
            lesson_parts = lesson.split("\n")
            if len(lesson_parts) == 3:
                subject, teacher, room = lesson_parts
            else:
                subject, teacher, room = lesson_parts[0], "", ""

            # 曜日ごとの授業情報を追加
            day_schedule[str(class_of_day + 1)] = {
                "Subject": subject,
                "Teacher": teacher,
                "Room": room
            }
        schedule[day_of_week[day]] = day_schedule

    class_schedule["Schedule"] = schedule  # スケジュールを追加
    return class_schedule

def cleanse_data(extracted_data):
    return [jaconv.z2h(item, digit=True, ascii=True) for item in extracted_data]

def extract_pdf_data(file_path, Class=True):
    with pdfplumber.open(file_path) as pdf:
        all_class_schedules = []  # すべてのクラススケジュールを格納するリスト

        for num_page in range(len(pdf.pages)):
            tables = pdf.pages[num_page].extract_tables()
            if tables and isinstance(tables[0], list):
                extracted_data = tables[0]
            else:
                continue

            cleansed_data = [cleanse_data(row) for row in extracted_data]
            class_schedules = [extract_schedule(row, Class) for row in cleansed_data[1:]]  # ヘッダーを削除

            all_class_schedules.extend(class_schedules)  # スケジュールを統合

        return all_class_schedules  # 返り値を修正
