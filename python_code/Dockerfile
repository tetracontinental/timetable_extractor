# Pythonの公式イメージを使用
FROM python:latest

# 作業ディレクトリを作成
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# サーバーを実行
