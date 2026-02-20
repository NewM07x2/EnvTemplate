# Docker セットアップガイド

Docker を使用した開発環境のセットアップと実行方法について説明します。

## 目次

- [前提条件](#前提条件)
- [クイックスタート](#クイックスタート)
- [環境変数設定](#環境変数設定)
- [Docker コマンド](#docker-コマンド)
- [トラブルシューティング](#トラブルシューティング)
- [本番環境設定](#本番環境設定)

## 前提条件

以下がインストールされていることを確認してください：

- **Docker**: 20.10 以上
- **Docker Compose**: 2.0 以上

```bash
# バージョン確認
docker --version
docker-compose --version
```

### Docker Desktop インストール

- **Windows/Mac**: [Docker Desktop](https://www.docker.com/products/docker-desktop) をダウンロード
- **Linux**: 以下コマンドでインストール

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# CentOS/RHEL
sudo yum install docker docker-compose
```

## クイックスタート

### 1. 環境ファイルの準備

```bash
# プロジェクトルートで
cp .env.example .env

# または docker ディレクトリから実行
cd docker
cp ../.env.example .env
```

### 2. Docker イメージのビルド

```bash
# 最初の実行時、またはファイル変更時
docker-compose build

# 特定のサービスのみビルド
docker-compose build api       # FastAPI のみ
docker-compose build frontend  # Next.js のみ
```

### 3. コンテナの起動

```bash
# 全サービスを起動
docker-compose up

# バックグラウンド実行
docker-compose up -d

# 特定のサービスのみ起動
docker-compose up postgres api  # PostgreSQL と FastAPI のみ
```

### 4. ログ確認

```bash
# すべてのサービスのログを表示
docker-compose logs -f

# 特定のサービスのログのみ
docker-compose logs -f api       # FastAPI のログ
docker-compose logs -f frontend  # Next.js のログ
docker-compose logs -f postgres  # PostgreSQL のログ

# 最後の100行を表示
docker-compose logs --tail=100
```

### 5. アプリケーションアクセス

起動後、以下の URL でアクセスできます：

- **Next.js フロントエンド**: http://localhost:3000
- **FastAPI バックエンド**: http://localhost:8000
- **GraphQL Playground**: http://localhost:8000/graphql
- **API ドキュメント**: http://localhost:8000/docs

## 環境変数設定

### .env ファイルの重要な設定

```env
# アプリケーション環境
APP_ENV=development          # development または production
DEBUG=True                   # 開発時は True

# PostgreSQL
POSTGRES_USER=postgres       # DB ユーザー名
POSTGRES_PASSWORD=postgres   # DB パスワード（本番では複雑にする）
POSTGRES_DB=nextpy_db        # DB 名
POSTGRES_PORT=5432           # DB ポート

# サービスポート
API_PORT=8000               # FastAPI ポート
FRONTEND_PORT=3000          # Next.js ポート

# 認証（本番では必ず変更）
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### 本番環境用 .env の例

```env
APP_ENV=production
DEBUG=False
POSTGRES_PASSWORD=<secure-random-password>
JWT_SECRET=<secure-random-secret>
LOG_LEVEL=WARNING
```

## Docker コマンド

### ライフサイクル管理

```bash
# コンテナの起動
docker-compose up -d

# コンテナの停止
docker-compose stop

# コンテナの再起動
docker-compose restart

# コンテナの停止と削除
docker-compose down

# ボリュームも含めて削除（注意：データが失われます）
docker-compose down -v

# コンテナを再作成して起動
docker-compose up -d --force-recreate
```

### ステータス確認

```bash
# 実行中のコンテナを表示
docker-compose ps

# 詳細情報を表示
docker ps -a

# ボリュームを確認
docker volume ls

# ネットワークを確認
docker network ls
```

### データベース操作

```bash
# PostgreSQL コンテナにアクセス
docker-compose exec postgres psql -U postgres -d nextpy_db

# Prisma マイグレーション実行
docker-compose exec api prisma migrate dev

# Prisma スキーマの確認
docker-compose exec api prisma studio

# データベースをリセット（注意：すべてのデータが削除されます）
docker-compose exec api prisma migrate reset
```

### アプリケーション操作

```bash
# FastAPI コンテナで Python コマンドを実行
docker-compose exec api python -m pytest

# Next.js コンテナで npm コマンドを実行
docker-compose exec frontend npm install package-name

# シェルアクセス
docker-compose exec api bash          # FastAPI
docker-compose exec frontend sh       # Next.js
```

### イメージ管理

```bash
# イメージ一覧を表示
docker images

# 不要なイメージを削除
docker image prune

# ビルドキャッシュをクリア
docker-compose build --no-cache

# 全ローカルイメージを削除
docker rmi $(docker images -q)
```

## トラブルシューティング

### ポートがすでに使用されている

```
Error: Port 3000 is already in use

# 解決方法 1: ポート番号を変更
FRONTEND_PORT=3001 docker-compose up

# 解決方法 2: 既存プロセスを終了
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

### データベース接続エラー

```
Error: Connection refused on postgres:5432

# 解決方法
# 1. PostgreSQL ヘルスチェック確認
docker-compose ps

# 2. ログ確認
docker-compose logs postgres

# 3. コンテナ再起動
docker-compose restart postgres

# 4. 完全リセット
docker-compose down -v
docker-compose up -d
```

### ビルドエラー

```bash
# 解決方法：キャッシュをクリアしてリビルド
docker-compose build --no-cache --pull

# または全削除して再構築
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### メモリ不足エラー

```
Error: Cannot allocate memory

# 解決方法: Docker の メモリ制限を増やす
# Docker Desktop 設定 → Resources → Memory を増加（推奨: 4GB以上）

# Dockerfile-web の NODE_OPTIONS も調整
ENV NODE_OPTIONS="--max-old-space-size=1024"
```

### ホットリロード が機能しない

```bash
# 原因：ボリュームマウント設定の問題
# 解決方法 1: コンテナ再起動
docker-compose restart api frontend

# 解決方法 2: キャッシュクリア
docker-compose down
rm -rf .docker-cache .next node_modules
docker-compose up -d

# 解決方法 3: docker-compose.override.yml で上書き
# ファイルを作成して特定環境用設定を追加
```

### サービス起動順序の問題

```
解決方法: Docker Compose の depends_on と healthcheck を確認

# ログで起動順序を確認
docker-compose logs --timestamps

# 各サービスのヘルスチェック確認
docker-compose ps
```

## 本番環境設定

### セキュリティチェックリスト

- [ ] `DEBUG=False` に設定
- [ ] `JWT_SECRET` を安全なランダム文字列に変更
- [ ] `POSTGRES_PASSWORD` を複雑なパスワードに変更
- [ ] `ALLOWED_ORIGINS` を本番ドメインに設定
- [ ] `LOG_LEVEL` を `WARNING` に設定
- [ ] `.env` ファイルを `.gitignore` に追加

### 本番用 docker-compose.yml の作成

```bash
# 基本ファイルをコピー
cp docker-compose.yml docker-compose.prod.yml

# 本番用設定を編集
# - rebuild cache を無効化
# - ボリューム設定を削除
# - リスタートポリシーを always に設定
```

### デプロイ例（Heroku）

```bash
# Heroku CLI インストール後
heroku login
heroku create your-app-name

# Docker を使用してデプロイ
heroku container:push web --app your-app-name
heroku container:release web --app your-app-name
```

### デプロイ例（AWS ECS）

```bash
# ECR にプッシュ
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/app:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/app:latest

# ECS にデプロイ
# AWS コンソール or terraform/CDK で設定
```

## よくある質問

### Q: Docker イメージサイズを削減したい

```bash
# ビルドステージを最適化
# Dockerfile で multi-stage build を使用
# - 依存関係のみを別ステージでビルド
# - 最終ステージで必要ファイルのみコピー

# 結果：イメージサイズを 50-70% 削減可能
```

### Q: 本番環境でホットリロードを無効化したい

```yaml
# docker-compose.prod.yml
services:
  api:
    command: "uvicorn main:app --host 0.0.0.0 --port 8000"
  frontend:
    command: "npm run build && npm start"
```

### Q: 複数環境（dev/staging/prod）を管理したい

```bash
# ファイル構成
docker-compose.yml              # 共通設定
docker-compose.override.yml     # ローカル開発用（.gitignore に追加）
docker-compose.staging.yml      # ステージング用
docker-compose.prod.yml         # 本番用

# 実行
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## まとめ

- **開発**：`docker-compose up -d` で全サービス起動
- **テスト**：`docker-compose exec api pytest` でテスト実行
- **デバッグ**：`docker-compose logs -f` でログ確認
- **本番**：`.env.example` を参考に本番用 `.env` を作成してデプロイ

詳細は [docker-compose.yml](docker-compose.yml) の設定を参照してください。
