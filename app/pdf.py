import os
import pdfplumber

# ディレクトリ内のファイルを巡回
directory = '../data'

for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        filepath = os.path.join(directory, filename)
        # PDFファイルを開く
        with pdfplumber.open(filepath) as pdf:
            page = pdf.pages[0]
            # テーブルを抽出
            table = page.extract_table()
            # テーブルの内容を表示
            if table:
                print(f"Table from {filename}:")
                for row in table:
                    print(row)
            else:
                print(f"No table found in {filename}")
