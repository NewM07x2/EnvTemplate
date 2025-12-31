# Astro + React + Tailwind CSS テンプレート

Astro + React + TypeScript + Docker + Prisma + Vitest を使用した静的サイト生成テンプレートです。
ブログ、ドキュメントサイト、ポートフォリオなど、様々な用途に使用できます。

## 🎯 概要

このテンプレートは、練習用・学習用の Astro アプリケーション環境を提供します。

### 特徴

- 🐳 **Docker 完全対応** - すぐに開発を開始できる
- ⚡ **高速ビルド** - Vite ベースの爆速ビルド
- 🏝️ **アイランドアーキテクチャ** - 必要な部分だけ JavaScript 配信
- 📝 **MDX サポート** - マークダウンに React コンポーネント埋め込み
- 🎨 **Tailwind CSS** - ユーティリティファースト CSS
- 🗄️ **Prisma** - モダンな ORM
- 🧪 **Vitest** - 高速テストフレームワーク

## 📦 技術スタック

### フロントエンド

- **Astro 4.16** - 静的サイト生成フレームワーク
- **React 18.3** - インタラクティブコンポーネント用
- **TypeScript 5.7** - 型安全性
- **Tailwind CSS 3.4** - スタイリング
- **MDX 3.1** - マークダウン拡張

### データベース・ORM

- **Prisma 6.4** - ORM・データベースクライアント
- **PostgreSQL 16** - リレーショナルデータベース

### テスト

- **Vitest 2.1** - テストフレームワーク
- **React Testing Library 16.1** - React コンポーネントテスト
- **happy-dom 15.11** - DOM 環境シミュレーション

### インフラ

- **Docker & Docker Compose** - コンテナ化

## 📁 プロジェクト構造

```
astro/
├── docker/
│   └── Dockerfile              # フロントエンド用Dockerファイル
├── src/
│   ├── layouts/
│   │   └── Layout.astro        # ベースレイアウト
│   ├── pages/
│   │   ├── index.astro         # トップページ
│   │   ├── about.astro         # Aboutページ
│   │   └── blog/
│   │       └── index.astro     # ブログ一覧
│   ├── components/
│   │   ├── Counter.tsx         # Reactコンポーネント例
│   │   └── Counter.test.tsx    # コンポーネントテスト
│   ├── lib/
│   │   └── prisma/             # Prisma設定
│   │       ├── client.ts       # Prismaクライアント
│   │       └── schema.prisma   # DBスキーマ定義
│   ├── test/                   # テスト設定
│   │   ├── setup.ts            # テストセットアップ
│   │   └── example.test.ts     # サンプルテスト
│   └── styles/
│       └── global.css          # グローバルスタイル
├── public/                     # 静的ファイル
├── astro.config.mjs           # Astro設定
├── vitest.config.ts           # Vitest設定
├── tailwind.config.mjs        # Tailwind設定
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
cp -r astro my-new-astro-site
cd my-new-astro-site

# 環境変数ファイルを作成
cp .env.example .env

# Docker Composeで起動
docker-compose up
```

### 2. アクセス

- **フロントエンド**: http://localhost:4321
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

## 🏝️ アイランドアーキテクチャ

Astro の最大の特徴は「アイランドアーキテクチャ」です。ページ全体は静的 HTML で、必要な部分だけ React コンポーネントを使用します。

### クライアントディレクティブ

```astro
---
import Counter from '../components/Counter';
---

<!-- ページロード時に即座にロード -->
<Counter client:load />

<!-- 要素が表示されたらロード -->
<Counter client:visible />

<!-- ページがアイドル状態になったらロード -->
<Counter client:idle />

<!-- メディアクエリに一致したらロード -->
<Counter client:media="(max-width: 768px)" />

<!-- インタラクティブ機能なし（静的HTML） -->
<Counter client:only="react" />
```

## 📝 コンテンツの追加

### 新しいページの作成

`src/pages/`に Astro ファイルを追加:

```astro
---
// src/pages/contact.astro
import Layout from '../layouts/Layout.astro';
---

<Layout title="お問い合わせ">
  <h1>お問い合わせ</h1>
  <p>お気軽にお問い合わせください。</p>
</Layout>
```

### ブログ記事の作成

MDX ファイルを使用してブログ記事を作成:

