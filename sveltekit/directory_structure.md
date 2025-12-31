# SvelteKit ディレクトリ構造

```
sveltekit/
├── .node-version              # Node.jsバージョン指定 (22)
├── .gitignore                 # Git除外ファイル
├── .env.example               # 環境変数テンプレート
├── package.json               # 依存関係とスクリプト
├── svelte.config.js          # SvelteKit設定
├── tsconfig.json             # TypeScript設定
├── vite.config.ts            # Vite + Vitest設定
├── docker-compose.yml        # Docker構成
├── Dockerfile                # Dockerイメージ定義
├── prisma/
│   └── schema.prisma         # Prismaスキーマ定義
└── src/
    ├── app.css               # グローバルスタイル
    ├── lib/
    │   ├── components/       # 再利用可能なコンポーネント
    │   │   └── Counter.svelte  # カウンターコンポーネント (Svelte 5 Runes)
    │   └── server/           # サーバーサイドコード
    │       └── prisma.ts     # Prismaクライアント
    ├── routes/               # ファイルベースルーティング
    │   ├── +layout.svelte    # ルートレイアウト
    │   ├── +page.svelte      # ホームページ (/)
    │   ├── users/
    │   │   ├── +page.server.ts  # サーバーサイドデータ取得
    │   │   └── +page.svelte     # ユーザー一覧 (/users)
    │   ├── counter/
    │   │   └── +page.svelte  # カウンターデモ (/counter)
    │   └── about/
    │       └── +page.svelte  # Aboutページ (/about)
    └── test/
        ├── setup.ts          # テストセットアップ
        └── example.test.ts   # サンプルテスト
```

## 📁 ディレクトリ説明

### ルート

- **`.node-version`** - Node.js 22を指定
- **`svelte.config.js`** - SvelteKitの設定（adapter、alias、preprocess）
- **`vite.config.ts`** - Viteビルド設定とVitest設定
- **`docker-compose.yml`** - PostgreSQL + SvelteKitのコンテナ構成
- **`Dockerfile`** - SvelteKitアプリのイメージ定義

### `src/routes/` - ファイルベースルーティング

SvelteKitはファイル名とディレクトリ構造からルートを自動生成します。

#### ファイル命名規則

- **`+page.svelte`** - ページコンポーネント
- **`+page.server.ts`** - サーバーサイドロジック（SSR用）
- **`+page.ts`** - クライアント/サーバー共通ロジック
- **`+layout.svelte`** - レイアウトコンポーネント
- **`+layout.server.ts`** - レイアウト用サーバーロジック
- **`+server.ts`** - APIルート

#### ルート例

```
src/routes/+page.svelte              → /
src/routes/about/+page.svelte        → /about
src/routes/users/+page.svelte        → /users
src/routes/users/[id]/+page.svelte   → /users/:id
src/routes/api/users/+server.ts      → /api/users (API)
```

### `src/lib/` - 共有コード

- **`components/`** - 再利用可能なSvelteコンポーネント
- **`server/`** - サーバーサイド専用コード（Prismaクライアントなど）

`$lib`エイリアスで簡単にインポート可能：

```typescript
import Counter from '$lib/components/Counter.svelte';
import { prisma } from '$lib/server/prisma';
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

### `src/test/` - テストファイル

- **`setup.ts`** - Vitestセットアップ（グローバル設定）
- **`*.test.ts`** - テストファイル

## 🎯 主要概念

### 1. ファイルベースルーティング

ディレクトリ構造がそのままURLに対応：

```
src/routes/
├── +page.svelte           # /
├── about/
│   └── +page.svelte       # /about
└── blog/
    ├── +page.svelte       # /blog
    └── [slug]/
        └── +page.svelte   # /blog/:slug
```

### 2. レイアウト

`+layout.svelte`は配下のすべてのルートで共有されます：

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  let { children } = $props();
</script>

<nav>...</nav>
{@render children()}
<footer>...</footer>
```

### 3. サーバーサイドデータ取得

`+page.server.ts`でSSR用のデータを取得：

```typescript
// src/routes/users/+page.server.ts
import type { PageServerLoad } from './$types';
import { prisma } from '$lib/server/prisma';

export const load: PageServerLoad = async () => {
  const users = await prisma.user.findMany();
  return { users };
};
```

ページコンポーネントで受け取る：

```svelte
<!-- src/routes/users/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';
  let { data }: { data: PageData } = $props();
</script>

{#each data.users as user}
  <p>{user.username}</p>
{/each}
```

### 4. Svelte 5 Runes

最新のリアクティブAPIを使用：

```svelte
<script lang="ts">
  // $state: リアクティブな状態
  let count = $state(0);
  
  // $derived: 派生状態
  let doubled = $derived(count * 2);
  
  // $effect: 副作用
  $effect(() => {
    console.log('Count changed:', count);
  });
</script>
```

### 5. APIルート

`+server.ts`でREST APIを作成：

```typescript
// src/routes/api/users/+server.ts
import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
  const users = await prisma.user.findMany();
  return json(users);
};

export const POST: RequestHandler = async ({ request }) => {
  const data = await request.json();
  const user = await prisma.user.create({ data });
  return json(user, { status: 201 });
};
```

## 🔧 設定ファイル

### `svelte.config.js`

```javascript
import adapter from '@sveltejs/adapter-auto';

export default {
  kit: {
    adapter: adapter(),
    alias: {
      $lib: './src/lib',
      $components: './src/lib/components'
    }
  }
};
```

### `vite.config.ts`

```typescript
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    include: ['src/**/*.{test,spec}.{js,ts}'],
    environment: 'jsdom'
  }
});
```

## 🚀 開発ワークフロー

### 1. 新しいページを追加

```bash
# src/routes/products/+page.svelteを作成
mkdir src/routes/products
touch src/routes/products/+page.svelte
```

自動的に`/products`ルートが生成されます。

### 2. サーバーサイドデータ取得

```typescript
// src/routes/products/+page.server.ts
export const load = async () => {
  const products = await prisma.product.findMany();
  return { products };
};
```

### 3. コンポーネント作成

```bash
# src/lib/components/ProductCard.svelteを作成
touch src/lib/components/ProductCard.svelte
```

```svelte
<!-- ProductCard.svelte -->
<script lang="ts">
  let { product } = $props();
</script>

<div class="card">
  <h3>{product.name}</h3>
  <p>{product.price}</p>
</div>
```

### 4. テスト作成

```typescript
// src/lib/components/ProductCard.test.ts
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/svelte';
import ProductCard from './ProductCard.svelte';

describe('ProductCard', () => {
  it('renders product name', () => {
    const { getByText } = render(ProductCard, {
      props: { product: { name: 'Test', price: 100 } }
    });
    expect(getByText('Test')).toBeInTheDocument();
  });
});
```

## 📚 補足

### パスエイリアス

`tsconfig.json`と`svelte.config.js`で設定されたエイリアス：

```typescript
import Counter from '$lib/components/Counter.svelte';
import { prisma } from '$lib/server/prisma';
```

### TypeScript型生成

SvelteKitは自動的に型を生成します：

```typescript
import type { PageData, PageServerLoad } from './$types';
```

`.svelte-kit/types/`に型定義が生成されます。

### Prisma統合

`src/lib/server/`にPrismaクライアントを配置し、サーバーサイドコードでのみ使用します。
