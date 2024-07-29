# ベースイメージを指定
FROM python:3.8

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential

# 作業ディレクトリを指定
WORKDIR /code

# 依存関係ファイルをコピー
COPY requirements.txt /code/

# 依存関係をインストール
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY . /code/

# コマンドを実行
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
