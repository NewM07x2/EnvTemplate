# Nuxt 3 + GraphQL + Prisma テンプレート

Nuxt 3 + TypeScript + Docker + GraphQL (urql) + Prisma + Vitest のフルスタックテンプレートです。
Vue 3 の完全な SSR フレームワークとして、あらゆる規模のアプリケーションに対応します。

## 🎯 概要

このテンプレートは、練習用・学習用の Nuxt 3 アプリケーション環境を提供します。Vue テンプレートの上位版として、完全な SSR 機能を備えています。

### 特徴

- 🐳 **Docker 完全対応** - すぐに開発を開始できる
- 🔄 **完全な SSR** - サーバーサイドレンダリング対応
- 🚀 **自動インポート** - コンポーネントや Composables を自動インポート
- 📁 **ファイルベースルーティング** - pages ディレクトリから自動生成
- 📡 **urql (CSR)** - GraphQL クライアントサイドデータ取得
- 🗄️ **Prisma (SSR)** - サーバーサイドデータベースアクセス
- 🔄 **Pinia** - 公式状態管理ライブラリ
- 🧪 **Vitest** - 高速テストフレームワーク

## 📦 技術スタック

### フロントエンド

- **Nuxt 3.15** - Vue 3 のフルスタックフレームワーク
- **Vue 3.5** - プログレッシブ JavaScript フレームワーク
- **TypeScript 5.7** - 型安全性
- **Pinia 2.3** - 状態管理（Vuex の後継）
- **Tailwind CSS** - ユーティリティファースト CSS（Nuxt Module 経由）

### データ取得

- **urql 1.3** - CSR 用 GraphQL クライアント
- **Prisma 6.4** - SSR 用 ORM・データベースクライアント
- **useFetch / useAsyncData** - Nuxt 3 組み込み Data Fetching

### テスト

- **Vitest 2.1** - テストフレームワーク
- **Vue Test Utils 2.4** - Vue コンポーネントテスト
- **@testing-library/vue 8.1** - Testing Library サポート
- **happy-dom 15.11** - DOM 環境シミュレーション

### インフラ

- **PostgreSQL 16** - リレーショナルデータベース
- **Docker & Docker Compose** - コンテナ化

## 📁 プロジェクト構造

```
nuxt/
├── docker/
│   └── Dockerfile              # フロントエンド用Dockerファイル
├── assets/
│   └── css/
│       └── main.css            # Tailwind CSS
├── components/
│   ├── Counter.vue             # カウンターコンポーネント
│   └── Counter.test.ts         # コンポーネントテスト
├── composables/
│   └── useUrqlClient.ts        # urqlクライアント
├── layouts/
│   └── default.vue             # デフォルトレイアウト
├── pages/
│   ├── index.vue               # トップページ
│   ├── about.vue               # Aboutページ
│   ├── graphql.vue             # GraphQL (CSR) 例
│   └── prisma.vue              # Prisma (SSR) 例
├── server/
│   └── api/
│       └── users.get.ts        # APIルート（SSR）
├── stores/
│   ├── counter.ts              # Piniaストア
│   └── counter.test.ts         # ストアテスト
├── lib/
│   └── prisma/
│       ├── client.ts           # Prismaクライアント
│       └── schema.prisma       # DBスキーマ定義
├── test/                       # テスト設定
│   ├── setup.ts                # テストセットアップ
│   └── example.test.ts         # サンプルテスト
├── public/                     # 静的ファイル
├── app.vue                     # ルートアプリ
├── nuxt.config.ts             # Nuxt設定
├── vitest.config.ts           # Vitest設定
├── tailwind.config.js         # Tailwind設定
├── docker-compose.yml         # Docker Compose設定
└── package.json               # 依存関係
```

## 🚀 クイックスタート

### 前提条件

- Docker Desktop がインストールされていること
- Git がインストールされていること

### 1. プロジェクトのセットアップ

```bash
# このフォルダをコピー
cp -r nuxt my-new-nuxt-app
cd my-new-nuxt-app

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

# 開発サーバーの起動
npm run dev

# 本番ビルド
npm run build

# プレビュー
npm run preview

# 静的サイト生成
npm run generate
```

## 🔄 データ取得方法

Nuxt 3 では、複数のデータ取得方法を提供しています。

### 1. SSR - Nuxt 組み込み Composables（推奨）

**useFetch** または **useAsyncData** を使用:

```vue
<script setup lang="ts">
// APIルートから取得（SSR）
const { data, pending, error } = await useFetch('/api/users')

// Prisma経由でデータベースから直接取得も可能
</script>
```

### 2. SSR - Prisma（サーバーサイドのみ）

