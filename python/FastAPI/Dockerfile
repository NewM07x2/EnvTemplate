# Python 3.12 slim イメージを使用して依存関係をインストールするベースステージ
FROM python:3.12-slim AS base

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# システム依存関係をインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# requirements.txt をコピー
COPY requirements.txt .

# Python 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt graphene

# 最終ステージとして軽量なイメージを使用
FROM python:3.12-slim AS final

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 作業ディレクトリを設定
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libatomic1 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ベースステージから依存関係をコピー
COPY --from=base /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /app /app

# アプリケーションコードをコピー
COPY . .

# Prisma クライアントを生成
RUN prisma generate

# ポートを公開
EXPOSE 8000

# アプリケーションを実行
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
