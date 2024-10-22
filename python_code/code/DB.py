# MongoDB接続とデータベース設定
def connect_to_mongodb(host='localhost', port=27017, db_name='school_schedule'):
    try:
        client = MongoClient(host, port)
        db = client[db_name]
        return client, db
    except Exception as e:
        print(f"MongoDB接続エラー: {e}")
        raise

# PDFファイルを読み込んでMongoDBに保存する
def extract_pdf_to_mongodb(file_path, db, collection_name='schedules', Class=True):
    try:
        # コレクションの取得
        collection = db[collection_name]

        # PDFファイル名を取得
        file_name = os.path.basename(file_path)

        with pdfplumber.open(file_path) as pdf:
            for num_page in range(len(pdf.pages)):
                # 表を抽出する
                tables = pdf.pages[num_page].extract_tables()
                if tables and isinstance(tables[0], list):
                    extracted_data = tables[0]
                else:
                    continue

                cleansed_data = [cleanse_data(row) for row in extracted_data]

                # 各クラス情報を個別に処理してMongoDBに保存
                for class_info in list_extractor(cleansed_data, file_name, Class=Class):
                    # メタデータを追加
                    class_info['metadata'] = {
                        'source_file': file_name,
                        'page_number': num_page + 1,
                        'imported_at': datetime.now(),
                        'last_updated': datetime.now()
                    }

                    # upsert処理（クラス名とweek_typeが同じ場合は更新、なければ新規作成）
                    collection.update_one(
                        {'Class': class_info['Class'], 'week_type': class_info['week_type']},
                        {'$set': class_info},
                        upsert=True
                    )
                    
                    # ACの場合、Cも追加する
                    if class_info["week_type"] == "A":
                        class_info_copy = class_info.copy()
                        class_info_copy["week_type"] = "C"
                        collection.update_one(
                            {'Class': class_info_copy['Class'], 'week_type': class_info_copy['week_type']},
                            {'$set': class_info_copy},
                            upsert=True
                        )

        print(f"ファイル {file_name} のデータを正常にMongoDBに保存しました。")

    except Exception as e:
        print(f"データ保存中にエラーが発生しました: {e}")
        raise