from pymongo import MongoClient

def get_class_schedule(db_name, collection_name, class_name):
    # MongoDBに接続
    client = MongoClient('mongodb://localhost:27017/')
    
    # データベース選択
    db = client[db_name]
    
    # コレクション選択
    collection = db[collection_name]
    
    # クラスのデータを取得
    class_schedule = collection.find_one({'Class': class_name})
    
    return class_schedule

def get_subject(class_schedule, day, period):
    # 指定された曜日と時限目の科目を取得
    subject = class_schedule['Schedule'][day][period]['Subject']
    return subject
