import pandas as pd
import json
from typing import Dict, List, Tuple, Union

def format_csv(input_file: str, output_file: str) -> None:
    """
    CSVファイルから不要な行と列を削除し、新しいCSVファイルに保存する
    
    Args:
        input_file (str): 入力CSVファイルのパス
        output_file (str): 出力CSVファイルのパス
    """
    # ヘッダーなしでCSVファイルを読み込む
    data = pd.read_csv(input_file, header=None)
    
    # 最初の3行と最初の5列、最後の不要な列を削除
    # 最後の行はページによって異なるため削除しない
    processed_data = data.iloc[4:62, 5:47]

    # インデックスをリセット
    processed_data.reset_index(drop=True, inplace=True)

    # データを出力（ヘッダーなし）
    processed_data.to_csv(output_file, index=False, header=False)

def extract_events_from_day(
    data: pd.DataFrame, 
    index: int, 
    local_row: int, 
    current_month: int,
    row_type: str = 'event'
) -> Tuple[Dict[int, Dict[str, Union[List[str], List[List[str]]]]], int]:
    """
    特定の日付のイベントを抽出し、月情報も更新する
    
    Args:
        data (pd.DataFrame): イベントデータ
        index (int): 行インデックス
        local_row (int): 列インデックス
        current_month (int): 現在の月
        row_type (str): 取得する行のタイプ ('event', '3', '2G', '2I', '1')

    Returns:
        Tuple[Dict, int]: イベント辞書と更新された月
    """
    date = data.iloc[index, local_row]
    if pd.isna(date):
        return {}, current_month

    day = int(date)
    
    # より明示的な月の遷移ロジック
    if day == 1 and current_month != 1:
        current_month += 1

    if row_type == 'event':
        events = data.iloc[index, local_row + 1:local_row + 6].dropna().tolist()
        return {current_month: {f"{day:02d}": {"events": events}}}, current_month
    else:
        # 2、3、4行目の取得
        row_offset = {'3': 1, '2G': 2, '2I': 3, '1':4}[row_type]
        events_rows = data.iloc[index + row_offset, local_row:local_row + 6].dropna().tolist()
        return {current_month: {f"{day:02d}": {f"{row_type}_grade": events_rows}}}, current_month

def merge_event_dictionaries(
    base_events: Dict[int, Dict[str, Dict[str, Union[List[str], List[List[str]]]]]],
    new_events: Dict[int, Dict[str, Dict[str, Union[List[str], List[List[str]]]]]
]) -> Dict[int, Dict[str, Dict[str, Union[List[str], List[List[str]]]]]]:
    """
    イベント辞書を結合する
    
    Args:
        base_events (Dict): ベースとなるイベント辞書
        new_events (Dict): 追加するイベント辞書

    Returns:
        Dict: 結合されたイベント辞書
    """

    for month, dates in new_events.items():
        if month not in base_events:
            base_events[month] = {}
        for day, day_events in dates.items():
            if day not in base_events[month]:
                base_events[month][day] = {}
            base_events[month][day].update(day_events)
    return base_events

def process_week(data: pd.DataFrame) -> Dict[int, Dict[str, Dict[str, Union[List[str], List[List[str]]]]]]:
    """
    週単位でイベントを処理する
    
    Args:
        data (pd.DataFrame): イベントデータ

    Returns:
        Dict: 月ごとのイベント辞書
    """
    events_by_date: Dict[int, Dict[str, Dict[str, Union[List[str], List[List[str]]]]]] = {}
    current_month = 4 # 4月から開始

    for index in range(0, len(data), 5):  # 5行ずつ処理
        for local_row in range(0, len(data.columns), 6):
            # 1行目のイベント
            new_events, new_month = extract_events_from_day(data, index, local_row, current_month, 'event')
            
            if new_events:
                events_by_date = merge_event_dictionaries(events_by_date, new_events)
                current_month = new_month

                # 2~4行目のイベント
                for row_type in ['3', '2G', '2I', '1']:
                    additional_events, _ = extract_events_from_day(data, index, local_row, current_month, row_type)
                    if additional_events:
                        events_by_date = merge_event_dictionaries(events_by_date, additional_events)

    return events_by_date

def main():
    """
    メイン処理
    CSVファイルの処理とJSONへの変換を行う
    """
    # CSVをフォーマット
    format_csv('input.csv', 'output.csv')
    
    # イベントを処理
    data = pd.read_csv('output.csv', header=None)
    processed_events = process_week(data)
    
    # JSONに変換して出力
    json_output = json.dumps(processed_events, indent=4, ensure_ascii=False)
    print(json_output)

main()
