# ベースイメージを指定
FROM python:3.8 as base

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを指定
WORKDIR /code

# 依存関係ファイルをコピー
COPY requirements.txt /code/

# pip を最新にアップグレード
RUN pip install --upgrade pip

# 依存関係をインストール
RUN pip install --default-timeout=1000 -r requirements.txt

# アプリケーションコードをコピー
COPY . /code/

FROM base as development

    # エントリーポイントを実行 権限を変更
    RUN chmod +x ./entrypoint.sh

    # マイグレーションを実行
    ENTRYPOINT ["./entrypoint.sh"]

    # コマンドを実行
    CMD python3 manage.py runserver

FROM base as production

    # コマンドを実行
    CMD exec gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --timeout 0 stock_price_prediction.wsgi:application