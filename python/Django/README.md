# Django Template# template

python template

Django 5.0 + GraphQL + Prisma + Docker のベストプラクティステンプレート

## 📋 目次

- [概要](#概要)
- [機能](#機能)
- [技術スタック](#技術スタック)
- [ディレクトリ構造](#ディレクトリ構造)
- [前提条件](#前提条件)
- [セットアップ](#セットアップ)
- [Docker での起動方法](#dockerでの起動方法)
- [ローカル開発環境での起動](#ローカル開発環境での起動)
- [使用方法](#使用方法)
- [開発ガイド](#開発ガイド)
- [テスト](#テスト)
- [デプロイ](#デプロイ)

## 概要

このプロジェクトは、Django 5.0 を使用したモダンな Web アプリケーション開発のためのテンプレートです。  
REST API と GraphQL の両方をサポートし、Prisma を使用したデータベース管理も可能です（Django ORM と併用可能）。

## 機能

- ✅ **Django 5.0** - 最新の Django フレームワーク
- ✅ **Django REST Framework** - 強力な REST API
- ✅ **GraphQL** - Graphene-Django を使用した GraphQL API
- ✅ **Prisma (Optional)** - 型安全な ORM（Django ORM と併用可能）
- ✅ **JWT 認証** - SimpleJWT による認証システム
- ✅ **カスタムユーザーモデル** - 拡張可能なユーザー管理
- ✅ **レイヤードアーキテクチャ** - Repository/Service/Controller パターン
- ✅ **Docker** - Docker Compose による簡単なデプロイ
- ✅ **OpenAPI/Swagger** - drf-spectacular による API ドキュメント
- ✅ **Celery (Optional)** - バックグラウンドタスク処理
- ✅ **テスト** - pytest-django を使用したテストフレームワーク

## 技術スタック

### コア
- **Python**: 3.12+
- **Django**: 5.0+
- **Django REST Framework**: 3.14+
- **Graphene-Django**: 3.2+

### データベース
- **PostgreSQL**: 16+ (推奨)
- **Prisma**: 0.15.0+ (オプション - Django ORM と併用可能)

### 認証・セキュリティ
- **djangorestframework-simplejwt**: JWT 認証
- **django-cors-headers**: CORS サポート

### オプション機能（必要に応じて削除可能）
- **Redis**: キャッシュ、セッション管理
- **Celery**: バックグラウンドタスク処理
- **django-celery-beat**: スケジュールタスク

## ディレクトリ構造

```
python/Django/
├── apps/                          # Django アプリケーション
│   ├── users/                     # ユーザー管理アプリ (サンプル)
│   │   ├── __init__.py
│   │   ├── admin.py              # Django Admin 設定
│   │   ├── apps.py               # アプリ設定
│   │   ├── models.py             # User モデル
│   │   ├── repositories.py       # データアクセス層 (サンプル)
│   │   ├── schema.py             # GraphQL スキーマ (サンプル)
│   │   ├── serializers.py        # DRF シリアライザー (サンプル)
│   │   ├── services.py           # ビジネスロジック層 (サンプル)
│   │   ├── urls.py               # URL 設定
│   │   └── views.py              # ビュー/コントローラー (サンプル)
│   └── posts/                     # 投稿管理アプリ (サンプル)
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py             # Post, Category モデル
│       ├── repositories.py       # データアクセス層 (サンプル)
│       ├── schema.py             # GraphQL スキーマ (サンプル)
│       ├── serializers.py        # DRF シリアライザー (サンプル)
│       ├── services.py           # ビジネスロジック層 (サンプル)
│       ├── urls.py
│       └── views.py              # ビュー/コントローラー (サンプル)
├── config/                        # Django プロジェクト設定
│   ├── __init__.py
│   ├── asgi.py                   # ASGI 設定
│   ├── schema.py                 # GraphQL ルートスキーマ
│   ├── settings.py               # Django 設定
│   ├── urls.py                   # ルート URL 設定
│   └── wsgi.py                   # WSGI 設定
├── core/                          # コア機能
│   ├── __init__.py
│   ├── urls.py
│   └── views.py                  # ヘルスチェック等
├── docker/                        # Docker 関連ファイル
│   └── Dockerfile.backend        # バックエンド用 Dockerfile
├── prisma/                        # Prisma スキーマ (オプション)
│   └── schema.prisma             # データベーススキーマ定義
├── tests/                         # テストコード
│   ├── __init__.py
│   ├── conftest.py               # pytest 設定
│   └── test_sample.py            # サンプルテスト
├── manage.py                      # Django 管理コマンド
├── requirements.txt               # Python 依存関係
├── pyproject.toml                 # Poetry プロジェクト設定
├── docker-compose.yml             # Docker Compose 設定
├── .env.example                   # 環境変数サンプル
├── .env.docker                    # Docker 用環境変数
├── .gitignore                     # Git 除外設定
└── README.md                      # このファイル
```

## 前提条件

- **Python 3.12 以上**
- **Docker & Docker Compose** (Docker での実行の場合)
- **PostgreSQL 16 以上** (ローカル開発の場合)
- **Node.js 18 以上** (Prisma CLI のため、オプション)

## セットアップ

### 環境変数の設定

```bash
# .env.example をコピーして .env を作成
cp .env.example .env

# .env ファイルを編集して設定を調整
# 重要: SECRET_KEY は必ず変更してください
```

### Prisma のセットアップ (オプション)

Prisma を使用する場合:

```bash
# Prisma CLI のインストール (グローバル)
npm install -g prisma

# Prisma Client の生成
prisma generate

# Prisma マイグレーション (Django migrations とは別)
prisma db push
```

**注意**: このテンプレートでは Django ORM と Prisma を併用できます。Prisma が不要な場合は、`prisma/` ディレクトリと関連する依存関係を削除してください。

## Docker での起動方法

### 1. 環境変数の確認

```bash
# .env.docker ファイルを確認・編集
# DATABASE_URL, SECRET_KEY などを適宜変更
```

### 2. Docker イメージのビルドと起動

```powershell
# すべてのサービスを起動
docker-compose up -d --build

# ログの確認
docker-compose logs -f app

# 特定のサービスのログを確認
docker-compose logs -f app
docker-compose logs -f db
```

### 3. データベースマイグレーション

```powershell
# マイグレーションは自動で実行されますが、手動で実行する場合:
docker-compose exec app python manage.py migrate

# スーパーユーザーの作成
docker-compose exec app python manage.py createsuperuser
```

### 4. アクセス

アプリケーションは以下の URL でアクセスできます:

- **アプリケーション**: <http://localhost:8000>
- **Admin**: <http://localhost:8000/admin>
- **Swagger UI**: <http://localhost:8000/api/docs/>
- **ReDoc**: <http://localhost:8000/api/redoc/>
- **GraphQL Playground**: <http://localhost:8000/graphql/>

### 5. サービスの停止

```powershell
# サービスの停止
docker-compose down

# ボリュームも含めて削除
docker-compose down -v
```

## ローカル開発環境での起動

### 1. 仮想環境の作成と有効化

```powershell
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化 (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 2. 依存関係のインストール

```powershell
# pip を使用
pip install -r requirements.txt

# または Poetry を使用 (推奨)
pip install poetry
poetry install
```

### 3. データベースのセットアップ

```powershell
# マイグレーションファイルの作成
python manage.py makemigrations

# マイグレーションの実行
python manage.py migrate

# スーパーユーザーの作成
python manage.py createsuperuser
```

### 4. 開発サーバーの起動

```powershell
# 開発サーバーの起動
python manage.py runserver

# または Gunicorn を使用
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --reload
```

## 使用方法

### REST API エンドポイント例

#### ユーザー管理

```bash
# ユーザー一覧取得
GET http://localhost:8000/api/users/

# ユーザー作成
POST http://localhost:8000/api/users/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "testuser",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "Test",
  "last_name": "User"
}

# ユーザー詳細取得
GET http://localhost:8000/api/users/1/

# 現在のユーザー情報取得
GET http://localhost:8000/api/users/me/
```

#### 投稿管理

```bash
# 投稿一覧取得
GET http://localhost:8000/api/posts/

# 公開済み投稿のみ取得
GET http://localhost:8000/api/posts/?published=true

# 投稿作成
POST http://localhost:8000/api/posts/
Content-Type: application/json
Authorization: Bearer <your-jwt-token>

{
  "title": "My First Post",
  "slug": "my-first-post",
  "content": "This is the content of my first post",
  "excerpt": "Short description",
  "is_published": true
}
```

### GraphQL クエリ例

```graphql
# ユーザー一覧取得
query {
  users(skip: 0, limit: 10) {
    id
    email
    username
    firstName
    lastName
    fullName
  }
}

# 投稿一覧取得
query {
  posts(publishedOnly: true, skip: 0, limit: 10) {
    id
    title
    slug
    excerpt
    author {
      username
      fullName
    }
    category {
      name
    }
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
    success
    message
    user {
      id
      email
    }
  }
}
```

## 開発ガイド

### 新しい Django App の追加

1. **App の作成**

```powershell
python manage.py startapp <app_name> apps/<app_name>
```

2. **設定への追加**

`config/settings.py` の `INSTALLED_APPS` に追加:

```python
INSTALLED_APPS = [
    # ...
    'apps.<app_name>',
]
```

### レイヤードアーキテクチャのベストプラクティス

このテンプレートは以下の層構造を採用しています:

1. **Models** (`models.py`): データベース構造の定義
2. **Repositories** (`repositories.py`): データアクセス層 (DB との直接的なやり取り)
3. **Services** (`services.py`): ビジネスロジック層 (バリデーション、権限チェック等)
4. **Serializers** (`serializers.py`): データのシリアライズ/デシリアライズ
5. **Views** (`views.py`): コントローラー層 (HTTP リクエスト/レスポンス処理)
6. **URLs** (`urls.py`): ルーティング設定

**サンプルファイルをコピーして使用**:

```powershell
# users アプリのファイルをコピーして新しいアプリを作成
cp apps/users/repositories.py apps/<new_app>/repositories.py
cp apps/users/services.py apps/<new_app>/services.py
# ...
```

### 不要な機能の削除

#### Celery/Redis を使用しない場合

1. `requirements.txt` から削除: `celery`, `redis`, `django-celery-beat`
2. `config/settings.py` から Celery 設定を削除
3. `docker-compose.yml` から `redis`, `celery_worker`, `celery_beat` サービスを削除

#### GraphQL を使用しない場合

1. `requirements.txt` から削除: `graphene-django`, `graphql-core`
2. 各アプリの `schema.py` を削除
3. `config/urls.py` から GraphQL エンドポイントを削除

#### Prisma を使用しない場合

1. `requirements.txt` から `prisma` を削除
2. `prisma/` ディレクトリを削除
3. `docker/Dockerfile.backend` から Prisma 関連のコマンドを削除

## テスト

```powershell
# すべてのテストを実行
pytest

# カバレッジ付きでテストを実行
pytest --cov=apps --cov=config --cov-report=html

# Docker 環境でテストを実行
docker-compose exec app pytest
```

## デプロイ

### 本番環境用の設定

必ず以下の環境変数を設定してください:

- `SECRET_KEY`: Django のシークレットキー
- `DEBUG`: `False` に設定
- `ALLOWED_HOSTS`: 本番ドメインを追加
- `DATABASE_URL`: 本番データベース接続 URL
- `CORS_ALLOWED_ORIGINS`: 許可するオリジンのリスト

## ライセンス

MIT License

---

**Happy Coding! 🚀**
