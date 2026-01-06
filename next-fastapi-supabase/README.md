# Next.js + FastAPI + Supabase Template

Next.js + FastAPI + Supabase (PostgreSQL) + Dockerによるフルスタックアプリケーション開発テンプレートです。

## ✨ 主な機能

- **Next.js 15** - App Router、Server Components、React 19
- **FastAPI** - 高速なPython Webフレームワーク
- **Supabase PostgreSQL** - スケーラブルなデータベース
- **JWT認証** - セキュアなトークンベース認証
- **Docker Compose** - 完全なコンテナ化環境
- **TypeScript** - 型安全な開発環境

## 🚀 クイックスタート

### 前提条件

- Docker & Docker Compose
- Node.js 22+（ローカル開発の場合）
- Python 3.12+（ローカル開発の場合）

### Dockerで起動

```bash
# 環境変数の設定
cp .env.example .env

# Docker Composeで起動
docker-compose up

# バックグラウンドで起動
docker-compose up -d

# ログ確認
docker-compose logs -f

# 停止
docker-compose down
```

### アクセスURL

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Supabase Studio**: http://localhost:3010

### ローカル環境で起動

#### Backend (FastAPI)

```bash
cd backend

# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt

# 環境変数設定
cp ../.env.example .env

# PostgreSQLが起動していることを確認してから
# 開発サーバー起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Next.js)

```bash
cd frontend

# 依存関係インストール
npm install

# 環境変数設定
cp ../.env.example .env.local

# 開発サーバー起動
npm run dev
```

## 📁 プロジェクト構造

```
next-fastapi-supabase/
├── backend/                  # FastAPI バックエンド
│   ├── app/
│   │   ├── main.py          # FastAPIアプリケーション
│   │   ├── core/
│   │   │   ├── config.py    # 設定
│   │   │   ├── database.py  # データベース接続
│   │   │   ├── supabase.py  # Supabaseクライアント
│   │   │   └── security.py  # JWT認証
│   │   ├── models/
│   │   │   └── models.py    # SQLAlchemyモデル
│   │   ├── schemas/
│   │   │   └── schemas.py   # Pydanticスキーマ
│   │   └── api/
│   │       └── routes/      # APIエンドポイント
│   │           ├── auth.py  # 認証API
│   │           ├── users.py # ユーザーAPI
│   │           └── posts.py # 投稿API
│   ├── migrations/          # データベースマイグレーション
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Next.js フロントエンド
│   ├── src/
│   │   ├── app/            # App Router
│   │   │   ├── layout.tsx  # ルートレイアウト
│   │   │   ├── page.tsx    # ホームページ
│   │   │   ├── users/      # ユーザーページ
│   │   │   ├── posts/      # 投稿ページ
│   │   │   └── about/      # Aboutページ
│   │   ├── lib/
│   │   │   ├── api.ts      # API通信（Axios）
│   │   │   └── supabase.ts # Supabaseクライアント
│   │   └── test/
│   │       ├── setup.ts
│   │       └── example.test.ts
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   └── vitest.config.ts
├── docker-compose.yml       # Docker構成
└── .env.example            # 環境変数テンプレート
```

## 🔐 認証システム

### ユーザー登録

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

### ログイン

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

レスポンス:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "email": "user@example.com",
    "username": "testuser"
  }
}
```

### 認証付きリクエスト

```bash
curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer <access_token>"
```

## 📡 API エンドポイント

### 認証 (`/api/auth`)

- `POST /api/auth/register` - ユーザー登録
- `POST /api/auth/login` - ログイン
- `POST /api/auth/logout` - ログアウト

### ユーザー (`/api/users`)

- `GET /api/users` - ユーザー一覧
- `GET /api/users/{user_id}` - 特定のユーザー
- `DELETE /api/users/{user_id}` - ユーザー削除

### 投稿 (`/api/posts`)

