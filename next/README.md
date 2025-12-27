# Next.js テンプレート環境

このフォルダは、Next.js + Docker + GraphQL + Prisma を使用したアプリケーションのテンプレート環境です。
このフォルダをコピーして新しいプロジェクトを開始できます。

## 📋 目次

- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [セットアップ方法](#セットアップ方法)
- [開発方法](#開発方法)
- [GraphQL の使い分け](#graphqlの使い分け)
- [運用方法](#運用方法)
- [注意点](#注意点)

## 🛠️ 技術スタック

### フロントエンド

- **Next.js 14.1.0** - React フレームワーク (App Router)
- **React 18** - UI ライブラリ
- **TypeScript 5** - 型安全な開発
- **Tailwind CSS** - ユーティリティファースト CSS
- **Redux Toolkit** - 状態管理

### GraphQL・データ取得

- **urql 4.0.6** - CSR 用 GraphQL クライアント
- **@urql/next 1.1.1** - Next.js 用 urql 統合
- **Prisma 6.4.1** - SSR 用 ORM・データベースクライアント

### インフラ

- **Docker** - コンテナ化
- **PostgreSQL 16** - データベース

## 📁 プロジェクト構成

```
next/
├── docker/                 # Docker設定
│   └── Dockerfile         # Next.jsアプリ用Dockerfile
├── docker-compose.yml     # Docker Compose設定
├── src/
│   ├── app/               # Next.js App Router
│   │   ├── layout.tsx    # ルートレイアウト
│   │   ├── page.tsx      # トップページ
│   │   ├── providers.tsx # Reduxとurqlのプロバイダー
│   │   └── graphql/      # GraphQLサンプルページ
│   │       ├── page.tsx  # CSR例 (urql)
│   │       └── ssr-example/
│   │           └── page.tsx  # SSR例 (Prisma)
│   ├── components/        # UIコンポーネント
│   │   ├── base/         # サイト全体のコンポーネント
│   │   ├── elements/     # 最小単位のコンポーネント
│   │   └── model/        # モデル定義
│   ├── lib/              # ライブラリとユーティリティ
│   │   ├── api.ts        # API関連の関数
│   │   ├── graphql/      # GraphQL設定
│   │   │   ├── urqlClient.ts  # urqlクライアント設定
│   │   │   └── graphql.md     # GraphQL使用ガイド
│   │   └── prisma/       # Prisma設定
│   │       ├── client.ts # Prismaクライアント
│   │       └── schema.prisma  # DBスキーマ定義
│   ├── store/            # Redux store
│   │   ├── store.ts      # Store設定
│   │   └── slices/       # Redux slices
│   ├── const/            # 定数定義
│   └── styles/           # グローバルスタイル
├── .env.example          # 環境変数のサンプル
├── package.json          # 依存関係
└── README.md             # このファイル
```

## 🚀 セットアップ方法

### 1. このフォルダをコピー

新しいプロジェクトを作成する際は、このフォルダ全体をコピーします:

```bash
# Windowsの場合
cp -r next my-new-project
cd my-new-project

# プロジェクト名を変更
# package.jsonの"name"フィールドを編集
```

### 2. 環境変数の設定

`.env.example`をコピーして`.env`を作成:

```bash
cp .env.example .env
```

`.env`ファイルを編集して、必要な値を設定:

```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/nextapp?schema=public"
NEXT_PUBLIC_GRAPHQL_ENDPOINT="http://localhost:4000/graphql"
NODE_ENV="development"
```

### 3. 依存関係のインストール

```bash
npm install
```

## 💻 開発方法

### Docker を使用する場合（推奨）

```bash
# コンテナの起動（初回はビルドも実行）
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d

# ログの確認
docker-compose logs -f app

# コンテナの停止
docker-compose down

# ボリュームも削除して完全にクリーンアップ
docker-compose down -v
```

ブラウザで http://localhost:3000 にアクセス

### ローカル環境で開発する場合

PostgreSQL が別途必要です:

```bash
# 開発サーバーの起動
npm run dev

# 本番ビルド
npm run build

# 本番サーバーの起動
npm start
```

### Prisma マイグレーション

データベーススキーマを変更した場合:

```bash
# マイグレーションファイルの作成と適用
npx prisma migrate dev --name migration_name

# Prisma Clientの再生成
npx prisma generate

# Prisma Studioでデータを確認
npx prisma studio
```

## 🔄 GraphQL の使い分け

このテンプレートでは、レンダリング方法によって GraphQL ライブラリを使い分けます。

### CSR (Client-Side Rendering) - urql を使用

クライアントサイドでデータを取得する場合は**urql**を使用します。

**設定ファイル**: `src/lib/graphql/urqlClient.ts`

**使用例**:

```typescript
'use client'
import { useQuery } from 'urql'

const USERS_QUERY = `
  query {
    users {
      id
      name
      email
    }
  }
`

export default function UsersPage() {
  const [result] = useQuery({ query: USERS_QUERY })

  if (result.fetching) return <div>Loading...</div>
  if (result.error) return <div>Error!</div>

  return <div>{/* データを表示 */}</div>
}
```

### SSR (Server-Side Rendering) - Prisma を使用

サーバーコンポーネントでデータを取得する場合は**Prisma**を使用します。

**設定ファイル**:

- `src/lib/prisma/client.ts` - クライアント設定
- `src/lib/prisma/schema.prisma` - スキーマ定義

**使用例**:

```typescript
// 'use client'ディレクティブなし（Server Component）
import { prisma } from '@/lib/prisma/client'

export default async function UsersPage() {
  const users = await prisma.user.findMany()

  return (
    <div>
      {users.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  )
}
```

## 🔧 運用方法

### 新しいプロジェクトの開始手順

1. **フォルダのコピー**

   ```bash
   cp -r next my-new-project
   cd my-new-project
   ```

2. **プロジェクト名の変更**
   - `package.json`の`name`フィールドを編集
3. **環境変数の設定**

   - `.env.example`を`.env`にコピー
   - プロジェクトに応じた値を設定

4. **Prisma スキーマの定義**

   - `src/lib/prisma/schema.prisma`を編集
   - マイグレーションを実行: `npx prisma migrate dev`

5. **開発開始**
   - `docker-compose up`または`npm run dev`

### GraphQL エンドポイントの設定

外部 GraphQL サーバーを使用する場合:

1. `.env`で`NEXT_PUBLIC_GRAPHQL_ENDPOINT`を設定
2. 必要に応じて`src/lib/graphql/urqlClient.ts`で認証設定を追加

### データベーススキーマの変更

1. `src/lib/prisma/schema.prisma`を編集
2. マイグレーションの作成: `npx prisma migrate dev --name description`
3. Prisma Client が自動的に再生成されます

## ⚠️ 注意点

### 1. GraphQL の使い分けを厳守

- **CSR (クライアントコンポーネント)**: urql を使用
- **SSR (サーバーコンポーネント)**: Prisma を使用
- クライアントコンポーネントで PrismaClient を直接インスタンス化しない

### 2. 環境変数

- `.env`ファイルは Git にコミットしない（`.gitignore`に含まれています）
- 本番環境では適切な値に変更すること
- `NEXT_PUBLIC_`プレフィックスは、クライアント側で使用可能な環境変数に必要

### 3. Docker 使用時の注意

- ホットリロードを有効にするためにボリュームマウントを使用
- `node_modules`は別ボリュームとしてマウント（パフォーマンス向上）
- データベースのデータは`postgres_data`ボリュームに永続化

### 4. Prisma マイグレーション

- 開発環境: `prisma migrate dev`
- 本番環境: `prisma migrate deploy`
- マイグレーションファイルは必ず Git にコミットする

### 5. TypeScript 設定

- `@/`エイリアスで`src/`フォルダを参照可能
- `tsconfig.json`の paths マッピングを変更しないこと

### 6. パッケージの更新

このテンプレートは以下のパッケージに依存しています:

- `urql`, `@urql/next`: CSR 用 GraphQL クライアント
- `@prisma/client`, `prisma`: SSR 用 ORM
- `@reduxjs/toolkit`, `react-redux`: 状態管理

アップデート時は互換性を確認してください。

## 📚 参考リンク

- [Next.js ドキュメント](https://nextjs.org/docs)
- [urql ドキュメント](https://formidable.com/open-source/urql/docs/)
- [Prisma ドキュメント](https://www.prisma.io/docs)
- [Redux Toolkit ドキュメント](https://redux-toolkit.js.org/)
- [Tailwind CSS ドキュメント](https://tailwindcss.com/docs)

## 🐛 トラブルシューティング

### Docker コンテナが起動しない

```bash
# キャッシュをクリアして再ビルド
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Prisma エラー

```bash
# Prisma Clientを再生成
npx prisma generate

# マイグレーションをリセット
npx prisma migrate reset
```

### urql の接続エラー

- `.env`の`NEXT_PUBLIC_GRAPHQL_ENDPOINT`が正しいか確認
- GraphQL サーバーが起動しているか確認
- CORS の設定を確認

---

質問や問題がある場合は、プロジェクトの issue を作成してください。
