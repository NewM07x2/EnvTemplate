# FastAPI Template

FastAPI + GraphQL + Prisma のベストプラクティスに基づいたテンプレートプロジェクト

## 📋 目次

- [概要](#概要)
- [機能](#機能)
- [技術スタック](#技術スタック)
- [ディレクトリ構造](#ディレクトリ構造)
- [前提条件](#前提条件)
- [セットアップ](#セットアップ)
- [起動方法](#起動方法)
- [使用方法](#使用方法)
- [開発ガイド](#開発ガイド)
- [テスト](#テスト)
- [デプロイ](#デプロイ)

## 概要

このプロジェクトは、FastAPIを使用したモダンなWebアプリケーション開発のためのテンプレートです。REST APIとGraphQLの両方をサポートし、Prismaを使用したデータベース管理を行います。

## 機能

- ✅ **FastAPI** - 高速で使いやすいPython Webフレームワーク
- ✅ **GraphQL** - Strawberryを使用したGraphQL API
- ✅ **Prisma** - 型安全なORM
- ✅ **認証** - JWT認証のサンプル実装
- ✅ **バリデーション** - Pydanticによる厳密なデータバリデーション
- ✅ **CORS** - クロスオリジンリクエストのサポート
- ✅ **ミドルウェア** - ロギング、タイミングなどのカスタムミドルウェア
- ✅ **Docker** - Docker Composeによる簡単なデプロイ
- ✅ **テスト** - Pytestを使用したテストフレームワーク

## 技術スタック

### コア
- **Python**: 3.12+
- **FastAPI**: 0.115.0+
- **Uvicorn**: 0.30.0+
- **Pydantic**: 2.9.0+

### データベース
- **Prisma**: 0.15.0+ (ORM)
- **PostgreSQL**: 16+ (推奨) / SQLite (開発環境)

### GraphQL
- **Strawberry**: 0.239.0+ (GraphQL実装)

### セキュリティ
- **python-jose**: JWT処理
- **passlib**: パスワードハッシュ化

### オプション (必要に応じて削除可能)
- **Redis**: キャッシュ、セッション管理
- **Celery**: バックグラウンドタスク処理

## ディレクトリ構造

```
python/FastAPI/
├── app/                        # アプリケーションコード
│   ├── __init__.py
│   ├── api/                    # APIエンドポイント
│   │   ├── __init__.py
│   │   └── v1/                 # API v1
│   │       ├── __init__.py
│   │       ├── health.py       # ヘルスチェックエンドポイント
│   │       └── sample_endpoints.py  # サンプルエンドポイント (コピーして使用)
│   ├── core/                   # コア機能
│   │   ├── __init__.py
│   │   ├── config.py           # 設定管理
│   │   ├── database.py         # データベース接続
│   │   └── security.py         # 認証・セキュリティ
│   ├── graphql/                # GraphQL関連
│   │   ├── __init__.py
│   │   ├── schema.py           # GraphQLスキーマ
│   │   ├── types.py            # GraphQL型定義
│   │   └── resolvers.py        # GraphQLリゾルバー (サンプル)
│   ├── middleware/             # カスタムミドルウェア
│   │   ├── __init__.py
│   │   ├── logging_middleware.py
│   │   └── timing_middleware.py
│   ├── models/                 # データモデル (Prismaで生成)
│   ├── repositories/           # データアクセス層
│   │   ├── __init__.py
│   │   └── sample_repository.py  # サンプルリポジトリ (コピーして使用)
│   ├── schemas/                # Pydanticスキーマ
│   │   ├── __init__.py
│   │   └── sample_schema.py    # サンプルスキーマ (コピーして使用)
│   ├── services/               # ビジネスロジック層
│   │   ├── __init__.py
│   │   └── sample_service.py   # サンプルサービス (コピーして使用)
│   └── utils/                  # ユーティリティ関数
│       ├── __init__.py
│       └── helpers.py
├── prisma/                     # Prismaスキーマ
│   └── schema.prisma           # データベーススキーマ定義
├── tests/                      # テストコード
├── main.py                     # アプリケーションエントリーポイント
├── requirements.txt            # Python依存関係
├── pyproject.toml              # Poetryプロジェクト設定
├── Dockerfile                  # Dockerイメージ定義
├── docker-compose.yml          # Docker Compose設定
├── .env.example                # 環境変数サンプル
├── .env.docker                 # Docker用環境変数
├── .gitignore                  # Git除外設定
└── README.md                   # このファイル
```

## 前提条件

- **Python 3.12以上**
- **Node.js 18以上** (Prisma CLIのため)
- **PostgreSQL 16以上** (本番環境推奨) または SQLite (開発環境)
- **Docker & Docker Compose** (オプション)

## セットアップ

### 1. リポジトリのクローン

```bash
cd python/FastAPI
```

### 2. 仮想環境の作成と有効化

```bash
# Windowsの場合
python -m venv venv
.\venv\Scripts\activate

# Linux/Macの場合
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存関係のインストール

#### 方法A: pip使用

```bash
pip install -r requirements.txt
```

#### 方法B: Poetry使用 (推奨)

```bash
pip install poetry
poetry install
```

### 4. 環境変数の設定

```bash
# .env.exampleをコピーして.envを作成
cp .env.example .env

# .envファイルを編集して設定を調整
# 重要: SECRET_KEYは必ず変更してください
```

### 5. Prismaのセットアップ

```bash
# Prisma Clientの生成
prisma generate

# データベースのマイグレーション
# PostgreSQLの場合
prisma db push

# または、マイグレーションファイルを作成
prisma migrate dev --name init
```

## 起動方法

### ローカル開発環境

```bash
# 開発サーバーの起動 (ホットリロード有効)
uvicorn main:app --reload

# または、main.pyを直接実行
python main.py
```

アプリケーションは `http://localhost:8000` で起動します。

### Docker使用

```bash
# .env.dockerファイルを編集 (必要に応じて)
# Docker Composeでサービスを起動
docker-compose up -d

# ログの確認
docker-compose logs -f app

# サービスの停止
docker-compose down
```

## 使用方法

### API ドキュメント

起動後、以下のURLでAPIドキュメントにアクセスできます:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GraphQL Playground**: http://localhost:8000/graphql

### エンドポイント例

#### REST API

```bash
# ヘルスチェック
GET http://localhost:8000/health

# ユーザー一覧取得
GET http://localhost:8000/api/v1/users

# ユーザー作成
POST http://localhost:8000/api/v1/users
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "testuser",
  "password": "password123",
  "first_name": "Test",
  "last_name": "User"
}
```

#### GraphQL

```graphql
# ユーザー一覧取得
query {
  users {
    id
    email
    username
    firstName
    lastName
  }
}

# ユーザー作成
mutation {
  createUser(input: {
    email: "user@example.com"
    username: "testuser"
    password: "password123"
    firstName: "Test"
    lastName: "User"
  }) {
    id
    email
    username
  }
}
```

## 開発ガイド

### 新しいエンドポイントの追加

1. **スキーマ定義** (`app/schemas/`)
   - `sample_schema.py` をコピーして新しいスキーマファイルを作成
   - リクエスト/レスポンスのPydanticモデルを定義

2. **リポジトリ作成** (`app/repositories/`)
   - `sample_repository.py` をコピーしてデータアクセス層を実装
   - データベースとの直接的なやり取りを記述

3. **サービス作成** (`app/services/`)
   - `sample_service.py` をコピーしてビジネスロジックを実装
   - バリデーション、権限チェックなどを実装

4. **エンドポイント作成** (`app/api/v1/`)
   - `sample_endpoints.py` をコピーして新しいエンドポイントファイルを作成
   - FastAPIのルーターを使用してエンドポイントを定義
   - `app/api/v1/__init__.py` でルーターを登録

### GraphQLの追加

1. **型定義** (`app/graphql/types.py`)
   - Strawberryの`@strawberry.type`デコレータを使用して型を定義

2. **リゾルバー実装** (`app/graphql/resolvers.py`)
   - QueryクラスまたはMutationクラスにメソッドを追加

### データベーススキーマの変更

1. `prisma/schema.prisma` を編集
2. マイグレーション実行:
   ```bash
   prisma migrate dev --name <migration_name>
   ```
3. Prisma Clientを再生成:
   ```bash
   prisma generate
   ```

### 不要な機能の削除

#### Redis/Celeryを使用しない場合

1. `requirements.txt` から以下を削除:
   ```
   redis==5.0.8
   celery==5.4.0
   ```

2. `.env.example` から以下を削除:
   ```
   REDIS_URL=...
   CELERY_BROKER_URL=...
   CELERY_RESULT_BACKEND=...
   ```

3. `docker-compose.yml` から `redis` サービスを削除

#### GraphQLを使用しない場合

1. `requirements.txt` から削除:
   ```
   strawberry-graphql[fastapi]==0.239.0
   ```

2. `main.py` から GraphQL関連のインポートと設定を削除

3. `app/graphql/` ディレクトリを削除

## テスト

```bash
# すべてのテストを実行
pytest

# カバレッジ付きでテストを実行
pytest --cov=app --cov-report=html

# 特定のテストファイルのみ実行
pytest tests/test_sample.py
```

## コードフォーマット・Lint

```bash
# コードフォーマット
black app/
isort app/

# Lint
flake8 app/
mypy app/
```

## デプロイ

### Docker使用

```bash
# 本番環境用のビルド
docker build -t fastapi-app:latest .

# イメージの実行
docker run -p 8000:8000 \
  -e DATABASE_URL=<your-database-url> \
  -e SECRET_KEY=<your-secret-key> \
  fastapi-app:latest
```

### 環境変数

本番環境では以下の環境変数を必ず設定してください:

- `DATABASE_URL`: データベース接続URL
- `SECRET_KEY`: JWT署名用のシークレットキー (強力なランダム文字列)
- `APP_ENV`: `production` に設定
- `DEBUG`: `False` に設定

## ライセンス

このテンプレートはMITライセンスの下で公開されています。

## サポート

問題が発生した場合は、GitHubのIssuesセクションで報告してください。

---

**Happy Coding! 🚀**
