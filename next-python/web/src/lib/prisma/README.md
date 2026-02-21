# Prisma セットアップガイド

このフォルダは、Prisma ORM の設定と管理を行うディレクトリです。

## ファイル構成

- **schema.prisma** - Prisma スキーマファイル（データベースモデル定義）
- **README.md** - このファイル

## セットアップ手順

### 1. Prisma を初期化

```bash
# Prisma をインストール（package.json に @prisma/client が含まれている場合）
npm install

# Prisma CLI をインストール
npm install -D prisma
```

### 2. schema.prisma を編集

`schema.prisma` ファイルにデータベースモデルを定義します。

#### 例: User モデルを定義

```prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  posts Post[]

  @@map("users")
}

model Post {
  id    Int     @id @default(autoincrement())
  title String
  content String?
  userId Int
  user  User @relation(fields: [userId], references: [id])

  @@map("posts")
}
```

### 3. マイグレーションを作成・実行

```bash
# スキーマをデータベースに適用（マイグレーションファイルを作成）
npx prisma migrate dev --name init

# または、スキーマのみ適用（マイグレーション履歴を記録しない）
npx prisma db push
```

### 4. Prisma クライアントを生成

```bash
# Prisma クライアントを生成
npx prisma generate
```

## 使用例

### API ルートでのデータ操作

```typescript
// src/app/api/users/route.ts
import { PrismaClient } from '@prisma/client'
import { NextRequest, NextResponse } from 'next/server'

const prisma = new PrismaClient()

// ユーザー一覧を取得
export async function GET() {
  const users = await prisma.user.findMany()
  return NextResponse.json(users)
}

// ユーザーを作成
export async function POST(request: NextRequest) {
  const data = await request.json()
  const user = await prisma.user.create({
    data,
  })
  return NextResponse.json(user, { status: 201 })
}
```

### Server Component での使用

```typescript
// src/app/users/page.tsx
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

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

## よく使うコマンド

```bash
# マイグレーション作成・実行
npx prisma migrate dev --name <migration_name>

# スキーマをデータベースに適用（マイグレーション履歴なし）
npx prisma db push

# マイグレーション状態を確認
npx prisma migrate status

# Prisma Studio でデータを確認・編集
npx prisma studio

# Prisma クライアントを再生成
npx prisma generate

# データベースをリセット
npx prisma migrate reset
```

## トラブルシューティング

### Prisma クライアント生成エラー

```bash
# キャッシュをクリアして再生成
rm -rf node_modules/.prisma
npx prisma generate
```

### データベース接続エラー

- `.env.local` の `DATABASE_URL` が正しいか確認
- PostgreSQL が起動しているか確認

```bash
# ローカルで PostgreSQL を起動（Docker）
docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:16
```

### マイグレーション失敗時

```bash
# マイグレーションをロールバック
npx prisma migrate resolve --rolled-back <migration_name>

# データベースを完全リセット（全データ削除）
npx prisma migrate reset --force
```

## 参考リンク

- [Prisma ドキュメント](https://www.prisma.io/docs/)
- [Prisma スキーマ参照](https://www.prisma.io/docs/orm/reference/prisma-schema-reference)
- [Prisma Client リファレンス](https://www.prisma.io/docs/orm/reference/prisma-client-reference)