**server/api/** ディレクトリで API ルートを作成:

```typescript
// server/api/users.get.ts
import { prisma } from '~/lib/prisma/client'

export default defineEventHandler(async (event) => {
  const users = await prisma.user.findMany()
  return { users }
})
```

ページから呼び出し:

```vue
<script setup lang="ts">
const { data } = await useFetch('/api/users')
</script>
```

### 3. CSR - urql（クライアントサイド）

**urql** を使用して GraphQL エンドポイントにアクセス:

```vue
<script setup lang="ts">
import { useQuery } from '@urql/vue'

const USERS_QUERY = `
  query {
    users {
      id
      username
      email
    }
  }
`

const { data, fetching, error } = await useQuery({ query: USERS_QUERY })
</script>
```

### 使い分けの基準

- **useFetch / useAsyncData**: Nuxt API ルート、外部 API（推奨）
- **Prisma**: データベース直接アクセス（server/api/内）
- **urql**: 外部 GraphQL API への CSR アクセス

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
docker-compose exec postgres psql -U postgres -d nuxt_db

# テーブル一覧
\dt

# データ確認
SELECT * FROM users;
```

## 🧪 テスト

このテンプレートには、**Vitest + Vue Test Utils**を使用したテスト環境が含まれています。

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

- `test/example.test.ts` - 基本的なテストの例
- `components/Counter.test.ts` - コンポーネントテスト
- `stores/counter.test.ts` - Pinia ストアのテスト

### テストの書き方

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Counter from './Counter.vue'

describe('Counter', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('初期値0で表示される', () => {
    const wrapper = mount(Counter)
    expect(wrapper.text()).toContain('0')
  })
})
```

## 🎨 Nuxt 3 の主要機能

### 1. 自動インポート

コンポーネント、Composables、ユーティリティを自動インポート:

```vue
<!-- components/Counter.vueは自動インポートされる -->
<template>
  <Counter />
</template>

<script setup>
// useCounterStoreは自動インポートされる
const counterStore = useCounterStore()
</script>
```

### 2. ファイルベースルーティング

`pages/`ディレクトリの構造がそのままルートになります:

```
pages/
  index.vue       → /
  about.vue       → /about
  users/
    index.vue     → /users
    [id].vue      → /users/:id
```

### 3. レイアウトシステム

複数のレイアウトを定義可能:

```vue
<!-- layouts/custom.vue -->
<template>
  <div class="custom-layout">
    <slot />
  </div>
</template>

<!-- pages/index.vue -->
<script setup>
definePageMeta({
  layout: 'custom'
})
</script>
```

### 4. ミドルウェア

認証やリダイレクトなど:

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  if (!isAuthenticated()) {
    return navigateTo('/login')
  }
})
```

## 🔧 運用方法

### 新しいプロジェクトの開始手順

1. **フォルダのコピー**

   ```bash
   cp -r nuxt my-new-nuxt-app
   cd my-new-nuxt-app
   ```

2. **環境変数の設定**

   - `.env.example` を `.env` にコピー
   - 必要に応じて値を変更

3. **package.json の更新**

   ```json
   {
     "name": "my-new-nuxt-app",
     "version": "0.1.0"
   }
   ```

4. **Prisma スキーマの初期化（必要に応じて）**

   - `lib/prisma/schema.prisma` を編集してモデルを定義
   - `docker-compose up` 後に `docker-compose exec frontend npx prisma db push` を実行

5. **Docker 起動**

   ```bash
   docker-compose up --build
   ```

### 出力モードの変更

`nuxt.config.ts`で出力モードを変更できます:

```typescript
export default defineNuxtConfig({
  // SSR（デフォルト）
  ssr: true,

  // SPA
  ssr: false

  // 静的サイト生成
  // npm run generateで生成
})
```

## 📚 よくある質問

### Q: Vue テンプレートと Nuxt テンプレートの違いは？

A:

- **Vue**: 純粋な CSR フレームワーク、SPA 向け
- **Nuxt**: SSR 対応フルスタックフレームワーク、SEO・初期ロード重視

### Q: Next.js との違いは？

A:

- **Next.js**: React 用 SSR フレームワーク
- **Nuxt**: Vue 用 SSR フレームワーク
- Nuxt の方が規約ベース、Next.js の方が柔軟性が高い

### Q: GraphQL API サーバーはどこにありますか？

A: このテンプレートには GraphQL API サーバーは含まれていません。`NUXT_PUBLIC_GRAPHQL_ENDPOINT`で指定されたエンドポイントに接続します。別途、Go や Node.js 等で GraphQL API サーバーを構築する必要があります。

参考: `next-go`フォルダの Go Echo GraphQL 実装

### Q: Prisma を使いたい場合はどうすればいいですか?

A: Nuxt 3 では、`server/api/`ディレクトリで API ルートを作成し、そこから Prisma を使用します。フロントエンドからは`useFetch`で呼び出します。

### Q: いつ Nuxt 3 を使うべき？

A: 以下の場合に最適です：

- SEO が重要なアプリケーション
- 初期ロード速度が重要
- フルスタックアプリケーション
- Vue エコシステムを活用したい

## 🐛 トラブルシューティング

### Docker コンテナが起動しない

```bash
# キャッシュをクリアして再ビルド
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### .nuxt ディレクトリのエラー

```bash
# .nuxtディレクトリを削除して再起動
rm -rf .nuxt
npm run dev
```

### Prisma の接続エラー

```bash
# Prismaクライアントを再生成
docker-compose exec frontend npx prisma generate

# スキーマをDBに適用
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

## 📚 参考リンク

### 公式ドキュメント

- [Nuxt 3 公式ドキュメント](https://nuxt.com/)
- [Vue 3 公式ドキュメント](https://vuejs.org/)
- [Pinia 公式ドキュメント](https://pinia.vuejs.org/)
- [urql ドキュメント](https://formidable.com/open-source/urql/docs/)
- [Prisma 公式ドキュメント](https://www.prisma.io/docs)
- [Vitest 公式ドキュメント](https://vitest.dev/)

### チュートリアル

- [Nuxt 3 入門ガイド](https://nuxt.com/docs/getting-started/introduction)
- [Data Fetching ガイド](https://nuxt.com/docs/getting-started/data-fetching)

### コミュニティ

- [Nuxt Discord](https://discord.com/invite/nuxt)
- [Nuxt GitHub](https://github.com/nuxt/nuxt)

## 🔗 関連テンプレート

- **vue/** - Vue 3 + Vite CSR テンプレート（軽量版）
- **next/** - Next.js SSR テンプレート（React 版）
- **react/** - React + Vite CSR テンプレート
- **astro/** - Astro 静的サイトテンプレート

---

質問や問題がある場合は、プロジェクトの issue を作成してください。
