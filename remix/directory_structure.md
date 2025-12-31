# Remix ディレクトリ構造

```
remix/
├── .node-version              # Node.jsバージョン指定 (22)
├── .gitignore                 # Git除外ファイル
├── .env.example               # 環境変数テンプレート
├── package.json               # 依存関係とスクリプト
├── tsconfig.json             # TypeScript設定
├── vite.config.ts            # Vite + Remix設定
├── docker-compose.yml        # Docker構成
├── Dockerfile                # Dockerイメージ定義
├── prisma/
│   └── schema.prisma         # Prismaスキーマ定義
└── app/
    ├── root.tsx              # ルートコンポーネント（レイアウト）
    ├── routes/               # ファイルベースルーティング
    │   ├── _index.tsx       # ホームページ (/)
    │   ├── users.tsx        # ユーザー一覧 (/users)
    │   ├── counter.tsx      # カウンター (/counter)
    │   └── about.tsx        # About (/about)
    ├── components/          # 再利用可能なコンポーネント
    │   └── Counter.tsx      # カウンターコンポーネント
    ├── lib/
    │   └── prisma.server.ts # Prismaクライアント（サーバーサイド専用）
    ├── styles/
    │   └── global.css       # グローバルスタイル
    └── test/
        ├── setup.ts         # テストセットアップ
        └── example.test.ts  # サンプルテスト
```

## 📁 ディレクトリ説明

### ルート

- **`.node-version`** - Node.js 22を指定
- **`vite.config.ts`** - Vite + Remix設定、Vitestテスト設定
- **`tsconfig.json`** - TypeScript設定（パスエイリアス `~/*`）
- **`docker-compose.yml`** - PostgreSQL + Remixのコンテナ構成
- **`Dockerfile`** - Remixアプリのイメージ定義

### `app/` - アプリケーションコード

Remixのすべてのコードは`app/`ディレクトリに配置されます。

#### `app/root.tsx` - ルートコンポーネント

すべてのルートを包含する最上位コンポーネント：

```typescript
import { Links, Meta, Outlet, Scripts } from "@remix-run/react";

export default function App() {
  return (
    <html>
      <head>
        <Meta />
        <Links />
      </head>
      <body>
        <Outlet /> {/* 各ルートがここにレンダリング */}
        <Scripts />
      </body>
    </html>
  );
}
```

### `app/routes/` - ファイルベースルーティング

Remixはファイル名とディレクトリ構造からルートを自動生成します。

#### ファイル命名規則

- **`_index.tsx`** - インデックスルート（`/`）
- **`about.tsx`** - 通常のルート（`/about`）
- **`$id.tsx`** - 動的パラメータ（`/:id`）
- **`_layout.tsx`** - パスレスレイアウト（URLに影響しない）
- **`_.tsx`** - ネストしないルート

#### ルート例

```
app/routes/
├── _index.tsx              → /
├── about.tsx               → /about
├── users.tsx               → /users
├── users.$id.tsx           → /users/:id
├── users.$id.edit.tsx      → /users/:id/edit
├── api.users.tsx           → /api/users
└── blog/
    ├── _index.tsx          → /blog
    └── $slug.tsx           → /blog/:slug
```

### `app/lib/` - 共有ライブラリ

- **`prisma.server.ts`** - Prismaクライアント（`.server`サフィックスでサーバーサイド専用）

パスエイリアス`~/*`で簡単にインポート可能：

```typescript
import { prisma } from "~/lib/prisma.server";
```

### `app/components/` - コンポーネント

再利用可能なReactコンポーネントを配置：

```typescript
import Counter from "~/components/Counter";
```

### `app/styles/` - スタイル

グローバルCSSやCSS Modulesを配置：

```typescript
import stylesheet from "~/styles/global.css?url";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: stylesheet }
];
```

### `prisma/` - データベーススキーマ

- **`schema.prisma`** - Prismaスキーマ定義（モデル、リレーション）

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  username  String
  posts     Post[]
}

model Post {
  id        String   @id @default(cuid())
  title     String
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
}
```

### `app/test/` - テストファイル

- **`setup.ts`** - Vitestセットアップ（グローバル設定）
- **`*.test.ts(x)`** - テストファイル

## 🎯 主要概念

### 1. ファイルベースルーティング

ファイル構造がそのままURLに対応：

```
app/routes/
├── _index.tsx           # /
├── about.tsx            # /about
└── users/
    ├── _index.tsx       # /users
    └── $id.tsx          # /users/:id
