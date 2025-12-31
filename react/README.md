# React + GraphQL + Prisma テンプレート

React + TypeScript + Docker + GraphQL (urql) + Prisma のサンプル環境テンプレートです。このフォルダをコピーして、すぐに新しいプロジェクトを始められます。

## 🎯 概要

このテンプレートは、練習用・学習用の React アプリケーション環境を提供します。

### 特徴

- 🐳 **Docker 完全対応** - すぐに開発を開始できる
- 📡 **urql (CSR)** - GraphQL クライアントサイドデータ取得
- 🗄️ **Prisma** - API 経由でのデータベースアクセス
- 🔄 **Redux Toolkit** - 状態管理
- 🎨 **Vite** - 高速ビルドツール
- 📱 **React Router** - ルーティング
- 🧪 **Vitest + React Testing Library** - テスト環境

## 📦 技術スタック

### フロントエンド

- **React 18.3** - UI ライブラリ
- **TypeScript 5.7** - 型安全性
- **Vite 6.0** - ビルドツール・開発サーバー
- **urql 4.0** - CSR 用 GraphQL クライアント
- **Prisma 6.4** - ORM・データベースクライアント（API 経由で使用）
- **Redux Toolkit 2.2** - 状態管理
- **React Router 7.1** - ルーティング
- **Axios 1.7** - HTTP クライアント

### テスト

- **Vitest 2.1** - テストフレームワーク
- **React Testing Library 16.1** - コンポーネントテスト
- **@testing-library/jest-dom** - カスタムマッチャー
- **jsdom** - ブラウザ環境シミュレーション

### データベース

- **PostgreSQL 16** - リレーショナルデータベース

### インフラ

- **Docker & Docker Compose** - コンテナ化

## 📁 プロジェクト構造

```
react/
├── docker/
│   └── Dockerfile              # フロントエンド用Dockerファイル
├── src/
│   ├── lib/
│   │   ├── graphql/           # CSR用GraphQL設定
│   │   │   ├── urqlClient.ts  # urqlクライアント
│   │   │   └── graphql.md     # 使用ガイド
│   │   └── prisma/            # Prisma設定（API経由使用）
│   │       ├── client.ts      # Prismaクライアント
│   │       └── schema.prisma  # DBスキーマ定義
│   ├── store/                 # Redux状態管理
│   ├── pages/                 # ページコンポーネント
│   ├── test/                  # テスト設定
│   │   ├── setup.ts           # テストセットアップ
│   │   └── testing-guide.md   # テストガイド
│   ├── styles/                # スタイル
│   ├── App.tsx                # メインアプリ
│   ├── App.test.tsx           # アプリテスト
│   └── main.tsx               # エントリーポイント
├── index.html                 # HTMLテンプレート
├── vite.config.ts            # Vite設定（Vitest含む）
├── docker-compose.yml        # Docker Compose設定
└── package.json              # 依存関係
```

## 🚀 クイックスタート

### 前提条件

- Docker Desktop がインストールされていること
- Git がインストールされていること

### 1. プロジェクトのセットアップ

```bash
# このフォルダをコピー
cp -r react my-new-react-app
cd my-new-react-app

# 環境変数ファイルを作成
cp .env.example .env

# Docker Composeで起動
docker-compose up
```

### 2. アクセス

- **フロントエンド**: http://localhost:3000
- **PostgreSQL**: localhost:5432

### 3. 初期セットアップ（初回のみ）

```bash
# Prismaマイグレーション（別ターミナルで）
docker-compose exec frontend npx prisma db push
```

## 💻 開発方法

### Docker を使用する場合（推奨）

```bash
# 全サービスの起動
docker-compose up

# バックグラウンドで起動
docker-compose up -d

# ログの確認
docker-compose logs -f frontend

# コンテナの停止
docker-compose down

# ボリュームも削除して完全にクリーンアップ
docker-compose down -v

# コンテナに入る
docker-compose exec frontend sh

# Prisma Studio起動
docker-compose exec frontend npx prisma studio
```

### ローカル環境で開発する場合

```bash
# 依存関係のインストール
npm install

# Prismaクライアント生成
npx prisma generate

# 開発サーバーの起動
npm run dev

# ビルド
npm run build

# プレビュー
npm run preview
```

## 🔄 データ取得方法

このテンプレートでは、2 つのデータ取得方法を提供しています。

### CSR (Client-Side Rendering) - urql 使用

**urql** を使用して GraphQL エンドポイントにアクセスします。

#### 設定

- エンドポイント: `http://localhost:8080/graphql`
- 設定ファイル: `src/lib/graphql/urqlClient.ts`

#### 使用例

```typescript
import { useQuery } from 'urql'

const USERS_QUERY = `
  query {
    users {
      id
      username
      email
    }
  }
