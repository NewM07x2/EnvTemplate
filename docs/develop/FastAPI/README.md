# FastAPI ガイド

> **対象者**: Python・FastAPI を初めて使う開発者  
> **関連テンプレート**: `python/FastAPI/`・`next-python/`  
> **所要時間**: 約 60 分

---

## 📚 目次

1. [FastAPI とは](#1-fastapi-とは)
2. [環境構築](#2-環境構築)
3. [テンプレートの構造](#3-テンプレートの構造)
4. [エンドポイントの定義](#4-エンドポイントの定義)
5. [Pydantic によるスキーマ・バリデーション](#5-pydantic-によるスキーマバリデーション)
6. [依存性注入（Depends）](#6-依存性注入depends)
7. [レイヤードアーキテクチャ](#7-レイヤードアーキテクチャ)
8. [設定管理（pydantic-settings）](#8-設定管理pydantic-settings)
9. [自動生成される API ドキュメント](#9-自動生成される-api-ドキュメント)
10. [Docker での起動](#10-docker-での起動)

---

## 1. FastAPI とは

**FastAPI** は Python 向けの高パフォーマンスな Web フレームワークです。

```
特徴:
  ✅ Python の型ヒントから自動でバリデーション
  ✅ Swagger UI / ReDoc が自動生成される
  ✅ async/await による高速な非同期処理
  ✅ Node.js や Go に匹敵するパフォーマンス
  ✅ 学習コストが低い（Flask + 型安全）
```

### Express（Node.js）との比較

```python
# FastAPI
@app.get("/users/{user_id}")
async def get_user(user_id: str) -> UserResponse:
    return await user_service.get_user(user_id)

# → 型ヒントから自動でバリデーション + Swagger ドキュメント生成
```

```typescript
// Express（Node.js）
app.get('/users/:id', async (req, res) => {
  const user = await userService.getUser(req.params.id)
  res.json(user)
  // → バリデーション・ドキュメントは別途設定が必要
})
```

---

## 2. 環境構築

### Python のインストール

```bash
# バージョン確認
python --version
# Python 3.12.x 以上を推奨

# Windows（winget）
winget install Python.Python.3.12
```

### 依存関係のインストール

```bash
cd python/FastAPI

# 仮想環境を作成（推奨）
python -m venv .venv

# 仮想環境を有効化
# Windows
.venv\Scripts\Activate.ps1
# Mac / Linux
source .venv/bin/activate

# パッケージをインストール
pip install -r requirements.txt
```

### ローカルで起動

```bash
# 開発サーバー起動（ホットリロード付き）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# → http://localhost:8000       API
# → http://localhost:8000/docs  Swagger UI
# → http://localhost:8000/redoc ReDoc
```

---

## 3. テンプレートの構造

```
python/FastAPI/
├── main.py               ← エントリポイント
├── requirements.txt      ← 依存パッケージ一覧
├── .env.example          ← 環境変数のサンプル
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── api/              ← エンドポイント定義（Controller 相当）
│   ├── core/
│   │   ├── config.py     ← 設定（環境変数の読み込み）
│   │   └── database.py   ← DB 接続
│   ├── models/           ← DB モデル
│   ├── schemas/          ← Pydantic スキーマ（型定義）
│   ├── services/         ← ビジネスロジック
│   ├── repositories/     ← データアクセス層
│   └── middleware/       ← カスタムミドルウェア
└── tests/                ← テストコード
```

---

## 4. エンドポイントの定義

```python
from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.sample_schema import UserCreate, UserResponse
from app.services.sample_service import UserService

router = APIRouter()

# GET /users → ユーザー一覧を取得
@router.get(
    "/users",
    response_model=list[UserResponse],   # レスポンスの型を宣言
    tags=["users"],                       # Swagger のタグ
    summary="ユーザー一覧を取得",         # Swagger の説明
)
async def get_users(
    skip: int = Query(0, ge=0),           # クエリパラメータ（ge=0 → 0以上）
    limit: int = Query(100, ge=1, le=1000),
    user_service: UserService = Depends(lambda: UserService()),
) -> list[UserResponse]:
    return await user_service.get_users(skip=skip, limit=limit)


# GET /users/{user_id} → 特定ユーザーを取得
@router.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(
    user_id: str,                         # パスパラメータ
    user_service: UserService = Depends(lambda: UserService()),
) -> UserResponse:
    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


# POST /users → ユーザーを作成
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,  # 201 Created を返す
    tags=["users"],
)
async def create_user(
    user_data: UserCreate,                # リクエストボディ（Pydantic モデル）
    user_service: UserService = Depends(lambda: UserService()),
) -> UserResponse:
    return await user_service.create_user(user_data)


# PUT /users/{user_id} → ユーザーを更新
@router.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = Depends(lambda: UserService()),
) -> UserResponse:
    updated = await user_service.update_user(user_id, user_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


# DELETE /users/{user_id} → ユーザーを削除
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(lambda: UserService()),
) -> None:
    await user_service.delete_user(user_id)
```

---

## 5. Pydantic によるスキーマ・バリデーション

**Pydantic** は Python の型ヒントを使ってデータバリデーションを行うライブラリです。

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

# リクエスト用スキーマ
class UserCreate(BaseModel):
    email: EmailStr                                     # メール形式チェック
    username: str = Field(min_length=1, max_length=50) # 文字数制限
    password: str = Field(min_length=8)

    # カスタムバリデーション
    @field_validator('username')
    @classmethod
    def username_must_not_contain_space(cls, v: str) -> str:
        if ' ' in v:
            raise ValueError('スペースは使用できません')
        return v


# レスポンス用スキーマ（パスワードは含めない）
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}  # ORM モデルからの変換を許可


# 更新用スキーマ（すべてのフィールドが任意）
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=1, max_length=50)
```

---

## 6. 依存性注入（Depends）

**Depends** を使って、認証チェック・DB セッション・サービスのインスタンスを注入できます。

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer

security = HTTPBearer()

# DB セッションを注入する依存関数
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# JWT 認証の依存関数
async def get_current_user(token: str = Security(security)):
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# エンドポイントで使う
@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user_id: str = Depends(get_current_user),  # 認証チェック
    db: AsyncSession = Depends(get_db),                # DB セッション
) -> UserResponse:
    return await user_service.get_user(current_user_id, db)
```

---

## 7. レイヤードアーキテクチャ

```
HTTP リクエスト
    ↓
エンドポイント（app/api/）← バリデーション・HTTP ロジック
    ↓
Service（app/services/）  ← ビジネスロジック
    ↓
Repository（app/repositories/）← データアクセス
    ↓
DB（Prisma / SQLAlchemy）
```

```python
# app/services/sample_service.py
class UserService:
    def __init__(self):
        self.users: dict = {}  # 実際は DB を使う

    async def create_user(self, data: UserCreate) -> UserResponse:
        # ビジネスロジック（重複チェック等）
        if any(u["email"] == data.email for u in self.users.values()):
            raise HTTPException(status_code=409, detail="Email already exists")

        user_id = str(uuid.uuid4())
        user = {"id": user_id, "email": data.email, "username": data.username}
        self.users[user_id] = user
        return UserResponse(**user)

    async def get_user(self, user_id: str) -> UserResponse | None:
        user = self.users.get(user_id)
        return UserResponse(**user) if user else None
```

---

## 8. 設定管理（pydantic-settings）

```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # .env ファイルから自動で読み込む
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "FastAPI Template"
    DEBUG: bool = True

    # DB
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/app"

    # セキュリティ
    SECRET_KEY: str = "change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

`.env` ファイル：

```env
APP_NAME=My API
DEBUG=true
DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp
SECRET_KEY=super-secret-key-change-this
ALLOWED_ORIGINS=["http://localhost:3000","https://example.com"]
```

---

## 9. 自動生成される API ドキュメント

FastAPI はコードから **Swagger UI** と **ReDoc** を自動生成します。

```
http://localhost:8000/docs    → Swagger UI（ブラウザからリクエスト送信可能）
http://localhost:8000/redoc   → ReDoc（読みやすい API ドキュメント）
```

デコレータのパラメータでドキュメントを充実させられます：

```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="新規ユーザーを作成",
    description="メールアドレスとパスワードで新規ユーザーを登録します。",
    responses={
        201: {"description": "作成成功"},
        409: {"description": "メールアドレスが既に使用されている"},
        422: {"description": "バリデーションエラー"},
    },
)
```

---

## 10. Docker での起動

```bash
cd python/FastAPI

# 環境変数ファイルを作成
cp .env.example .env

# コンテナを起動
docker compose up -d

# ログを確認
docker compose logs -f

# API ドキュメントを確認
# → http://localhost:8000/docs

# テストを実行
docker compose exec api pytest tests/ -v
```

### Next.js との組み合わせ（`next-python/`）

```bash
cd next-python
docker compose up -d
# Next.js  → http://localhost:3000
# FastAPI  → http://localhost:8000/docs
```

Next.js から FastAPI を呼び出す：

```typescript
// src/lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function getUsers() {
  const res = await fetch(`${API_BASE}/api/users`)
  if (!res.ok) throw new Error('Failed to fetch users')
  return res.json()
}
```

---

## 📌 まとめ

| 概念 | FastAPI | Express（Node.js） |
|------|---------|-----------------|
| エンドポイント定義 | `@router.get(...)` | `router.get(...)` |
| バリデーション | Pydantic（型ヒントで自動） | zod / express-validator |
| 設定管理 | pydantic-settings | dotenv |
| API ドキュメント | 自動生成（Swagger UI） | swagger-jsdoc 等が必要 |
| 型システム | Python 型ヒント | TypeScript |
| ORM | Prisma（Python） / SQLAlchemy | Prisma / Drizzle |

```bash
# よく使うコマンド
uvicorn main:app --reload    # 開発サーバー起動
pytest tests/ -v             # テスト実行
pip freeze > requirements.txt  # 依存関係を保存
```
