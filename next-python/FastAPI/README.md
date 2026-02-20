# FastAPI + GraphQL + Prisma テンプレート

GraphQL と Prisma をSSRで利用する FastAPI アプリケーション開発用のテンプレートです。
このフォルダをコピーして新しいプロジェクトをすぐに開始できます。

## 📋 目次

- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [前提条件](#前提条件)
- [セットアップ](#セットアップ)
- [起動方法](#起動方法)
- [API エンドポイント](#apiエンドポイント)
- [GraphQL の使用](#graphqlの使用)
- [Prisma の使用](#prismaの使用)
- [開発ガイド](#開発ガイド)
- [テスト](#テスト)
- [デプロイ](#デプロイ)

## 🛠️ 技術スタック

- **Python**: 3.12+
- **FastAPI**: 0.115.0+ (高速 Web フレームワーク)
- **Uvicorn**: 0.30.0+ (ASGI サーバー)
- **Strawberry GraphQL**: 0.239.0+ (GraphQL 実装)
- **Prisma**: 0.15.0+ (ORM)
- **PostgreSQL**: 16+ (推奨)
- **Pydantic**: 2.9.0+ (データバリデーション)
- **python-jose**: JWT 認証
- **passlib**: パスワードハッシュ化

## 📁 プロジェクト構成

```
FastAPI/
├── app/                        # アプリケーションコード
│   ├── api/                    # REST API エンドポイント
│   │   ├── __init__.py
│   │   └── health.py           # ヘルスチェック
│   ├── core/                   # コア機能
│   │   ├── config.py           # 設定管理
│   │   ├── database.py         # データベース接続
│   │   └── security.py         # 認証・セキュリティ
│   ├── graphql/                # GraphQL 関連
│   │   ├── schema.py           # GraphQL スキーマ
│   │   ├── types.py            # GraphQL 型定義
│   │   └── resolvers/          # GraphQL リゾルバー
│   │       ├── queries/        # Query リゾルバー
│   │       └── mutations/      # Mutation リゾルバー
│   ├── middleware/             # カスタムミドルウェア
│   │   ├── logging_middleware.py
│   │   └── timing_middleware.py
│   ├── models/                 # データモデル
│   ├── repositories/           # データアクセス層
│   ├── schemas/                # Pydantic スキーマ
│   ├── services/               # ビジネスロジック層
│   └── utils/                  # ユーティリティ関数
├── prisma/                     # Prisma スキーマ
│   └── schema.prisma           # データベーススキーマ定義
├── tests/                      # テストコード
├── main.py                     # アプリケーションエントリーポイント
├── requirements.txt            # Python 依存関係
├── Dockerfile                  # Docker イメージ定義
├── .env.example                # 環境変数サンプル
├── .gitignore                  # Git 除外設定
└── README.md                   # このファイル
```

## 前提条件

- **Python 3.12以上**
- **Node.js 18以上** (Prisma CLI のため)
- **PostgreSQL 16以上**（推奨）または SQLite（開発環境）
- **Docker & Docker Compose**（オプション）

## セットアップ

### 1. 仮想環境の作成と有効化

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

```bash
cp .env.example .env
```

`.env` ファイルを編集して必要な値を設定：

```env
# Application
APP_NAME=FastAPI App
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Prisma のセットアップ

```bash
# Prisma Client を生成
prisma generate

# データベースにスキーマを適用
prisma db push

# または、マイグレーションを作成して実行
prisma migrate dev --name init
```

## 起動方法

### ローカル開発環境

```bash
# 開発サーバーを起動 (ホットリロード有効)
uvicorn main:app --reload

# または、ポートを指定
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

アプリケーションは `http://localhost:8000` で起動します。

### Docker 使用

```bash
# イメージをビルドして起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d

# ログを確認
docker-compose logs -f app

# コンテナを停止
docker-compose down
```

### アクセス

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GraphQL Playground**: http://localhost:8000/graphql

## 🔌 API エンドポイント

### REST API

```bash
# ヘルスチェック
GET /health

# ユーザー一覧取得
GET /api/users

# ユーザー作成
POST /api/users
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "Test User",
  "age": 25
}
```

## 🔄 GraphQL の使用

### Query の例

```graphql
query {
  users {
    id
    email
    name
    age
  }
}
```

### Mutation の例

```graphql
mutation {
  createUser(input: {
    email: "user@example.com"
    name: "Test User"
    age: 25
  }) {
    id
    email
    name
  }
}
```

### GraphQL リゾルバーの実装

`app/graphql/resolvers/queries/` にクエリを定義：

```python
from typing import List
import strawberry
from app.graphql.types import UserType

@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> List[UserType]:
        """ユーザー一覧を取得"""
        # Prisma でデータ取得
        users = await prisma.user.find_many()
        return users
```

## 🗄️ Prisma の使用

### スキーマ定義

`prisma/schema.prisma` を編集：

```prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  age   Int?
  createdAt DateTime @default(now()) @map("created_at")

  @@map("users")
}
```

### マイグレーション実行

```bash
# マイグレーション作成・実行
prisma migrate dev --name add_users

# スキーマをデータベースに適用（マイグレーション履歴なし）
prisma db push

# Prisma Studio でデータ確認・編集
prisma studio
```

### データ操作

Repository パターンを使用：

```python
# app/repositories/user_repository.py
from prisma import Prisma

prisma = Prisma()

class UserRepository:
    async def get_all(self):
        return await prisma.user.find_many()
    
    async def create(self, email: str, name: str, age: int):
        return await prisma.user.create(
            data={"email": email, "name": name, "age": age}
        )
```

## 💻 開発ガイド

### 新しいエンドポイントの追加

1. **Pydantic スキーマ定義** (`app/schemas/`)

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str
    age: int
```

2. **Repository 作成** (`app/repositories/`)

```python
class UserRepository:
    async def create(self, data: dict):
        return await prisma.user.create(data=data)
```

3. **Service 作成** (`app/services/`)

```python
class UserService:
    async def create_user(self, user_data: UserCreate):
        # バリデーション・ビジネスロジック
        return await UserRepository().create(user_data.dict())
```

4. **API エンドポイント** (`app/api/users.py`)

```python
from fastapi import APIRouter
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
async def create_user(user_data: UserCreate):
    return await UserService().create_user(user_data)
```

5. **エンドポイント登録** (`app/api/__init__.py`)

```python
from .users import router as users_router

api_router.include_router(users_router)
```

### GraphQL の追加

1. **型定義** (`app/graphql/types.py`)

```python
import strawberry

@strawberry.type
class User:
    id: int
    email: str
    name: str | None
```

2. **Query/Mutation 実装** (`app/graphql/resolvers/`)

```python
@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> list[User]:
        return await prisma.user.find_many()
```

## 🧪 テスト

```bash
# すべてのテストを実行
pytest

# カバレッジ付きで実行
pytest --cov=app

# 特定のテストのみ実行
pytest tests/test_health.py
```

## 📋 コードフォーマット・Lint

```bash
# コードフォーマット
black app/
isort app/

# Lint チェック
flake8 app/
mypy app/
```

## 🚀 デプロイ

### Docker でのデプロイ

```bash
# イメージをビルド
docker build -t fastapi-app:latest .

# イメージを実行
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=your-secret-key \
  fastapi-app:latest
```

### 本番環境での設定

`.env` で以下を設定：

```env
DEBUG=False
SECRET_KEY=<強力なランダム文字列>
DATABASE_URL=<本番 DB URL>
ALLOWED_ORIGINS=["https://example.com"]
```

## ⚠️ 重要な注意点

1. **SECRET_KEY** は必ず強力なランダム文字列に変更してください
2. **本番環境では DEBUG=False** に設定
3. **Prisma Client の再生成** - スキーマ変更後に実行：`prisma generate`
4. **.env ファイルは Git にコミットしない** （`.gitignore` に含まれています）

## 📚 参考リンク

- [FastAPI ドキュメント](https://fastapi.tiangolo.com/)
- [Strawberry GraphQL ドキュメント](https://strawberry.rocks/)
- [Prisma ドキュメント](https://www.prisma.io/docs/)
- [Pydantic ドキュメント](https://docs.pydantic.dev/)

---

Happy Coding! 🚀