`

function UsersComponent() {
  const [result] = useQuery({ query: USERS_QUERY })

  if (result.fetching) return <div>Loading...</div>
  if (result.error) return <div>Error: {result.error.message}</div>

  return (
    <ul>
      {result.data.users.map((user) => (
        <li key={user.id}>{user.username}</li>
      ))}
    </ul>
  )
}
```

### Prisma - API 経由でのデータベースアクセス

**注意**: React は純粋な CSR フレームワークのため、完全な SSR はサポートしていません。
Prisma を使用する場合は、別途バックエンド API（Express 等）を実装し、そこから Prisma を使用します。

#### アーキテクチャ

```
React (Frontend) → Axios → Express API (Backend) → Prisma → PostgreSQL
```

#### フロントエンド例

```typescript
import { useEffect, useState } from 'react'
import axios from 'axios'

function UsersComponent() {
  const [users, setUsers] = useState([])

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await axios.get('/api/users')
      setUsers(response.data)
    }
    fetchUsers()
  }, [])

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.username}</li>
      ))}
    </ul>
  )
}
```

#### バックエンド例（別途実装が必要）

```typescript
// server.ts (Express + Prisma)
import express from 'express'
import { PrismaClient } from '@prisma/client'

const app = express()
const prisma = new PrismaClient()

app.get('/api/users', async (req, res) => {
  const users = await prisma.user.findMany()
  res.json(users)
})

app.listen(3001)
```

### 使い分けの基準

- **CSR (urql)**: GraphQL API が存在する場合、リアルタイム更新、ユーザーインタラクション後のデータ取得
- **Prisma (API 経由)**: データベース直接アクセス、複雑なクエリ、トランザクション処理

詳細は `src/lib/graphql/graphql.md` を参照してください。

## 🗄️ データベース操作

### Prisma マイグレーション

```bash
# コンテナに入る
docker-compose exec frontend sh

# スキーマをデータベースに適用
npx prisma db push

# マイグレーションファイルを作成
npx prisma migrate dev --name migration_name

# Prisma Studioでデータを確認
npx prisma studio
```

### PostgreSQL 直接アクセス

```bash
# PostgreSQLコンテナに接続
docker-compose exec postgres psql -U postgres -d react_db

# テーブル一覧
\dt

# データ確認
SELECT * FROM users;
```

## 🔧 運用方法

### 新しいプロジェクトの開始手順

1. **フォルダのコピー**

   ```bash
   cp -r react my-new-react-app
   cd my-new-react-app
   ```

2. **環境変数の設定**

   - `.env.example` を `.env` にコピー
   - 必要に応じて値を変更

3. **package.json の更新**

   ```json
   {
     "name": "my-new-react-app",
     "version": "0.1.0"
   }
   ```

4. **Prisma スキーマの初期化（必要に応じて）**

   - `src/lib/prisma/schema.prisma` を編集してモデルを定義
   - `docker-compose up` 後に `docker-compose exec frontend npx prisma db push` を実行

5. **Docker 起動**

   ```bash
   docker-compose up --build
   ```

6. **依存関係の追加**

   ```bash
   # コンテナ内で実行
   docker-compose exec frontend npm install <package-name>
   ```

### 環境変数

`.env`ファイルで以下の設定が可能です:

```bash
# PostgreSQL設定
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=react_db
POSTGRES_PORT=5432

# フロントエンド設定
FRONTEND_PORT=3000

# GraphQLエンドポイント (CSR用)
VITE_GRAPHQL_ENDPOINT=http://localhost:8080/graphql

# データベース接続URL（バックエンドAPI用）
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/react_db?schema=public
```

**注意**:

- `.env`ファイルは Git にコミットしない（`.gitignore`に含まれています）
- `VITE_`プレフィックス: Vite でクライアント側から参照可能

## 📚 ライブラリの追加

### 依存関係の追加

```bash
# コンテナ内で実行
docker-compose exec frontend sh
npm install <package-name>

# 開発依存関係
npm install -D <package-name>
```

### よく使うライブラリの例

```bash
# UI関連
npm install @mui/material @emotion/react @emotion/styled
npm install tailwindcss postcss autoprefixer

# フォーム管理
npm install react-hook-form zod

# 日付・時刻
npm install date-fns

# アイコン
npm install react-icons
```

## 🧪 テスト

このテンプレートには、**Vitest + React Testing Library**を使用したテスト環境が含まれています。

### テストツール

- **Vitest 2.1** - 高速テストフレームワーク
- **React Testing Library 16.1** - React コンポーネントテスト
- **@testing-library/jest-dom** - カスタムマッチャー
- **jsdom** - ブラウザ環境シミュレーション
- **Vitest UI** - テスト結果の UI 表示
- **Coverage** - カバレッジレポート生成

