import pandas as pd
import json
def format_csv(input_file, output_file):
    # Read the CSV file without headers
    data = pd.read_csv(input_file)
    
    # 最初の4行と最初の3列、最後の不要な列を削除
    # 最後の行はページによって違うので削除しない
    data = data.iloc[3:, 5:47]

    # インデックスをリセット
    data.reset_index(drop=True, inplace=True)

    # データを出力（ヘッダーなし）
    data.to_csv(output_file, index=False, header=False)

    
def process_week(data):
    # 1行ずつ処理する
    events_by_date: dict = {}
    current_month = 4
    for index in range(0, len(data), 5):  # 5行ずつ処理
        for i in range(0, len(data.columns), 6):
            new_events_by_date, new_month = process_events_day(index, i, data, events_by_date, current_month)
            if new_month != current_month:
                # 月が変わった場合、現在のevents_by_dateを出力してリセット
                print(json.dumps(events_by_date, indent=4, ensure_ascii=False))
                events_by_date = new_events_by_date
                current_month = new_month
            else:
                events_by_date = new_events_by_date

    return events_by_date

def process_events_day(index: int, local_row: int, data: any, events_by_date: any, current_month=4):
    date = data.iloc[index, local_row]  # 6つおきに日付がある
    if pd.notna(date):  # 日付が存在する場合のみ処理
        day = int(date)
        if day == 1 and events_by_date:  # 日付が1で、既にイベントがある場合は月を進める
            current_month += 1
        events = data.iloc[index, local_row + 1:local_row + 6].dropna().tolist()  # 日付後のイベントを取り出す
        if current_month not in events_by_date:
            events_by_date[current_month] = {}
        events_by_date[current_month][f"{day:02d}"] = events
    return events_by_date, current_month


'''
def process_schedule_grade(data):


format_csv('dev_csv_R6授業時数一覧.csv', 'output.csv')
'''
 # 4月から始まる  

data = pd.read_csv('dev_csv/dev_csv_output.csv', header=None)
data = process_week(data)
json_output = json.dumps(data, indent=4, ensure_ascii=False)
print(json_output)