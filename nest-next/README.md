# Nest.js + Next.js フルスタック TypeScript テンプレート

next-go や next-python の TypeScript 統一版として、NestJS と Next.js を組み合わせたエンタープライズグレードのフルスタック開発環境です。

## 📋 目次

- [概要](#概要)
- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [セットアップ](#セットアップ)
- [開発](#開発)
- [テスト](#テスト)
- [主な機能](#主な機能)
- [API 仕様](#api仕様)
- [デプロイ](#デプロイ)
- [トラブルシューティング](#トラブルシューティング)

## 概要

このテンプレートは、フロントエンドからバックエンドまで TypeScript で統一された開発環境を提供します。NestJS の堅牢なアーキテクチャと Next.js の柔軟なレンダリング機能を組み合わせることで、スケーラブルなアプリケーション開発を実現します。

### 主な特徴

- **完全 TypeScript 統一**: フロントエンドからバックエンドまで一貫した型安全性
- **GraphQL API**: コードファーストアプローチによる型安全な API 開発
- **モダンアーキテクチャ**: NestJS のモジュラー設計 + Next.js の App Router
- **Docker 対応**: PostgreSQL + バックエンド + フロントエンドの完全なコンテナ化
- **認証機能**: JWT 認証のサンプル実装
- **ORM 統合**: Prisma による型安全なデータベース操作

## 技術スタック

### バックエンド (NestJS)

- **NestJS 10**: エンタープライズグレードの Node.js フレームワーク
- **GraphQL**: Apollo Server による型安全な API
- **Prisma 6.4**: 次世代 TypeScript ORM
- **JWT 認証**: Passport.js による認証機能
- **Jest**: ユニットテスト・E2E テスト

### フロントエンド (Next.js)

- **Next.js 14**: App Router による最新の React 開発
- **Apollo Client 3**: GraphQL クライアント
- **Redux Toolkit 2**: 状態管理
- **Tailwind CSS 3**: ユーティリティファースト CSS
- **Vitest 2**: 高速テストランナー

### インフラ

- **PostgreSQL 16**: リレーショナルデータベース
- **Docker Compose**: マルチコンテナ開発環境
- **Node.js 22**: 最新 LTS バージョン

## プロジェクト構成

```
nest-next/
├── docker-compose.yml          # Docker Compose設定
├── .env.example                # 環境変数サンプル
├── nest-app/                   # バックエンド (NestJS)
│   ├── src/
│   │   ├── main.ts             # エントリーポイント
│   │   ├── app.module.ts       # ルートモジュール
│   │   ├── prisma/             # Prisma設定
│   │   │   ├── prisma.service.ts
│   │   │   └── prisma.module.ts
│   │   ├── users/              # ユーザーモジュール
│   │   │   ├── user.model.ts   # GraphQLモデル
│   │   │   ├── users.service.ts
│   │   │   ├── users.resolver.ts
│   │   │   └── users.module.ts
│   │   ├── posts/              # 投稿モジュール
│   │   │   ├── posts.service.ts
│   │   │   ├── posts.resolver.ts
│   │   │   └── posts.module.ts
│   │   └── auth/               # 認証モジュール
│   │       ├── auth.service.ts
│   │       ├── auth.module.ts
│   │       └── jwt.strategy.ts
│   ├── prisma/
│   │   └── schema.prisma       # Prismaスキーマ
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
└── next/                       # フロントエンド (Next.js)
    ├── src/
    │   ├── app/                # App Router
    │   │   ├── layout.tsx      # ルートレイアウト
    │   │   ├── page.tsx        # ホームページ
    │   │   ├── users/          # ユーザー一覧ページ
    │   │   └── graphql/        # GraphQL解説ページ
    │   ├── components/         # Reactコンポーネント
    │   │   ├── Counter.tsx     # Reduxカウンター
    │   │   └── Providers.tsx   # プロバイダー設定
    │   ├── store/              # Redux状態管理
    │   │   ├── store.ts
    │   │   └── slices/
    │   │       └── counterSlice.ts
    │   ├── lib/
    │   │   └── graphql/        # GraphQL設定
    │   │       ├── apolloClient.ts
    │   │       └── queries.ts
    │   └── test/               # テスト
    │       ├── setup.ts
    │       └── example.test.ts
    ├── package.json
    ├── tsconfig.json
    ├── vitest.config.ts
    └── Dockerfile
```

## セットアップ

### 前提条件

- Node.js 22 以上
- Docker & Docker Compose
- Git

### 初回セットアップ

1. **環境変数の設定**

```powershell
# .env.exampleをコピーして.envを作成
Copy-Item .env.example .env

# 必要に応じて.envを編集
# JWT_SECRETは本番環境では必ず変更してください
```

2. **Docker コンテナの起動**

```powershell
docker-compose up -d
```

3. **データベースマイグレーション**

```powershell
# バックエンドコンテナに入る
docker exec -it nest_backend sh

# Prismaマイグレーション実行
npx prisma migrate dev --name init

# サンプルデータの投入(オプション)
npx prisma db seed
```

4. **ブラウザで確認**

- フロントエンド: http://localhost:3000
- GraphQL Playground: http://localhost:4000/graphql

## 開発

### ローカル開発(コンテナ外)

バックエンドとフロントエンドを個別に起動する場合:

```powershell
# データベースのみ起動
docker-compose up postgres -d

# バックエンド開発サーバー
cd nest-app
npm install
npx prisma generate
npm run start:dev

# フロントエンド開発サーバー(別ターミナル)
cd next
npm install
npm run dev
```

### コンテナ開発

```powershell
# すべてのサービスを起動
docker-compose up

# 特定のサービスを再起動
docker-compose restart backend

# ログの確認
docker-compose logs -f backend
docker-compose logs -f frontend
```

### ホットリロード

両方のサービスはホットリロードに対応しているため、コードを変更すると自動的に再読み込みされます。

## テスト

### バックエンドテスト (NestJS + Jest)

```powershell
cd nest-app

# ユニットテスト
npm test

# ウォッチモード
npm run test:watch

# カバレッジ
npm run test:cov

# E2Eテスト
npm run test:e2e
```

### フロントエンドテスト (Vitest + React Testing Library)

```powershell
cd next

# テスト実行
npm test

# ウォッチモード
npm run test

# UIモード
npm run test:ui

# カバレッジ
npm run test:coverage
```

## 主な機能

### 1. GraphQL API (NestJS)

#### コードファースト設計

NestJS のデコレーターを使用して、TypeScript クラスから自動的に GraphQL スキーマを生成:

```typescript
@ObjectType()
export class User {
  @Field(() => ID)
  id: string

  @Field()
  email: string

  @Field()
  username: string
}
```

#### リゾルバー

```typescript
@Resolver(() => User)
export class UsersResolver {
  @Query(() => [User])
  async getUsers() {
    return this.usersService.findAll()
  }

  @Mutation(() => User)
  async createUser(@Args('email') email: string) {
    return this.usersService.create({ email })
  }
}
```

### 2. Prisma ORM

#### スキーマ定義

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  username  String
  password  String
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

#### 使用例

```typescript
// ユーザー作成
const user = await this.prisma.user.create({
  data: { email, username, password: hashedPassword }
})

// リレーション込みで取得
const users = await this.prisma.user.findMany({
  include: { posts: true }
})
```

### 3. JWT 認証

#### ログイン

```typescript
const result = await this.authService.login(email, password)
// { access_token: "...", user: {...} }
```

#### 保護されたルート

```typescript
@UseGuards(JwtAuthGuard)
@Query(() => User)
async me(@CurrentUser() user: User) {
  return user;
}
```

### 4. Apollo Client (Next.js)

#### クライアント設定

```typescript
const apolloClient = new ApolloClient({
  uri: 'http://localhost:4000/graphql',
  cache: new InMemoryCache()
})
```

#### クエリ使用例

```typescript
const { data, loading, error } = useQuery(GET_USERS)
```

### 5. Redux Toolkit

#### スライス定義

```typescript
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      state.value += 1
    }
  }
})
```

#### コンポーネントでの使用

```typescript
const count = useAppSelector((state) => state.counter.value)
const dispatch = useAppDispatch()
```

## API 仕様

### GraphQL エンドポイント

```
http://localhost:4000/graphql
```

### クエリ例

#### すべてのユーザーを取得

```graphql
query {
  users {
    id
    email
    username
    posts {
      id
      title
    }
  }
}
```

#### ユーザー作成

```graphql
mutation {
  createUser(
    email: "test@example.com"
    username: "testuser"
    password: "password123"
  ) {
    id
    email
    username
  }
}
```

#### 投稿作成

```graphql
mutation {
  createPost(
    title: "My First Post"
    content: "Hello World"
    authorId: "user_id_here"
  ) {
    id
    title
    published
  }
}
```

## デプロイ

### 環境変数の設定

本番環境では以下の環境変数を適切に設定してください:

```bash
# セキュリティ重要
JWT_SECRET=your-super-secret-production-key

# データベース
DATABASE_URL=postgresql://user:password@host:5432/dbname

# バックエンドURL
BACKEND_PORT=4000

# フロントエンドURL
FRONTEND_PORT=3000
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_GRAPHQL_ENDPOINT=https://api.yourdomain.com/graphql
```

### Docker 本番ビルド

```powershell
# プロダクションビルド
docker-compose -f docker-compose.prod.yml build

# 起動
docker-compose -f docker-compose.prod.yml up -d
```

### Vercel + Heroku 構成例

- **フロントエンド**: Vercel (Next.js)
- **バックエンド**: Heroku または Railway (NestJS)
- **データベース**: Supabase または Heroku Postgres

## トラブルシューティング

### データベース接続エラー

```powershell
# PostgreSQLが起動しているか確認
docker-compose ps

# ログを確認
docker-compose logs postgres

# データベースを再作成
docker-compose down -v
docker-compose up -d
```

### Prisma 関連エラー

```powershell
# Prismaクライアントを再生成
cd nest-app
npx prisma generate

# マイグレーションをリセット
npx prisma migrate reset
```

### ポート競合エラー

```powershell
# 使用中のポートを確認
netstat -ano | findstr :3000
netstat -ano | findstr :4000

# .envでポートを変更
FRONTEND_PORT=3001
BACKEND_PORT=4001
```

### GraphQL スキーマ更新が反映されない

```powershell
# バックエンドを再起動
docker-compose restart backend

# または、スキーマファイルを削除して自動生成
Remove-Item nest-app/src/schema.gql
```

### ホットリロードが効かない

Windows でファイル監視が効かない場合:

```json
// nest-app/nest-cli.json
{
  "compilerOptions": {
    "watchAssets": true
  }
}
```

```json
// next/next.config.js
module.exports = {
  webpack: (config) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    }
    return config
  },
}
```

## 参考リンク

- [NestJS 公式ドキュメント](https://docs.nestjs.com/)
- [Next.js 公式ドキュメント](https://nextjs.org/docs)
- [Prisma 公式ドキュメント](https://www.prisma.io/docs)
- [Apollo Client 公式ドキュメント](https://www.apollographql.com/docs/react/)
- [Redux Toolkit 公式ドキュメント](https://redux-toolkit.js.org/)
- [GraphQL 公式サイト](https://graphql.org/)

## ライセンス

MIT
