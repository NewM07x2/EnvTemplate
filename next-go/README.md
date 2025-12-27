# Next.js + Go Echo テンプレート環境

このフォルダは、**Next.js (フロントエンド)** + **Go Echo (バックエンド API)** + **PostgreSQL** + **Docker** を使用したフルスタックアプリケーションのテンプレート環境です。
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

### バックエンド (Go)

- **Go 1.24** - 高速・並行処理に強いプログラミング言語
- **Echo v4** - 高性能な Go ウェブフレームワーク
- **gqlgen** - Go 用 GraphQL サーバーライブラリ
- **GORM** (オプション) - Go の ORM

### インフラ

- **Docker & Docker Compose** - コンテナ化
- **PostgreSQL 16** - データベース

## 📁 プロジェクト構成

```
next-go/
├── docker-compose.yml          # 統合Docker Compose設定
├── .env.example               # 環境変数のサンプル
├── echo-app/                  # Go Echo バックエンドAPI
│   ├── cmd/
│   │   └── api/              # メインエントリーポイント
│   ├── internal/             # 内部パッケージ
│   ├── graph/                # GraphQLスキーマ・リゾルバ
│   ├── docker/
│   │   └── Dockerfile        # Go用Dockerfile
│   ├── go.mod                # Go依存関係
│   ├── gqlgen.yml           # GraphQL設定
│   └── .env.example         # Go環境変数サンプル
└── next/                     # Next.js フロントエンド
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
cp -r next-go my-new-project
cd my-new-project
```

### 2. 環境変数の設定

#### ルートの環境変数

`.env.example`をコピーして`.env`を作成:

```bash
cp .env.example .env
```

#### Go Echo API の環境変数

```bash
cd echo-app
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
- **Go Echo API**: http://localhost:8080
- **GraphQL Playground**: http://localhost:8080/graphql
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
docker-compose exec api sh
docker-compose exec frontend sh
```

### ローカル環境で開発する場合

#### Go Echo (バックエンド)

```bash
cd echo-app

# 依存関係のインストール
go mod download

# 開発サーバーの起動
go run cmd/api/main.go

# ビルド
go build -o bin/api cmd/api/main.go
```

#### Next.js (フロントエンド)

```bash
cd next

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev

# 本番ビルド
npm run build
```

### データベース操作

#### PostgreSQL に接続

```bash
# コンテナ内のpsqlを使用
docker-compose exec postgres psql -U postgres -d nextgo_db

# または外部から接続
psql -h localhost -U postgres -d nextgo_db
```

## 🔄 GraphQL 使用方法

### フロントエンド (Next.js) から GraphQL を使用

**urql** を使用して Go Echo の GraphQL エンドポイントにアクセスします。

#### 設定

- エンドポイント: `http://localhost:8080/graphql`
- 設定ファイル: `next/src/lib/graphql/urqlClient.ts`

#### 使用例

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
  if (result.error) return <div>Error: {result.error.message}</div>

  return (
    <div>
      {result.data.users.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  )
}
```

### バックエンド (Go) での GraphQL 定義

#### スキーマ定義

`echo-app/graph/schema.graphqls` にスキーマを定義:

```graphql
type User {
  id: ID!
  name: String!
  email: String!
}

type Query {
  users: [User!]!
  user(id: ID!): User
}

type Mutation {
  createUser(input: NewUser!): User!
}

input NewUser {
  name: String!
  email: String!
}
```

#### リゾルバの生成

```bash
cd echo-app
go run github.com/99designs/gqlgen generate
```

#### リゾルバの実装

`echo-app/graph/resolver.go` にビジネスロジックを実装:

```go
func (r *queryResolver) Users(ctx context.Context) ([]*model.User, error) {
    // データベースからユーザーを取得
    return r.userService.GetAllUsers(ctx)
}
```

## 🔧 API 開発

### REST API エンドポイントの追加

Echo フレームワークを使用して REST エンドポイントを追加:

```go
// cmd/api/main.go
e := echo.New()

// ルートの定義
e.GET("/api/users", handlers.GetUsers)
e.POST("/api/users", handlers.CreateUser)
e.GET("/api/users/:id", handlers.GetUser)
```

### データベースマイグレーション

#### マイグレーションツールの使用 (golang-migrate)

```bash
# インストール
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# マイグレーションファイルの作成
migrate create -ext sql -dir migrations -seq create_users_table

