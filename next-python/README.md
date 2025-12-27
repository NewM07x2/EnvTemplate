# Next.js + FastAPI テンプレート環境

このフォルダは、**Next.js (フロントエンド)** + **FastAPI (バックエンド API)** + **PostgreSQL** + **Docker** を使用したフルスタックアプリケーションのテンプレート環境です。
このフォルダをコピーして新しいプロジェクトを開始できます。

## 📋 目次

- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [セットアップ方法](#セットアップ方法)
- [開発方法](#開発方法)
- [GraphQL 使用方法](#graphql使用方法)
- [API 開発](#api開発)
- [運用方法](#運用方法)
- [注意点](#注意点)

## 🛠️ 技術スタック

### フロントエンド (Next.js)

- **Next.js 14.1.0** - React フレームワーク (App Router)
- **React 18** - UI ライブラリ
- **TypeScript 5** - 型安全な開発
- **Tailwind CSS** - ユーティリティファースト CSS
- **Redux Toolkit** - 状態管理
- **urql** - GraphQL クライアント

### バックエンド (FastAPI)

- **FastAPI 0.115.0** - 高性能 Python ウェブフレームワーク
- **Strawberry GraphQL** - Python 用 GraphQL ライブラリ
- **Prisma (Python)** - データベース ORM
- **Pydantic** - データバリデーション
- **Uvicorn** - ASGI サーバー

### インフラ

- **Docker & Docker Compose** - コンテナ化
- **PostgreSQL 16** - データベース

## 📁 プロジェクト構成

```
next-python/
├── docker-compose.yml          # 統合Docker Compose設定
├── .env.example               # 環境変数のサンプル
├── FastAPI/                   # バックエンドAPI
│   ├── main.py               # FastAPIエントリーポイント
│   ├── Dockerfile            # FastAPI用Dockerfile
│   ├── requirements.txt      # Python依存関係
│   ├── .env.example         # FastAPI環境変数サンプル
│   ├── prisma/
│   │   └── schema.prisma    # データベーススキーマ
│   └── app/
│       ├── api/             # REST APIエンドポイント
│       ├── core/            # 設定・DB接続
│       ├── graphql/         # GraphQLスキーマ・リゾルバ
│       ├── models/          # データモデル
│       ├── repositories/    # データアクセス層
│       ├── services/        # ビジネスロジック
│       ├── schemas/         # Pydanticスキーマ
│       └── middleware/      # ミドルウェア
└── next/                     # フロントエンド
    ├── docker/
    │   └── Dockerfile       # Next.js用Dockerfile
    ├── .env.example         # Next.js環境変数サンプル
    ├── package.json         # Node.js依存関係
    └── src/
        ├── app/             # Next.js App Router
        ├── components/      # UIコンポーネント
        ├── lib/
        │   └── graphql/     # GraphQL設定(urql)
        ├── store/           # Redux store
        └── styles/          # スタイル
```

## 🚀 セットアップ方法

### 1. このフォルダをコピー

新しいプロジェクトを作成する際は、このフォルダ全体をコピーします:

```bash
# Windowsの場合
cp -r next-python my-new-project
cd my-new-project
```

### 2. 環境変数の設定

#### ルートの環境変数

`.env.example`をコピーして`.env`を作成:

```bash
cp .env.example .env
```

#### FastAPI の環境変数

```bash
cd FastAPI
cp .env.example .env
cd ..
```

#### Next.js の環境変数

```bash
cd next
cp .env.example .env
cd ..
```

### 3. Docker コンテナの起動

プロジェクトルートで実行:

```bash
# コンテナのビルドと起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d
```

### 4. アクセス確認

- **フロントエンド**: http://localhost:3000
- **FastAPI ドキュメント**: http://localhost:8000/docs
- **GraphQL Playground**: http://localhost:8000/graphql
- **PostgreSQL**: localhost:5432

## 💻 開発方法

### Docker を使用する場合（推奨）

```bash
# 全サービスの起動
docker-compose up

# 特定のサービスのみ起動
docker-compose up frontend
docker-compose up api

# ログの確認
docker-compose logs -f api
docker-compose logs -f frontend

# コンテナの停止
docker-compose down

# ボリュームも削除して完全にクリーンアップ
docker-compose down -v

# コンテナに入る
docker-compose exec api bash
docker-compose exec frontend sh
```

### ローカル環境で開発する場合

#### FastAPI (バックエンド)

```bash
cd FastAPI

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# Prisma Clientの生成
prisma generate

# データベースマイグレーション
prisma db push

# 開発サーバーの起動
uvicorn main:app --reload
```

#### Next.js (フロントエンド)

```bash
cd next

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev
```

### データベース操作

#### Prisma マイグレーション

```bash
# FastAPIコンテナに入る
docker-compose exec api bash

# スキーマをデータベースに適用
prisma db push

# マイグレーションファイルを作成
prisma migrate dev --name migration_name

# Prisma Studioでデータを確認
prisma studio
```

## 🔄 GraphQL 使用方法

### フロントエンド (Next.js) から GraphQL を使用

**urql** を使用して FastAPI の GraphQL エンドポイントにアクセスします。

#### 設定

- エンドポイント: `http://localhost:8000/graphql`
- 設定ファイル: `next/src/lib/graphql/urqlClient.ts`

#### 使用例

```typescript
'use client'
import { useQuery } from 'urql'

const USERS_QUERY = `
  query {
    users {
      id
      email
      username
    }
  }
`

export default function UsersPage() {
  const [result] = useQuery({ query: USERS_QUERY })

  if (result.fetching) return <div>Loading...</div>
  if (result.error) return <div>Error: {result.error.message}</div>

  return (
    <div>
      {result.data.users.map((user) => (
        <div key={user.id}>{user.username}</div>
      ))}
    </div>
  )
}
```

### バックエンド (FastAPI) での GraphQL 定義

#### スキーマ定義

`FastAPI/app/graphql/schemas/` にスキーマを定義:

```python
# user_schema.py
import strawberry

@strawberry.type
class User:
    id: str
    email: str
    username: str
```

#### リゾルバ定義

`FastAPI/app/graphql/resolvers/queries/` にクエリを定義:

```python
from typing import List
import strawberry
from app.graphql.schemas.user_schema import User

@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> List[User]:
        # データベースからユーザーを取得
        return []
```

## 🔧 API 開発

### REST API エンドポイントの追加

1. `FastAPI/app/api/` に新しいルーターファイルを作成
2. `FastAPI/app/api/__init__.py` でルーターを登録

#### 例: ユーザーエンドポイント

```python
# app/api/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_users():
    return {"users": []}

@router.post("/")
async def create_user(user_data: dict):
    return {"user": user_data}
```

### Prisma スキーマの編集

`FastAPI/prisma/schema.prisma` を編集してモデルを追加:

```prisma
model Product {
  id        String   @id @default(uuid())
  name      String
  price     Float
  createdAt DateTime @default(now()) @map("created_at")

  @@map("products")
}
```

変更後:

```bash
docker-compose exec api prisma db push
docker-compose exec api prisma generate
```

## 🔧 運用方法

### 新しいプロジェクトの開始手順

1. **フォルダのコピー**

   ```bash
   cp -r next-python my-new-project
   cd my-new-project
   ```

2. **環境変数の設定**

   - `.env.example` を `.env` にコピー
   - `FastAPI/.env.example` を `FastAPI/.env` にコピー
   - `next/.env.example` を `next/.env` にコピー
   - 必要に応じて値を変更

3. **Docker 起動**

   ```bash
   docker-compose up --build
   ```

4. **データベース初期化**

   ```bash
   docker-compose exec api prisma db push
   ```

5. **開発開始**
   - フロントエンド: http://localhost:3000
   - API: http://localhost:8000/docs

### プロジェクト名の変更

- `FastAPI/.env`: `APP_NAME` を変更
- `next/package.json`: `name` フィールドを変更
- コンテナ名を変更したい場合は `docker-compose.yml` を編集

## ⚠️ 注意点

### 1. Docker 使用時

- **ホットリロード**: ボリュームマウントにより、コード変更が自動で反映されます
- **ポート競合**: 3000, 8000, 5432 番ポートが使用可能であることを確認
- **初回ビルド**: 初回は依存関係のダウンロードで時間がかかります

### 2. データベース

- **PostgreSQL**: コンテナの PostgreSQL を使用（ローカルに PostgreSQL は不要）
- **データ永続化**: `postgres_data` ボリュームにデータが保存されます
- **リセット**: `docker-compose down -v` でデータも削除されます

### 3. GraphQL

- **エンドポイント**: FastAPI が `/graphql` で GraphQL を提供
- **Next.js からアクセス**: urql を使用して CSR でアクセス
- **スキーマ確認**: http://localhost:8000/graphql で Playground にアクセス

### 4. 環境変数

- `.env`ファイルは Git にコミットしない（`.gitignore`に含まれています）
- `NEXT_PUBLIC_`プレフィックス: Next.js でクライアント側から参照可能
- FastAPI の環境変数はコンテナ内でのみ使用

### 5. 依存関係の管理

#### Python (FastAPI)

- `requirements.txt` を編集後、コンテナを再ビルド
- 不要なパッケージ(Redis, Celery 等)は削除済み

#### Node.js (Next.js)

- `package.json` を編集後、`npm install` 実行
- Prisma は使用しない（FastAPI 側で Prisma を使用）

### 6. 本番環境へのデプロイ

本番環境では以下を変更してください:

- `DEBUG=False` に設定
- `SECRET_KEY` を強力なランダム文字列に変更
- `ALLOWED_ORIGINS` を本番ドメインに設定
- PostgreSQL のパスワードを変更
- `docker-compose.yml` の `command` を本番用に変更

## 📚 参考リンク

### フロントエンド

- [Next.js ドキュメント](https://nextjs.org/docs)
- [urql ドキュメント](https://formidable.com/open-source/urql/docs/)
- [Redux Toolkit ドキュメント](https://redux-toolkit.js.org/)
- [Tailwind CSS ドキュメント](https://tailwindcss.com/docs)

### バックエンド

- [FastAPI ドキュメント](https://fastapi.tiangolo.com/)
- [Strawberry GraphQL ドキュメント](https://strawberry.rocks/)
- [Prisma (Python) ドキュメント](https://prisma-client-py.readthedocs.io/)
- [Pydantic ドキュメント](https://docs.pydantic.dev/)

## 🐛 トラブルシューティング

### Docker コンテナが起動しない

```bash
# キャッシュをクリアして再ビルド
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### FastAPI で Prisma エラー

```bash
# コンテナに入る
docker-compose exec api bash

# Prisma Clientを再生成
prisma generate

# データベーススキーマを適用
prisma db push
```

### Next.js で urql の接続エラー

- `.env`の`NEXT_PUBLIC_GRAPHQL_ENDPOINT`が正しいか確認
- FastAPI コンテナが起動しているか確認: `docker-compose ps`
- FastAPI の CORS 設定を確認: `FastAPI/.env`の`ALLOWED_ORIGINS`

### ポート競合エラー

```bash
# 使用中のポートを確認
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# 別のポートを使用する場合は .env を編集
```

### データベース接続エラー

- PostgreSQL コンテナが起動しているか確認
- `DATABASE_URL`の設定が正しいか確認
- ヘルスチェックが完了するまで待つ

---

質問や問題がある場合は、プロジェクトの issue を作成してください。
