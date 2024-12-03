import pandas as pd

def format_csv(input_file, output_file):
    # Read the CSV file without headers
    df = pd.read_csv(input_file)
    
    # 最初の4行と最初の3列、最後の不要な列を削除
    # 最後の行はページによって違うので削除しない
    df = df.iloc[3:, 5:47]

    
    # ヘッダーを追加しないでCSVファイルに書き込む
    df.to_csv(output_file, index=False, header=False)


grade_list = ['1', '2G', '2I', '3']

input_end_index = 20

# スケジュールを格納する辞書
schedule_dict = {}



format_csv('R6授業時数一覧.csv', 'output.csv')