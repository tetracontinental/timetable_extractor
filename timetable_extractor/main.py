import os
import json
from pdfToJson import extract_pdf_data
from DB import MongoDBHandler, json_serial

def main():
    db_handler = MongoDBHandler()

    while True:
        pdf_path = input("PDFファイルのパスを入力してください (終了するには'quit'と入力): ")
        if pdf_path.lower() == 'quit':
            break

        week_type = input("週の種類 (A, B, C, D) を入力してください: ").upper()
        if week_type not in ['A', 'B', 'C', 'D']:
            print("無効な週の種類です。再度入力してください。")
            continue

        Class_input = input("クラス時間割ならYを、教室時間割ならNを (y/n): ").lower()
        Class = Class_input == 'y'

        if Class:
            class_base_schedules = extract_pdf_data(pdf_path, Class)
        else:
            class_schedules = extract_pdf_data(pdf_path, Class)

        # AとC、またはB、Dの処理
        if week_type in ['A', 'C']:
            if Class:
                db_handler.insert_to_mongodb(class_base_schedules, 'base_schedules_A')
                db_handler.insert_to_mongodb(class_base_schedules, 'base_schedules_C')
            else:
                db_handler.insert_to_mongodb(class_schedules, 'schedules_A')
                db_handler.insert_to_mongodb(class_schedules, 'schedules_C')
        elif week_type == 'B':
            if Class:
                db_handler.insert_to_mongodb(class_base_schedules, 'base_schedules_B')
            else:
                db_handler.insert_to_mongodb(class_schedules, 'schedules_B')
        elif week_type == 'D':
            if Class:
                db_handler.insert_to_mongodb(class_base_schedules, 'base_schedules_D')
            else:
                db_handler.insert_to_mongodb(class_schedules, 'schedules_D')

    db_handler.close()
    print("全ての処理が完了しました。")

if __name__ == "__main__":
    main()