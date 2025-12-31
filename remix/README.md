# Remix Template

Remix (React Router v7) + Prisma + TypeScript + Vitest による最新のフルスタックWebアプリケーション開発テンプレートです。

## ✨ 主な機能

- **Remix 2** - React Router v7ベースのフルスタックフレームワーク
- **React 18** - 最新のReactライブラリ
- **Prisma ORM** - 型安全なデータベースアクセス
- **TypeScript** - 完全な型安全性
- **Vitest** - 高速テストランナーとカバレッジ
- **Docker** - PostgreSQL + Remixのコンテナ化

## 🚀 クイックスタート

### ローカル環境で起動

```bash
# 依存関係のインストール
npm install

# 環境変数の設定
cp .env.example .env

# Prismaのセットアップ
npx prisma generate
npx prisma db push

# 開発サーバー起動
npm run dev
```

アプリケーションが `http://localhost:3000` で起動します。

### Dockerで起動

```bash
# Docker Composeで起動
docker-compose up

# バックグラウンドで起動
docker-compose up -d

# ログ確認
docker-compose logs -f

# 停止
docker-compose down
```

## 📁 プロジェクト構造

```
remix/
├── app/
│   ├── routes/               # ファイルベースルーティング
│   │   ├── _index.tsx       # ホームページ (/)
│   │   ├── users.tsx        # ユーザー一覧 (/users)
│   │   ├── counter.tsx      # カウンター (/counter)
│   │   └── about.tsx        # About (/about)
│   ├── components/          # 再利用可能なコンポーネント
│   │   └── Counter.tsx
│   ├── lib/
│   │   └── prisma.server.ts # Prismaクライアント
│   ├── styles/
│   │   └── global.css       # グローバルスタイル
│   ├── test/
│   │   ├── setup.ts         # テストセットアップ
│   │   └── example.test.ts  # サンプルテスト
│   └── root.tsx             # ルートコンポーネント
├── prisma/
│   └── schema.prisma        # Prismaスキーマ定義
├── docker-compose.yml       # Docker構成
├── Dockerfile               # Dockerイメージ定義
├── vite.config.ts          # Vite + Remix設定
└── package.json
```

## 🎯 Remixの特徴

### Loader - サーバーサイドデータ取得

```typescript
// app/routes/users.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { prisma } from "~/lib/prisma.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const users = await prisma.user.findMany();
  return json({ users });
};

export default function Users() {
  const { users } = useLoaderData<typeof loader>();
  
  return (
    <div>
      {users.map(user => (
        <p key={user.id}>{user.username}</p>
      ))}
    </div>
  );
}
```

### Action - フォーム処理

```typescript
import type { ActionFunctionArgs } from "@remix-run/node";
import { redirect } from "@remix-run/node";
import { Form } from "@remix-run/react";

export const action = async ({ request }: ActionFunctionArgs) => {
  const formData = await request.formData();
  const username = formData.get("username");
  
  await prisma.user.create({
    data: { username, email: `${username}@example.com` }
  });
  
  return redirect("/users");
};

export default function NewUser() {
  return (
    <Form method="post">
      <input name="username" required />
      <button type="submit">Create</button>
    </Form>
  );
}
```

### Meta - SEO対応

```typescript
import type { MetaFunction } from "@remix-run/node";

export const meta: MetaFunction = () => {
  return [
    { title: "Users - Remix App" },
    { name: "description", content: "User list page" }
  ];
};
```

### Error Boundary

```typescript
export function ErrorBoundary() {
  const error = useRouteError();
  
  if (isRouteErrorResponse(error)) {
    return (
      <div>
        <h1>{error.status} {error.statusText}</h1>
        <p>{error.data}</p>
      </div>
    );
  }
  
  return <h1>Unexpected Error</h1>;
}
```

## 🗄️ Prismaの使用

### スキーマ定義

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  username  String
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Prismaコマンド

```bash
# マイグレーション作成
npx prisma migrate dev --name init

# Prisma Studioでデータ確認
npx prisma studio

# スキーマからクライアント生成
npx prisma generate

# データベースと同期（開発時）
npx prisma db push
```

## 🧪 テスト

```bash
# テスト実行
npm test

# UIモードでテスト
npm run test:ui

# カバレッジ計測
npm run test:coverage

# 監視モード
npm test -- --watch
```

### テスト例

