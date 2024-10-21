# MongoDBの公式イメージを使用
FROM mongo:latest

# 初期データを格納するディレクトリを作成
RUN mkdir -p /docker-entrypoint-initdb.d

# JSONデータをコピー
COPY /output_json /docker-entrypoint-initdb.d/output_json

# 初期データを挿入するためのスクリプトを作成
COPY init.js /docker-entrypoint-initdb.d/init.js
