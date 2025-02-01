from pymongo import MongoClient
import logging
import os

logging.basicConfig(level=logging.ERROR)

class ExtractDB:
    """MongoDBから時間割データを抽出するためのクラス。
    このクラスは、MongoDBデータベースから時間割情報にアクセスし取得する機能を提供し、
    異なる学年レベルとクラスタイプを処理します。

    属性:
        client (MongoClient): MongoDBクライアント接続
        class_dict (dict): 学年レベルとクラスタイプのマッピング辞書

    メソッド:
        get_collection_name(grade, class_name): 特定のクラスのコレクション名を取得
        get_class_schedule(db_name, grade, class_name): 特定のクラスの時間割を取得
        normalize_class_name(grade, class_type): クラス名を一貫性のある形式に正規化
        get_base_schedule(db_name, week_type, day, period): 特定の時間枠の基本時間割を取得
        get_fourth_grade_subject(document, period): 4年生の科目を抽出
        close(): MongoDB接続を閉じる
    """

    def __init__(self):
        """ExtractDBクラスの初期化"""
        try:
            self.client = MongoClient(os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/'))
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
        self.class_dict = {
            '3': ['1', '2', '3', '4', '国', '理'],
            '2I': ['国', '理'],
            '2G': ['1', '2', '3', '4'],
            '1': ['1', '2', '3', '4', '5', '6']
        }

    def get_class_schedule(self, week_type, grade_name:str, class_name:str, db_name:str="school_schedule_db"):
        """特定のクラスの時間割を取得する
        
        Args:
            db_name: データベース名
            grade: 学年
            class_name: クラス名
            
        Returns:
            dict: クラスの時間割データ
        """
        try:
            db = self.client[db_name]
            collection_name = f"base_schedule_{week_type}"
            collection = db[collection_name]
            DB_class=f"{grade_name}-{class_name}"
            return collection.find_one({'Class': DB_class})
        except Exception as e:
            logging.error(f"Error retrieving class schedule: {e}")

    def normalize_class_name(self, grade, class_type):
        """クラス名を正規化する
        
        Args:
            grade: 学年
            class_type: クラスタイプ
            
        Returns:
            str: 正規化されたクラス名
        """
        try:
            if grade == '2':
                if class_type in ['国', '理']:
                    return '2I'
                return '2G'
            return grade
        except Exception as e:
            logging.error(f"Error normalizing class name: {e}")
    def annual_grade_schedule(self, grade, month, date):
        """年間スケジュールを取得する
        
        Args:
            grade: 学年
            month: 月
            date: 日
            
        Returns:
            list: スケジュール情報
        """
        try:
            db = self.client['school_schedule_db']
            collection = db['annual_schedule']
            schedule = collection.find_one({''})
            if schedule:
                return schedule[month][date][f"{grade}_grade"]
        except Exception as e:
            logging.error(f"Error retrieving annual schedule: {e}")

    def get_base_schedule_info(self, week_type, day, period, info_type:str="Subject"):
        """基本時間割を取得する
        
        Args:
            week_type: 週のタイプ[A, B, C, D]
            day: 曜日
            period: 時限
            info_type: 取得する情報のタイプ [Subject, Teacher, Room]
            
        Returns:
            str: 科目名
        """
        try:
            db = self.client['school_schedule_db']
            collection_name = f"base_schedule_{week_type}"
            collection = db[collection_name]
            schedule = collection.find_one({})
            if schedule and 'Schedule' in schedule:
                return schedule['Schedule'][day][period][info_type]
        except Exception as e:
            logging.error(f"Error retrieving base schedule info: {e}")


    def annual_event_schedule(self, month, date):
        """年間イベントスケジュールを取得する
        
        Args:
            month: 月
            date: 日
            
        Returns:
            list: イベント情報
        """
        try:
            db = self.client['school_schedule_db']
            collection = db['annual_schedule']
            schedule = collection.find_one({})
            return schedule[month][date]['events']
        except Exception as e:
            logging.error(f"Error retrieving annual event schedule: {e}")

    def close(self):
        """MongoDBの接続を閉じる"""
        try:
            self.client.close()
        except Exception as e:
            logging.error(f"Error closing MongoDB connection: {e}")

if __name__ == "__main__":
    extractor = ExtractDB()
    print(extractor.annual_grade_schedule(3, 1, 4))
    extractor.close()

EOF > /workspace/timetable_extractor/backend/DBclass.py
from pymongo import MongoClient
import logging
import os

logging.basicConfig(level=logging.ERROR)

class ExtractDB:
    """MongoDBから時間割データを抽出するためのクラス。
    このクラスは、MongoDBデータベースから時間割情報にアクセスし取得する機能を提供し、
    異なる学年レベルとクラスタイプを処理します。

    属性:
        client (MongoClient): MongoDBクライアント接続
        class_dict (dict): 学年レベルとクラスタイプのマッピング辞書

    メソッド:
        get_collection_name(grade, class_name): 特定のクラスのコレクション名を取得
        get_class_schedule(db_name, grade, class_name): 特定のクラスの時間割を取得
        normalize_class_name(grade, class_type): クラス名を一貫性のある形式に正規化
        get_base_schedule(db_name, week_type, day, period): 特定の時間枠の基本時間割を取得
        get_fourth_grade_subject(document, period): 4年生の科目を抽出
        close(): MongoDB接続を閉じる
    """

    def __init__(self):
        """ExtractDBクラスの初期化"""
        try:
            self.client = MongoClient(os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/'))
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
        self.class_dict = {
            '3': ['1', '2', '3', '4', '国', '理'],
            '2I': ['国', '理'],
            '2G': ['1', '2', '3', '4'],
            '1': ['1', '2', '3', '4', '5', '6']
        }

    def get_class_schedule(self, week_type, grade_name:str, class_name:str, db_name:str="school_schedule_db"):
        """特定のクラスの時間割を取得する
        
        Args:
            db_name: データベース名
            grade: 学年
            class_name: クラス名
            
        Returns:
            dict: クラスの時間割データ
        """
        try:
            db = self.client[db_name]
            collection_name = f"base_schedule_{week_type}"
            collection = db[collection_name]
            DB_class=f"{grade_name}-{class_name}"
            return collection.find_one({'Class': DB_class})
        except Exception as e:
            logging.error(f"Error retrieving class schedule: {e}")

    def normalize_class_name(self, grade, class_type):
        """クラス名を正規化する
        
        Args:
            grade: 学年
            class_type: クラスタイプ
            
        Returns:
            str: 正規化されたクラス名
        """
        try:
            if grade == '2':
                if class_type in ['国', '理']:
                    return '2I'
                return '2G'
            return grade
        except Exception as e:
            logging.error(f"Error normalizing class name: {e}")
    def annual_grade_schedule(self, grade, month, date):
        """年間スケジュールを取得する
        
        Args:
            grade: 学年
            month: 月
            date: 日
            
        Returns:
            list: スケジュール情報
        """
        try:
            db = self.client['school_schedule_db']
            collection = db['annual_schedule']
            schedule = collection.find_one({''})
            if schedule:
                return schedule[month][date][f"{grade}_grade"]
        except Exception as e:
            logging.error(f"Error retrieving annual schedule: {e}")

    def get_base_schedule_info(self, week_type, day, period, info_type:str="Subject"):
        """基本時間割を取得する
        
        Args:
            week_type: 週のタイプ[A, B, C, D]
            day: 曜日
            period: 時限
            info_type: 取得する情報のタイプ [Subject, Teacher, Room]
            
        Returns:
            str: 科目名
        """
        try:
            db = self.client['school_schedule_db']
            collection_name = f"base_schedule_{week_type}"
            collection = db[collection_name]
            schedule = collection.find_one({})
            if schedule and 'Schedule' in schedule:
                return schedule['Schedule'][day][period][info_type]
        except Exception as e:
            logging.error(f"Error retrieving base schedule info: {e}")


    def annual_event_schedule(self, month, date):
        """年間イベントスケジュールを取得する
        
        Args:
            month: 月
            date: 日
            
        Returns:
            list: イベント情報
        """
        try:
            db = self.client['school_schedule_db']
            collection = db['annual_schedule']
            schedule = collection.find_one({})
            return schedule[month][date]['events']
        except Exception as e:
            logging.error(f"Error retrieving annual event schedule: {e}")

    def close(self):
        """MongoDBの接続を閉じる"""
        try:
            self.client.close()
        except Exception as e:
            logging.error(f"Error closing MongoDB connection: {e}")

if __name__ == "__main__":
    extractor = ExtractDB()
    print(extractor.annual_grade_schedule(3, 1, 4))
    extractor.close()