```typescript
import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import Counter from "~/components/Counter";

describe("Counter", () => {
  it("renders initial count", () => {
    const { getByText } = render(<Counter />);
    expect(getByText("0")).toBeInTheDocument();
  });
});
```

## 🛣️ ルーティング

Remixはファイルベースルーティングを採用しています。

### ファイル名とURL

- `app/routes/_index.tsx` → `/`
- `app/routes/about.tsx` → `/about`
- `app/routes/users.tsx` → `/users`
- `app/routes/users.$id.tsx` → `/users/:id`
- `app/routes/users._index.tsx` → `/users` (nested)
- `app/routes/api.users.tsx` → `/api/users`

### 動的ルーティング

```typescript
// app/routes/users.$id.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { id } = params;
  const user = await prisma.user.findUnique({ where: { id } });
  return json({ user });
};
```

### ネストされたレイアウト

```typescript
// app/routes/users.tsx (親ルート)
import { Outlet } from "@remix-run/react";

export default function UsersLayout() {
  return (
    <div>
      <h1>Users</h1>
      <Outlet /> {/* 子ルートがここにレンダリング */}
    </div>
  );
}
```

## 🎨 スタイリング

### グローバルCSS

```typescript
// app/root.tsx
import type { LinksFunction } from "@remix-run/node";
import stylesheet from "~/styles/global.css?url";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: stylesheet }
];
```

### CSS Modules（オプション）

```bash
npm install -D @vanilla-extract/css
```

## 📦 ビルドとデプロイ

### 本番ビルド

```bash
# 本番ビルド
npm run build

# 本番サーバー起動
npm start
```

### Flyへのデプロイ

```bash
# Fly CLIをインストール
curl -L https://fly.io/install.sh | sh

# アプリ作成
fly launch

# デプロイ
fly deploy
```

### Vercelへのデプロイ

```bash
# Vercel CLIをインストール
npm i -g vercel

# デプロイ
vercel
```

### Render.comへのデプロイ

1. GitHubリポジトリに接続
2. ビルドコマンド: `npm run build`
3. 起動コマンド: `npm start`

## 🔧 開発

### コード整形

```bash
# チェック
npm run lint

# 自動修正
npm run format
```

### 型チェック

```bash
# 型チェック実行
npm run typecheck
```

## 🐳 Docker開発環境

### サービス構成

- **postgres** - PostgreSQL 16データベース
- **app** - Remixアプリケーション

### コマンド

```bash
# 起動
docker-compose up -d

# ログ確認
docker-compose logs -f app

# コンテナ内でコマンド実行
docker-compose exec app npm run typecheck

# 再ビルド
docker-compose up --build

# 停止と削除
docker-compose down -v
```

## 🌟 Remixの主な特徴

### Progressive Enhancement

JavaScriptなしでも動作するフォーム：

```typescript
import { Form } from "@remix-run/react";

export default function NewUser() {
  return (
    <Form method="post">
      <input name="username" required />
      <button type="submit">Create</button>
    </Form>
  );
}
```

### Optimistic UI

楽観的UIアップデート：

```typescript
import { useFetcher } from "@remix-run/react";

export default function LikeButton({ postId }: { postId: string }) {
  const fetcher = useFetcher();
  
  return (
    <fetcher.Form method="post" action={`/posts/${postId}/like`}>
      <button type="submit">
        {fetcher.state === "submitting" ? "Liking..." : "Like"}
      </button>
    </fetcher.Form>
  );
}
```

### Nested Routes

ネストされたルーティングとデータ取得：

```
app/routes/
├── users.tsx           # レイアウト
├── users._index.tsx    # /users
└── users.$id.tsx       # /users/:id
```

各ルートが独立して`loader`を持ち、並列でデータを取得できます。

### Web Standard APIs

標準のWeb Fetch APIを使用：

```typescript
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const url = new URL(request.url);
  const search = url.searchParams.get("q");
  
  // 標準のResponse
  return new Response(JSON.stringify({ search }), {
    headers: { "Content-Type": "application/json" }
  });
};
```

## 📚 参考リンク

- [Remix公式ドキュメント](https://remix.run/)
- [React Router公式ドキュメント](https://reactrouter.com/)
- [Prisma公式ドキュメント](https://www.prisma.io/)
- [Vitest公式ドキュメント](https://vitest.dev/)
- [Remix Stacks](https://remix.run/stacks)

## 🤝 コントリビューション

このテンプレートはMITライセンスのもとで公開されています。自由にカスタマイズしてご利用ください。

## 📝 ライセンス

MIT License