- `GET /api/posts` - 投稿一覧（`?published=true`でフィルター可能）
- `GET /api/posts/{post_id}` - 特定の投稿
- `POST /api/posts` - 新規投稿作成
- `PUT /api/posts/{post_id}` - 投稿更新
- `DELETE /api/posts/{post_id}` - 投稿削除

### API ドキュメント

FastAPIが自動生成するドキュメント:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ データベース

### マイグレーション

初回起動時、`backend/migrations/001_init.sql`が自動実行されます。

手動でマイグレーションを実行する場合:

```bash
# PostgreSQLコンテナに接続
docker-compose exec postgres psql -U postgres -d postgres

# SQLファイルを実行
\i /docker-entrypoint-initdb.d/001_init.sql
```

### Supabase Studio

データベースUIでデータを視覚的に管理:
http://localhost:3010

### データベース接続

```bash
# PostgreSQLに直接接続
docker-compose exec postgres psql -U postgres -d postgres

# テーブル一覧
\dt

# ユーザー確認
SELECT * FROM users;
```

## 🧪 テスト

### Backend (FastAPI)

```bash
cd backend

# テストライブラリをインストール
pip install pytest pytest-asyncio httpx

# テスト実行
pytest
```

### Frontend (Next.js)

```bash
cd frontend

# テスト実行
npm test

# UIモードでテスト
npm run test:ui

# カバレッジ計測
npm run test:coverage

# 監視モード
npm test -- --watch
```

## 🎨 フロントエンド

### Supabaseクライアント

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

### API通信

```typescript
// src/lib/api.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// 自動トークン付与
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Tailwind CSS

Supabaseカラーをカスタマイズ:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'supabase-green': '#3ECF8E',
        'supabase-dark': '#1E1E1E',
      },
    },
  },
};
```

## 🐳 Docker環境

### サービス構成

- **postgres** - Supabase PostgreSQL 15
- **studio** - Supabase Studio（データベースUI）
- **backend** - FastAPI (Python 3.12)
- **frontend** - Next.js (Node.js 22)

### コマンド

```bash
# すべてのサービスを起動
docker-compose up

# 特定のサービスのみ起動
docker-compose up postgres backend

# ログ確認
docker-compose logs -f backend

# コンテナ内でコマンド実行
docker-compose exec backend python -m pytest

# ボリュームも削除して停止
docker-compose down -v

# 再ビルド
docker-compose up --build
```

## 🔧 環境変数

### Backend (`.env`)

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/postgres
SUPABASE_URL=http://postgres:5432
SUPABASE_KEY=<service_role_key>
SUPABASE_JWT_SECRET=<jwt_secret>
```

### Frontend (`.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=http://localhost:5432
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key>
```

## 📦 デプロイ

### Frontend (Vercel)

```bash
# Vercel CLIをインストール
npm i -g vercel

# デプロイ
cd frontend
vercel
```

環境変数を設定:
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Backend (Fly.io / Render)

#### Fly.io

```bash
# Fly CLIをインストール
curl -L https://fly.io/install.sh | sh

# アプリ作成
cd backend
fly launch

# デプロイ
fly deploy
```

#### Render

1. `backend/`をデプロイ
2. ビルドコマンド: `pip install -r requirements.txt`
3. 起動コマンド: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Supabase (本番環境)

1. [Supabase](https://supabase.com)でプロジェクト作成
2. 接続情報を取得
3. 環境変数を更新:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `DATABASE_URL`

## 📚 参考リンク

- [Next.js公式ドキュメント](https://nextjs.org/)
- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [Supabase公式ドキュメント](https://supabase.com/docs)
- [Docker公式ドキュメント](https://docs.docker.com/)
- [Tailwind CSS公式ドキュメント](https://tailwindcss.com/)

## 🤝 コントリビューション

このテンプレートはMITライセンスのもとで公開されています。自由にカスタマイズしてご利用ください。

## 📝 ライセンス

MIT License
