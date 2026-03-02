# Prisma ORM ガイド

> **対象者**: データベース操作に Prisma を使いたい開発者  
> **関連テンプレート**: `next/`・`remix/`・`sveltekit/`・`python/FastAPI/`  
> **所要時間**: 約 60 分

---

## 📚 目次

| # | ドキュメント | 説明 | 対象者 | 所要時間 |
|---|---|---|---|---|
| 01 | [基本情報](./01_基本情報.md) | Prisma とは何か、ORM の基本概念、他社製品との比較 | 初心者向け | 15 分 |
| 02 | [クイックスタート](./02_クイックスタート.md) | インストール、初期化、データベース接続、最初のマイグレーション | 初心者向け | 20 分 |
| 03 | [ローカル環境構築方法](./03_ローカル環境構築方法.md) | Docker を使った環境構築、PostgreSQL/MySQL/SQLite のセットアップ | 開発実践 | 20 分 |
| 04 | [マイグレーション方法](./04_マイグレーション方法.md) | マイグレーション戦略、コマンド詳解、ワークフロー | 開発実践 | 30 分 |
| 05 | [開発サンプルソース](./05_開発サンプルソース.md) | CRUD 操作、リレーション、フィルタリング、トランザクション | 開発実践 | 40 分 |
| 06 | [運用方法](./06_運用方法.md) | 本番環境での運用、接続プーリング、監視、スケーリング | 本番運用 | 30 分 |

### 🎯 学習パス

**初心者向け（30 分で Prisma の基本を理解）**
1. [01_基本情報](./01_基本情報.md) - Prisma とは、ORM の価値
2. [02_クイックスタート](./02_クイックスタート.md) - 初めてのプロジェクト

**開発実践向け（90 分で実装スキルを習得）**
1. [03_ローカル環境構築方法](./03_ローカル環境構築方法.md) - 堅牢な開発環境
2. [04_マイグレーション方法](./04_マイグレーション方法.md) - スキーマ管理戦略
3. [05_開発サンプルソース](./05_開発サンプルソース.md) - コード実装

**本番運用向け（30 分で本番環境対応を確認）**
1. [06_運用方法](./06_運用方法.md) - パフォーマンス、セキュリティ、スケーリング

### 🔗 クイックリンク
- [Prisma 公式ドキュメント](https://www.prisma.io/docs/)
- [Prisma GitHub リポジトリ](https://github.com/prismajs/prisma)
- [Prisma コミュニティ Slack](https://slack.prisma.io/)

---

## 1. Prisma とは

**Prisma** は、TypeScript / JavaScript 向けの **ORM（Object-Relational Mapper）** です。  
SQL を直接書く代わりに、TypeScript のコードでデータベース操作を行えます。

```
従来の SQL:
  const result = await db.query('SELECT * FROM users WHERE id = $1', [id])
  // 型情報がなく、スペルミスも実行時にしかわからない 😢

Prisma:
  const user = await prisma.user.findUnique({ where: { id } })
  // 型安全・補完が効く・SQL を書かなくてよい ✅
```

### Prisma の構成要素

| 構成要素 | 役割 |
|---------|------|
| **Prisma Schema** | DB の構造（テーブル・カラム）を定義するファイル |
| **Prisma Client** | TypeScript から DB を操作するためのクライアント（自動生成） |
| **Prisma Migrate** | スキーマ変更を SQL マイグレーションファイルに変換するツール |
| **Prisma Studio** | DB をブラウザで操作できる GUI ツール |

### 対応データベース

- PostgreSQL ✅（このリポジトリで使用）
- MySQL / MariaDB
- SQLite
- SQL Server
- MongoDB

---

## 2. セットアップ

### インストール

```bash
# Prisma CLI と Prisma Client をインストール
npm install prisma @prisma/client

# Prisma を初期化（schema.prisma と .env を生成）
npx prisma init
```

生成されるファイル：

```
prisma/
└── schema.prisma   ← スキーマ定義ファイル
.env                ← DATABASE_URL を設定するファイル
```

### DATABASE_URL の設定（`.env`）

```env
# PostgreSQL
DATABASE_URL="postgresql://ユーザー名:パスワード@ホスト:5432/DB名?schema=public"

# Docker 環境の場合（docker-compose.yml に合わせる）
DATABASE_URL="postgresql://postgres:postgres@db:5432/nextapp?schema=public"

# Supabase の場合
DATABASE_URL="postgresql://postgres:[パスワード]@db.[プロジェクトID].supabase.co:5432/postgres"
```

---

## 3. スキーマ定義（schema.prisma）

### このリポジトリの schema.prisma（remix / sveltekit 共通）

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())   // cuid() = ランダムな文字列 ID
  email     String   @unique
  username  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt             // 更新時に自動で現在日時をセット
  posts     Post[]                          // Post との 1:N リレーション
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?                         // ? = NULL 許容
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### フィールドの型

| Prisma 型 | SQL 型 | 説明 |
|----------|--------|------|
| `String` | `VARCHAR` / `TEXT` | 文字列 |
| `Int` | `INTEGER` | 整数 |
| `Float` | `FLOAT` | 浮動小数点 |
| `Boolean` | `BOOLEAN` | 真偽値 |
| `DateTime` | `TIMESTAMP` | 日時 |
| `Json` | `JSONB` | JSON データ |

### よく使うデコレータ

| デコレータ | 説明 | 例 |
|-----------|------|-----|
| `@id` | 主キー | `@id` |
| `@default()` | デフォルト値 | `@default(now())` |
| `@unique` | ユニーク制約 | `@unique` |
| `@updatedAt` | 更新時に自動セット | `@updatedAt` |
| `@relation` | リレーションを定義 | `@relation(fields: [userId], references: [id])` |
| `@@index` | インデックスを作成 | `@@index([email, createdAt])` |

### インデックスの追加

```prisma
model Post {
  id        String   @id @default(cuid())
  title     String
  authorId  String
  createdAt DateTime @default(now())

  // 複合インデックス（authorId + createdAt でよく検索する場合）
  @@index([authorId, createdAt])
}
```

---

## 4. マイグレーション

スキーマを変更したあとは、マイグレーションコマンドで DB に反映します。

### 開発時

```bash
# マイグレーションファイルを作成して DB に適用
npx prisma migrate dev --name add_users_table

# 実行後、以下が自動で行われる
# 1. prisma/migrations/[timestamp]_add_users_table/ にSQLファイルが生成
# 2. DB にマイグレーションを適用
# 3. Prisma Client を再生成
```

### 本番環境

```bash
# 本番では migrate deploy（新しいマイグレーションのみ適用）
npx prisma migrate deploy
```

### スキーマだけ変更して DB には反映しない場合

```bash
# DB の構造から schema.prisma を逆生成（既存 DB がある場合）
npx prisma db pull

# schema.prisma を DB に反映（マイグレーションファイルなし）
npx prisma db push
```

### Prisma Client の再生成

スキーマを変更したら Client を更新します：

```bash
npx prisma generate
```

---

## 5. CRUD 操作

まず Prisma Client を初期化します：

```typescript
// lib/prisma.ts（Next.js の場合）
import { PrismaClient } from '@prisma/client'

// 開発時のホットリロードでインスタンスが増えないようにする
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient }

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: ['query'],  // SQL クエリをログ出力（開発時）
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

### CREATE（作成）

```typescript
// 1 件作成
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    username: 'Alice',
  },
})