```mdx
---
// src/pages/blog/my-first-post.mdx
title: 私の最初の記事
pubDate: 2026-01-01
description: Astroで初めてのブログ記事を書きました
---

import Counter from '../../components/Counter'

# {frontmatter.title}

これは私の最初のブログ記事です。

<Counter client:load />
```

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

### Prisma の使用例

Astro ページでデータを取得:

```astro
---
import { prisma } from '../lib/prisma/client';
import Layout from '../layouts/Layout.astro';

const users = await prisma.user.findMany();
---

<Layout title="ユーザー一覧">
  <h1>ユーザー一覧</h1>
  <ul>
    {users.map(user => (
      <li>{user.username}</li>
    ))}
  </ul>
</Layout>
```

## 🧪 テスト

このテンプレートには、**Vitest + React Testing Library**を使用したテスト環境が含まれています。

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

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import Counter from './Counter'

describe('Counter', () => {
  it('初期値0で表示される', () => {
    render(<Counter />)
    expect(screen.getByText('0')).toBeInTheDocument()
  })
})
```

## 🔧 運用方法

### 新しいプロジェクトの開始手順

1. **フォルダのコピー**

   ```bash
   cp -r astro my-new-site
   cd my-new-site
   ```

2. **環境変数の設定**

   - `.env.example` を `.env` にコピー
   - 必要に応じて値を変更

3. **package.json の更新**

   ```json
   {
     "name": "my-new-site",
     "version": "0.1.0"
   }
   ```

4. **サイト URL の設定**

   - `astro.config.mjs`の`site`を変更
   - `.env`の`SITE_URL`を変更

5. **Docker 起動**

   ```bash
   docker-compose up --build
   ```

### ビルドとデプロイ

```bash
# 本番ビルド
npm run build

# dist/ フォルダが生成される
# 静的ホスティングサービスにデプロイ可能
```

**デプロイ先の例**:

- Vercel
- Netlify
- GitHub Pages
- Cloudflare Pages

## 📚 よくある質問

### Q: SPA との違いは？

A: Astro は基本的に静的 HTML 生成です。必要な部分だけ JavaScript を使用するため、初期ロードが高速で、SEO にも強いです。

### Q: React コンポーネントは必須？

A: いいえ。Astro コンポーネント（.astro）だけでも開発可能です。インタラクティブな機能が必要な場合のみ React を使用します。

### Q: Vue/Svelte も使える？

A: はい。`astro add vue`や`astro add svelte`で追加できます。同じプロジェクト内で複数フレームワークを混在可能です。

### Q: SSR はできる？

A: はい。`astro.config.mjs`で`output: 'server'`に変更すると、SSR モードになります。

### Q: いつ Astro を使うべき？

A: 以下の場合に最適です：

- ブログ、ドキュメントサイト
- ポートフォリオ、ランディングページ
- SEO が重要なマーケティングサイト
- パフォーマンス重視のサイト

## 🐛 トラブルシューティング

### Docker コンテナが起動しない

```bash
# キャッシュをクリアして再ビルド
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Prisma の接続エラー

```bash
# Prismaクライアントを再生成
docker-compose exec frontend npx prisma generate

# スキーマをDBに適用
docker-compose exec frontend npx prisma db push
```

### ビルドエラー

```bash
# node_modulesを削除して再インストール
rm -rf node_modules
npm install
```

## 📚 参考リンク

### 公式ドキュメント

- [Astro 公式ドキュメント](https://docs.astro.build)
- [Astro 統合ガイド](https://docs.astro.build/en/guides/integrations-guide/)
- [React 公式ドキュメント](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Prisma](https://www.prisma.io/docs)
- [Vitest](https://vitest.dev/)

### チュートリアル

- [Astro ブログチュートリアル](https://docs.astro.build/en/tutorial/0-introduction/)
- [MDX ガイド](https://mdxjs.com/)

### コミュニティ

- [Astro Discord](https://astro.build/chat)
- [Astro GitHub](https://github.com/withastro/astro)

## 🔗 関連テンプレート

- **react/** - React + Vite CSR テンプレート
- **vue/** - Vue 3 + Vite CSR テンプレート
- **next/** - Next.js SSR テンプレート
- **nuxt/** - Nuxt.js SSR テンプレート（Vue）

---

質問や問題がある場合は、プロジェクトの issue を作成してください。
