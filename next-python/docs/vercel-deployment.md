# Vercel デプロイメントガイド

このドキュメントは、Next.js アプリケーションを Vercel にデプロイし、運用・管理する方法について説明します。

## 📋 目次

- [前提条件](#前提条件)
- [初期セットアップ](#初期セットアップ)
- [デプロイ方法](#デプロイ方法)
- [環境変数の管理](#環境変数の管理)
- [Prisma の設定](#prismaの設定)
- [ドメイン設定](#ドメイン設定)
- [本番環境での最適化](#本番環境での最適化)
- [モニタリング・ログ確認](#モニタリングログ確認)
- [トラブルシューティング](#トラブルシューティング)

## 前提条件

- GitHub アカウント
- Vercel アカウント（https://vercel.com で作成）
- Next.js プロジェクトが GitHub にプッシュされていること

## 初期セットアップ

### 1. GitHub にプッシュ

プロジェクトを GitHub にプッシュします：

```bash
# Git リポジトリを初期化（初回のみ）
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2. Vercel にサインアップ

1. https://vercel.com にアクセス
2. GitHub アカウントでサインアップ
3. GitHub への認可を許可

### 3. プロジェクトをインポート

#### 方法 1: Vercel ダッシュボードから

1. Vercel ダッシュボード（https://vercel.com/dashboard）にアクセス
2. **Add New** → **Project** をクリック
3. GitHub からリポジトリを選択
4. **Import** をクリック

#### 方法 2: Vercel CLI から

```bash
# Vercel CLI をインストール
npm i -g vercel

# ログイン
vercel login

# デプロイ
vercel

# 本番環境にデプロイ
vercel --prod
```

## デプロイ方法

### 自動デプロイ（推奨）

GitHub に main ブランチにプッシュすると、自動的に Vercel にデプロイされます。

```bash
# コードを編集して git にプッシュ
git add .
git commit -m "Update feature"
git push origin main

# Vercel は自動でビルド・デプロイを開始
```

### 手動デプロイ

```bash
# ローカルで本番ビルドをテスト
npm run build
npm start

# 本番環境にデプロイ
vercel --prod
```

### プレビューデプロイ

任意のブランチにプッシュすると、プレビューデプロイが自動作成されます：

```bash
# 新しいブランチを作成
git checkout -b feature/new-feature

# コードを編集
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# GitHub で Pull Request を作成
# Vercel が自動でプレビューデプロイを作成
```

## 環境変数の管理

### 1. 環境変数を設定

**Vercel ダッシュボード** → **Settings** → **Environment Variables** から設定：

```bash
# 開発環境
DATABASE_URL=postgresql://...
NEXT_PUBLIC_GRAPHQL_ENDPOINT=http://localhost:8000/graphql

# 本番環境
DATABASE_URL=postgresql://...  (本番 DB)
NEXT_PUBLIC_GRAPHQL_ENDPOINT=https://api.example.com/graphql
```

#### 環境ごとに設定

**Environment** を選択して、各環境用の変数を設定：

- **Production** - `main` ブランチ、本番環境用
- **Preview** - Pull Request 用のプレビュー環境
- **Development** - ローカル開発用

### 2. ローカル環境での環境変数

`.env.local` を作成：

```env
DATABASE_URL=postgresql://user:password@localhost:5432/nextapp
NEXT_PUBLIC_GRAPHQL_ENDPOINT=http://localhost:8000/graphql
```

### 3. 重要な環境変数

本番環境では以下を必ず設定してください：

```env
# Prisma
DATABASE_URL=postgresql://user:password@host:5432/db

# GraphQL エンドポイント
NEXT_PUBLIC_GRAPHQL_ENDPOINT=https://api.example.com/graphql

# API URL
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Prisma の設定

### 1. Prisma Client の生成

Vercel にデプロイ前に、Prisma Client を生成する必要があります。

```bash
npx prisma generate
```

### 2. ビルドコマンドの設定

Vercel ダッシュボード → **Settings** → **Build & Development Settings**：

- **Build Command**: `npx prisma generate && npm run build`
- **Output Directory**: `.next`

または `vercel.json` で設定：

```json
{
  "buildCommand": "npx prisma generate && npm run build",
  "outputDirectory": ".next"
}
```

### 3. マイグレーション実行

Vercel では、自動的にマイグレーションが実行されません。手動で実行が必要な場合があります：

```bash
# ローカルで実行
npx prisma migrate deploy

# または
npx prisma db push
```

### 4. Prisma Studio

Vercel では Prisma Studio は使用できません。ローカルでのみ使用可能です：

```bash
npx prisma studio
```

## ドメイン設定

### 1. カスタムドメインを追加

1. Vercel ダッシュボード → **Domains**
2. **Add** をクリック
3. ドメイン名を入力
4. DNS 設定を完了

### 2. DNS レコード設定

Vercel が提供する DNS レコードをドメインレジストラに設定：

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com.
```

または

```
Type: A
Name: @
Value: 76.76.19.0
```

### 3. HTTPS 設定

Vercel は自動的に Let's Encrypt SSL 証明書を発行します。追加の設定は不要です。

## 本番環境での最適化

### 1. 環境変数の確認

```bash
# 本番環境で使用される環境変数を確認
vercel env ls
```

### 2. Next.js 設定の最適化

`next.config.mjs` で本番環境用の設定：

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // 画像最適化
  images: {
    domains: ['example.com'],
    formats: ['image/avif', 'image/webp'],
  },
  
  // リダイレクト
  redirects: async () => [
    {
      source: '/old-page',
      destination: '/new-page',
      permanent: true,
    },
  ],

  // セキュリティヘッダー
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
        ],
      },
    ]
  },
}

export default nextConfig
```

### 3. パフォーマンス最適化

```typescript
// next/image を使用
import Image from 'next/image'

export default function Hero() {
  return (
    <Image
      src="/hero.webp"
      alt="Hero"
      width={1200}
      height={600}
      priority // First Contentful Paint を最適化
    />
  )
}
```

### 4. ビルド最適化

```bash
# ビルド時間を確認
npm run build

# 不要な依存を削除
npm prune --production
```

## モニタリング・ログ確認

### 1. Vercel Analytics

Vercel ダッシュボード → **Analytics** で パフォーマンスを確認：

- Page Speed Insights
- Web Vitals
- Deployment の実行時間

### 2. ログ確認

```bash
# デプロイログを確認
vercel logs

# リアルタイムログを表示
vercel logs -f
```

Vercel ダッシュボード → **Deployments** → 特定のデプロイを選択 → **Logs** タブ

### 3. エラー監視

- **Sentry** を統合してエラートラッキング
- **Datadog** でログ・メトリクス監視
- **LogRocket** でセッション記録

```bash
# Sentry を統合
npm install @sentry/nextjs
```

## トラブルシューティング

### ビルドエラー

```bash
# ローカルでビルドテスト
npm run build

# キャッシュをクリアして再ビルド
npm run build --no-cache

# Vercel でキャッシュをクリア
vercel env pull  # ローカルに環境変数を取得
npm install
npm run build
```

### Prisma エラー

```
error: unreachable code after "describe" call.
```

**解決方法:**

```bash
# node_modules をクリア
rm -rf node_modules
npm install

# Prisma を再生成
npx prisma generate
```

### 環境変数が反映されない

1. Vercel ダッシュボード → **Settings** → **Environment Variables** で確認
2. デプロイを再実行

```bash
# デプロイを再実行
vercel --prod
```

### Database 接続エラー

- `DATABASE_URL` が正しいか確認
- ファイアウォール設定を確認
- Prisma Client が生成されているか確認

```bash
ls -la node_modules/.prisma/client/
```

### Cold Start 時間が長い

- 不要な依存を削除
- コード分割を改善
- Serverless Function の最適化

```bash
# バンドルサイズを確認
npm install -g webpack-bundle-analyzer
```

## CI/CD パイプライン

### 自動テストを追加

```bash
# package.json に test スクリプトを追加
npm install --save-dev vitest

# vercel.json で test コマンドを実行
```

`vercel.json`:

```json
{
  "buildCommand": "npm run test && npx prisma generate && npm run build"
}
```

## セキュリティ設定

### CORS 設定

GraphQL エンドポイントへのアクセスを制限：

```typescript
// src/app/api/route.ts
export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://example.com')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST')
}
```

### レート制限

```bash
npm install express-rate-limit
```

## 参考リンク

- [Vercel ドキュメント](https://vercel.com/docs)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs)
- [Vercel CLI ドキュメント](https://vercel.com/docs/cli)
- [Prisma × Vercel](https://www.prisma.io/docs/guides/deployment/deployment-guides/deploying-to-vercel)

## よくある質問（FAQ）

### Q: 開発環境と本番環境で異なる DATABASE_URL を使用したい

**A:** Vercel ダッシュボード → **Environment Variables** で環境ごとに設定：

- Production: 本番 DB URL
- Preview: ステージング DB URL
- Development: ローカル DB URL

### Q: 既存の Vercel プロジェクトに新しい環境変数を追加したい

**A:** 環境変数を追加後、デプロイを再実行してください：

```bash
vercel env pull  # 環境変数を取得
vercel --prod    # 再デプロイ
```

### Q: Vercel でのビルド時間を短縮したい

**A:** 以下の対策を実施：

- 不要な依存を削除
- Tree-shaking を有効化
- 画像を最適化
- 静的生成（SSG）を活用

### Q: 本番環境で問題が発生した場合、ロールバックしたい

**A:** Vercel ダッシュボード → **Deployments** から以前のデプロイを選択 → **Redeploy**

---

質問や問題がある場合は、[Vercel サポート](https://vercel.com/support)にお問い合わせください。