// 複数件作成
await prisma.user.createMany({
  data: [
    { email: 'bob@example.com', username: 'Bob' },
    { email: 'charlie@example.com', username: 'Charlie' },
  ],
})
```

### READ（取得）

```typescript
// ID で 1 件取得（見つからなければ null）
const user = await prisma.user.findUnique({
  where: { id: 'user-id-123' },
})

// 条件で 1 件取得
const user = await prisma.user.findFirst({
  where: { email: 'alice@example.com' },
})

// 全件取得
const users = await prisma.user.findMany()

// 件数を取得
const count = await prisma.user.count({
  where: { username: { startsWith: 'A' } },
})
```

### UPDATE（更新）

```typescript
// ID で 1 件更新
const updated = await prisma.user.update({
  where: { id: 'user-id-123' },
  data: { username: 'Alice Updated' },
})

// 条件に一致する全件を更新
await prisma.user.updateMany({
  where: { email: { endsWith: '@example.com' } },
  data: { username: '匿名' },
})

// 存在しなければ作成、あれば更新（Upsert）
const user = await prisma.user.upsert({
  where: { email: 'alice@example.com' },
  create: { email: 'alice@example.com', username: 'Alice' },
  update: { username: 'Alice Updated' },
})
```

### DELETE（削除）

```typescript
// ID で 1 件削除
await prisma.user.delete({
  where: { id: 'user-id-123' },
})

// 条件に一致する全件を削除
await prisma.user.deleteMany({
  where: { createdAt: { lt: new Date('2024-01-01') } },
})
```

---

## 6. リレーション（テーブル結合）

### 関連データを含めて取得（`include`）

```typescript
// User と関連する Post をまとめて取得
const userWithPosts = await prisma.user.findUnique({
  where: { id: 'user-id-123' },
  include: {
    posts: true,                    // posts をすべて含める
  },
})
// userWithPosts.posts → Post[]