# マイグレーションの実行
migrate -path migrations -database "postgresql://postgres:postgres@localhost:5432/nextgo_db?sslmode=disable" up
```

## 🔧 運用方法

### 新しいプロジェクトの開始手順

1. **フォルダのコピー**

   ```bash
   cp -r next-go my-new-project
   cd my-new-project
   ```

2. **環境変数の設定**

   - `.env.example` を `.env` にコピー
   - `echo-app/.env.example` を `echo-app/.env` にコピー
   - `next/.env.example` を `next/.env` にコピー
   - 必要に応じて値を変更

3. **Go モジュール名の変更**

   - `echo-app/go.mod` の `module` 名を変更

   ```go
   module your-project-name
   ```

4. **Docker 起動**

   ```bash
   docker-compose up --build
   ```

5. **開発開始**
   - フロントエンド: http://localhost:3000
   - API: http://localhost:8080

### プロジェクト名の変更

- `echo-app/go.mod`: モジュール名を変更
- `next/package.json`: `name` フィールドを変更
- コンテナ名を変更したい場合は `docker-compose.yml` を編集

## ⚠️ 注意点

### 1. Docker 使用時

- **ホットリロード**:
  - Go: ボリュームマウントにより、コード変更時は再ビルドが必要
  - Next.js: 自動でリロードされます
- **ポート競合**: 3000, 8080, 5432 番ポートが使用可能であることを確認
- **初回ビルド**: 初回は依存関係のダウンロードで時間がかかります

### 2. データベース

- **PostgreSQL**: コンテナの PostgreSQL を使用（ローカルに PostgreSQL は不要）
- **データ永続化**: `postgres_data` ボリュームにデータが保存されます
- **リセット**: `docker-compose down -v` でデータも削除されます

### 3. GraphQL

- **エンドポイント**: Go Echo が `/graphql` で GraphQL を提供
- **Next.js からアクセス**: urql を使用して CSR でアクセス
- **スキーマ確認**: http://localhost:8080/graphql で Playground にアクセス

### 4. Go 開発

- **モジュール管理**: `go.mod` で依存関係を管理
- **コード変更時**: コンテナの再ビルドが必要な場合があります
  ```bash
  docker-compose up --build api
  ```
- **GraphQL 再生成**: スキーマ変更時は `gqlgen generate` を実行

### 5. 環境変数

- `.env`ファイルは Git にコミットしない（`.gitignore`に含まれています）
- `NEXT_PUBLIC_`プレフィックス: Next.js でクライアント側から参照可能
- Go 側の環境変数はコンテナ内でのみ使用

### 6. 依存関係の管理

#### Go

- `go.mod` を編集後、`go mod tidy` 実行
- コンテナを再ビルド

#### Node.js (Next.js)

- `package.json` を編集後、`npm install` 実行

### 7. 本番環境へのデプロイ

本番環境では以下を変更してください:

- Go: リリースビルドを使用
- Next.js: `NODE_ENV=production` に設定
- PostgreSQL のパスワードを変更
- CORS 設定を本番ドメインに限定
- `docker-compose.yml` の `command` を本番用に変更

## 📚 参考リンク

### フロントエンド

- [Next.js ドキュメント](https://nextjs.org/docs)
- [urql ドキュメント](https://formidable.com/open-source/urql/docs/)
- [Redux Toolkit ドキュメント](https://redux-toolkit.js.org/)
- [Tailwind CSS ドキュメント](https://tailwindcss.com/docs)

### バックエンド

- [Go ドキュメント](https://go.dev/doc/)
- [Echo フレームワーク](https://echo.labstack.com/)
- [gqlgen ドキュメント](https://gqlgen.com/)
- [GORM ドキュメント](https://gorm.io/)

## 🐛 トラブルシューティング

### Docker コンテナが起動しない

```bash
# キャッシュをクリアして再ビルド
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Go でビルドエラー

```bash
# コンテナに入る
docker-compose exec api sh

# 依存関係を更新
go mod tidy
go mod download

# 再ビルド
go build -o bin/api cmd/api/main.go
```

### Next.js で urql の接続エラー

- `.env`の`NEXT_PUBLIC_GRAPHQL_ENDPOINT`が正しいか確認
- Go API コンテナが起動しているか確認: `docker-compose ps`
- Go の CORS 設定を確認

### GraphQL スキーマの変更が反映されない

```bash
# GraphQLコードを再生成
cd echo-app
go run github.com/99designs/gqlgen generate

# コンテナを再ビルド
docker-compose up --build api
```

### ポート競合エラー

```bash
# 使用中のポートを確認
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8080

# 別のポートを使用する場合は .env を編集
```

### データベース接続エラー

- PostgreSQL コンテナが起動しているか確認
- 環境変数の設定が正しいか確認
- ヘルスチェックが完了するまで待つ

---

質問や問題がある場合は、プロジェクトの issue を作成してください。
