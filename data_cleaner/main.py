from pdfToJson import extract_pdf_data
from insertDB import MongoDBHandler

def get_pdf_path():
    return input("PDFファイルのパスを入力してください (終了するには'quit'と入力): ")

def get_week_type():
    while True:
        week_type = input("週の種類 (A, B, C, D) を入力してください: ").upper()
        if week_type in ['A', 'B', 'C', 'D']:
            return week_type
        print("無効な週の種類です。再度入力してください。")

def get_class_type():
    return input("クラス時間割ならYを、教室時間割ならNを (y/n): ").lower() == 'y'

def insert_schedules(db_handler, schedules, week_type, is_class):
    base_key = 'base_schedules_' if is_class else 'schedules_'
    if week_type in ['A', 'C']:
        db_handler.insert_to_mongodb(schedules, f'{base_key}A')
        db_handler.insert_to_mongodb(schedules, f'{base_key}C')
    else:
        db_handler.insert_to_mongodb(schedules, f'{base_key}{week_type}')

def main():
    db_handler = MongoDBHandler()

    while True:
        pdf_path = get_pdf_path()
        if pdf_path.lower() == 'quit':
            break

        week_type = get_week_type()
        is_class = get_class_type()

        schedules = extract_pdf_data(pdf_path, is_class)
        insert_schedules(db_handler, schedules, week_type, is_class)

    db_handler.close()
    print("全ての処理が完了しました。")

if __name__ == "__main__":
    main()