// ネストして取得
const postWithAuthor = await prisma.post.findUnique({
  where: { id: 'post-id-456' },
  include: {
    author: {
      select: { id: true, username: true },  // 必要なカラムだけ選択
    },
  },
})
```

### 特定フィールドだけ取得（`select`）

```typescript
// パスワードなど不要なフィールドを除外
const users = await prisma.user.findMany({
  select: {
    id: true,
    username: true,
    email: true,
    // password: false  // 明示的に除外（デフォルトで含まれない）
  },
})
```

### 関連データを同時に作成

```typescript
// User と Post を同時に作成
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    username: 'Alice',
    posts: {
      create: [
        { title: '最初の投稿', content: '内容' },
        { title: '2 番目の投稿' },
      ],
    },
  },
  include: { posts: true },
})
```

---

## 7. フィルタ・ソート・ページネーション

### フィルタ

```typescript
const posts = await prisma.post.findMany({
  where: {
    published: true,                    // 等値
    title: { contains: 'Prisma' },     // 部分一致
    title: { startsWith: 'Hello' },    // 前方一致
    createdAt: { gte: new Date('2024-01-01') },  // 日付以降
    authorId: { in: ['id-1', 'id-2'] },          // いずれかに一致
    // AND / OR / NOT も使える
    AND: [
      { published: true },
      { title: { contains: 'TypeScript' } },
    ],
  },
})
```

### ソート

```typescript
const posts = await prisma.post.findMany({
  orderBy: [
    { createdAt: 'desc' },   // 新しい順
    { title: 'asc' },        // タイトル昇順（同日時の場合）
  ],
})
```

### ページネーション（オフセット方式）

```typescript
const PAGE_SIZE = 10

const posts = await prisma.post.findMany({
  skip: (page - 1) * PAGE_SIZE,  // 何件スキップするか
  take: PAGE_SIZE,               // 何件取得するか
  orderBy: { createdAt: 'desc' },
})
```

### カーソルベースのページネーション（大量データに推奨）

```typescript
const posts = await prisma.post.findMany({
  take: 10,
  cursor: { id: lastPostId },  // 前ページの最後の ID を渡す
  skip: 1,                     // カーソルの次から取得
  orderBy: { id: 'asc' },
})
```

---

## 8. トランザクション

複数の操作をまとめて実行し、どれか 1 つが失敗したら全部ロールバックします。

```typescript
// 方法 1: $transaction（配列形式・シンプル）
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'alice@example.com', username: 'Alice' } }),
  prisma.post.create({ data: { title: '投稿', authorId: 'user-id' } }),
])

// 方法 2: $transaction（コールバック形式・エラー処理が明確）
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'bob@example.com', username: 'Bob' },
  })

  await tx.post.create({
    data: { title: 'Bob の最初の投稿', authorId: user.id },
  })

  // この中でエラーが起きると、user.create も自動でロールバック
})
```

---

## 9. Prisma Studio（GUI ツール）

DB の内容をブラウザで確認・編集できる GUI ツールです。

```bash
npx prisma studio
# → http://localhost:5555 でブラウザが開く
```

Docker 環境の場合：

```bash
# コンテナ内で実行
docker compose exec app npx prisma studio

# ただし Docker 内では --browser none で起動し、ホスト PC でアクセス
docker compose exec app npx prisma studio --browser none
# → http://localhost:5555
```

---

## 10. Docker 環境での使い方

### よく使うコマンド

```bash
# マイグレーションを実行
docker compose exec app npx prisma migrate dev --name 変更内容の名前

# Prisma Client を再生成
docker compose exec app npx prisma generate

# DB をリセット（全データ削除 + マイグレーション再実行）
docker compose exec app npx prisma migrate reset

# シードデータを投入（prisma/seed.ts が必要）
docker compose exec app npx prisma db seed

# Prisma Studio を起動
docker compose exec app npx prisma studio --browser none
```

### シードデータの設定（`prisma/seed.ts`）

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

async function main() {
  // テスト用ユーザーを作成
  const alice = await prisma.user.upsert({
    where: { email: 'alice@example.com' },
    update: {},
    create: {
      email: 'alice@example.com',
      username: 'Alice',
      posts: {
        create: [
          { title: 'Hello World', content: '最初の投稿', published: true },
        ],
      },
    },
  })
  console.log('シード完了:', alice)
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect())
```

`package.json` に追加：

```json
{
  "prisma": {
    "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seed.ts"
  }
}
```

---

## 📌 まとめ

```bash
# よく使うコマンド一覧
npx prisma init                           # 初期化
npx prisma migrate dev --name 変更名     # マイグレーション作成・適用
npx prisma generate                       # Client 再生成
npx prisma migrate deploy                 # 本番環境へのマイグレーション適用
npx prisma db seed                        # シードデータ投入
npx prisma studio                         # GUI ツール起動
npx prisma migrate reset                  # DB リセット（開発時）
```

| 操作 | メソッド |
|------|---------|
| 1 件取得（ID） | `findUnique` |
| 1 件取得（条件） | `findFirst` |
| 全件取得 | `findMany` |
| 作成 | `create` / `createMany` |
| 更新 | `update` / `updateMany` / `upsert` |
| 削除 | `delete` / `deleteMany` |
| 件数 | `count` |
