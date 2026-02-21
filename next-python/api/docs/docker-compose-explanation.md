# docker-compose.yml 解説

このドキュメントは、`next-python/api/docs/docker-compose.yml` の内容を分かりやすく解説したものです。

## 概要

`docker-compose.yml` は以下の3つのサービスを定義しています:

- `postgres`: PostgreSQL データベース
- `redis`: Redis キャッシュ（オプション）
- `app`: FastAPI アプリケーション（Prisma と uvicorn を利用）

また、永続化用の `volumes` とサービス間通信のための `networks` を定義しています。

---

## services の詳細

### 1) postgres

- image: `postgres:16-alpine`
  - 軽量な Alpine ベースの PostgreSQL 16 イメージを使用します。
- container_name: `fastapi-postgres`
  - コンテナ名を指定します。
- environment:
  - `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` を環境変数から取得（未指定時はデフォルト値を使用）。
- ports:
  - ホストの `${POSTGRES_PORT:-5432}` をコンテナの 5432 にマッピングします。
- volumes:
  - `postgres_data:/var/lib/postgresql/data` によりデータを永続化します。
- healthcheck:
  - `pg_isready` を用いたヘルスチェックを定義しています。

用途: データ永続化（ユーザ、投稿など）。本番ではパスワード等を強固に設定してください。

---

### 2) redis (オプション)

- image: `redis:7-alpine`
- container_name: `fastapi-redis`
- ports: ホストの `${REDIS_PORT:-6379}` をコンテナの 6379 にマッピング
- volumes: `redis_data:/data` により永続化
- healthcheck: `redis-cli ping` を実行して動作確認

用途: キャッシュ、セッション、Celeryブローカー等。不要なら設定から削除可能です。

---

### 3) app (FastAPI)

- build:
  - context: `.`、dockerfile: `Dockerfile` を使ってビルド
- container_name: `fastapi-app`
- environment:
  - `DATABASE_URL` は内部で `postgres` ホストを指すように設定されています。
  - `REDIS_URL`, `APP_ENV`, `DEBUG` などを設定しています。
- ports:
  - ホストの `${APP_PORT:-8000}` をコンテナの 8000 にマッピング
- depends_on:
  - `postgres` と `redis` に依存し、`condition: service_healthy` を指定（ヘルスチェック成功を待つように）
- volumes:
  - `./app:/app/app` と `./main.py:/app/main.py` をマウント（開発向けホットリロード対応）
- networks: `app-network`
- command:
  - 起動時に `prisma db push` を実行してスキーマを DB に反映し、その後 `uvicorn` で起動します。
  - 開発向けに `--reload` が付与されています。

用途: アプリケーション本体。開発用の設定が多く含まれるため、本番では調整が必要です。

---

## volumes

- `postgres_data`, `redis_data` を定義（`driver: local`）。各サービスのデータを永続化します。

---

## networks

- `app-network`: ブリッジドライバーを使用したカスタムネットワーク。サービス間通信に使用されます。

---

## 注意点・改善提案

- `DATABASE_URL` やパスワードなどの機密値は `.env.docker` や Docker Secrets を使って安全に管理してください。
- `depends_on: condition: service_healthy` は Compose のバージョンによって動作が異なることがあるため、アプリ側で接続リトライを実装することを推奨します。
- `prisma db push` は開発で有効ですが、本番では明示的なマイグレーション（`prisma migrate`）を利用するほうが安全です。
- `--reload` は開発専用。productionでは取り除いてください。
- ホストマウント（`./app:/app/app`）は開発には便利だが、本番デプロイではイメージにコードを含める方式が望ましい。

---

## よく使うコマンド（PowerShell用）

- ビルドして起動（バックグラウンド）:
```pwsh
docker-compose up -d --build
```

- ログを追跡:
```pwsh
docker-compose logs -f app
```

- 全サービス停止（ボリュームは残す）:
```pwsh
docker-compose down
```

- ボリュームも含めてクリーンアップ:
```pwsh
docker-compose down -v
```

---

## 次の提案
- 必要ならこの `docker-compose.yml` を本番向けに調整（`--reload` 削除、シークレット化、明示的マイグレーション）して反映します。必要なら私が変更案を作成します。
