import pymongo

# MongoDBサーバーに接続
client = pymongo.MongoClient("mongodb://localhost:27017/")

# 使用するデータベースとコレクションの選択
db = client["school_schedule_db"]  # ここで自分のデータベース名を指定
collection = db["base_schedules_A"]  # ここで自分のコレクション名を指定

# クラスと科目を指定
class_name = "2-4"
subject_name = "数学Ⅱ"

# クエリ作成
query = {
    "$or": [
        {"Schedule.Monday.1.Subject": subject_name, "Class": class_name},
        {"Schedule.Monday.2.Subject": subject_name, "Class": class_name},
        {"Schedule.Monday.3.Subject": subject_name, "Class": class_name},
        {"Schedule.Monday.4.Subject": subject_name, "Class": class_name},
        {"Schedule.Monday.5.Subject": subject_name, "Class": class_name},
        {"Schedule.Monday.6.Subject": subject_name, "Class": class_name},
        {"Schedule.Tuesday.1.Subject": subject_name, "Class": class_name},
        {"Schedule.Tuesday.2.Subject": subject_name, "Class": class_name},
        {"Schedule.Tuesday.3.Subject": subject_name, "Class": class_name},
        {"Schedule.Tuesday.4.Subject": subject_name, "Class": class_name},
        {"Schedule.Tuesday.5.Subject": subject_name, "Class": class_name},
        {"Schedule.Tuesday.6.Subject": subject_name, "Class": class_name},
        {"Schedule.Wednesday.1.Subject": subject_name, "Class": class_name},
        {"Schedule.Wednesday.2.Subject": subject_name, "Class": class_name},
        {"Schedule.Wednesday.3.Subject": subject_name, "Class": class_name},
        {"Schedule.Wednesday.4.Subject": subject_name, "Class": class_name},
        {"Schedule.Wednesday.5.Subject": subject_name, "Class": class_name},
        {"Schedule.Wednesday.6.Subject": subject_name, "Class": class_name},
        {"Schedule.Thursday.1.Subject": subject_name, "Class": class_name},
        {"Schedule.Thursday.2.Subject": subject_name, "Class": class_name},
        {"Schedule.Thursday.3.Subject": subject_name, "Class": class_name},
        {"Schedule.Thursday.4.Subject": subject_name, "Class": class_name},
        {"Schedule.Thursday.5.Subject": subject_name, "Class": class_name},
        {"Schedule.Thursday.6.Subject": subject_name, "Class": class_name},
        {"Schedule.Friday.1.Subject": subject_name, "Class": class_name},
        {"Schedule.Friday.2.Subject": subject_name, "Class": class_name},
        {"Schedule.Friday.3.Subject": subject_name, "Class": class_name},
        {"Schedule.Friday.4.Subject": subject_name, "Class": class_name},
        {"Schedule.Friday.5.Subject": subject_name, "Class": class_name},
        {"Schedule.Friday.6.Subject": subject_name, "Class": class_name}
    ]
}

# クエリを実行して結果を取得
results = collection.find(query)

# 結果を表示
for result in results:
    print(result)
