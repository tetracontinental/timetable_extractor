from pymongo import MongoClient
import json
import os

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def insert_data(collection, data, data_type):
    if data:
        result = collection.insert_many(data)
        print(f'{len(result.inserted_ids)} 件の{data_type}データを挿入しました。')

def process_file(file_path, db):
    data = load_json(file_path)
    
    # ファイル名からテーブル名を決定
    base_name = os.path.basename(file_path)
    if 'class' in base_name.lower():
        collection_name = 'Class_Timetable'
        data_type = 'クラス一覧'
    elif 'room' in base_name.lower():
        collection_name = 'Room_Timetable'
        data_type = '教室一覧'
    else:
        print(f'ファイル名 "{base_name}" に対応するテーブルが見つかりません。')
        return

    insert_data(db[collection_name], data, data_type)

def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['School_Timetable']

    directory = 'output_json'  # JSONファイルが格納されているディレクトリのパスを指定

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            process_file(file_path, db)

    client.close()

if __name__ == "__main__":
    main()
