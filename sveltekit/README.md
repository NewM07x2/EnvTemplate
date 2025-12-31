# SvelteKit Template

Svelte 5 + SvelteKit 2 + Prisma + TypeScript + Vitest による最新のWebアプリケーション開発テンプレートです。

## ✨ 主な機能

- **Svelte 5** - 最新のRunes API ($state, $derived, $effect)
- **SvelteKit 2** - ファイルベースルーティング、SSR/SSG対応
- **Prisma ORM** - 型安全なデータベースアクセス
- **TypeScript** - 完全な型安全性
- **Vitest** - 高速テストランナーとカバレッジ
- **Docker** - PostgreSQL + SvelteKitのコンテナ化

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

アプリケーションが `http://localhost:5173` で起動します。

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
sveltekit/
├── prisma/
│   └── schema.prisma          # Prismaスキーマ定義
├── src/
│   ├── lib/
│   │   ├── components/        # 再利用可能なコンポーネント
│   │   │   └── Counter.svelte
│   │   └── server/
│   │       └── prisma.ts      # Prismaクライアント
│   ├── routes/
│   │   ├── +layout.svelte     # ルートレイアウト
│   │   ├── +page.svelte       # ホームページ
│   │   ├── users/
│   │   │   ├── +page.server.ts  # サーバーサイドデータ取得
│   │   │   └── +page.svelte      # ユーザー一覧ページ
│   │   ├── counter/
│   │   │   └── +page.svelte   # カウンターデモ
│   │   └── about/
│   │       └── +page.svelte   # Aboutページ
│   ├── test/
│   │   ├── setup.ts           # テストセットアップ
│   │   └── example.test.ts    # サンプルテスト
│   └── app.css                # グローバルスタイル
├── docker-compose.yml         # Docker構成
├── Dockerfile                 # Dockerイメージ定義
├── svelte.config.js          # SvelteKit設定
├── vite.config.ts            # Vite + Vitest設定
└── package.json
```

## 🎯 Svelte 5 Runes API

### $state - リアクティブな状態

```svelte
<script lang="ts">
  let count = $state(0);
  
  function increment() {
    count++;
  }
</script>

<button onclick={increment}>Count: {count}</button>
```

### $derived - 派生状態

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
  let isEven = $derived(count % 2 === 0);
</script>

<p>Count: {count}</p>
<p>Doubled: {doubled}</p>
<p>Even: {isEven}</p>
```

### $effect - 副作用

```svelte
<script lang="ts">
  let count = $state(0);
  
  $effect(() => {
    console.log(`Count changed to: ${count}`);
  });
</script>
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

### サーバーサイドでのデータ取得

```typescript
// src/routes/users/+page.server.ts
import type { PageServerLoad } from './$types';
import { prisma } from '$lib/server/prisma';

export const load: PageServerLoad = async () => {
  const users = await prisma.user.findMany({
    include: { posts: true }
  });
  
  return { users };
};
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
import { describe, it, expect } from 'vitest';

describe('Counter logic', () => {
  it('should increment correctly', () => {
    let count = 0;
    count++;
    expect(count).toBe(1);
  });
});
```

## 🛣️ ルーティング

SvelteKitはファイルベースルーティングを採用しています。

- `src/routes/+page.svelte` → `/`
- `src/routes/about/+page.svelte` → `/about`
- `src/routes/users/+page.svelte` → `/users`
- `src/routes/users/[id]/+page.svelte` → `/users/:id`

### レイアウト

`+layout.svelte`はネストされたルートで共有されます。

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  let { children } = $props();
</script>

<header>...</header>
<main>{@render children()}</main>
<footer>...</footer>
```

### サーバーサイドデータ読み込み

`+page.server.ts`でサーバーサイドロジックを実装：

```typescript
export const load: PageServerLoad = async () => {
  // データベースクエリなど
  return { data };
};
```

## 🎨 スタイリング

### コンポーネントスコープCSS

```svelte
<style>
  /* このスタイルはコンポーネント内でのみ有効 */
  .container {
    padding: 2rem;
  }
</style>
```

### グローバルスタイル

`src/app.css`に定義されたスタイルはアプリ全体で適用されます。

## 📦 ビルドとデプロイ

### 本番ビルド

```bash
# 本番ビルド
npm run build

# プレビュー
npm run preview
```

### Vercelへのデプロイ

```bash
# Vercel CLIをインストール
npm i -g vercel

# デプロイ
vercel
```

### Netlifyへのデプロイ

1. GitHubリポジトリに接続
2. ビルドコマンド: `npm run build`
3. 公開ディレクトリ: `build`

### Adapterの変更

デプロイ先に応じてAdapterを変更：

```bash
# Node.js
npm i -D @sveltejs/adapter-node

# Static (SSG)
npm i -D @sveltejs/adapter-static

# Vercel
npm i -D @sveltejs/adapter-vercel

# Netlify
npm i -D @sveltejs/adapter-netlify
```

`svelte.config.js`を更新：

```javascript
import adapter from '@sveltejs/adapter-node';

export default {
  kit: {
    adapter: adapter()
  }
};
```

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
npm run check

# 監視モード
npm run check:watch
```

## 🐳 Docker開発環境

### サービス構成

- **postgres** - PostgreSQL 16データベース
- **frontend** - SvelteKitアプリケーション

### コマンド

```bash
# 起動
docker-compose up -d

# ログ確認
docker-compose logs -f frontend

# コンテナ内でコマンド実行
docker-compose exec frontend npm run check

# 再ビルド
docker-compose up --build

# 停止と削除
docker-compose down -v
```

## 🌟 Svelte 5の主な変更点

### Runes API

従来の`$:`リアクティブステートメントから、明示的なRunesへ移行：

**従来 (Svelte 4)**
```svelte
<script>
  let count = 0;
  $: doubled = count * 2;
</script>
```

**新方式 (Svelte 5)**
```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);
</script>
```

### Snippets

コンポーネント内でのテンプレート再利用：

```svelte
<script>
  let { children } = $props();
</script>

{@render children()}
```

## 📚 参考リンク

- [Svelte公式ドキュメント](https://svelte.dev/)
- [SvelteKit公式ドキュメント](https://kit.svelte.dev/)
- [Svelte 5 Runes](https://svelte-5-preview.vercel.app/docs/runes)
- [Prisma公式ドキュメント](https://www.prisma.io/)
- [Vitest公式ドキュメント](https://vitest.dev/)

## 🤝 コントリビューション

このテンプレートはMITライセンスのもとで公開されています。自由にカスタマイズしてご利用ください。

## 📝 ライセンス

MIT License