```

### 2. Loader - サーバーサイドデータ取得

各ルートで`loader`関数を export してSSRデータを取得：

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
      {users.map(user => <p key={user.id}>{user.username}</p>)}
    </div>
  );
}
```

### 3. Action - フォームとミューテーション

`action`関数でフォーム送信やデータ更新を処理：

```typescript
import type { ActionFunctionArgs } from "@remix-run/node";
import { Form, redirect } from "@remix-run/react";

export const action = async ({ request }: ActionFunctionArgs) => {
  const formData = await request.formData();
  const username = formData.get("username") as string;
  
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

### 4. Meta - SEO対応

`meta`関数でページメタデータを定義：

```typescript
import type { MetaFunction } from "@remix-run/node";

export const meta: MetaFunction = () => {
  return [
    { title: "Users - Remix App" },
    { name: "description", content: "User list page" }
  ];
};
```

### 5. Error Boundary

エラーハンドリングを各ルートで定義：

```typescript
import { useRouteError, isRouteErrorResponse } from "@remix-run/react";

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

## 🔧 設定ファイル

### `vite.config.ts`

```typescript
import { vitePlugin as remix } from "@remix-run/dev";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [
    remix(),
    tsconfigPaths(), // tsconfig.jsonのpathsを解決
  ],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./app/test/setup.ts"],
  },
});
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "~/*": ["./app/*"]
    }
  }
}
```

## 🚀 開発ワークフロー

### 1. 新しいページを追加

```bash
# app/routes/products.tsxを作成
touch app/routes/products.tsx
```

```typescript
// app/routes/products.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const products = await prisma.product.findMany();
  return json({ products });
};

export default function Products() {
  const { products } = useLoaderData<typeof loader>();
  
  return (
    <div>
      <h1>Products</h1>
      {products.map(p => <p key={p.id}>{p.name}</p>)}
    </div>
  );
}
```

自動的に`/products`ルートが生成されます。

### 2. 動的ルーティング

```typescript
// app/routes/products.$id.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { id } = params; // URLから:idを取得
  const product = await prisma.product.findUnique({ where: { id } });
  return json({ product });
};
```

### 3. APIルート

```typescript
// app/routes/api.users.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { json } from "@remix-run/node";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const users = await prisma.user.findMany();
  return json(users); // JSON APIレスポンス
};
```

`GET /api/users`でアクセス可能。

### 4. コンポーネント作成

```bash
# app/components/ProductCard.tsxを作成
touch app/components/ProductCard.tsx
```

```typescript
// ProductCard.tsx
export default function ProductCard({ product }: { product: any }) {
  return (
    <div className="card">
      <h3>{product.name}</h3>
      <p>{product.price}</p>
    </div>
  );
}
```

### 5. テスト作成

```typescript
// app/components/ProductCard.test.tsx
import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import ProductCard from "./ProductCard";

describe("ProductCard", () => {
  it("renders product name", () => {
    const { getByText } = render(
      <ProductCard product={{ name: "Test", price: 100 }} />
    );
    expect(getByText("Test")).toBeInTheDocument();
  });
});
```

## 📚 補足

### パスエイリアス

`tsconfig.json`で設定された`~/*`エイリアス：

```typescript
import Counter from "~/components/Counter";
import { prisma } from "~/lib/prisma.server";
```

### サーバーサイド専用コード

`.server`サフィックスをつけたファイルはクライアントバンドルから除外されます：

```typescript
// app/lib/prisma.server.ts
// クライアントにバンドルされない
import { PrismaClient } from "@prisma/client";
export const prisma = new PrismaClient();
```

### Prisma統合

`app/lib/`にPrismaクライアントを配置し、`loader`や`action`でのみ使用します。

### Nested Routes

親ルートが`<Outlet />`を使用することで、子ルートをネスト可能：

```typescript
// app/routes/users.tsx（親）
import { Outlet } from "@remix-run/react";

export default function UsersLayout() {
  return (
    <div>
      <h1>Users</h1>
      <Outlet /> {/* 子ルートがここに */}
    </div>
  );
}

// app/routes/users._index.tsx（子 /users）
// app/routes/users.$id.tsx（子 /users/:id）
```

### Progressive Enhancement

Remixの`<Form>`はJavaScriptなしでも動作します：

```typescript
import { Form } from "@remix-run/react";

<Form method="post">
  <input name="username" />
  <button type="submit">Submit</button>
</Form>
```

JavaScriptが有効な場合は、自動的にSPA風の動作に切り替わります。
