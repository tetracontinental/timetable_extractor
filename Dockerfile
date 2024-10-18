FROM postgres:13

# 環境変数の設定
ENV POSTGRES_DB=school_schedule
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=secret

# 初期化スクリプトをコピー
COPY ./init /docker-entrypoint-initdb.d/

# データベースの設定を最適化（オプション）
# RUN echo "max_connections = 100" >> /usr/share/postgresql/postgresql.conf.sample
# RUN echo "shared_buffers = 128MB" >> /usr/share/postgresql/postgresql.conf.sample

# ポートの公開
EXPOSE 5432