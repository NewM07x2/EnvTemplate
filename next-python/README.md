# Next.js + GraphQL + Prisma テンプレート環境

このフォルダは、**Next.js 14.1.0** でGraphQLとPrismaをSSRで利用するフルスタックWebアプリケーション開発用のテンプレート環境です。
このフォルダをコピーして新しいプロジェクトをすぐに開始できます。

## 📋 目次

- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [セットアップ方法](#セットアップ方法)
- [開発方法](#開発方法)
- [GraphQL 使用方法](#graphql使用方法)
- [Prisma の使用方法](#prismaの使用方法)
- [データベース操作](#データベース操作)
- [運用方法](#運用方法)
- [注意点](#注意点)

## 🛠️ 技術スタック

### フロントエンド (Next.js)

- **Next.js 14.1.0** - React フレームワーク (App Router)
- **React 18** - UI ライブラリ
- **TypeScript 5** - 型安全な開発
- **Tailwind CSS** - ユーティリティファースト CSS
- **Redux Toolkit** - 状態管理
- **urql** - GraphQL クライアント (SSR対応)
- **@prisma/client** - Prismaクライアント

### インフラ

- **Docker & Docker Compose** - コンテナ化
- **PostgreSQL** - データベース（オプション）

## 📁 プロジェクト構成

```
next/
├── .env.example               # 環境変数のサンプル
├── docker/
│   └── Dockerfile            # Next.js用Dockerfile
├── public/                   # 静的アセット（画像、フォントなど）
├── src/
│   ├── app/                  # Next.js App Router
│   │   ├── api/             # API ルート
│   │   ├── graphql/         # GraphQL ページ
│   │   ├── layout.tsx       # ルートレイアウト
│   │   ├── page.tsx         # ホームページ
│   │   ├── error.tsx        # エラーページ
│   │   ├── not-found.tsx    # 404 ページ
│   │   └── providers.tsx    # アプリプロバイダー
│   ├── components/          # React コンポーネント
│   │   ├── base/           # レイアウト、ヘッダーなど
│   │   └── elements/       # ボタン、入力フィールドなど
│   ├── const/              # 定数定義
│   ├── hooks/              # カスタム React フック
│   ├── lib/                # ユーティリティとライブラリ
│   │   ├── graphql/        # GraphQL クライアント設定 (urql)
│   │   └── prisma/         # Prisma スキーマ
│   ├── store/              # Redux ストア
│   │   └── slices/         # Redux スライス
│   └── styles/             # グローバル CSS
├── package.json            # Node.js 依存関係
├── tsconfig.json           # TypeScript 設定
├── next.config.mjs         # Next.js 設定
├── tailwind.config.ts      # Tailwind CSS 設定
├── postcss.config.js       # PostCSS 設定
└── .eslintrc.json          # ESLint 設定
```

## 🚀 セットアップ方法

### 1. このフォルダをコピー

新しいプロジェクトを作成する際は、このフォルダ全体をコピーします:

```bash
# フォルダのコピー
cp -r next my-new-project
cd my-new-project
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env.local` を作成:

```bash
cp .env.example .env.local
```

`.env.local` の内容を編集します:

```env
# データベース (PostgreSQL)
DATABASE_URL="postgresql://user:password@localhost:5432/nextapp"

# GraphQL エンドポイント (バックエンドがある場合)
NEXT_PUBLIC_GRAPHQL_ENDPOINT=http://localhost:8000/graphql

# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# 環境
NODE_ENV=development
```

### 3. 依存パッケージをインストール

```bash
npm install
```

### 4. Prisma をセットアップ

```bash
# Prisma を初期化 (初回のみ)
npx prisma init

# データベーススキーマを定義後、マイグレーションを実行
npx prisma migrate dev --name init

# Prisma クライアントを生成
npx prisma generate
```

### 5. 開発サーバーを起動

```bash
npm run dev
```

[http://localhost:3000](http://localhost:3000) にアクセスしてアプリが起動しているか確認してください。

## 💻 開発方法

### ローカル環境で開発する場合

#### Next.js の起動

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev

# 本番ビルド
npm run build

# 本番サーバーの起動
npm start

# Lint チェック
npm run lint
```

### Docker を使用する場合

```bash
# イメージをビルドして起動
docker-compose -f docker/docker-compose.yml up --build

# バックグラウンドで起動
docker-compose -f docker/docker-compose.yml up -d

# ログの確認
docker-compose -f docker/docker-compose.yml logs -f

# コンテナの停止
docker-compose -f docker/docker-compose.yml down

# コンテナに入る
docker-compose -f docker/docker-compose.yml exec web sh
```

## 🔄 GraphQL 使用方法

### GraphQL クライアントの設定

**urql** を使用してGraphQLエンドポイントにアクセスします（SSR対応）。

#### 設定ファイル

- 設定: `src/lib/graphql/urqlClient.ts`
- ドキュメント: `src/lib/graphql/graphql.md`

#### 使用例

```typescript
'use client'
import { useQuery } from 'urql'

const USERS_QUERY = `
  query {
    users {
      id
      email
      name
    }
  }
`

export default function UsersPage() {
  const [result] = useQuery({ query: USERS_QUERY })

  if (result.fetching) return <div>Loading...</div>
  if (result.error) return <div>Error: {result.error.message}</div>

  return (
    <div>
      {result.data?.users.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  )
}
```

#### Server Component での使用

GraphQLクエリはServer Componentでも実行できます:

```typescript
// src/app/users/page.tsx (Server Component)
import { urqlClient } from '@/lib/graphql/urqlClient'

export default async function UsersPage() {
  const result = await urqlClient.query(USERS_QUERY, {}).toPromise()

  return (
    <div>
      {result.data?.users.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  )
}
```

## 🗄️ Prisma の使用方法

### スキーマ定義

`src/lib/prisma/schema.prisma` を編集してモデルを定義します:

```prisma
// This is your Prisma schema file
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  createdAt DateTime @default(now()) @map("created_at")

  @@map("users")
}

model Post {
  id    Int     @id @default(autoincrement())
  title String
  content String?
  userId Int
  createdAt DateTime @default(now()) @map("created_at")

  @@map("posts")
}
```

### マイグレーション

```bash
# マイグレーションを作成して実行
npx prisma migrate dev --name add_users

# スキーマをデータベースに適用（マイグレーションファイルなし）
npx prisma db push

# マイグレーション履歴を確認
npx prisma migrate status

# 特定のマイグレーションにロールバック
npx prisma migrate resolve --rolled-back <migration_name>
```

### データ操作

API ルート (`src/app/api`) でPrismaを使用してデータを操作:

```typescript
// src/app/api/users/route.ts
import { PrismaClient } from '@prisma/client'
import { NextRequest, NextResponse } from 'next/server'

const prisma = new PrismaClient()

export async function GET() {
  const users = await prisma.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const data = await request.json()
  const user = await prisma.user.create({
    data,
  })
  return NextResponse.json(user, { status: 201 })
}
```

### Prisma Studio でデータ確認

```bash
# Prisma Studio を起動
npx prisma studio

# ブラウザで http://localhost:5555 にアクセス
```

## 🗄️ データベース操作

### PostgreSQL の起動 (ローカル環境)

PostgreSQL がインストールされている場合:

```bash
# Windows
# PostgreSQL サービスを起動

# macOS / Linux
brew services start postgresql
# または
sudo service postgresql start
```

### Docker で PostgreSQL を起動

```bash
# Docker で PostgreSQL を実行
docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:16

# コンテナの停止
docker stop postgres

# コンテナの削除
docker rm postgres
```

### データベースのリセット

```bash
# マイグレーションをリセット（全データ削除）
npx prisma migrate reset

# 確認プロンプトをスキップ
npx prisma migrate reset --force
```

## 🔧 運用方法

### 新しいプロジェクトの開始手順

1. **フォルダのコピー**
   ```bash
   cp -r next my-new-project
   cd my-new-project
   ```

2. **環境変数の設定**
   ```bash
   cp .env.example .env.local
   # .env.local を編集
   ```

3. **依存パッケージをインストール**
   ```bash
   npm install
   ```

4. **Prisma をセットアップ**
   ```bash
   npx prisma init
   npx prisma migrate dev --name init
   ```

5. **開発開始**
   ```bash
   npm run dev
   # http://localhost:3000 にアクセス
   ```

### 本番環境へのデプロイ

本番環境では以下を変更してください:

- `NODE_ENV=production` に設定
- `NEXT_PUBLIC_GRAPHQL_ENDPOINT` を本番のエンドポイントに変更
- `DATABASE_URL` を本番のデータベースに変更
- `npm run build` でプロダクションビルドを作成
- `npm start` で本番サーバーを起動

#### Vercel へのデプロイ

```bash
# Vercel CLI をインストール
npm i -g vercel

# デプロイ
vercel
```

## ⚠️ 注意点

### 1. 環境変数

- `.env.local` ファイルはGitにコミットしない（`.gitignore`に含まれています）
- `NEXT_PUBLIC_` プレフィックス: ブラウザ側から参照可能になります
- サーバーサイドのみで使用する変数にはプレフィックスを付けない

### 2. Prisma の使用

- **スキーマは src/lib/prisma/schema.prisma に配置**
- マイグレーションの実行前に必ずスキーマをバックアップしてください
- ローカル開発と本番環境では異なる `DATABASE_URL` を使用してください

### 3. GraphQL

- **urql はSSR対応**：Server Component でもClient Component でも使用可能
- GraphQLエンドポイントが外部にある場合は、CORS設定を確認してください

### 4. Docker 使用時

- ホットリロード: ボリュームマウントにより、コード変更が自動で反映されます
- ポート競合: 3000 番ポートが使用可能であることを確認
- 初回ビルド: 初回は依存関係のダウンロードで時間がかかります

### 5. 依存関係の管理

```bash
# 依存関係を更新
npm update

# 新しいパッケージをインストール
npm install <package-name>

# 開発依存関係として追加
npm install --save-dev <package-name>
```

### 6. パフォーマンス最適化

- **Image の最適化**: `next/image` コンポーネントを使用
- **Code Splitting**: Next.js が自動で行います
- **Static Generation**: `generateStaticParams()` で静的ページを生成

## 📚 参考リンク

### フロントエンド

- [Next.js ドキュメント](https://nextjs.org/docs)
- [React ドキュメント](https://react.dev/)
- [urql ドキュメント](https://formidable.com/open-source/urql/docs/)
- [Redux Toolkit ドキュメント](https://redux-toolkit.js.org/)
- [Tailwind CSS ドキュメント](https://tailwindcss.com/docs)
- [TypeScript ドキュメント](https://www.typescriptlang.org/docs/)

### データベース

- [Prisma ドキュメント](https://www.prisma.io/docs/)
- [PostgreSQL ドキュメント](https://www.postgresql.org/docs/)

### ツール

- [Docker ドキュメント](https://docs.docker.com/)
- [ESLint ドキュメント](https://eslint.org/)

## 🐛 トラブルシューティング

### Prisma クライアント生成エラー

```bash
# Prisma クライアントを再生成
npx prisma generate

# キャッシュをクリア
rm -rf node_modules/.prisma
npx prisma generate
```

### GraphQL の接続エラー

- `.env.local` の `NEXT_PUBLIC_GRAPHQL_ENDPOINT` が正しいか確認
- GraphQL サーバーが起動しているか確認
- CORS 設定を確認

### ポート 3000 が使用中

```bash
# 別のポート で起動
npm run dev -- -p 3001

# Windows: 使用中のプロセスを確認
netstat -ano | findstr :3000
```

### データベース接続エラー

```bash
# DATABASE_URL の形式を確認
# postgresql://user:password@localhost:5432/dbname

# PostgreSQL が起動しているか確認
# psql -U postgres -h localhost
```

### node_modules に関するエラー

```bash
# node_modules を削除して再インストール
rm -rf node_modules package-lock.json
npm install
```

---

質問や問題がある場合は、GitHubのissueを作成してください。