### テストコマンド

```bash
# すべてのテストを実行
npm run test

# ウォッチモードで実行
npm run test -- --watch

# UIモードで実行（ブラウザでテスト結果表示）
npm run test:ui

# カバレッジレポートを生成
npm run test:coverage
```

### Docker コンテナ内でテスト実行

```bash
# コンテナに入る
docker-compose exec frontend sh

# テスト実行
npm run test

# カバレッジ生成
npm run test:coverage
```

### テストファイルの例

プロジェクトには以下のサンプルテストが含まれています:

- `src/App.test.tsx` - アプリケーションのテスト
- `src/pages/HomePage.test.tsx` - ホームページのテスト
- `src/pages/GraphQLPage.test.tsx` - GraphQL ページのテスト
- `src/pages/PrismaPage.test.tsx` - Prisma ページのテスト
- `src/store/slices/counterSlice.test.ts` - Redux slice のテスト
- `src/lib/graphql/urqlClient.test.ts` - urql クライアントのテスト

### テストの書き方

詳細なテストガイドは `src/test/testing-guide.md` を参照してください。

基本的なテスト例:

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MyComponent from './MyComponent'

describe('MyComponent', () => {
  it('正しくレンダリングされる', () => {
    render(<MyComponent />)
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })
})
```

## 📝 よくある質問

### Q: SSR (Server-Side Rendering) は使えますか？

A: React は純粋な CSR フレームワークのため、完全な SSR はサポートしていません。SSR が必要な場合は、**Next.js**の使用を推奨します。このテンプレートでは、バックエンド API 経由でのデータ取得を想定しています。

### Q: GraphQL API サーバーはどこにありますか？

A: このテンプレートには GraphQL API サーバーは含まれていません。`VITE_GRAPHQL_ENDPOINT`で指定されたエンドポイントに接続します。別途、Go や Node.js 等で GraphQL API サーバーを構築する必要があります。

参考: `next-go`フォルダの Go Echo GraphQL 実装

### Q: Prisma を使いたい場合はどうすればいいですか?

A: Express 等のバックエンド API サーバーを実装し、そこから Prisma を使用してください。フロントエンド（React）からは Axios 等で API エンドポイントを呼び出します。

## 🐛 トラブルシューティング

### Docker コンテナが起動しない

```bash
# キャッシュをクリアして再ビルド
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### urql の接続エラー (CSR)

- `.env`の`VITE_GRAPHQL_ENDPOINT`が正しいか確認
- GraphQL API サーバーが起動しているか確認
- CORS 設定を確認

### Prisma の接続エラー

```bash
# Prismaクライアントを再生成
docker-compose exec frontend npx prisma generate

# スキーマをDBに適用
docker-compose exec frontend npx prisma db push

# データベース接続を確認
docker-compose exec frontend npx prisma studio
```

### Prisma マイグレーションエラー

```bash
# マイグレーション状態の確認
docker-compose exec frontend npx prisma migrate status

# マイグレーションのリセット（開発環境のみ）
docker-compose exec frontend npx prisma migrate reset

# スキーマを直接適用（開発時）
docker-compose exec frontend npx prisma db push
```

### ポート競合エラー

```bash
# 使用中のポートを確認
# Windows
netstat -ano | findstr :3000

# 別のポートを使用する場合は .env を編集
FRONTEND_PORT=3001
```

### ホットリロードが動作しない

Docker コンテナ内でホットリロードが動作しない場合、`vite.config.ts`の`watch.usePolling`が`true`になっているか確認してください。

## 📚 参考リンク

### フロントエンド

- [React 公式ドキュメント](https://react.dev/)
- [Vite 公式ドキュメント](https://vite.dev/)
- [TypeScript 公式ドキュメント](https://www.typescriptlang.org/)
- [urql ドキュメント](https://formidable.com/open-source/urql/docs/)
- [Redux Toolkit ドキュメント](https://redux-toolkit.js.org/)
- [React Router ドキュメント](https://reactrouter.com/)

### データベース・ORM

- [Prisma 公式ドキュメント](https://www.prisma.io/docs)
- [PostgreSQL 公式ドキュメント](https://www.postgresql.org/docs/)

### Docker

- [Docker 公式ドキュメント](https://docs.docker.com/)
- [Docker Compose 公式ドキュメント](https://docs.docker.com/compose/)

## 🔗 関連テンプレート

- **next/** - Next.js + urql (CSR) + Prisma (SSR) の完全な SSR 対応テンプレート
- **next-go/** - Next.js + Go Echo + GraphQL + Prisma
- **next-python/** - Next.js + FastAPI + GraphQL

---

質問や問題がある場合は、プロジェクトの issue を作成してください.
